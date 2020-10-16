#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <stdlib.h>

#define FASTLED_ESP8266_NODEMCU_PIN_ORDER

#include <FastLED.h>

#include "pixels.h"
#include "structs.h"
#include "version.h"
#include "wifi_credentials.h"

#define BUILTINLED_A 16
#define BUILTINLED_B 2
#define SHOWLED_DELAY 25

#define MAX_BRIGHTNESS 127

// Change the following values if needed
#define LED_PIN_0 5
#define LED_PIN_1 6

// WIFI_SSID and WIFI_PASSWORD are set in wifi_credentials.h

void handleRoot();
void handleInit();
void handleNotFound();
void handleFreeHeap();
void handleGetPixels();
void handleData();
void handleBrightness();
void handleVersionInfo();
void handleLEDOn();
void handleLEDOff();

void updatePixels();
void setArgs(AnimationArgs& args, JsonObject values);

ESP8266WebServer server(80);

typedef struct {
    Pixels* pixels[LED_STRIP_COUNT];
    CRGB leds[LED_STRIP_COUNT][MAX_LED_PER_STRIP];
    CLEDController* controllers[LED_STRIP_COUNT];
} Neopixels;

Neopixels neopixels;

unsigned int total_frame_counter;

void setup() {
    Serial.begin(115200);  // Start the Serial communication to send messages to the computer
    delay(10);
    Serial.println('\n');
    pinMode(BUILTINLED_A, OUTPUT);
    pinMode(BUILTINLED_B, OUTPUT);
    digitalWrite(BUILTINLED_A, HIGH);
    total_frame_counter = 0;
    
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
    server.on("/init", handleInit);
    server.on("/data", handleData);
    server.on("/brightness", handleBrightness);
    server.on("/getpixels", handleGetPixels);
    server.on("/versioninfo", handleVersionInfo);
    server.on("/heapfree", handleFreeHeap);
    server.on("/ledon", handleLEDOn);
    server.on("/ledoff", handleLEDOff);
    server.onNotFound(handleNotFound);

    Serial.println("Setup strip 0 with " + String(MAX_LED_PER_STRIP) + " pixels on pin " + String(LED_PIN_0));
    neopixels.controllers[0] = &FastLED.addLeds<NEOPIXEL, LED_PIN_0>(neopixels.leds[0], MAX_LED_PER_STRIP);
    neopixels.pixels[0] = new Pixels(MAX_LED_PER_STRIP, MAX_BRIGHTNESS);

    Serial.println("Setup strip 1 with " + String(MAX_LED_PER_STRIP) + " pixels on pin " + String(LED_PIN_1));
    neopixels.controllers[1] = &FastLED.addLeds<NEOPIXEL, LED_PIN_1>(neopixels.leds[1], MAX_LED_PER_STRIP);
    neopixels.pixels[1] = new Pixels(MAX_LED_PER_STRIP, MAX_BRIGHTNESS);

    Serial.println("Started neopixels");

    server.begin();  // Start the server
    Serial.println("HTTP server started");
    digitalWrite(BUILTINLED_A, LOW);
}

void loop(void) {
    server.handleClient();  // Listen for HTTP requests from clients
    yield();
    updatePixels();
}

/**
 * Write leds to strip if enough time has passed since last write
 */
void updatePixels() {
    for (unsigned int i = 0; i < LED_STRIP_COUNT; i++) {
        if (neopixels.pixels[i]->canShow(millis())) {
            neopixels.pixels[i]->increment();
            Frame* data = neopixels.pixels[i]->get();
            for (unsigned int j = 0; j < neopixels.pixels[i]->size(); j++) {
                unsigned int value = data->main[j];
                if (neopixels.pixels[i]->isGRB()) {
                    unsigned int r = (value >> 8) & 0xFF;
                    unsigned int g = (value >> 16) & 0xFF;
                    unsigned int b = value & 0xFF;
                    value = r << 16 | g << 8 | b;
                }
                neopixels.leds[i][j] = (uint32_t) value;
            }
            neopixels.controllers[i]->showLeds(neopixels.pixels[i]->getBrightness());
            total_frame_counter += 1;
            if (total_frame_counter % SHOWLED_DELAY == 0) {
                digitalWrite(BUILTINLED_B, LOW);
            } else {
                digitalWrite(BUILTINLED_B, HIGH);
            }
        }
        yield();
    }
}

/**
 * Return 2D array containing values of each pixel on each strip 
 */
String printPixels() {
    String result = "[[";
    for (unsigned int i = 0; i < LED_STRIP_COUNT; i++) {
        for (unsigned int j = 0; j < MAX_LED_PER_STRIP && j < neopixels.pixels[i]->size(); j++) {
            result += String(neopixels.pixels[i]->get()->main[j]);
            if (j < MAX_LED_PER_STRIP - 1) {
                result += ',';
            }
        }
        result += ']';
        if (i < LED_STRIP_COUNT - 1) {
            result += ", [";
        }
    }
    result += ']';
    return result;
}

/**
 * Return array as string with values seperated by ','
 */
String arrayToString(unsigned int* array, unsigned int length) {
    String result = "";
    for (unsigned int i = 0; i < length; i++) {
        result += String(array[i]);
        if (i < length - 1) {
            result += ',';
        }
    }
    return result;
}

/**
 * Set values of AnimationArgs object from JsonObject values.
 * Although not checked, JsonObject should contain all of the AnimationArgs properties
 */ 
void setArgs(AnimationArgs& args, JsonObject values) {
    args.color = values["color"].as<int>();
    args.color_bg = values["color_bg"].as<int>();
    args.animation = values["animation"].as<Animation>();
    args.wait_ms = values["wait_ms"].as<unsigned int>();
    args.arg1 = values["arg1"].as<unsigned int>();
    args.arg2 = values["arg2"].as<unsigned int>();
    args.arg3 = values["arg3"].as<unsigned int>();
    args.arg4 = values["arg4"].as<int>();
    args.arg5 = values["arg5"].as<int>();
    args.arg6 = values["arg6"].as<bool>();
    args.arg7 = values["arg7"].as<bool>();
    args.arg8 = values["arg8"].as<bool>();
    JsonArray color_array = values["colors"].as<JsonArray>();
    args.colors = new List(color_array.size());
    for (unsigned int j = 0; j < args.colors->size(); j++) {
        args.colors->set(j, color_array[j].as<unsigned int>());
    }
}

/**
 * Route: /
 * Methods: GET
 * 
 * Should only be called for ping or connected check
 */ 
void handleRoot() {
    server.send(200, "text/plain", "Hello!");
}

/**
 * Route: /init
 * Methods: GET, POST
 * 
 * POST JSON Properties:
 *      - unsigned int id:              id of strip to initialize
 *      - unsigned int init.brightness: initial brightness value
 *      - unsigned int init.num_leds:   number of pixels on strip
 *      - unsigned int init.milliwatts: maximum milliwatts (not implemented)
 *      - bool         init.grb:        grb mode
 * 
 * Initialze strip with brightness, number of leds, 
 */
void handleInit() {
    if (server.hasArg("plain") == true) {  //Check if body received
        StaticJsonDocument<1024> doc;
        deserializeJson(doc, server.arg("plain"));
        unsigned int id = doc["id"].as<unsigned int>();
        unsigned int brightness = doc["init"]["brightness"].as<unsigned int>();
        unsigned int num_leds = doc["init"]["num_leds"].as<unsigned int>();
        unsigned int milliwatts = doc["init"]["milliwatts"].as<unsigned int>();
        unsigned int grb = doc["init"]["grb"].as<bool>();
        if (id < LED_STRIP_COUNT) {
            neopixels.pixels[id]->initialize(num_leds, milliwatts, brightness, MAX_BRIGHTNESS, grb);
        }
    }
    const size_t CAPACITY = JSON_ARRAY_SIZE(LED_STRIP_COUNT);
    StaticJsonDocument<CAPACITY> doc;
    JsonArray array = doc.to<JsonArray>();
    for (unsigned int i = 0; i < LED_STRIP_COUNT; i++) {
        array.add(neopixels.pixels[i]->isInitialized());
    }
    String info;
    serializeJson(doc, info);
    server.send(200, "application/json", info);
}

