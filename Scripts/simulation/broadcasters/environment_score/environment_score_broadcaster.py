# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\broadcasters\environment_score\environment_score_broadcaster.py
# Compiled at: 2018-02-02 04:56:23
# Size of source mod 2**32: 1502 bytes
from broadcasters.broadcaster import Broadcaster
from broadcasters.broadcaster_effect import _BroadcasterEffect
from broadcasters.broadcaster_utils import BroadcasterClockType
from sims4.tuning.instances import lock_instance_tunables

class BroadcasterEffectEnvironmentScore(_BroadcasterEffect):

    def apply_broadcaster_effect(self, broadcaster, affected_object):
        if affected_object.is_sim:
            affected_object.add_environment_score_broadcaster(broadcaster)

    def remove_broadcaster_effect(self, broadcaster, affected_object):
        if affected_object.is_sim:
            affected_object.remove_environment_score_broadcaster(broadcaster)


class BroadcasterEnvironmentScore(Broadcaster):
    REMOVE_INSTANCE_TUNABLES = ('effects', )

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.effects = (BroadcasterEffectEnvironmentScore(),)


lock_instance_tunables(BroadcasterEnvironmentScore, clock_type=(BroadcasterClockType.REAL_TIME))