#ifndef SRC_MODULES_LOGGER_H_
#define SRC_MODULES_LOGGER_H_

#include <stdarg.h>

void internalPrinter(const char* text, bool new_line = true);
void printFormattedString(const char* text, va_list args);

namespace Logger {
void println(const char* text, ...);
void good(const char* text, ...);
void warning(const char* text, ...);
void error(const char* text, ...);
}  // namespace Logger

#endif  // SRC_MODULES_LOGGER_H_
