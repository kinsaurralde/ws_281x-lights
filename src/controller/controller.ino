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

WiFiUDP Udp;
// IPAddress server_addr;
ESP8266WebServer server(80);
uint8_t buffer[PACKET_BUFFER_SIZE];

typedef struct {
  Pixels pixels;
  CRGB leds[MAX_LED];
  CLEDController* controllers;
  bool grb;
  bool initialized;
} Neopixels;

typedef struct {
  unsigned long last_frame_millis;
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

  server.on("/", handleRoot);
  server.on("/restart", handleRestart);
  server.on("/proto", handleHTTP);
  server.begin();

  neopixels.controllers = &FastLED.addLeds<NEOPIXEL, LED_PIN>(neopixels.leds, MAX_LED);

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
  Serial.print("Initialize HTTP Response Code: ");
  Serial.println(httpResponseCode);

  digitalWrite(BUILTIN_LED_A, LOW);
  digitalWrite(BUILTIN_LED_B, HIGH);
  Serial.println("Finished Setup");
}

void loop() {
  server.handleClient();
  handleUDP();
  updatePixels();
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

void updatePixels() {
  if (neopixels.pixels.frameReady(millis())) {
    neopixels.pixels.increment();
    displayFrameBuffer(neopixels.pixels.get());
    stats.frame_count += 1;
    stats.last_frame_millis = millis();
  }
}

void displayFrameBuffer(const FrameBuffer& frame) {
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    int value = frame.pixels[i];
    if (neopixels.grb) {
      int r = (value >> 8) & 0xFF;
      int g = (value >> 16) & 0xFF;
      int b = value & 0xFF;
      value = r << 16 | g << 8 | b;
    }
    neopixels.leds[i] = (uint32_t)value;
  }
  neopixels.controllers->showLeds(frame.brightness);
}

Status displayFrame(Packet& packet) {
  Frame frame = packet.payload.payload.frame;
  if (!frame.has_brightness) {
    frame.brightness = Brightness_init_zero;
    frame.brightness.brightness = neopixels.pixels.getLEDInfo().brightness;
  }
  if (frame.pixel_count == 0) {
    return Status_ARGUMENT_ERROR;
  }
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    int index = i / ITEMS_PER_COLOR_BLOCK;
    int offset = (i % ITEMS_PER_COLOR_BLOCK) * BITS_PER_BYTE;
    int r = (frame.red[index] >> offset) & 0xFF;
    int g = (frame.green[index] >> offset) & 0xFF;
    int b = (frame.blue[index] >> offset) & 0xFF;
    int value = r << 16 | g << 8 | b;
    neopixels.leds[i] = (uint32_t)value;
  }
  neopixels.controllers->showLeds(frame.brightness.brightness);
  return Status_GOOD;
}

Status beginAnimation(Packet& packet) {
  neopixels.pixels.animation(packet.payload.payload.animation_args);
  return Status_GOOD;
}

Status handleLEDInfo(Packet& packet) {
  if (packet.payload.payload.led_info.initialize) {
    neopixels.grb = packet.payload.payload.led_info.grb;
    neopixels.initialized = true;
    IPAddress remote_address = Udp.remoteIP();
    IPAddress saved_address = readSavedServerIp();
    uint16_t remote_port = packet.payload.payload.led_info.initialize_port;
    uint16_t saved_port = readSavedPort();
    if (saved_address != remote_address || saved_port != remote_port) {
      for (int i = 0; i < 4; i++) {
        EEPROM.write(EEPROM_ADDRESS_START + i, remote_address[i]);
      }
      EEPROM.write(EEPROM_ADDRESS_START + 4, (remote_port >> 8) & 0xFF);
      EEPROM.write(EEPROM_ADDRESS_START + 5, remote_port & 0xFF);
      EEPROM.commit();
    }
    Serial.println("Initialized");
  }
  neopixels.pixels.setLEDInfo(packet.payload.payload.led_info);
  if (packet.payload.payload.led_info.set_brightness) {
    neopixels.controllers->showLeds(packet.payload.payload.led_info.brightness);
  }
  return Status_GOOD;
}

