#include <Arduino.h>
#include <EEPROM.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <WiFiUDP.h>

#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#include <FastLED.h>

#include "config.h"
#include "src/modules/controller.h"
#include "src/modules/logger.h"
#include "src/modules/packet_utils.h"
#include "src/modules/pixels.h"
#include "version.h"

#define WIFI_SSID "thebetterapartment"
#define WIFI_PASSWORD "Mocha_Rosie4ever"

#define EEPROM_ADDRESS_START 0
#define EEPROM_SIZE 512
#define LED_PIN 5
#define BUILTIN_LED_A 16
#define BUILTIN_LED_B 2

ADC_MODE(ADC_VCC);

void handleRoot();
void handleRestart();
void handleHTTP();
void handleRequest();

void saveServerIp(uint16_t remote_port);

WiFiUDP Udp;
ESP8266WebServer server(80);
uint8_t buffer[PACKET_BUFFER_SIZE];

typedef struct {
  CRGB leds[MAX_LED];
  CLEDController* cled_controller;
  Controller controller;
} Neopixels;

typedef struct {
  uint64_t last_frame_millis;
  int frame_count;
  int udp_packet_count;
  int http_packet_count;
} Stats;

Neopixels neopixels;
Stats stats;

void setup() {
  Serial.begin(115200);  // Start the Serial communication to send messages to the computer
  pinMode(BUILTIN_LED_A, OUTPUT);
  pinMode(BUILTIN_LED_B, OUTPUT);
  digitalWrite(BUILTIN_LED_A, HIGH);
  digitalWrite(BUILTIN_LED_B, LOW);
  Logger::setSendLogMessage(sendLogMessage);
  neopixels.controller.setSaveServerIp(saveServerIp);
  delay(10);
  Serial.println('\n');

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);  // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) {  // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i);
    Serial.print(' ');
  }
  Serial.println('\n');
  Serial.println("Connection established!");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());  // Send the IP address of the ESP8266 to the computer
  Serial.print("Last Reset Reason: ");
  Serial.println(ESP.getResetReason());

  server.on("/", handleRoot);
  server.on("/restart", handleRestart);
  server.on("/proto", handleHTTP);
  server.begin();

  neopixels.cled_controller = &FastLED.addLeds<NEOPIXEL, LED_PIN>(neopixels.leds, MAX_LED);

  Udp.begin(UDP_PORT);
  EEPROM.begin(EEPROM_SIZE);

  IPAddress previous_server_ip = readSavedServerIp();
  uint16_t previous_server_port = readSavedPort();
  Serial.print("Saved Server IP Address ");
  Serial.print(previous_server_ip);
  Serial.print(":");
  Serial.println(previous_server_port);
  HTTPClient http;
  WiFiClient client;

  String server_path =
      "http://" + previous_server_ip.toString() + ":" + String(previous_server_port) + "/controllerstartup";
  http.begin(client, server_path.c_str());

  // Send HTTP GET request
  int httpResponseCode = http.POST(nullptr, 0);
  Logger::println("Initialize HTTP Response Code: %d", httpResponseCode);

  digitalWrite(BUILTIN_LED_A, LOW);
  digitalWrite(BUILTIN_LED_B, HIGH);
  Logger::good("Finished Setup");
}

void loop() {
  server.handleClient();
  handleUDP();
  updatePixels(millis());
}

void saveServerIp(uint16_t remote_port) {
  IPAddress remote_address = Udp.remoteIP();
  IPAddress saved_address = readSavedServerIp();
  uint16_t saved_port = readSavedPort();
  if (saved_address != remote_address || saved_port != remote_port) {
    Logger::println("Saving Server IP: %s:%d", remote_address.toString().c_str(), remote_port);
    for (int i = 0; i < 4; i++) {
      EEPROM.write(EEPROM_ADDRESS_START + i, remote_address[i]);
    }
    EEPROM.write(EEPROM_ADDRESS_START + 4, (remote_port >> 8) & 0xFF);
    EEPROM.write(EEPROM_ADDRESS_START + 5, remote_port & 0xFF);
    EEPROM.commit();
  }
}

IPAddress readSavedServerIp() {
  IPAddress saved_address;
  for (int i = 0; i < 4; i++) {
    saved_address[i] = EEPROM.read(EEPROM_ADDRESS_START + i);
  }
  return saved_address;
}

uint16_t readSavedPort() {
  uint8_t l_byte = EEPROM.read(EEPROM_ADDRESS_START + 4);
  uint8_t r_byte = EEPROM.read(EEPROM_ADDRESS_START + 5);
  return (l_byte << 8) | (r_byte & 0xFF);
}

void sendLogMessage(LogMessage message) {
  uint8_t message_buffer[260];
  IPAddress server = readSavedServerIp();
  Udp.beginPacket(server, 8002);
  pb_ostream_t ostream = pb_ostream_from_buffer(message_buffer, 260);
  pb_encode(&ostream, LogMessage_fields, &message);
  int message_length = ostream.bytes_written;
  Udp.write(message_buffer, message_length);
  Udp.endPacket();
}

void updatePixels(uint64_t millis) {
  if (neopixels.controller.updatePixels(millis)) {
    stats.frame_count += 1;
    stats.last_frame_millis = millis;
    displayFrameBuffer(neopixels.controller.getFrameBuffer());
  }
}

