#include "../src/modules/logger.h"
#include "../src/nanopb/packet.pb.h"
#include "../src/modules/packet_utils.h"
#include "../src/modules/framebuffer.h"
#include "../src/modules/controller.h"

#include <iostream>

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

AnimationArgs createColorArgs(int color) {
    AnimationArgs args = AnimationArgs_init_zero;
    args.type = AnimationType_COLOR;
    args.color = color;
    args.frame_ms = 50;
    return args;
}

AnimationArgs createRainbowArgs() {
    AnimationArgs args = AnimationArgs_init_zero;
    args.type = AnimationType_RAINBOW;
    args.frame_ms = 50;
    return args;
}

AnimationArgs createPulseArgs() {
    ListMax25 colors = ListMax25_init_zero;
    colors.items[0] = 255;
    colors.items[1] = 500;
    colors.items[2] = 1000;
    colors.items[3] = 2000;
    colors.items[4] = 3000;
    colors.items[5] = 4000;
    colors.items_count = 6;
    AnimationArgs args = AnimationArgs_init_zero;
    args.type = AnimationType_PULSE;
    args.background_color = 3;
    args.length = 5;
    args.spacing = 5;
    args.colors = colors;
    args.frame_ms = 50;
    return args;
}

void setAnimationArgs(Packet& packet, AnimationArgs args) {
    packet.payload.payload.animation_args = args;
    packet.has_payload = true;
    packet.payload.which_payload = Payload_animation_args_tag;
}

void printLeds(uint32_t* leds) {
    for (int i = 0; i < MAX_LED; i++) {
        std::cout << leds[i] << " ";
    }
    std::cout << std::endl << std::endl;
}

void runAnimation(Controller& controller, int loops) {
    for (int i = 0; i < loops; i++) {
        FrameBuffer frame_buffer = controller.getFrameBuffer();
        controller.updatePixels(0);
        printLeds(frame_buffer.pixels);
    }
}

int main() {
    Controller* controller = new Controller();
    Logger::println("Test1");
    Logger::println("Test%d", 2);
    Logger::error("This is %cn error", 'a');
    Logger::good("This is good message");
    Logger::warning("This is a warning");
    Packet p = createPacket();
    Header header = p.header;
    serialWritePacketHeader(header);
    setAnimationArgs(p, createRainbowArgs());
    Logger::println("Handle Packet Status: %d", controller->handlePacket(p));
    runAnimation(*controller, 3);
    return 0;
}
