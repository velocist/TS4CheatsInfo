# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\PersistenceBlobs_pb2.py
# Compiled at: 2020-12-13 14:23:57
# Size of source mod 2**32: 4786 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.Consts_pb2 as Consts_pb2
import protocolbuffers.S4Common_pb2 as S4Common_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='PersistenceBlobs.proto',
  package='EA.Sims4.Persistence',
  serialized_pb='\n\x16PersistenceBlobs.proto\x12\x14EA.Sims4.Persistence\x1a\x0cConsts.proto\x1a\x0eS4Common.proto"\x8c\x02\n\x1eBlobSimFacialCustomizationData\x12\x13\n\x07sculpts\x18\x01 \x03(\x04B\x02\x10\x01\x12U\n\x0eface_modifiers\x18\x02 \x03(\x0b2=.EA.Sims4.Persistence.BlobSimFacialCustomizationData.Modifier\x12U\n\x0ebody_modifiers\x18\x03 \x03(\x0b2=.EA.Sims4.Persistence.BlobSimFacialCustomizationData.Modifier\x1a\'\n\x08Modifier\x12\x0b\n\x03key\x18\x01 \x01(\x04\x12\x0e\n\x06amount\x18\x02 \x01(\x02')
_BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER = descriptor.Descriptor(name='Modifier',
  full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.Modifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='key',
   full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.Modifier.key',
   index=0,
   number=1,
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
   options=None),
 descriptor.FieldDescriptor(name='amount',
   full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.Modifier.amount',
   index=1,
   number=2,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=308,
  serialized_end=347)
_BLOBSIMFACIALCUSTOMIZATIONDATA = descriptor.Descriptor(name='BlobSimFacialCustomizationData',
  full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='sculpts',
   full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.sculpts',
   index=0,
   number=1,
   type=4,
   cpp_type=4,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=(descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '\x10\x01'))),
 descriptor.FieldDescriptor(name='face_modifiers',
   full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.face_modifiers',
   index=1,
   number=2,
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
   options=None),
 descriptor.FieldDescriptor(name='body_modifiers',
   full_name='EA.Sims4.Persistence.BlobSimFacialCustomizationData.body_modifiers',
   index=2,
   number=3,
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
  nested_types=[
 _BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=79,
  serialized_end=347)
_BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER.containing_type = _BLOBSIMFACIALCUSTOMIZATIONDATA
_BLOBSIMFACIALCUSTOMIZATIONDATA.fields_by_name['face_modifiers'].message_type = _BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER
_BLOBSIMFACIALCUSTOMIZATIONDATA.fields_by_name['body_modifiers'].message_type = _BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER
DESCRIPTOR.message_types_by_name['BlobSimFacialCustomizationData'] = _BLOBSIMFACIALCUSTOMIZATIONDATA

class BlobSimFacialCustomizationData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class Modifier(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _BLOBSIMFACIALCUSTOMIZATIONDATA_MODIFIER

    DESCRIPTOR = _BLOBSIMFACIALCUSTOMIZATIONDATA