/* Automatically generated nanopb header */
/* Generated by nanopb-0.4.6-dev at Wed Nov  3 19:52:39 2021. */

#ifndef PB_PACKET_PB_H_INCLUDED
#define PB_PACKET_PB_H_INCLUDED
#include "pb.h"
#include "animation.pb.h"

#if PB_PROTO_HEADER_VERSION != 40
#error Regenerate this file with the current version of nanopb generator.
#endif

/* Enum definitions */
typedef enum _Status { 
    /* Set REQUEST for outgoing packet */
    Status_REQUEST = 0, 
    /* Set a value below for ACK packet
 Success */
    Status_GOOD = 1, 
    /* Error */
    Status_ERROR = 10, 
    Status_CONNECTION_ERROR = 11, 
    Status_ARGUMENT_ERROR = 12, 
    Status_NOT_IMPLEMENTED = 13, 
    Status_MISSING_PAYLOAD = 20, 
    Status_MISSING_HEADER = 21, 
    Status_MISSING_OPTIONS = 22, 
    Status_PACKET_TOO_LARGE = 30, 
    Status_ESP_ONLY_OPTION = 31 
} Status;

typedef enum _LogType { 
    LogType_LOG_UNSET = 0, 
    LogType_LOG_GOOD = 1, 
    LogType_LOG_WARNING = 2, 
    LogType_LOG_ERROR = 3 
} LogType;

/* Struct definitions */
typedef struct _ESPInfo { 
    /* Set true if values filled. If false, then request values be filled */
    bool is_request; 
    /* Values */
    uint32_t heap_free; 
    uint32_t heap_frag; 
    uint32_t sketch_size; 
    uint32_t free_sketch_size; 
    uint32_t flash_chip_size; 
    uint32_t flash_chip_speed; 
    uint32_t cpu_freq; 
    uint32_t cycle_count; 
    uint32_t supply_voltage; 
    uint32_t chip_id; 
    uint32_t flash_id; 
    uint32_t flash_crc; 
    uint32_t millis; 
} ESPInfo;

typedef struct _Hash { 
    pb_byte_t value[64]; 
} Hash;

typedef struct _LogMessage { 
    LogType type; 
    char message[257]; 
} LogMessage;

typedef struct _Options { 
    bool send_ack; 
} Options;

typedef struct _Version { 
    int32_t major; 
    int32_t minor; 
    int32_t patch; 
    char label[17]; 
    bool has_esp;
    Hash esp; 
    bool has_pixels;
    Hash pixels; 
} Version;

typedef struct _Header { 
    bool has_version;
    Version version; 
    Status status; 
    int64_t id; 
    int64_t timestamp_millis; 
} Header;

typedef struct _Payload { 
    /* Frequent */
    pb_size_t which_payload;
    union {
        LEDInfo led_info;
        AnimationArgs animation_args;
        Frame frame;
        Version version;
        ESPInfo esp_info;
    } payload; 
} Payload;

typedef struct _Packet { 
    bool has_header;
    Header header; 
    bool has_options;
    Options options; 
    bool has_payload;
    Payload payload; 
} Packet;


/* Helper constants for enums */
#define _Status_MIN Status_REQUEST
#define _Status_MAX Status_ESP_ONLY_OPTION
#define _Status_ARRAYSIZE ((Status)(Status_ESP_ONLY_OPTION+1))

#define _LogType_MIN LogType_LOG_UNSET
#define _LogType_MAX LogType_LOG_ERROR
#define _LogType_ARRAYSIZE ((LogType)(LogType_LOG_ERROR+1))


