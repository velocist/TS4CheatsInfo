# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\Telemetry_pb2.py
# Compiled at: 2020-12-13 14:24:11
# Size of source mod 2**32: 8424 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='Telemetry.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\x0fTelemetry.proto\x12\x10EA.Sims4.Network"\x9f\x02\n\x12TelemetryAttribute\x12\x0c\n\x04name\x18\x01 \x02(\r\x127\n\x04type\x18\x02 \x02(\x0e2).EA.Sims4.Network.TelemetryAttribute.Type\x12\x0f\n\x07boolval\x18\x03 \x01(\x08\x12\x10\n\x08int32val\x18\x04 \x01(\x05\x12\x11\n\tuint32val\x18\x05 \x01(\r\x12\x10\n\x08floatval\x18\x06 \x01(\x02\x12\x11\n\tstringval\x18\x07 \x01(\t\x12\x11\n\tuint64val\x18\x08 \x01(\x04"T\n\x04Type\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04BOOL\x10\x01\x12\t\n\x05INT32\x10\x02\x12\n\n\x06UINT32\x10\x03\x12\t\n\x05FLOAT\x10\x04\x12\n\n\x06STRING\x10\x05\x12\n\n\x06UINT64\x10\x06"\x87\x01\n\x10TelemetryMessage\x12\x0e\n\x06module\x18\x01 \x02(\r\x12\r\n\x05group\x18\x02 \x02(\r\x12\x0c\n\x04name\x18\x03 \x02(\r\x12\x11\n\ttimestamp\x18\x04 \x02(\x07\x123\n\x05attrs\x18\x05 \x03(\x0b2$.EA.Sims4.Network.TelemetryAttribute')
_TELEMETRYATTRIBUTE_TYPE = descriptor.EnumDescriptor(name='Type',
  full_name='EA.Sims4.Network.TelemetryAttribute.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
 descriptor.EnumValueDescriptor(name='NONE',
   index=0,
   number=0,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='BOOL',
   index=1,
   number=1,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='INT32',
   index=2,
   number=2,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='UINT32',
   index=3,
   number=3,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='FLOAT',
   index=4,
   number=4,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='STRING',
   index=5,
   number=5,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='UINT64',
   index=6,
   number=6,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=241,
  serialized_end=325)
_TELEMETRYATTRIBUTE = descriptor.Descriptor(name='TelemetryAttribute',
  full_name='EA.Sims4.Network.TelemetryAttribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='name',
   full_name='EA.Sims4.Network.TelemetryAttribute.name',
   index=0,
   number=1,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='type',
   full_name='EA.Sims4.Network.TelemetryAttribute.type',
   index=1,
   number=2,
   type=14,
   cpp_type=8,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='boolval',
   full_name='EA.Sims4.Network.TelemetryAttribute.boolval',
   index=2,
   number=3,
   type=8,
   cpp_type=7,
   label=1,
   has_default_value=False,
   default_value=False,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='int32val',
   full_name='EA.Sims4.Network.TelemetryAttribute.int32val',
   index=3,
   number=4,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='uint32val',
   full_name='EA.Sims4.Network.TelemetryAttribute.uint32val',
   index=4,
   number=5,
   type=13,
   cpp_type=3,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='floatval',
   full_name='EA.Sims4.Network.TelemetryAttribute.floatval',
   index=5,
   number=6,
   type=2,
   cpp_type=6,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='stringval',
   full_name='EA.Sims4.Network.TelemetryAttribute.stringval',
   index=6,
   number=7,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=((b'').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='uint64val',
   full_name='EA.Sims4.Network.TelemetryAttribute.uint64val',
   index=7,
   number=8,
   type=4,
   cpp_type=4,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[
 _TELEMETRYATTRIBUTE_TYPE],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=38,
  serialized_end=325)
_TELEMETRYMESSAGE = descriptor.Descriptor(name='TelemetryMessage',
  full_name='EA.Sims4.Network.TelemetryMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='module',
   full_name='EA.Sims4.Network.TelemetryMessage.module',
   index=0,
   number=1,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='group',
   full_name='EA.Sims4.Network.TelemetryMessage.group',
   index=1,
   number=2,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='name',
   full_name='EA.Sims4.Network.TelemetryMessage.name',
   index=2,
   number=3,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='timestamp',
   full_name='EA.Sims4.Network.TelemetryMessage.timestamp',
   index=3,
   number=4,
   type=7,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='attrs',
   full_name='EA.Sims4.Network.TelemetryMessage.attrs',
   index=4,
   number=5,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=328,
  serialized_end=463)
_TELEMETRYATTRIBUTE.fields_by_name['type'].enum_type = _TELEMETRYATTRIBUTE_TYPE
_TELEMETRYATTRIBUTE_TYPE.containing_type = _TELEMETRYATTRIBUTE
_TELEMETRYMESSAGE.fields_by_name['attrs'].message_type = _TELEMETRYATTRIBUTE
DESCRIPTOR.message_types_by_name['TelemetryAttribute'] = _TELEMETRYATTRIBUTE
DESCRIPTOR.message_types_by_name['TelemetryMessage'] = _TELEMETRYMESSAGE

class TelemetryAttribute(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TELEMETRYATTRIBUTE


class TelemetryMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TELEMETRYMESSAGE