# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\seasons\seasonal_parameters_mixin.py
# Compiled at: 2020-03-03 20:37:39
# Size of source mod 2**32: 3258 bytes
from seasons.seasons_enums import SeasonType, SeasonParameters
from sims4.tuning.tunable import Tunable, TunableMapping, TunableEnumEntry, TunableList, TunableTuple, TunableRange

@staticmethod
def verify_seasonal_parameters(instance_class, tunable_name, source, value, **kwargs):
    for season_param_type, param_values in value.items():
        timings = list(((pv.season.value + pv.time_in_season) % len(SeasonType) for pv in param_values))
        sorted_timings = sorted(timings)
        start_idx = timings.index(sorted_timings[0])
        for i, sorted_value in enumerate(sorted_timings):
            idx_in_original = (start_idx + i) % len(timings)
            if timings[idx_in_original] != sorted_value:
                logger.error('Incorrect timing order detected! {} appears out of place for {}@{} in {} params.', param_values[idx_in_original].season, param_values[idx_in_original].time_in_season, str(instance_class), season_param_type)


class SeasonalParametersMixin:
    INSTANCE_TUNABLES = {'seasonal_parameters': TunableMapping(description='\n            ',
                              key_type=TunableEnumEntry(description='\n                The parameter that we wish to change.\n                ',
                              tunable_type=SeasonParameters,
                              default=(SeasonParameters.LEAF_ACCUMULATION)),
                              value_type=TunableList(description='\n                A list of the different seasonal parameter changes that we want to\n                send over the course of a year.\n                ',
                              tunable=TunableTuple(season=TunableEnumEntry(description='\n                        The Season that this change is in.\n                        ',
                              tunable_type=SeasonType,
                              default=(SeasonType.SPRING)),
                              time_in_season=TunableRange(description='\n                        The time within the season that this will occur.\n                        ',
                              tunable_type=float,
                              minimum=0.0,
                              maximum=1.0,
                              default=0.0),
                              value=Tunable(description='\n                        The value that we will set this parameter to in the\n                        season\n                        ',
                              tunable_type=float,
                              default=0.0))),
                              verify_tunable_callback=verify_seasonal_parameters)}