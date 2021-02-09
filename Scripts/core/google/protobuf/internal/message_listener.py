# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\google\protobuf\internal\message_listener.py
# Compiled at: 2011-01-24 08:39:36
# Size of source mod 2**32: 3432 bytes
__author__ = 'robinson@google.com (Will Robinson)'

class MessageListener(object):

    def Modified(self):
        raise NotImplementedError


class NullMessageListener(object):

    def Modified(self):
        pass