#ifdef __cplusplus
extern "C" {
#endif

/* Initializer values for message structs */
#define Packet_init_default                      {false, Header_init_default, false, Options_init_default, false, Payload_init_default}
#define Payload_init_default                     {0, {LEDInfo_init_default}}
#define Header_init_default                      {false, Version_init_default, _Status_MIN, 0, 0}
#define Options_init_default                     {0}
#define ESPInfo_init_default                     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
#define Version_init_default                     {0, 0, 0, "", false, Hash_init_default, false, Hash_init_default}
#define Hash_init_default                        {{0}}
#define LogMessage_init_default                  {_LogType_MIN, ""}
#define Packet_init_zero                         {false, Header_init_zero, false, Options_init_zero, false, Payload_init_zero}
#define Payload_init_zero                        {0, {LEDInfo_init_zero}}
#define Header_init_zero                         {false, Version_init_zero, _Status_MIN, 0, 0}
#define Options_init_zero                        {0}
#define ESPInfo_init_zero                        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
#define Version_init_zero                        {0, 0, 0, "", false, Hash_init_zero, false, Hash_init_zero}
#define Hash_init_zero                           {{0}}
#define LogMessage_init_zero                     {_LogType_MIN, ""}

/* Field tags (for use in manual encoding/decoding) */
#define ESPInfo_is_request_tag                   1
#define ESPInfo_heap_free_tag                    2
#define ESPInfo_heap_frag_tag                    3
#define ESPInfo_sketch_size_tag                  4
#define ESPInfo_free_sketch_size_tag             5
#define ESPInfo_flash_chip_size_tag              6
#define ESPInfo_flash_chip_speed_tag             7
#define ESPInfo_cpu_freq_tag                     8
#define ESPInfo_cycle_count_tag                  9
#define ESPInfo_supply_voltage_tag               10
#define ESPInfo_chip_id_tag                      11
#define ESPInfo_flash_id_tag                     12
#define ESPInfo_flash_crc_tag                    13
#define ESPInfo_millis_tag                       14
#define Hash_value_tag                           1
#define LogMessage_type_tag                      1
#define LogMessage_message_tag                   2
#define Options_send_ack_tag                     1
#define Version_major_tag                        1
#define Version_minor_tag                        2
#define Version_patch_tag                        3
#define Version_label_tag                        4
#define Version_esp_tag                          5
#define Version_pixels_tag                       6
#define Header_version_tag                       1
#define Header_status_tag                        2
#define Header_id_tag                            3
#define Header_timestamp_millis_tag              4
#define Payload_led_info_tag                     1
#define Payload_animation_args_tag               10
#define Payload_frame_tag                        11
#define Payload_version_tag                      100
#define Payload_esp_info_tag                     101
#define Packet_header_tag                        1
#define Packet_options_tag                       2
#define Packet_payload_tag                       10

/* Struct field encoding specification for nanopb */
#define Packet_FIELDLIST(X, a) \
X(a, STATIC,   OPTIONAL, MESSAGE,  header,            1) \
X(a, STATIC,   OPTIONAL, MESSAGE,  options,           2) \
X(a, STATIC,   OPTIONAL, MESSAGE,  payload,          10)
#define Packet_CALLBACK NULL
#define Packet_DEFAULT NULL
#define Packet_header_MSGTYPE Header
#define Packet_options_MSGTYPE Options
#define Packet_payload_MSGTYPE Payload

#define Payload_FIELDLIST(X, a) \
X(a, STATIC,   ONEOF,    MESSAGE,  (payload,led_info,payload.led_info),   1) \
X(a, STATIC,   ONEOF,    MESSAGE,  (payload,animation_args,payload.animation_args),  10) \
X(a, STATIC,   ONEOF,    MESSAGE,  (payload,frame,payload.frame),  11) \
X(a, STATIC,   ONEOF,    MESSAGE,  (payload,version,payload.version), 100) \
X(a, STATIC,   ONEOF,    MESSAGE,  (payload,esp_info,payload.esp_info), 101)
#define Payload_CALLBACK NULL
#define Payload_DEFAULT NULL
#define Payload_payload_led_info_MSGTYPE LEDInfo
#define Payload_payload_animation_args_MSGTYPE AnimationArgs
#define Payload_payload_frame_MSGTYPE Frame
#define Payload_payload_version_MSGTYPE Version
#define Payload_payload_esp_info_MSGTYPE ESPInfo

#define Header_FIELDLIST(X, a) \
X(a, STATIC,   OPTIONAL, MESSAGE,  version,           1) \
X(a, STATIC,   SINGULAR, UENUM,    status,            2) \
X(a, STATIC,   SINGULAR, INT64,    id,                3) \
X(a, STATIC,   SINGULAR, INT64,    timestamp_millis,   4)
#define Header_CALLBACK NULL
#define Header_DEFAULT NULL
#define Header_version_MSGTYPE Version

#define Options_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, BOOL,     send_ack,          1)
#define Options_CALLBACK NULL
#define Options_DEFAULT NULL

#define ESPInfo_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, BOOL,     is_request,        1) \
X(a, STATIC,   SINGULAR, UINT32,   heap_free,         2) \
X(a, STATIC,   SINGULAR, UINT32,   heap_frag,         3) \
X(a, STATIC,   SINGULAR, UINT32,   sketch_size,       4) \
X(a, STATIC,   SINGULAR, UINT32,   free_sketch_size,   5) \
X(a, STATIC,   SINGULAR, UINT32,   flash_chip_size,   6) \
X(a, STATIC,   SINGULAR, UINT32,   flash_chip_speed,   7) \
X(a, STATIC,   SINGULAR, UINT32,   cpu_freq,          8) \
X(a, STATIC,   SINGULAR, UINT32,   cycle_count,       9) \
X(a, STATIC,   SINGULAR, UINT32,   supply_voltage,   10) \
X(a, STATIC,   SINGULAR, UINT32,   chip_id,          11) \
X(a, STATIC,   SINGULAR, UINT32,   flash_id,         12) \
X(a, STATIC,   SINGULAR, UINT32,   flash_crc,        13) \
X(a, STATIC,   SINGULAR, UINT32,   millis,           14)
#define ESPInfo_CALLBACK NULL
#define ESPInfo_DEFAULT NULL

#define Version_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, INT32,    major,             1) \
X(a, STATIC,   SINGULAR, INT32,    minor,             2) \
X(a, STATIC,   SINGULAR, INT32,    patch,             3) \
X(a, STATIC,   SINGULAR, STRING,   label,             4) \
X(a, STATIC,   OPTIONAL, MESSAGE,  esp,               5) \
X(a, STATIC,   OPTIONAL, MESSAGE,  pixels,            6)
#define Version_CALLBACK NULL
#define Version_DEFAULT NULL
#define Version_esp_MSGTYPE Hash
#define Version_pixels_MSGTYPE Hash

#define Hash_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, FIXED_LENGTH_BYTES, value,             1)
#define Hash_CALLBACK NULL
#define Hash_DEFAULT NULL

#define LogMessage_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, UENUM,    type,              1) \
X(a, STATIC,   SINGULAR, STRING,   message,           2)
#define LogMessage_CALLBACK NULL
#define LogMessage_DEFAULT NULL

extern const pb_msgdesc_t Packet_msg;
extern const pb_msgdesc_t Payload_msg;
extern const pb_msgdesc_t Header_msg;
extern const pb_msgdesc_t Options_msg;
extern const pb_msgdesc_t ESPInfo_msg;
extern const pb_msgdesc_t Version_msg;
extern const pb_msgdesc_t Hash_msg;
extern const pb_msgdesc_t LogMessage_msg;

/* Defines for backwards compatibility with code written before nanopb-0.4.0 */
#define Packet_fields &Packet_msg
#define Payload_fields &Payload_msg
#define Header_fields &Header_msg
#define Options_fields &Options_msg
#define ESPInfo_fields &ESPInfo_msg
#define Version_fields &Version_msg
#define Hash_fields &Hash_msg
#define LogMessage_fields &LogMessage_msg

/* Maximum encoded size of messages (where known) */
#define ESPInfo_size                             80
#define Hash_size                                66
#define Header_size                              214
#define LogMessage_size                          261
#define Options_size                             2
#define Packet_size                              1646
#define Payload_size                             1422
#define Version_size                             187

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif
