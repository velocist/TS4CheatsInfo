# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\statistics\continuous_statistic_tracker.py
# Compiled at: 2020-01-11 01:34:09
# Size of source mod 2**32: 2160 bytes
import sims4.log, statistics.base_statistic_tracker, services
logger = sims4.log.Logger('Statistic')

class ContinuousStatisticTracker(statistics.base_statistic_tracker.BaseStatisticTracker):
    __slots__ = ()

    def get_decay_time(self, stat_type, threshold):
        stat = self.get_statistic(stat_type)
        if stat is not None:
            return stat.get_decay_time(threshold)

    def debug_output_all(self, _connection):
        if self._statistics is None:
            return
        stat_iter = (stat for stat in self._statistics.values() if stat is not None)
        for stat in sorted((list(stat_iter)), key=(lambda stat: stat.stat_type.__name__)):
            sims4.commands.output('{:<44} ID:{:<6} Value: {:-8.2f}, Decay: {:-5.2f}, ChangeRate: {:-5.2f}'.format(stat.__class__.__name__, stat.guid64, stat.get_value(), stat.get_decay_rate(), stat.get_change_rate()), _connection)

    def debug_output_all_automation(self, _connection):
        if self._statistics is None:
            return
        stat_iter = (stat for stat in self._statistics.values() if stat is not None)
        for stat in list(stat_iter):
            sims4.commands.automation_output('CommodityInfo; Type:DATA, Name:{}, Value:{}, Decay:{}'.format(stat.__class__.__name__, stat.get_value(), stat.get_decay_rate()), _connection)

    def set_convergence(self, stat_type, convergence):
        if convergence != stat_type.default_convergence_value:
            stat_inst = self.get_statistic(stat_type, add=(stat_type.add_if_not_in_tracker))
        else:
            stat_inst = self.get_statistic(stat_type)
        if stat_inst is not None:
            if stat_inst.convergence_value != convergence:
                stat_inst.convergence_value = convergence

    def reset_convergence(self, stat_type):
        stat_inst = self.get_statistic(stat_type)
        if stat_inst is not None:
            stat_inst.reset_convergence_value()