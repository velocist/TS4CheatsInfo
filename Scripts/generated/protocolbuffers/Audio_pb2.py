# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\Audio_pb2.py
# Compiled at: 2020-12-13 14:21:39
# Size of source mod 2**32: 7988 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.ResourceKey_pb2 as ResourceKey_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='Audio.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\x0bAudio.proto\x12\x10EA.Sims4.Network\x1a\x11ResourceKey.proto"\x8c\x01\n\nSoundStart\x12\x11\n\tobject_id\x18\x01 \x01(\x04\x12\x0f\n\x07channel\x18\x02 \x01(\r\x12\x10\n\x08sound_id\x18\x03 \x02(\x04\x12\x0e\n\x06is_vox\x18\x04 \x01(\x08\x12\x17\n\x0fjoint_name_hash\x18\x05 \x01(\r\x12\x1f\n\x17play_on_active_sim_only\x18\x06 \x01(\x08"/\n\tSoundStop\x12\x11\n\tobject_id\x18\x01 \x02(\x04\x12\x0f\n\x07channel\x18\x02 \x02(\r"5\n\x0fSoundSkipToNext\x12\x11\n\tobject_id\x18\x01 \x02(\x04\x12\x0f\n\x07channel\x18\x02 \x02(\r"y\n\rSoundResource\x12,\n\x05sound\x18\x01 \x01(\x0b2\x1d.EA.Sims4.Network.ResourceKey\x12:\n\x13music_track_snippet\x18\x02 \x01(\x0b2\x1d.EA.Sims4.Network.ResourceKey')
_SOUNDSTART = descriptor.Descriptor(name='SoundStart',
  full_name='EA.Sims4.Network.SoundStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.SoundStart.object_id',
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
 descriptor.FieldDescriptor(name='channel',
   full_name='EA.Sims4.Network.SoundStart.channel',
   index=1,
   number=2,
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
 descriptor.FieldDescriptor(name='sound_id',
   full_name='EA.Sims4.Network.SoundStart.sound_id',
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
 descriptor.FieldDescriptor(name='is_vox',
   full_name='EA.Sims4.Network.SoundStart.is_vox',
   index=3,
   number=4,
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
 descriptor.FieldDescriptor(name='joint_name_hash',
   full_name='EA.Sims4.Network.SoundStart.joint_name_hash',
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
 descriptor.FieldDescriptor(name='play_on_active_sim_only',
   full_name='EA.Sims4.Network.SoundStart.play_on_active_sim_only',
   index=5,
   number=6,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=53,
  serialized_end=193)
_SOUNDSTOP = descriptor.Descriptor(name='SoundStop',
  full_name='EA.Sims4.Network.SoundStop',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.SoundStop.object_id',
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
 descriptor.FieldDescriptor(name='channel',
   full_name='EA.Sims4.Network.SoundStop.channel',
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=195,
  serialized_end=242)
_SOUNDSKIPTONEXT = descriptor.Descriptor(name='SoundSkipToNext',
  full_name='EA.Sims4.Network.SoundSkipToNext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='object_id',
   full_name='EA.Sims4.Network.SoundSkipToNext.object_id',
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
 descriptor.FieldDescriptor(name='channel',
   full_name='EA.Sims4.Network.SoundSkipToNext.channel',
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=244,
  serialized_end=297)
_SOUNDRESOURCE = descriptor.Descriptor(name='SoundResource',
  full_name='EA.Sims4.Network.SoundResource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='sound',
   full_name='EA.Sims4.Network.SoundResource.sound',
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
 descriptor.FieldDescriptor(name='music_track_snippet',
   full_name='EA.Sims4.Network.SoundResource.music_track_snippet',
   index=1,
   number=2,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=299,
  serialized_end=420)
_SOUNDRESOURCE.fields_by_name['sound'].message_type = ResourceKey_pb2._RESOURCEKEY
_SOUNDRESOURCE.fields_by_name['music_track_snippet'].message_type = ResourceKey_pb2._RESOURCEKEY
DESCRIPTOR.message_types_by_name['SoundStart'] = _SOUNDSTART
DESCRIPTOR.message_types_by_name['SoundStop'] = _SOUNDSTOP
DESCRIPTOR.message_types_by_name['SoundSkipToNext'] = _SOUNDSKIPTONEXT
DESCRIPTOR.message_types_by_name['SoundResource'] = _SOUNDRESOURCE

class SoundStart(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOUNDSTART


class SoundStop(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOUNDSTOP


class SoundSkipToNext(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOUNDSKIPTONEXT


class SoundResource(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOUNDRESOURCE