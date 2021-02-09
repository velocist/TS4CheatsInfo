# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\Distributor_pb2.py
# Compiled at: 2020-12-13 14:22:40
# Size of source mod 2**32: 3501 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.Consts_pb2 as Consts_pb2
import protocolbuffers.DistributorOps_pb2 as DistributorOps_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='Distributor.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\x11Distributor.proto\x12\x10EA.Sims4.Network\x1a\x0cConsts.proto\x1a\x14DistributorOps.proto"\x87\x01\n\x0fViewUpdateEntry\x12;\n\x0fprimary_channel\x18\x01 \x02(\x0b2".EA.Sims4.Network.OperationChannel\x127\n\x0eoperation_list\x18\x02 \x02(\x0b2\x1f.EA.Sims4.Network.OperationList"@\n\nViewUpdate\x122\n\x07entries\x18\x01 \x03(\x0b2!.EA.Sims4.Network.ViewUpdateEntry')
_VIEWUPDATEENTRY = descriptor.Descriptor(name='ViewUpdateEntry',
  full_name='EA.Sims4.Network.ViewUpdateEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='primary_channel',
   full_name='EA.Sims4.Network.ViewUpdateEntry.primary_channel',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=2,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='operation_list',
   full_name='EA.Sims4.Network.ViewUpdateEntry.operation_list',
   index=1,
   number=2,
   type=11,
   cpp_type=10,
   label=2,
   has_default_value=False,
   default_value=None,
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
  serialized_start=76,
  serialized_end=211)
_VIEWUPDATE = descriptor.Descriptor(name='ViewUpdate',
  full_name='EA.Sims4.Network.ViewUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='entries',
   full_name='EA.Sims4.Network.ViewUpdate.entries',
   index=0,
   number=1,
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
  serialized_start=213,
  serialized_end=277)
_VIEWUPDATEENTRY.fields_by_name['primary_channel'].message_type = Consts_pb2._OPERATIONCHANNEL
_VIEWUPDATEENTRY.fields_by_name['operation_list'].message_type = DistributorOps_pb2._OPERATIONLIST
_VIEWUPDATE.fields_by_name['entries'].message_type = _VIEWUPDATEENTRY
DESCRIPTOR.message_types_by_name['ViewUpdateEntry'] = _VIEWUPDATEENTRY
DESCRIPTOR.message_types_by_name['ViewUpdate'] = _VIEWUPDATE

class ViewUpdateEntry(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VIEWUPDATEENTRY


class ViewUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VIEWUPDATE