/* Automatically generated nanopb header */
/* Generated by nanopb-0.4.6-dev at Mon Oct 25 22:53:52 2021. */

#ifndef PB_ANIMATION_PB_H_INCLUDED
#define PB_ANIMATION_PB_H_INCLUDED
#include "pb.h"

#if PB_PROTO_HEADER_VERSION != 40
#error Regenerate this file with the current version of nanopb generator.
#endif

/* Enum definitions */
typedef enum _AnimationType { 
    AnimationType_NONE = 0, 
    AnimationType_COLOR = 1, 
    AnimationType_WIPE = 2, 
    AnimationType_PULSE = 3, 
    AnimationType_RAINBOW = 4, 
    AnimationType_CYCLE = 5, 
    AnimationType_RANDOM_CYCLE = 6, 
    AnimationType_REVERSER = 7 
} AnimationType;

/* Struct definitions */
typedef struct _Brightness { 
    bool response; 
    int32_t brightness; 
} Brightness;

typedef struct _LEDInfo { 
    bool set_brightness; 
    int32_t brightness; 
    bool set_num_leds; 
    int32_t num_leds; 
    bool set_frame_ms; 
    int32_t frame_ms; 
    bool set_frame_multiplier; 
    int32_t frame_multiplier; 
    bool initialize; 
    int32_t initialize_port; 
    bool grb; 
} LEDInfo;

typedef struct _ListMax25 { 
    pb_size_t items_count;
    int32_t items[25]; 
} ListMax25;

typedef struct _AnimationArgs { 
    int32_t frame_ms; 
    AnimationType type; 
    bool has_colors;
    ListMax25 colors; 
    int32_t color; 
    int32_t background_color; 
    int32_t length; 
    int32_t spacing; 
    int32_t steps; 
    int32_t frame_multiplier; 
    bool reverse; 
    bool reverse2; 
} AnimationArgs;

typedef struct _Frame { 
    bool is_response; 
    bool has_brightness;
    Brightness brightness; 
    int32_t start_pixel; 
    int32_t pixel_count; 
    pb_size_t usage_flag_count;
    uint32_t usage_flag[10]; 
    pb_size_t red_count;
    uint64_t red[40]; 
    pb_size_t green_count;
    uint64_t green[40]; 
    pb_size_t blue_count;
    uint64_t blue[40]; 
} Frame;


/* Helper constants for enums */
#define _AnimationType_MIN AnimationType_NONE
#define _AnimationType_MAX AnimationType_REVERSER
#define _AnimationType_ARRAYSIZE ((AnimationType)(AnimationType_REVERSER+1))


