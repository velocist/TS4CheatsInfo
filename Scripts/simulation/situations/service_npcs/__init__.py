# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\situations\service_npcs\__init__.py
# Compiled at: 2013-11-20 23:52:16
# Size of source mod 2**32: 653 bytes
from sims4.tuning.dynamic_enum import DynamicEnumLocked
import enum

class ServiceNpcEndWorkReason(enum.Int):
    NO_WORK_TO_DO = 0
    FINISHED_WORK = 1
    FIRED = 2
    NOT_PAID = 3
    ASKED_TO_HANG_OUT = 4
    DISMISSED = 5