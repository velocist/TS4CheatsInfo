# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\notebook\notebook_tests.py
# Compiled at: 2019-01-07 19:32:52
# Size of source mod 2**32: 2327 bytes
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from event_testing.test_events import cached_test
from interactions import ParticipantTypeActorTargetSim
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry
from tunable_utils.tunable_white_black_list import TunableWhiteBlackList
from ui.notebook_tuning import NotebookCategories
import sims4.log
logger = sims4.log.Logger('Notebook', default_owner='mkartika')

class NotebookCategoriesTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {'subject':TunableEnumEntry(description='\n            The subject of the test.\n            ',
       tunable_type=ParticipantTypeActorTargetSim,
       default=ParticipantTypeActorTargetSim.Actor), 
     'unlocked_categories':TunableWhiteBlackList(description='\n            This white/black list will check whether or not the subject has\n            unlocked notebook categories.\n            ',
       tunable=TunableEnumEntry(description='\n                Notebook categories.\n                ',
       tunable_type=NotebookCategories,
       default=(NotebookCategories.INVALID),
       invalid_enums=(
      NotebookCategories.INVALID,),
       pack_safe=True))}

    def get_expected_args(self):
        return {'subject': self.subject}

    @cached_test
    def __call__(self, subject=None):
        subject = next(iter(subject))
        tracker = subject.notebook_tracker
        if tracker is None:
            return TestResult(False, 'Sim {} has no notebook tracker', subject,
              tooltip=(self.tooltip))
        else:
            return self.unlocked_categories.test_collection(tracker.unlocked_category_ids) or TestResult(False, 'Sim {} do not meet white/black list unlocked notebook categories requirements.', subject,
              tooltip=(self.tooltip))
        return TestResult.TRUE