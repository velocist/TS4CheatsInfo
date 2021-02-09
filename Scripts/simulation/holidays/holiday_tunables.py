# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\holidays\holiday_tunables.py
# Compiled at: 2018-03-21 02:20:27
# Size of source mod 2**32: 3357 bytes
from sims4.resources import Types
from sims4.tuning.tunable import TunableVariant, TunableFactory, TunableReferenceFactory
import services

class TunableActiveHoliday(TunableFactory):

    @staticmethod
    def _get_active_holiday():
        active_household = services.active_household()
        if active_household is None:
            return
        return active_household.holiday_tracker.active_holiday_id

    FACTORY_TYPE = _get_active_holiday


class TunableUpcomingHoliday(TunableFactory):

    @staticmethod
    def _get_upcoming_holiday():
        active_household = services.active_household()
        if active_household is None:
            return
        return active_household.holiday_tracker.upcoming_holiday_id

    FACTORY_TYPE = _get_upcoming_holiday


class TunableActiveOrUpcomingHoliday(TunableFactory):

    @staticmethod
    def _get_active_or_upcoming_holiday():
        active_household = services.active_household()
        if active_household is None:
            return
        return active_household.holiday_tracker.get_active_or_upcoming_holiday()

    FACTORY_TYPE = _get_active_or_upcoming_holiday


class TunableHolidayVariant(TunableVariant):

    def __init__(self, *args, default='specific_holiday', **kwargs):
        (super().__init__)(args, active_holiday=TunableActiveHoliday(description='\n                The current holiday in pre-holiday state.\n                \n                Can return no holiday if there is no holiday in pre-holiday\n                state.\n                '), 
         upcoming_holiday=TunableUpcomingHoliday(description='\n                The active holiday.\n                \n                Can return no holiday if there is no holiday running.\n                '), 
         active_or_upcoming=TunableActiveOrUpcomingHoliday(description='\n                The active or upcoming holiday.\n                \n                First checks for an active holiday.\n                If there is no active holiday, falls back to a holiday that\n                is in pre-holiday state.\n                \n                Can return no holiday if there is no holiday in either state.\n                \n                '), 
         specific_holiday=TunableReferenceFactory(description='\n                The holiday definition.\n                ',
  manager=(services.get_instance_manager(Types.HOLIDAY_DEFINITION))), 
         default=default, **kwargs)