# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\LotTemplate_pb2.py
# Compiled at: 2020-12-13 14:23:20
# Size of source mod 2**32: 13746 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.Math_pb2 as Math_pb2
import protocolbuffers.ResourceKey_pb2 as ResourceKey_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='LotTemplate.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\x11LotTemplate.proto\x12\x10EA.Sims4.Network\x1a\nMath.proto\x1a\x11ResourceKey.proto"÷\x04\n\tLotObject\x12\n\n\x02id\x18\x01 \x01(\x04\x12-\n\x08quat_pos\x18\x03 \x01(\x0b2\x1b.EA.Sims4.Network.Transform\x12\x17\n\x0fobject_def_guid\x18\x04 \x01(\r\x12\r\n\x05level\x18\x05 \x01(\x05\x12\x11\n\tparent_id\x18\x06 \x01(\x04\x12\x11\n\tslot_hash\x18\x07 \x01(\r\x12\x12\n\nslot_index\x18\x08 \x01(\r\x12\x18\n\x10object_state_idx\x18\t \x01(\r\x12\x13\n\x0bparent_type\x18\n \x01(\r\x12\x17\n\x0fparent_location\x18\x0b \x01(\x04\x12.\n\x0blight_color\x18\x0c \x01(\x0b2\x19.EA.Sims4.Network.Vector3\x12\r\n\x05scale\x18\r \x01(\x02\x12\x1a\n\x12light_dimmer_value\x18\x0e \x01(\x02\x12\x19\n\x11object_def_guid64\x18\x0f \x01(\x04\x12\x14\n\x0cgeo_state_id\x18\x10 \x01(\r\x129\n\x12model_override_key\x18\x11 \x01(\x0b2\x1d.EA.Sims4.Network.ResourceKey\x12\x19\n\x11material_state_id\x18\x12 \x01(\r\x12\x1a\n\x12buildbuy_use_flags\x18\x13 \x01(\r\x12\x12\n\ntexture_id\x18\x14 \x01(\x06\x12\x12\n\nattributes\x18\x15 \x01(\x0c\x12\x18\n\x10material_variant\x18\x16 \x01(\r\x12\x16\n\x0etexture_effect\x18\x17 \x01(\r\x12-\n\nmulticolor\x18\x18 \x03(\x0b2\x19.EA.Sims4.Network.Vector3"Q\n\rLotObjectList\x12\x0e\n\x06lot_id\x18\x01 \x01(\r\x120\n\x0blot_objects\x18\x02 \x03(\x0b2\x1b.EA.Sims4.Network.LotObject"]\n\x0bLotTemplate\x128\n\x0flot_object_list\x18\x01 \x01(\x0b2\x1f.EA.Sims4.Network.LotObjectList\x12\x14\n\x0carchitecture\x18\x02 \x01(\x0cB\x0fB\rLotTemplatePB')
_LOTOBJECT = descriptor.Descriptor(name='LotObject',
  full_name='EA.Sims4.Network.LotObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='id',
   full_name='EA.Sims4.Network.LotObject.id',
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
 descriptor.FieldDescriptor(name='quat_pos',
   full_name='EA.Sims4.Network.LotObject.quat_pos',
   index=1,
   number=3,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='object_def_guid',
   full_name='EA.Sims4.Network.LotObject.object_def_guid',
   index=2,
   number=4,
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
 descriptor.FieldDescriptor(name='level',
   full_name='EA.Sims4.Network.LotObject.level',
   index=3,
   number=5,
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
 descriptor.FieldDescriptor(name='parent_id',
   full_name='EA.Sims4.Network.LotObject.parent_id',
   index=4,
   number=6,
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
 descriptor.FieldDescriptor(name='slot_hash',
   full_name='EA.Sims4.Network.LotObject.slot_hash',
   index=5,
   number=7,
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
 descriptor.FieldDescriptor(name='slot_index',
   full_name='EA.Sims4.Network.LotObject.slot_index',
   index=6,
   number=8,
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
 descriptor.FieldDescriptor(name='object_state_idx',
   full_name='EA.Sims4.Network.LotObject.object_state_idx',
   index=7,
   number=9,
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
 descriptor.FieldDescriptor(name='parent_type',
   full_name='EA.Sims4.Network.LotObject.parent_type',
   index=8,
   number=10,
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
 descriptor.FieldDescriptor(name='parent_location',
   full_name='EA.Sims4.Network.LotObject.parent_location',
   index=9,
   number=11,
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
 descriptor.FieldDescriptor(name='light_color',
   full_name='EA.Sims4.Network.LotObject.light_color',
   index=10,
   number=12,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='scale',
   full_name='EA.Sims4.Network.LotObject.scale',
   index=11,
   number=13,
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
 descriptor.FieldDescriptor(name='light_dimmer_value',
   full_name='EA.Sims4.Network.LotObject.light_dimmer_value',
   index=12,
   number=14,
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
 descriptor.FieldDescriptor(name='object_def_guid64',
   full_name='EA.Sims4.Network.LotObject.object_def_guid64',
   index=13,
   number=15,
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
 descriptor.FieldDescriptor(name='geo_state_id',
   full_name='EA.Sims4.Network.LotObject.geo_state_id',
   index=14,
   number=16,
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
 descriptor.FieldDescriptor(name='model_override_key',
   full_name='EA.Sims4.Network.LotObject.model_override_key',
   index=15,
   number=17,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='material_state_id',
   full_name='EA.Sims4.Network.LotObject.material_state_id',
   index=16,
   number=18,
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
 descriptor.FieldDescriptor(name='buildbuy_use_flags',
   full_name='EA.Sims4.Network.LotObject.buildbuy_use_flags',
   index=17,
   number=19,
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
 descriptor.FieldDescriptor(name='texture_id',
   full_name='EA.Sims4.Network.LotObject.texture_id',
   index=18,
   number=20,
   type=6,
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
 descriptor.FieldDescriptor(name='attributes',
   full_name='EA.Sims4.Network.LotObject.attributes',
   index=19,
   number=21,
   type=12,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=b'',
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='material_variant',
   full_name='EA.Sims4.Network.LotObject.material_variant',
   index=20,
   number=22,
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
 descriptor.FieldDescriptor(name='texture_effect',
   full_name='EA.Sims4.Network.LotObject.texture_effect',
   index=21,
   number=23,
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
 descriptor.FieldDescriptor(name='multicolor',
   full_name='EA.Sims4.Network.LotObject.multicolor',
   index=22,
   number=24,
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
  serialized_start=71,
  serialized_end=702)
_LOTOBJECTLIST = descriptor.Descriptor(name='LotObjectList',
  full_name='EA.Sims4.Network.LotObjectList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='lot_id',
   full_name='EA.Sims4.Network.LotObjectList.lot_id',
   index=0,
   number=1,
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
 descriptor.FieldDescriptor(name='lot_objects',
   full_name='EA.Sims4.Network.LotObjectList.lot_objects',
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=704,
  serialized_end=785)
_LOTTEMPLATE = descriptor.Descriptor(name='LotTemplate',
  full_name='EA.Sims4.Network.LotTemplate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='lot_object_list',
   full_name='EA.Sims4.Network.LotTemplate.lot_object_list',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='architecture',
   full_name='EA.Sims4.Network.LotTemplate.architecture',
   index=1,
   number=2,
   type=12,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=b'',
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
  serialized_start=787,
  serialized_end=880)
_LOTOBJECT.fields_by_name['quat_pos'].message_type = Math_pb2._TRANSFORM
_LOTOBJECT.fields_by_name['light_color'].message_type = Math_pb2._VECTOR3
_LOTOBJECT.fields_by_name['model_override_key'].message_type = ResourceKey_pb2._RESOURCEKEY
_LOTOBJECT.fields_by_name['multicolor'].message_type = Math_pb2._VECTOR3
_LOTOBJECTLIST.fields_by_name['lot_objects'].message_type = _LOTOBJECT
_LOTTEMPLATE.fields_by_name['lot_object_list'].message_type = _LOTOBJECTLIST
DESCRIPTOR.message_types_by_name['LotObject'] = _LOTOBJECT
DESCRIPTOR.message_types_by_name['LotObjectList'] = _LOTOBJECTLIST
DESCRIPTOR.message_types_by_name['LotTemplate'] = _LOTTEMPLATE

class LotObject(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LOTOBJECT


class LotObjectList(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LOTOBJECTLIST


class LotTemplate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LOTTEMPLATE