# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\rewards\reward_operation.py
# Compiled at: 2016-03-03 03:00:16
# Size of source mod 2**32: 1062 bytes
from interactions.utils.loot_basic_op import BaseLootOperation
from rewards.reward import Reward
import sims4.log
logger = sims4.log.Logger('RewardOperation', default_owner='rmccord')

class RewardOperation(BaseLootOperation):
    FACTORY_TUNABLES = {'reward': Reward.TunableReference(description='\n            The reward given to the subject of the loot operation.\n            ')}

    def __init__(self, *args, reward, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.reward = reward

    def _apply_to_subject_and_target(self, subject, target, resolver):
        if not subject.is_sim:
            logger.error('Attempting to apply Reward Loot Op to {} which is not a Sim.', subject)
            return False
        self.reward.give_reward(subject)
        return True