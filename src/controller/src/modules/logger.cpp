#include "logger.h"

#include <stdarg.h>

#include "../nanopb/packet.pb.h"

#define RST_COLOR_CODE "\x1B[0m"
#define RED_COLOR_CODE "\x1B[31m"
#define GRN_COLOR_CODE "\x1B[32m"
#define YEL_COLOR_CODE "\x1B[33m"
#define BLU_COLOR_CODE "\x1B[34m"
#define MAG_COLOR_CODE "\x1B[35m"
#define CYN_COLOR_CODE "\x1B[36m"
#define WHT_COLOR_CODE "\x1B[37m"

#define STRING_BUFFER_SIZE 256

constexpr const char* COLORS[4] = {RST_COLOR_CODE, GRN_COLOR_CODE, YEL_COLOR_CODE, RED_COLOR_CODE};

LogType current_type = LogType_LOG_UNSET;
void (*sendLogMessage)(LogMessage);

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
  LogMessage message = LogMessage_init_zero;
  message.type = current_type;
  strcpy(message.message, buffer);
  if (sendLogMessage) {
    sendLogMessage(message);
  }
}

void setColor(LogType type) {
  current_type = type;
  if (IS_SERIAL_PRINT) {
    switch (type) {
      case LogType_LOG_ERROR:
        internalPrinter("Error: ", false);
        break;
      case LogType_LOG_WARNING:
        internalPrinter("Warning: ", false);
        break;
      case LogType_LOG_GOOD:
        internalPrinter("Good: ", false);
        break;
      default:
        break;
    }
  } else {
    internalPrinter(COLORS[type], false);
  }
}

void resetColor() { setColor(LogType_LOG_UNSET); }

namespace Logger {

void setSendLogMessage(void (*callback)(LogMessage)) { sendLogMessage = callback; }

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
  setColor(LogType_LOG_GOOD);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}

void warning(const char* text, ...) {
  va_list args;
  va_start(args, text);
  char buffer[STRING_BUFFER_SIZE];
  setColor(LogType_LOG_WARNING);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}

void error(const char* text, ...) {
  va_list args;
  va_start(args, text);
  char buffer[STRING_BUFFER_SIZE];
  setColor(LogType_LOG_ERROR);
  printFormattedString(text, args);
  resetColor();
  va_end(args);
}
}  // namespace Logger
