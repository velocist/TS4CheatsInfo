# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\event_testing\test_based_score_threshold.py
# Compiled at: 2019-08-17 02:49:05
# Size of source mod 2**32: 2638 bytes
from event_testing.resolver import RESOLVER_PARTICIPANT
from event_testing.results import TestResult
from interactions import ParticipantType
from sims4.math import Operator
from sims4.tuning.tunable import TunableSingletonFactory, TunableThreshold, TunableEnumEntry, TunableReference
import event_testing.test_base, services, sims4.log
logger = sims4.log.Logger('Tests')

class TestBasedScoreThresholdTest(event_testing.test_base.BaseTest):
    FACTORY_TUNABLES = {'description':'Gate availability by a statistic on the actor or target.', 
     'who':TunableEnumEntry(ParticipantType, ParticipantType.Actor, description='Who or what to apply this test to.'), 
     'test_based_score':TunableReference(services.test_based_score_manager(), description='The specific cumulative test.  This is pack safe because this particular test was being used for module tuning, so be careful that you are not referencing from one pack to the next.', pack_safe=True), 
     'threshold':TunableThreshold(description="The threshold to control availability based on the statistic's value")}

    def __init__(self, who, test_based_score, threshold, **kwargs):
        (super().__init__)(safe_to_skip=True, **kwargs)
        self.who = who
        self.test_based_score = test_based_score
        self.threshold = threshold

    def get_expected_args(self):
        return {'resolver': RESOLVER_PARTICIPANT}

    def __call__(self, resolver=None):
        if self.test_based_score is None:
            return TestResult(False, 'Failed, no test_based_score provided.')
        else:
            operator_symbol = self.test_based_score.passes_threshold(resolver, self.threshold) or Operator.from_function(self.threshold.comparison).symbol
            return TestResult(False, 'Failed {}. Operator: {}. Threshold: {}', (self.test_based_score.__name__),
              operator_symbol, (self.threshold),
              tooltip=(self.tooltip))
        return TestResult.TRUE


TunableTestBasedScoreThresholdTest = TunableSingletonFactory.create_auto_factory(TestBasedScoreThresholdTest)