Status handleVersion(Packet& packet) {
  packet.payload.payload.version.major = MAJOR;
  packet.payload.payload.version.minor = MINOR;
  packet.payload.payload.version.patch = PATCH;
  // packet.payload.payload.version.label = LABEL;
  // strcpy(packet.payload.payload.version.label, LABEL);
  return Status_GOOD;
}

Status handlePacket(Packet& packet) {
  if (!packet.has_payload) {
    return Status_MISSING_PAYLOAD;
  }
  if (DEBUG_PRINT) {
    Serial.print("Packet payload type: ");
    Serial.println(packet.payload.which_payload);
  }
  Status status = Status_REQUEST;
  switch (packet.payload.which_payload) {
    case Payload_animation_args_tag:
      status = beginAnimation(packet);
      break;
    case Payload_frame_tag:
      status = displayFrame(packet);
      break;
    case Payload_version_tag:
      status = handleVersion(packet);
      break;
    case Payload_led_info_tag:
      status = handleLEDInfo(packet);
      break;
    case Payload_esp_info_tag:
      status = setESPInfo(&packet);
      break;
    default:
      status = Status_MISSING_PAYLOAD;
      break;
  }
  return status;
}

void handleUDP() {
  int packet_size = Udp.parsePacket();
  if (packet_size <= 0) {
    return;
  }
  stats.udp_packet_count += 1;
  Serial.print("Received UDP packet of size ");
  Serial.print(packet_size);
  Serial.print(" From ");
  Serial.print(Udp.remoteIP());
  Serial.print(", port ");
  Serial.println(Udp.remotePort());
  if (packet_size > PACKET_BUFFER_SIZE) {
    Serial.println("Packet exceeds UDP_BUFFER_SIZE");
    return;
  }
  digitalWrite(BUILTIN_LED_B, LOW);
  Udp.read(buffer, PACKET_BUFFER_SIZE);
  Packet packet = decodePacket(buffer, packet_size);
  Status status = handlePacket(packet);
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
  Serial.print("Recieved HTTP request of size ");
  Serial.print(packet_size);
  Serial.print(" From ");
  Serial.println(server.client().remoteIP());
  if (packet_size >= PACKET_BUFFER_SIZE) {
    server.send(200, "text/plain", "Too Big");
    return;
  }
  packet_string.getBytes(buffer, PACKET_BUFFER_SIZE);
  Packet packet = decodePacket(buffer, packet_size);
  Status status = handlePacket(packet);
  packet.header.status = status;
  packet_size = encodePacket(buffer, PACKET_BUFFER_SIZE, packet);
  buffer[packet_size] = 0;
  server.send(200, "application/octet-stream", String((char*)buffer));
}

void handleRoot() {
  constexpr int PAGE_SIZE = 1024;
  constexpr int BYTES_WRITTEN_SIZE = 3;
  char page[PAGE_SIZE];
  const LEDInfo& pixel_info = neopixels.pixels.getLEDInfo();
  const AnimationArgs& animation_args = neopixels.pixels.getAnimationArgs();
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
      "%d<br>Flash Chip Speed: %d<br>CPU Frequency: %dMHz<br>Chip Id: %d<br>Flash Id: %d<br>Flash Crc: %d<br><br>Bytes "
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
      ESP.getFlashChipSpeed(), ESP.getCpuFreqMHz(), ESP.getChipId(), ESP.getFlashChipId(), ESP.checkFlashCRC());
  page_bytes_written += snprintf(page + page_bytes_written, PAGE_SIZE, "%d", page_bytes_written + BYTES_WRITTEN_SIZE);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/html", page);
}

void handleRestart() {
  Serial.println("Restarting . . .");
  server.send(200, "text/html", "Restarting");
  delay(1000);
  ESP.restart();
}
