# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\world\premade_lot_status.py
# Compiled at: 2015-02-12 01:32:15
# Size of source mod 2**32: 535 bytes
import enum

class PremadeLotStatus(enum.Int):
    NOT_TRACKED = 0
    IS_PREMADE = 1
    NOT_PREMADE = 2
    export = False