#ifdef __cplusplus
extern "C" {
#endif

/* Initializer values for message structs */
#define AnimationArgs_init_default               {0, _AnimationType_MIN, false, ListMax25_init_default, 0, 0, 0, 0, 0, 0, 0, 0}
#define ListMax25_init_default                   {0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}
#define Frame_init_default                       {0, false, Brightness_init_default, 0, 0, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}
#define Brightness_init_default                  {0, 0}
#define LEDInfo_init_default                     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
#define AnimationArgs_init_zero                  {0, _AnimationType_MIN, false, ListMax25_init_zero, 0, 0, 0, 0, 0, 0, 0, 0}
#define ListMax25_init_zero                      {0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}
#define Frame_init_zero                          {0, false, Brightness_init_zero, 0, 0, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, 0, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}
#define Brightness_init_zero                     {0, 0}
#define LEDInfo_init_zero                        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}

/* Field tags (for use in manual encoding/decoding) */
#define Brightness_response_tag                  1
#define Brightness_brightness_tag                2
#define LEDInfo_set_brightness_tag               1
#define LEDInfo_brightness_tag                   2
#define LEDInfo_set_num_leds_tag                 3
#define LEDInfo_num_leds_tag                     4
#define LEDInfo_set_frame_ms_tag                 5
#define LEDInfo_frame_ms_tag                     6
#define LEDInfo_set_frame_multiplier_tag         7
#define LEDInfo_frame_multiplier_tag             8
#define LEDInfo_initialize_tag                   9
#define LEDInfo_initialize_port_tag              10
#define LEDInfo_grb_tag                          11
#define ListMax25_items_tag                      1
#define AnimationArgs_frame_ms_tag               1
#define AnimationArgs_type_tag                   2
#define AnimationArgs_colors_tag                 4
#define AnimationArgs_color_tag                  5
#define AnimationArgs_background_color_tag       6
#define AnimationArgs_length_tag                 7
#define AnimationArgs_spacing_tag                8
#define AnimationArgs_steps_tag                  9
#define AnimationArgs_frame_multiplier_tag       10
#define AnimationArgs_reverse_tag                14
#define AnimationArgs_reverse2_tag               15
#define Frame_is_response_tag                    1
#define Frame_brightness_tag                     2
#define Frame_start_pixel_tag                    7
#define Frame_pixel_count_tag                    8
#define Frame_usage_flag_tag                     9
#define Frame_red_tag                            10
#define Frame_green_tag                          11
#define Frame_blue_tag                           12

/* Struct field encoding specification for nanopb */
#define AnimationArgs_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, INT32,    frame_ms,          1) \
X(a, STATIC,   SINGULAR, UENUM,    type,              2) \
X(a, STATIC,   OPTIONAL, MESSAGE,  colors,            4) \
X(a, STATIC,   SINGULAR, INT32,    color,             5) \
X(a, STATIC,   SINGULAR, INT32,    background_color,   6) \
X(a, STATIC,   SINGULAR, INT32,    length,            7) \
X(a, STATIC,   SINGULAR, INT32,    spacing,           8) \
X(a, STATIC,   SINGULAR, INT32,    steps,             9) \
X(a, STATIC,   SINGULAR, INT32,    frame_multiplier,  10) \
X(a, STATIC,   SINGULAR, BOOL,     reverse,          14) \
X(a, STATIC,   SINGULAR, BOOL,     reverse2,         15)
#define AnimationArgs_CALLBACK NULL
#define AnimationArgs_DEFAULT NULL
#define AnimationArgs_colors_MSGTYPE ListMax25

#define ListMax25_FIELDLIST(X, a) \
X(a, STATIC,   REPEATED, INT32,    items,             1)
#define ListMax25_CALLBACK NULL
#define ListMax25_DEFAULT NULL

#define Frame_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, BOOL,     is_response,       1) \
X(a, STATIC,   OPTIONAL, MESSAGE,  brightness,        2) \
X(a, STATIC,   SINGULAR, INT32,    start_pixel,       7) \
X(a, STATIC,   SINGULAR, INT32,    pixel_count,       8) \
X(a, STATIC,   REPEATED, UINT32,   usage_flag,        9) \
X(a, STATIC,   REPEATED, UINT64,   red,              10) \
X(a, STATIC,   REPEATED, UINT64,   green,            11) \
X(a, STATIC,   REPEATED, UINT64,   blue,             12)
#define Frame_CALLBACK NULL
#define Frame_DEFAULT NULL
#define Frame_brightness_MSGTYPE Brightness

#define Brightness_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, BOOL,     response,          1) \
X(a, STATIC,   SINGULAR, INT32,    brightness,        2)
#define Brightness_CALLBACK NULL
#define Brightness_DEFAULT NULL

#define LEDInfo_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, BOOL,     set_brightness,    1) \
X(a, STATIC,   SINGULAR, INT32,    brightness,        2) \
X(a, STATIC,   SINGULAR, BOOL,     set_num_leds,      3) \
X(a, STATIC,   SINGULAR, INT32,    num_leds,          4) \
X(a, STATIC,   SINGULAR, BOOL,     set_frame_ms,      5) \
X(a, STATIC,   SINGULAR, INT32,    frame_ms,          6) \
X(a, STATIC,   SINGULAR, BOOL,     set_frame_multiplier,   7) \
X(a, STATIC,   SINGULAR, INT32,    frame_multiplier,   8) \
X(a, STATIC,   SINGULAR, BOOL,     initialize,        9) \
X(a, STATIC,   SINGULAR, INT32,    initialize_port,  10) \
X(a, STATIC,   SINGULAR, BOOL,     grb,              11)
#define LEDInfo_CALLBACK NULL
#define LEDInfo_DEFAULT NULL

extern const pb_msgdesc_t AnimationArgs_msg;
extern const pb_msgdesc_t ListMax25_msg;
extern const pb_msgdesc_t Frame_msg;
extern const pb_msgdesc_t Brightness_msg;
extern const pb_msgdesc_t LEDInfo_msg;

/* Defines for backwards compatibility with code written before nanopb-0.4.0 */
#define AnimationArgs_fields &AnimationArgs_msg
#define ListMax25_fields &ListMax25_msg
#define Frame_fields &Frame_msg
#define Brightness_fields &Brightness_msg
#define LEDInfo_fields &LEDInfo_msg

/* Maximum encoded size of messages (where known) */
#define AnimationArgs_size                       361
#define Brightness_size                          13
#define Frame_size                               1419
#define LEDInfo_size                             67
#define ListMax25_size                           275

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif
