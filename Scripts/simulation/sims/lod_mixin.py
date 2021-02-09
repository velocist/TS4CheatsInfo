# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\lod_mixin.py
# Compiled at: 2020-08-06 02:45:08
# Size of source mod 2**32: 702 bytes
from sims.sim_info_lod import SimInfoLODLevel
from sims4.tuning.tunable import TunableEnumEntry

class HasTunableLodMixin:
    INSTANCE_TUNABLES = {'min_lod_value': TunableEnumEntry(description='\n            The minimum Sim info LOD necessary for this information to persist\n            on the sim info. e.g. A statistic tuned to FULL will not persist on\n            sims that lower than FULL. LOD order, high to low, is FULL, INTERACTED,\n            BASE, BACKGROUND, MINIMUM.\n            ',
                        tunable_type=SimInfoLODLevel,
                        default=(SimInfoLODLevel.BACKGROUND))}