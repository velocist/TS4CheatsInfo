# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\headlines\headline_op.py
# Compiled at: 2020-10-08 20:34:36
# Size of source mod 2**32: 1464 bytes
from interactions.utils.loot_basic_op import BaseLootOperation
from sims4.tuning.tunable import TunableReference, TunableSet, Tunable
import services, sims4.resources
logger = sims4.log.Logger('HeadlineOp', default_owner='yozhang')

class HeadlineOp(BaseLootOperation):
    FACTORY_TUNABLES = {'headline':TunableReference(description='\n            The headline that we want to send down when this loot is applied.\n            ',
       manager=services.get_instance_manager(sims4.resources.Types.HEADLINE)), 
     'amount':Tunable(description='\n            The amount we want to apply to the headline message. Value applied here has no gameplay impact.\n            ',
       tunable_type=float,
       default=0.0)}

    def __init__(self, *args, headline, amount, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.headline = headline
        self.amount = amount

    def _apply_to_subject_and_target(self, subject, target, resolver):
        if not subject.is_sim:
            logger.error('Attempting to play a headline on subject: {}, that is not a Sim. Loot: {}', self.subject, self)
            return
        self.headline.send_headline_message(subject.sim_info, self.amount)