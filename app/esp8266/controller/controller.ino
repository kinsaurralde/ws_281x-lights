#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <ESP8266WebServer.h>

#define LED_PIN       14
#define LED_COUNT     60
#define LED_PER_STRIP 60

const char* ssid     = "CellSpot_2.4GHz_D390";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "kcm5a7sstfde";     // The password of the Wi-Fi network

void handleRoot();
void handleNotFound();
void handleJSON();
void handleFreeHeap();

ESP8266WebServer server(80);
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

typedef struct {
  unsigned int data[LED_PER_STRIP];
} Frame;

Frame current;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');
  
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); 
  Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); 
    Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

  server.on("/", handleRoot);               // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/data", handleJSON);
  server.on("/heapfree", handleFreeHeap);
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(50); // Set BRIGHTNESS to about 1/5 (max = 255)
  Serial.println("Started neopixels");

  for (unsigned int i = 0; i < LED_PER_STRIP; i++) {
    current.data[i] = 0;
  }

  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();                    // Listen for HTTP requests from clients
  //updatePixels();
}

void updatePixels() {
  for (unsigned int i = 0; i < LED_PER_STRIP; i++) {
    strip.setPixelColor(i, current.data[i]);
  }
  strip.show();
}

void handleRoot() {
  server.send(200, "text/plain", "Hello world!");   // Send HTTP status 200 (Ok) and send some text to the browser/client
}

void handleJSON() {
  Serial.print("received ");
  if (server.hasArg("plain") == false){ //Check if body received
    server.send(200, "text/plain", "Body not received");
    return;
  }
  StaticJsonDocument<1024> doc;
  deserializeJson(doc, server.arg("plain"));
  JsonArray pixels = doc["data"].as<JsonArray>();
  int i = 0;
  for(JsonVariant v : pixels) {
    if (i >= LED_PER_STRIP) {
      break;
    }
    current.data[i] = v.as<int>();
    Serial.print(current.data[i]);
    Serial.print(' ');
    i++;
  }
  Serial.println(i);
  Serial.println("");
  server.send(200);
}

void handleFreeHeap() {
  server.send(200, "text/plain", String(ESP.getFreeHeap()));
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not foundDD"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}
