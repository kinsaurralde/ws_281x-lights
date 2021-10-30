#include "../src/modules/logger.h"

int main() {
    Logger::println("Test1");
    Logger::println("Test%d", 2);
    Logger::error("This is %cn error", 'a');
    Logger::good("This is good message");
    Logger::warning("This is a warning");
    return 0;
}
