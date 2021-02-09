# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\object_tag_tuning.py
# Compiled at: 2017-06-23 00:50:12
# Size of source mod 2**32: 2692 bytes
from interactions.utils.loot_basic_op import BaseLootOperation
from sims4.tuning.tunable import TunableSet, TunableFactory
from tag import TunableTag, TunableTags
import interactions, sims4.log, singletons
logger = sims4.log.Logger('Object Tag Tuning', default_owner='skorman')

class ApplyTagsToObject(BaseLootOperation):
    FACTORY_TUNABLES = {'apply_unpersisted_tags':TunableTags(description='\n                A set of unpersisted category tags to apply to the finished product.\n                '), 
     'apply_persisted_tags':TunableTags(description='\n                A set of persisted category tags to apply to the finished product.\n                ')}

    def __init__(self, apply_unpersisted_tags, apply_persisted_tags, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._apply_unpersisted_tags = apply_unpersisted_tags
        self._apply_persisted_tags = apply_persisted_tags

    def _apply_to_subject_and_target(self, subject, target, resolver):
        if subject is None:
            return
        elif hasattr(subject, 'append_tags'):
            subject.append_tags((self._apply_unpersisted_tags), persist=False)
            subject.append_tags((self._apply_persisted_tags), persist=True)
        else:
            logger.error("ApplyTagsToObject Tuning: Subject {} does not have attribute 'append_tags'", subject)

    @TunableFactory.factory_option
    def subject_participant_type_options(description=singletons.DEFAULT, **kwargs):
        if description is singletons.DEFAULT:
            description = 'The object the tags are applied to.'
        return (BaseLootOperation.get_participant_tunable)('subject', description=description, 
         default_participant=interactions.ParticipantType.Object, **kwargs)