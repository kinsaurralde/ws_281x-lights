#include "../src/modules/logger.h"
#include "../src/nanopb/packet.pb.h"
#include "../src/modules/packet_utils.h"

Packet createPacket() {
    Packet packet = Packet_init_zero;
    Header header = Header_init_zero;
    Version version = Version_init_zero;
    version.major = 2;
    version.minor = 3;
    version.patch = 4;
    header.id = 8;
    header.status = Status::Status_GOOD;
    header.timestamp_millis = 13436523531;
    header.version = version;
    packet.header = header;
    return packet;
}

int main() {
    Logger::println("Test1");
    Logger::println("Test%d", 2);
    Logger::error("This is %cn error", 'a');
    Logger::good("This is good message");
    Logger::warning("This is a warning");
    Packet p = createPacket();
    Header header = p.header;
    serialWritePacketHeader(header);
    return 0;
}
