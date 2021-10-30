#include "logger.h"

#define RST_COLOR_CODE "\x1B[0m"
#define RED_COLOR_CODE "\x1B[31m"
#define GRN_COLOR_CODE "\x1B[32m"
#define YEL_COLOR_CODE "\x1B[33m"
#define BLU_COLOR_CODE "\x1B[34m"
#define MAG_COLOR_CODE "\x1B[35m"
#define CYN_COLOR_CODE "\x1B[36m"
#define WHT_COLOR_CODE "\x1B[37m"

#define STRING_BUFFER_SIZE 256

#include <stdarg.h>

constexpr const char* COLORS[4] = {RST_COLOR_CODE, RED_COLOR_CODE, GRN_COLOR_CODE, YEL_COLOR_CODE};
constexpr int RST_CODE = 0;
constexpr int RED_CODE = 1;
constexpr int GRN_CODE = 2;
constexpr int YEL_CODE = 3;

#if defined(ESP8266)
#include <Arduino.h>

constexpr bool IS_SERIAL_PRINT = true;

void internalPrinter(const char* text, bool new_line) {
  if (new_line) {
    Serial.println(text);
  } else {
    Serial.print(text);
  }
}

#else
#include <iostream>

constexpr bool IS_SERIAL_PRINT = false;

void internalPrinter(const char* text, bool new_line) {
  std::cout << text;
  if (new_line) {
    std::cout << std::endl;
  }
}

#endif

void printFormattedString(const char* text, va_list args) {
  char buffer[STRING_BUFFER_SIZE];
  vsprintf(buffer, text, args);
  internalPrinter(buffer);
}

void setColor(int color_index) {
  if (IS_SERIAL_PRINT) {
    switch (color_index) {
      case RED_CODE:
        internalPrinter("Error: ", false);
        break;
      case YEL_CODE:
        internalPrinter("Warning: ", false);
        break;
      case GRN_CODE:
        internalPrinter("Good: ", false);
        break;
      default:
        break;
    }
  } else {
    internalPrinter(COLORS[color_index], false);
  }
}

void resetColor() { setColor(RST_CODE); }

namespace Logger {

void println(const char* text, ...) {
  va_list args;
  va_start(args, text);
  printFormattedString(text, args);
  va_end(args);
}

void good(const char* text, ...) {
  va_list args;
  va_start(args, text);
  char buffer[STRING_BUFFER_SIZE];
  setColor(GRN_CODE);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}

void warning(const char* text, ...) {
  va_list args;
  va_start(args, text);
  char buffer[STRING_BUFFER_SIZE];
  setColor(YEL_CODE);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}

void error(const char* text, ...) {
  va_list args;
  va_start(args, text);
  char buffer[STRING_BUFFER_SIZE];
  setColor(RED_CODE);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}
}  // namespace Logger
