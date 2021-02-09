# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\occult\occult_enums.py
# Compiled at: 2019-04-22 23:18:44
# Size of source mod 2**32: 396 bytes
import enum

class OccultType(enum.IntFlags):
    HUMAN = 1
    ALIEN = 2
    VAMPIRE = 4
    MERMAID = 8
    WITCH = 16