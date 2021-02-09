# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\performance\test_profiling.py
# Compiled at: 2017-12-05 03:37:08
# Size of source mod 2**32: 1956 bytes


class ProfileMetrics:

    def __init__(self, is_test_set=False):
        self.count = 0
        self.resolve_time = 0
        self.test_time = 0
        self.is_test_set = is_test_set

    def get_total_time(self, include_test_set=True):
        if not self.is_test_set or include_test_set:
            return self.resolve_time + self.test_time
        return self.resolve_time

    def get_average_time(self, include_test_set=True):
        if self.count == 0:
            return 0
        total_time = self.get_total_time(include_test_set=include_test_set)
        if total_time == 0:
            return 0
        return total_time / self.count

    def update(self, resolve_time, test_time):
        self.count += 1
        self.resolve_time += resolve_time
        self.test_time += test_time


class TestProfileRecord:

    def __init__(self, is_test_set=False):
        self.metrics = ProfileMetrics(is_test_set=is_test_set)
        self.resolvers = dict()