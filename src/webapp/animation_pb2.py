# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: animation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='animation.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0f\x61nimation.proto\"\xf1\x01\n\rAnimationArgs\x12\x10\n\x08\x66rame_ms\x18\x01 \x01(\x05\x12\x1c\n\x04type\x18\x02 \x01(\x0e\x32\x0e.AnimationType\x12\x1a\n\x06\x63olors\x18\x04 \x01(\x0b\x32\n.ListMax25\x12\r\n\x05\x63olor\x18\x05 \x01(\x05\x12\x18\n\x10\x62\x61\x63kground_color\x18\x06 \x01(\x05\x12\x0e\n\x06length\x18\x07 \x01(\x05\x12\x0f\n\x07spacing\x18\x08 \x01(\x05\x12\r\n\x05steps\x18\t \x01(\x05\x12\x18\n\x10\x66rame_multiplier\x18\n \x01(\x05\x12\x0f\n\x07reverse\x18\x0e \x01(\x08\x12\x10\n\x08reverse2\x18\x0f \x01(\x08\"\x1a\n\tListMax25\x12\r\n\x05items\x18\x01 \x03(\x05\"\xa5\x01\n\x05\x46rame\x12\x13\n\x0bis_response\x18\x01 \x01(\x08\x12\x1f\n\nbrightness\x18\x02 \x01(\x0b\x32\x0b.Brightness\x12\x13\n\x0bstart_pixel\x18\x07 \x01(\x05\x12\x13\n\x0bpixel_count\x18\x08 \x01(\x05\x12\x12\n\nusage_flag\x18\t \x03(\r\x12\x0b\n\x03red\x18\n \x03(\x04\x12\r\n\x05green\x18\x0b \x03(\x04\x12\x0c\n\x04\x62lue\x18\x0c \x03(\x04\"2\n\nBrightness\x12\x10\n\x08response\x18\x01 \x01(\x08\x12\x12\n\nbrightness\x18\x02 \x01(\x05\"\xf7\x01\n\x07LEDInfo\x12\x16\n\x0eset_brightness\x18\x01 \x01(\x08\x12\x12\n\nbrightness\x18\x02 \x01(\x05\x12\x14\n\x0cset_num_leds\x18\x03 \x01(\x08\x12\x10\n\x08num_leds\x18\x04 \x01(\x05\x12\x14\n\x0cset_frame_ms\x18\x05 \x01(\x08\x12\x10\n\x08\x66rame_ms\x18\x06 \x01(\x05\x12\x1c\n\x14set_frame_multiplier\x18\x07 \x01(\x08\x12\x18\n\x10\x66rame_multiplier\x18\x08 \x01(\x05\x12\x12\n\ninitialize\x18\t \x01(\x08\x12\x17\n\x0finitialize_port\x18\n \x01(\x05\x12\x0b\n\x03grb\x18\x0b \x01(\x08*q\n\rAnimationType\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05\x43OLOR\x10\x01\x12\x08\n\x04WIPE\x10\x02\x12\t\n\x05PULSE\x10\x03\x12\x0b\n\x07RAINBOW\x10\x04\x12\t\n\x05\x43YCLE\x10\x05\x12\x10\n\x0cRANDOM_CYCLE\x10\x06\x12\x0c\n\x08REVERSER\x10\x07\x62\x06proto3')
)

_ANIMATIONTYPE = _descriptor.EnumDescriptor(
  name='AnimationType',
  full_name='AnimationType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COLOR', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WIPE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PULSE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RAINBOW', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CYCLE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RANDOM_CYCLE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REVERSER', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=761,
  serialized_end=874,
)
_sym_db.RegisterEnumDescriptor(_ANIMATIONTYPE)

AnimationType = enum_type_wrapper.EnumTypeWrapper(_ANIMATIONTYPE)
NONE = 0
COLOR = 1
WIPE = 2
PULSE = 3
RAINBOW = 4
CYCLE = 5
RANDOM_CYCLE = 6
REVERSER = 7



_ANIMATIONARGS = _descriptor.Descriptor(
  name='AnimationArgs',
  full_name='AnimationArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_ms', full_name='AnimationArgs.frame_ms', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='AnimationArgs.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='colors', full_name='AnimationArgs.colors', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='color', full_name='AnimationArgs.color', index=3,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='background_color', full_name='AnimationArgs.background_color', index=4,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='length', full_name='AnimationArgs.length', index=5,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='spacing', full_name='AnimationArgs.spacing', index=6,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='steps', full_name='AnimationArgs.steps', index=7,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frame_multiplier', full_name='AnimationArgs.frame_multiplier', index=8,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reverse', full_name='AnimationArgs.reverse', index=9,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reverse2', full_name='AnimationArgs.reverse2', index=10,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=261,
)


