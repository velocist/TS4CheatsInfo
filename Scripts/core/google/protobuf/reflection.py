# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\google\protobuf\reflection.py
# Compiled at: 2013-10-04 18:43:25
# Size of source mod 2**32: 6260 bytes
__author__ = 'robinson@google.com (Will Robinson)'
from google.protobuf.internal import api_implementation
import google.protobuf as descriptor_mod
from google.protobuf import message
_FieldDescriptor = descriptor_mod.FieldDescriptor
if api_implementation.Type() == 'cpp':
    if api_implementation.Version() == 2:
        from google.protobuf.internal.cpp import cpp_message
        _NewMessage = cpp_message.NewMessage
        _InitMessage = cpp_message.InitMessage
    else:
        from google.protobuf.internal import cpp_message
        _NewMessage = cpp_message.NewMessage
        _InitMessage = cpp_message.InitMessage
else:
    from google.protobuf.internal import python_message
    _NewMessage = python_message.NewMessage
    _InitMessage = python_message.InitMessage

class GeneratedProtocolMessageType(type):
    _DESCRIPTOR_KEY = 'DESCRIPTOR'

    def __new__(cls, name, bases, dictionary):
        descriptor = dictionary[GeneratedProtocolMessageType._DESCRIPTOR_KEY]
        bases = _NewMessage(bases, descriptor, dictionary)
        superclass = super(GeneratedProtocolMessageType, cls)
        new_class = superclass.__new__(cls, name, bases, dictionary)
        setattr(descriptor, '_concrete_class', new_class)
        return new_class

    def __init__(cls, name, bases, dictionary):
        descriptor = dictionary[GeneratedProtocolMessageType._DESCRIPTOR_KEY]
        _InitMessage(descriptor, cls)
        superclass = super(GeneratedProtocolMessageType, cls)
        superclass.__init__(name, bases, dictionary)