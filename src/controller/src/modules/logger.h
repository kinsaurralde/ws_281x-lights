#ifndef SRC_MODULES_LOGGER_H_
#define SRC_MODULES_LOGGER_H_

#if defined(ESP8266)
#include <Arduino.h>

void print(String text) { Serial.print(text); }

void print(int value) { Serial.print(value); }

void println(String text) { Serial.println(text); }

void println(int value) { Serial.println(value); }

#else
#include <iostream>
#include <string>

void print(std::string text) { std::cout << text; }

void println(std::string text) { std::cout << text << std::endl; }
#endif

#endif  // SRC_MODULES_LOGGER_H_