void displayFrameBuffer(const FrameBuffer& frame) {
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    neopixels.leds[i] = (uint32_t)frame.pixels[i];
  }
  neopixels.cled_controller->showLeds(frame.brightness);
}

void handleUDP() {
  int packet_size = Udp.parsePacket();
  if (packet_size <= 0) {
    return;
  }
  stats.udp_packet_count += 1;
  Logger::println("Recieved UDP packet of size %d From %s:%d", packet_size, Udp.remoteIP().toString().c_str(),
                  Udp.remotePort());
  if (packet_size > PACKET_BUFFER_SIZE) {
    Logger::error("Packet exceeds PACKET_BUFFER_SIZE (%d)", PACKET_BUFFER_SIZE);
    return;
  }
  digitalWrite(BUILTIN_LED_B, LOW);
  Udp.read(buffer, PACKET_BUFFER_SIZE);
  Packet packet = decodePacket(buffer, packet_size);
  Status status = neopixels.controller.handlePacket(packet);
  if (packet.has_options && packet.options.send_ack) {
    Udp.beginPacket(Udp.remoteIP(), ACK_PORT);
    packet.header.status = status;
    packet.options = Options_init_zero;
    packet.payload = Payload_init_zero;
    packet_size = encodePacket(buffer, PACKET_BUFFER_SIZE, packet);
    Udp.write(buffer, packet_size);
    Udp.endPacket();
  }
  digitalWrite(BUILTIN_LED_B, HIGH);
}

void handleHTTP() {
  stats.http_packet_count += 1;
  if (server.hasArg("plain") == false) {  // Check if body received
    server.send(200, "text/plain", "Use POST Method");
    return;
  }
  String packet_string = server.arg("plain");
  int packet_size = packet_string.length();
  Logger::println("Recieved HTTP request of size %d From %s", packet_size, server.client().remoteIP());
  if (packet_size >= PACKET_BUFFER_SIZE) {
    server.send(200, "text/plain", "Too Big");
    return;
  }
  packet_string.getBytes(buffer, PACKET_BUFFER_SIZE);
  Packet packet = decodePacket(buffer, packet_size);
  Status status = neopixels.controller.handlePacket(packet);
  packet.header.status = status;
  packet_size = encodePacket(buffer, PACKET_BUFFER_SIZE, packet);
  buffer[packet_size] = 0;
  server.send(200, "application/octet-stream", String((char*)buffer));
}

void handleRoot() {
  constexpr int PAGE_SIZE = 1024;
  constexpr int BYTES_WRITTEN_SIZE = 3;
  char page[PAGE_SIZE];
  const LEDInfo& pixel_info = neopixels.controller.getPixels().getLEDInfo();
  const AnimationArgs& animation_args = neopixels.controller.getPixels().getAnimationArgs();
  int page_bytes_written = snprintf(
      page, PAGE_SIZE,
      "<b>STATUS</b><br>Millis: %lu<br>Last Frame Millis: %lu<br>Frame Count: %d<br>UDP Request Count: %d<br>HTTP "
      "Request Count: %d<br>VCC: %d<br>Free Heap: %d<br>Heap Fragmentation: %d<br>WiFi RSSI: %d<br>Server Ip: "
      "%s<br><br>"
      "<b>PIXELS INFO</b><br>Frame ms: %d<br>Frame Multiplier: %d<br>Brightness: %d<br>Initialized: %d<br>GRB: "
      "%d<br>Num Leds: %d<br><br>"
      "<b>ANIMATION ARGS</b><br>Type: %d<br>Color: %d<br>Background Color: %d<br>Length: %d<br>Spacing: %d<br>Steps: "
      "%d<br><br>"
      "<b>ESP INFO</b><br>Software Version: %d.%d.%d_%s<br>Sketch Size: %d<br>Free Sketch Size: %d<br>Flash Chip Size: "
      "%d<br>Flash Chip Speed: %d<br>CPU Frequency: %dMHz<br>Chip Id: %d<br>Flash Id: %d<br>Flash Crc: %d<br>Stack "
      "Free Cont: %d<br><br>Bytes "
      "Written: ",
      // Status
      millis(), stats.last_frame_millis, stats.frame_count, stats.udp_packet_count, stats.http_packet_count,
      ESP.getVcc(), ESP.getFreeHeap(), ESP.getHeapFragmentation(), WiFi.RSSI(), readSavedServerIp().toString(),
      // Pixels Info
      pixel_info.frame_ms, pixel_info.frame_multiplier, pixel_info.brightness, pixel_info.initialize, pixel_info.grb,
      pixel_info.num_leds,
      // Animation Args
      animation_args.type, animation_args.color, animation_args.background_color, animation_args.length,
      animation_args.spacing, animation_args.steps,
      // Esp Info
      MAJOR, MINOR, PATCH, LABEL, ESP.getSketchSize(), ESP.getFreeSketchSpace(), ESP.getFlashChipSize(),
      ESP.getFlashChipSpeed(), ESP.getCpuFreqMHz(), ESP.getChipId(), ESP.getFlashChipId(), ESP.checkFlashCRC(),
      ESP.getFreeContStack());
  page_bytes_written += snprintf(page + page_bytes_written, PAGE_SIZE, "%d", page_bytes_written + BYTES_WRITTEN_SIZE);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/html", page);
}

void handleRestart() {
  Logger::error("Restarting . . .");
  server.send(200, "text/html", "Restarting");
  delay(1000);
  ESP.restart();
}
