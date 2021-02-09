# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\audio\object_voice_actor_state.py
# Compiled at: 2020-03-20 00:23:37
# Size of source mod 2**32: 1999 bytes
import sims4.log
from distributor.ops import SetVoiceActor, ElementDistributionOpMixin
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, OptionalTunable
from sims4.tuning.tunable_hash import TunableStringHash32
logger = sims4.log.Logger('SetObjectVoiceActorState', default_owner='yozhang')

class SetObjectVoiceActorState(ElementDistributionOpMixin, HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'voice_actor_override': OptionalTunable(description='\n            We can override an object\'s voice actor. This will be sent to Client,\n            then when audio request the actor suffix, we check for this override\n            on the object.\n            If "No Override" is chosen, existing override will be removed.\n            ',
                               tunable=(TunableStringHash32()),
                               disabled_name='no_override',
                               enabled_name='override_voice_actor',
                               enabled_by_default=True)}

    def __init__(self, target, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._target = target

    def start(self, *args, **kwargs):
        if not self.is_attached:
            self.attach(self._target)

    def stop(self, *args, **kwargs):
        if self.is_attached:
            self.detach()

    def write(self, msg):
        suffix_hash = self.voice_actor_override if self.voice_actor_override else 0
        voice_op = SetVoiceActor(suffix_hash)
        voice_op.write(msg)