_LISTMAX25 = _descriptor.Descriptor(
  name='ListMax25',
  full_name='ListMax25',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='ListMax25.items', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=263,
  serialized_end=289,
)


_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_response', full_name='Frame.is_response', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='brightness', full_name='Frame.brightness', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_pixel', full_name='Frame.start_pixel', index=2,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pixel_count', full_name='Frame.pixel_count', index=3,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='usage_flag', full_name='Frame.usage_flag', index=4,
      number=9, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='red', full_name='Frame.red', index=5,
      number=10, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='green', full_name='Frame.green', index=6,
      number=11, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blue', full_name='Frame.blue', index=7,
      number=12, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=292,
  serialized_end=457,
)


_BRIGHTNESS = _descriptor.Descriptor(
  name='Brightness',
  full_name='Brightness',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='Brightness.response', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='brightness', full_name='Brightness.brightness', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=459,
  serialized_end=509,
)


_LEDINFO = _descriptor.Descriptor(
  name='LEDInfo',
  full_name='LEDInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='set_brightness', full_name='LEDInfo.set_brightness', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='brightness', full_name='LEDInfo.brightness', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_num_leds', full_name='LEDInfo.set_num_leds', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_leds', full_name='LEDInfo.num_leds', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_frame_ms', full_name='LEDInfo.set_frame_ms', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frame_ms', full_name='LEDInfo.frame_ms', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_frame_multiplier', full_name='LEDInfo.set_frame_multiplier', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frame_multiplier', full_name='LEDInfo.frame_multiplier', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='initialize', full_name='LEDInfo.initialize', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='initialize_port', full_name='LEDInfo.initialize_port', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='grb', full_name='LEDInfo.grb', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=512,
  serialized_end=759,
)

_ANIMATIONARGS.fields_by_name['type'].enum_type = _ANIMATIONTYPE
_ANIMATIONARGS.fields_by_name['colors'].message_type = _LISTMAX25
_FRAME.fields_by_name['brightness'].message_type = _BRIGHTNESS
DESCRIPTOR.message_types_by_name['AnimationArgs'] = _ANIMATIONARGS
DESCRIPTOR.message_types_by_name['ListMax25'] = _LISTMAX25
DESCRIPTOR.message_types_by_name['Frame'] = _FRAME
DESCRIPTOR.message_types_by_name['Brightness'] = _BRIGHTNESS
DESCRIPTOR.message_types_by_name['LEDInfo'] = _LEDINFO
DESCRIPTOR.enum_types_by_name['AnimationType'] = _ANIMATIONTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AnimationArgs = _reflection.GeneratedProtocolMessageType('AnimationArgs', (_message.Message,), dict(
  DESCRIPTOR = _ANIMATIONARGS,
  __module__ = 'animation_pb2'
  # @@protoc_insertion_point(class_scope:AnimationArgs)
  ))
_sym_db.RegisterMessage(AnimationArgs)

ListMax25 = _reflection.GeneratedProtocolMessageType('ListMax25', (_message.Message,), dict(
  DESCRIPTOR = _LISTMAX25,
  __module__ = 'animation_pb2'
  # @@protoc_insertion_point(class_scope:ListMax25)
  ))
_sym_db.RegisterMessage(ListMax25)

Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
  DESCRIPTOR = _FRAME,
  __module__ = 'animation_pb2'
  # @@protoc_insertion_point(class_scope:Frame)
  ))
_sym_db.RegisterMessage(Frame)

Brightness = _reflection.GeneratedProtocolMessageType('Brightness', (_message.Message,), dict(
  DESCRIPTOR = _BRIGHTNESS,
  __module__ = 'animation_pb2'
  # @@protoc_insertion_point(class_scope:Brightness)
  ))
_sym_db.RegisterMessage(Brightness)

LEDInfo = _reflection.GeneratedProtocolMessageType('LEDInfo', (_message.Message,), dict(
  DESCRIPTOR = _LEDINFO,
  __module__ = 'animation_pb2'
  # @@protoc_insertion_point(class_scope:LEDInfo)
  ))
_sym_db.RegisterMessage(LEDInfo)


# @@protoc_insertion_point(module_scope)
