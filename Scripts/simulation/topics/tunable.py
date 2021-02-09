# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\topics\tunable.py
# Compiled at: 2018-05-22 23:53:50
# Size of source mod 2**32: 1487 bytes
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from sims4.tuning.tunable import Tunable, TunableReference
from topics.topic import Topic
import services, sims4.log
logger = sims4.log.Logger('Topic')

class TopicUpdate(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {'topic':TunableReference(description='\n            The topic we are updating.',
       manager=services.get_instance_manager(sims4.resources.Types.TOPIC),
       class_restrictions=Topic), 
     'add':Tunable(description='\n            Topic will be added to recipient. if unchecked topic will be\n            removed from recipient.',
       tunable_type=bool,
       default=True)}

    def __init__(self, topic, add, **kwargs):
        (super().__init__)(**kwargs)
        self._topic_type = topic
        self._add = add

    def _apply_to_subject_and_target(self, subject, target, resolver):
        sim = self._get_object_from_recipient(subject)
        if sim is None:
            return
        elif self._add:
            sim.add_topic((self._topic_type), target=target)
        else:
            sim.remove_topic((self._topic_type), target=target)