/**
 * Route: /data 
 * Methods: POST
 * 
 * Parameters:
 *      - Array of commands, command properties in docs
 * 
 * Run animation commands
 */
void handleData() {
    if (server.hasArg("plain") == false) {  //Check if body received
        server.send(200, "text/plain", "Use POST Method");
        return;
    }
    StaticJsonDocument<4096> doc;
    deserializeJson(doc, server.arg("plain"));
    JsonArray commands = doc.as<JsonArray>();
    for (unsigned int i = 0; i < commands.size(); i++) {
        unsigned int id = commands[i]["id"].as<unsigned int>();
        neopixels.pixels[id]->setIncrementSteps(commands[i]["inc_steps"].as<unsigned int>());
        AnimationArgs args;
        setArgs(args, commands[i]);
        if (args.wait_ms > 0) {
            neopixels.pixels[id]->setDelay(args.wait_ms);
        }
        Serial.println("Run animation " + String(args.animation) + " on id " + String(id));
        switch (args.animation) {
            case Animation::color:
                neopixels.pixels[id]->color(args);
                break;
            case Animation::wipe:
                neopixels.pixels[id]->wipe(args);
                break;
            case Animation::pulse:
                neopixels.pixels[id]->pulse(args);
                break;
            case Animation::rainbow:
                neopixels.pixels[id]->rainbow(args);
                break;
            case Animation::cycle:
                neopixels.pixels[id]->cycle(args);
                break;
        }
        delete args.colors;
    }
    server.send(200, "application/json", "[]");
}

/**
 * Route: /brightness
 * Methods: GET
 * 
 * Query Parameters:
 *      - unsigned integer id:    which strip to read/change
 *      - unsigned integer value: new brightness value (optional)
 * 
 * Sets brightness of strip id to value (if exists) then returns current value
 */
void handleBrightness() {
    String brightness = server.arg("value");
    int id = server.arg("id").toInt();
    if (brightness != "") {
        neopixels.pixels[id]->setBrightness(brightness.toInt());
    }
    server.send(200, "text/plain", String(neopixels.pixels[id]->getBrightness()));
}

/**
 * Route: /getpixels 
 * Methods: GET
 * 
 * Returns json array of each pixel for each strip
 */
void handleGetPixels() {
    server.send(200, "application/json", printPixels());
}

/**
 * Route: /versioninfo 
 * Methods: GET
 * 
 * Return version info of this controller
 */
void handleVersionInfo() {
    StaticJsonDocument<512> doc;
    JsonObject obj = doc.to<JsonObject>();
    obj["major"] = MAJOR;
    obj["minor"] = MINOR;
    obj["patch"] = PATCH;
    obj["label"] = LABEL;
    obj["esp_hash"] = ESP_HASH;
    obj["rpi_hash"] = RPI_HASH;
    String info;
    serializeJson(doc, info);
    server.send(200, "application/json", info);
}

/**
 * Route:
 * Methods: GET
 * 
 * Returns number of free bytes in heap
 */
void handleFreeHeap() {
    server.send(200, "text/plain", String(ESP.getFreeHeap()));
}

/**
 * Route:
 * Methods: GET
 * 
 * Turns BUILTINLED_A on
 */
void handleLEDOn() {
    digitalWrite(BUILTINLED_A, LOW);
    server.send(200, "text/plain", "On");
}

/**
 * Route:
 * Methods: GET
 * 
 * Turns BUILTINLED_A off
 */
void handleLEDOff() {
    digitalWrite(BUILTINLED_A, HIGH);
    server.send(200, "text/plain", "Off");
}

/**
 * Route: Any Invalid Route
 * Methods: GET
 * 
 * Returns 404 message if route not found
 */
void handleNotFound() {
    server.send(404, "text/plain", "404: Not found");  // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}
