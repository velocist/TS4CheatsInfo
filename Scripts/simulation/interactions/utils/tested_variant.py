# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\utils\tested_variant.py
# Compiled at: 2020-04-24 00:20:04
# Size of source mod 2**32: 4474 bytes
from civic_policies.street_civic_policy_tests import StreetCivicPolicyTest
from conditional_layers.conditional_layer_tests import ConditionalLayerLoadedTest
from event_testing.tests import TunableTestSet
from sims4.tuning.tunable import TunableVariant, HasTunableSingletonFactory, AutoFactoryInit, TunableList, TunableTuple
import event_testing, global_policies, narrative
from venues.civic_policies.venue_civic_policy_tests import VenueCivicPolicyTest

class TunableTestedVariant(TunableVariant):

    @staticmethod
    def _create_tested_selector(tunable_type, is_noncallable_type=False):

        class _TestedSelector(HasTunableSingletonFactory):
            FACTORY_TUNABLES = {'records': TunableList(tunable=TunableTuple(tests=(TunableTestSet()),
                          item=tunable_type))}

            def __call__(self, *args, resolver=None, **kwargs):
                for item_pair in self.records:
                    if item_pair.tests.run_tests(resolver):
                        if is_noncallable_type:
                            return item_pair.item
                        return (item_pair.item)(args, resolver=resolver, **kwargs)

        return _TestedSelector.TunableFactory()

    @staticmethod
    def _create_noncallable_item_factory(tunable_type):

        class _NonCallableItem(HasTunableSingletonFactory):
            FACTORY_TUNABLES = {'item': tunable_type}

            def __call__(self, *args, **kwargs):
                return self.item

        return _NonCallableItem.TunableFactory()

    def __init__(self, tunable_type, is_noncallable_type=False, **kwargs):
        (super().__init__)(single=TunableTestedVariant._create_noncallable_item_factory(tunable_type) if is_noncallable_type else tunable_type, 
         tested=TunableTestedVariant._create_tested_selector(tunable_type, is_noncallable_type=is_noncallable_type), 
         default='single', **kwargs)


class TunableGlobalTestList(event_testing.tests.TestListLoadingMixin):
    DEFAULT_LIST = event_testing.tests.TestList()

    def __init__(self, description=None):
        if description is None:
            description = 'A list of tests.  All tests must succeed to pass the TestSet.'
        super().__init__(description=description, tunable=(TunableGlobalTestVariant()))


class TunableGlobalTestVariant(TunableVariant):

    def __init__(self, description='A tunable test supported for a global resolver.', **kwargs):
        (super().__init__)(narrative=narrative.narrative_tests.NarrativeTest.TunableFactory(locked_args={'tooltip': None}), 
         global_policy=global_policies.global_policy_tests.GlobalPolicyStateTest.TunableFactory(locked_args={'tooltip': None}), 
         street_civic_policy=StreetCivicPolicyTest.TunableFactory(locked_args={'tooltip': None}), 
         venue_civic_policy=VenueCivicPolicyTest.TunableFactory(locked_args={'tooltip': None}), 
         conditional_layer_loaded=ConditionalLayerLoadedTest.TunableFactory(locked_args={'tooltip': None}), 
         description=description, **kwargs)