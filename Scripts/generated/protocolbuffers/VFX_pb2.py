# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\VFX_pb2.py
# Compiled at: 2020-12-13 14:24:12
# Size of source mod 2**32: 12663 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.Math_pb2 as Math_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='VFX.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\tVFX.proto\x12\x10EA.Sims4.Network\x1a\nMath.proto"æ\x03\n\x08VFXStart\x12\x11\n\tobject_id\x18\x01 \x01(\x04\x12\x13\n\x0beffect_name\x18\x02 \x02(\t\x12\x10\n\x08actor_id\x18\x03 \x02(\x04\x12\x17\n\x0fjoint_name_hash\x18\x04 \x02(\r\x12\x17\n\x0ftarget_actor_id\x18\x05 \x01(\x04\x12\x1e\n\x16target_joint_name_hash\x18\x06 \x01(\r\x12\x1c\n\rmirror_effect\x18\x07 \x01(\x08:\x05false\x12\x1d\n\x0eauto_on_effect\x18\x08 \x01(\x08:\x05false\x12J\n\x0ftransition_type\x18\t \x01(\x0e21.EA.Sims4.Network.VFXStart.VFXStartTransitionType\x12.\n\ttransform\x18\n \x01(\x0b2\x1b.EA.Sims4.Network.Transform\x126\n\x13target_joint_offset\x18\x0b \x01(\x0b2\x19.EA.Sims4.Network.Vector3\x12\x19\n\x11callback_event_id\x18\x0c \x01(\r"B\n\x16VFXStartTransitionType\x12\x13\n\x0fSOFT_TRANSITION\x10\x00\x12\x13\n\x0fHARD_TRANSITION\x10\x01"»\x01\n\x07VFXStop\x12\x11\n\tobject_id\x18\x01 \x02(\x04\x12\x10\n\x08actor_id\x18\x02 \x02(\x04\x12H\n\x0ftransition_type\x18\x03 \x01(\x0e2/.EA.Sims4.Network.VFXStop.VFXStopTransitionType"A\n\x15VFXStopTransitionType\x12\x13\n\x0fSOFT_TRANSITION\x10\x00\x12\x13\n\x0fHARD_TRANSITION\x10\x01"\x96\x01\n\x0bVFXSetState\x12\x11\n\tobject_id\x18\x01 \x02(\x04\x12\x10\n\x08actor_id\x18\x02 \x02(\x04\x12\x13\n\x0bstate_index\x18\x03 \x02(\x05\x12M\n\x0ftransition_type\x18\x04 \x01(\x0e2#.EA.Sims4.Network.VFXTransitionType:\x0fHARD_TRANSITION*=\n\x11VFXTransitionType\x12\x13\n\x0fSOFT_TRANSITION\x10\x00\x12\x13\n\x0fHARD_TRANSITION\x10\x01')
_VFXTRANSITIONTYPE = descriptor.EnumDescriptor(name='VFXTransitionType',
  full_name='EA.Sims4.Network.VFXTransitionType',
  filename=None,
  file=DESCRIPTOR,
  values=[
 descriptor.EnumValueDescriptor(name='SOFT_TRANSITION',
   index=0,
   number=0,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='HARD_TRANSITION',
   index=1,
   number=1,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=875,
  serialized_end=936)
SOFT_TRANSITION = 0
HARD_TRANSITION = 1
_VFXSTART_VFXSTARTTRANSITIONTYPE = descriptor.EnumDescriptor(name='VFXStartTransitionType',
  full_name='EA.Sims4.Network.VFXStart.VFXStartTransitionType',
  filename=None,
  file=DESCRIPTOR,
  values=[
 descriptor.EnumValueDescriptor(name='SOFT_TRANSITION',
   index=0,
   number=0,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='HARD_TRANSITION',
   index=1,
   number=1,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=464,
  serialized_end=530)
_VFXSTOP_VFXSTOPTRANSITIONTYPE = descriptor.EnumDescriptor(name='VFXStopTransitionType',
  full_name='EA.Sims4.Network.VFXStop.VFXStopTransitionType',
  filename=None,
  file=DESCRIPTOR,
  values=[
 descriptor.EnumValueDescriptor(name='SOFT_TRANSITION',
   index=0,
   number=0,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='HARD_TRANSITION',
   index=1,
   number=1,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=655,
  serialized_end=720)
_VFXSTART = descriptor.Descriptor(name='VFXStart',
  full_name='EA.Sims4.Network.VFXStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.VFXStart.object_id',
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
 descriptor.FieldDescriptor(name='effect_name',
   full_name='EA.Sims4.Network.VFXStart.effect_name',
   index=1,
   number=2,
   type=9,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=((b'').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='actor_id',
   full_name='EA.Sims4.Network.VFXStart.actor_id',
   index=2,
   number=3,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='joint_name_hash',
   full_name='EA.Sims4.Network.VFXStart.joint_name_hash',
   index=3,
   number=4,
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
 descriptor.FieldDescriptor(name='target_actor_id',
   full_name='EA.Sims4.Network.VFXStart.target_actor_id',
   index=4,
   number=5,
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
 descriptor.FieldDescriptor(name='target_joint_name_hash',
   full_name='EA.Sims4.Network.VFXStart.target_joint_name_hash',
   index=5,
   number=6,
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
 descriptor.FieldDescriptor(name='mirror_effect',
   full_name='EA.Sims4.Network.VFXStart.mirror_effect',
   index=6,
   number=7,
   type=8,
   cpp_type=7,
   label=1,
   has_default_value=True,
   default_value=False,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='auto_on_effect',
   full_name='EA.Sims4.Network.VFXStart.auto_on_effect',
   index=7,
   number=8,
   type=8,
   cpp_type=7,
   label=1,
   has_default_value=True,
   default_value=False,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='transition_type',
   full_name='EA.Sims4.Network.VFXStart.transition_type',
   index=8,
   number=9,
   type=14,
   cpp_type=8,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='transform',
   full_name='EA.Sims4.Network.VFXStart.transform',
   index=9,
   number=10,
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
 descriptor.FieldDescriptor(name='target_joint_offset',
   full_name='EA.Sims4.Network.VFXStart.target_joint_offset',
   index=10,
   number=11,
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
 descriptor.FieldDescriptor(name='callback_event_id',
   full_name='EA.Sims4.Network.VFXStart.callback_event_id',
   index=11,
   number=12,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[
 _VFXSTART_VFXSTARTTRANSITIONTYPE],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=44,
  serialized_end=530)
_VFXSTOP = descriptor.Descriptor(name='VFXStop',
  full_name='EA.Sims4.Network.VFXStop',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.VFXStop.object_id',
   index=0,
   number=1,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='actor_id',
   full_name='EA.Sims4.Network.VFXStop.actor_id',
   index=1,
   number=2,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='transition_type',
   full_name='EA.Sims4.Network.VFXStop.transition_type',
   index=2,
   number=3,
   type=14,
   cpp_type=8,
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
 _VFXSTOP_VFXSTOPTRANSITIONTYPE],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=533,
  serialized_end=720)
_VFXSETSTATE = descriptor.Descriptor(name='VFXSetState',
  full_name='EA.Sims4.Network.VFXSetState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.VFXSetState.object_id',
   index=0,
   number=1,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='actor_id',
   full_name='EA.Sims4.Network.VFXSetState.actor_id',
   index=1,
   number=2,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='state_index',
   full_name='EA.Sims4.Network.VFXSetState.state_index',
   index=2,
   number=3,
   type=5,
   cpp_type=1,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='transition_type',
   full_name='EA.Sims4.Network.VFXSetState.transition_type',
   index=3,
   number=4,
   type=14,
   cpp_type=8,
   label=1,
   has_default_value=True,
   default_value=1,
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
  serialized_start=723,
  serialized_end=873)
_VFXSTART.fields_by_name['transition_type'].enum_type = _VFXSTART_VFXSTARTTRANSITIONTYPE
_VFXSTART.fields_by_name['transform'].message_type = Math_pb2._TRANSFORM
_VFXSTART.fields_by_name['target_joint_offset'].message_type = Math_pb2._VECTOR3
_VFXSTART_VFXSTARTTRANSITIONTYPE.containing_type = _VFXSTART
_VFXSTOP.fields_by_name['transition_type'].enum_type = _VFXSTOP_VFXSTOPTRANSITIONTYPE
_VFXSTOP_VFXSTOPTRANSITIONTYPE.containing_type = _VFXSTOP
_VFXSETSTATE.fields_by_name['transition_type'].enum_type = _VFXTRANSITIONTYPE
DESCRIPTOR.message_types_by_name['VFXStart'] = _VFXSTART
DESCRIPTOR.message_types_by_name['VFXStop'] = _VFXSTOP
DESCRIPTOR.message_types_by_name['VFXSetState'] = _VFXSETSTATE

class VFXStart(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VFXSTART


class VFXStop(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VFXSTOP


class VFXSetState(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VFXSETSTATE