# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\tunable_utils\tested_list.py
# Compiled at: 2020-06-24 01:38:09
# Size of source mod 2**32: 2186 bytes
from event_testing.tests import TunableTestSet
from sims4.tuning.tunable import TunableList, TunableTuple, Tunable
from singletons import DEFAULT

class _TestedList(tuple):

    def get_all(self):
        for item_data in self:
            yield item_data.item

    def __call__(self, *, resolver):
        for item_data in self:
            if item_data.test.run_tests(resolver):
                yield item_data.item
                if item_data.stop_processing:
                    break


STOP_PROCESSING_ALWAYS = 'stop_processing_always'

class TunableTestedList(TunableList):
    DEFAULT_LIST = _TestedList()

    def __init__(self, *args, tunable_type, stop_processing_behavior=DEFAULT, **kwargs):
        tuple_args = {}
        if stop_processing_behavior is DEFAULT:
            tuple_args['stop_processing'] = Tunable(description='\n                If checked, no other element from this list is considered if\n                this element passes its associated test.\n                ',
              tunable_type=bool,
              default=False)
        else:
            if stop_processing_behavior == STOP_PROCESSING_ALWAYS:
                tuple_args['locked_args'] = {'stop_processing': True}
        (super().__init__)(args, tunable=TunableTuple(description='\n                An entry in this tested list.\n                ', 
                   test=TunableTestSet(), 
                   item=tunable_type, **tuple_args), **kwargs)

    def load_etree_node(self, node, source, expect_error):
        value = super().load_etree_node(node, source, expect_error)
        return _TestedList(value)