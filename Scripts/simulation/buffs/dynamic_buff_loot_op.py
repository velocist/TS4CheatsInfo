# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\buffs\dynamic_buff_loot_op.py
# Compiled at: 2018-07-24 02:07:43
# Size of source mod 2**32: 3117 bytes
from interactions import ParticipantType
from interactions.utils.loot_basic_op import BaseLootOperation
from sims4.localization import TunableLocalizedString
from sims4.tuning.tunable import TunableMapping, TunableReference, Tunable, OptionalTunable, TunableFactory
import services, sims4.random, singletons
logger = sims4.log.Logger('Buffs')

class DynamicBuffLootOp(BaseLootOperation):
    FACTORY_TUNABLES = {'description':'\n        This loot will give a random buff based on the weight get tuned inside.\n        ', 
     'buffs':TunableMapping(description='\n            ',
       key_type=TunableReference(description='\n                Buff that will get this weight in the random.',
       manager=(services.buff_manager())),
       value_type=Tunable(description='\n                The weight value.',
       tunable_type=float,
       default=0)), 
     'buff_reason':OptionalTunable(description='\n            If set, specify a reason why the buff was added.\n            ',
       tunable=TunableLocalizedString(description='\n                The reason the buff was added. This will be displayed in the\n                buff tooltip.\n                '))}

    def __init__(self, buffs, buff_reason, **kwargs):
        (super().__init__)(**kwargs)
        self._buffs = buffs
        self._buff_reason = buff_reason
        self._random_buff = None

    @TunableFactory.factory_option
    def subject_participant_type_options(description=singletons.DEFAULT, **kwargs):
        return (BaseLootOperation.get_participant_tunable)('subject', invalid_participants=(
                                ParticipantType.Invalid, ParticipantType.All, ParticipantType.PickedItemId), **kwargs)

    def _get_random_buff(self):
        if self._random_buff is None:
            buff_pair_list = list(self._buffs.items())
            self._random_buff = sims4.random.pop_weighted(buff_pair_list, flipped=True)
        return self._random_buff

    def _apply_to_subject_and_target(self, subject, target, resolver):
        random_buff = self._get_random_buff()
        if random_buff is not None:
            if not subject.is_sim:
                logger.error('Tuning error: subject {} of DynamicBuffLootOp giving buff {} for reason {} is not a sim', self.subject, random_buff, self._buff_reason)
                return
            subject.add_buff_from_op(random_buff, self._buff_reason)

    def _on_apply_completed(self):
        random_buff = self._random_buff
        self._random_buff = None
        return random_buff