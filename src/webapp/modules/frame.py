import animation_pb2 as proto_animation
from config import BITS_PER_BYTE, BITS_PER_USAGE_FLAG, ITEMS_PER_COLOR_BLOCK, MAX_PIXELS_PER_FRAME

# pylint: disable=no-member


def encode(pixels, brigtness=100):
    frame = proto_animation.Frame()
    frame.brightness.brightness = brigtness
    frame.pixel_count = min(len(pixels), MAX_PIXELS_PER_FRAME)
    for i in range(frame.pixel_count):
        color = pixels[i]
        usage_flag_index = i // BITS_PER_USAGE_FLAG
        item_color_index = i // ITEMS_PER_COLOR_BLOCK
        usage_flag_pos = i % BITS_PER_USAGE_FLAG
        item_color_pos = i % ITEMS_PER_COLOR_BLOCK
        if usage_flag_pos == 0:
            frame.usage_flag.extend([0])
        frame.usage_flag[usage_flag_index] |= 1 << usage_flag_pos
        if item_color_pos == 0:
            frame.red.extend([0])
            frame.green.extend([0])
            frame.blue.extend([0])
        frame.red[item_color_index] |= color[0] << (item_color_pos * BITS_PER_BYTE)
        frame.green[item_color_index] |= color[1] << (item_color_pos * BITS_PER_BYTE)
        frame.blue[item_color_index] |= color[2] << (item_color_pos * BITS_PER_BYTE)
    return frame


def decode(frame):
    pixels = []
    for i in range(frame.pixel_count):
        r, g, b = 0, 0, 0
        usage_flag_index = i // BITS_PER_USAGE_FLAG
        item_color_index = i // ITEMS_PER_COLOR_BLOCK
        usage_flag_pos = i % BITS_PER_USAGE_FLAG
        item_color_pos = i % ITEMS_PER_COLOR_BLOCK
        if frame.usage_flag[usage_flag_index] & (1 << usage_flag_pos):
            r = (frame.red[item_color_index] >> (item_color_pos * BITS_PER_BYTE)) & 0xFF
            g = (frame.green[item_color_index] >> (item_color_pos * BITS_PER_BYTE)) & 0xFF
            b = (frame.blue[item_color_index] >> (item_color_pos * BITS_PER_BYTE)) & 0xFF
        pixels.append((r, g, b))
    return (frame.brightness.brightness, pixels)
