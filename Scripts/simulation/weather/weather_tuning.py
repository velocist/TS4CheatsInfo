# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\weather\weather_tuning.py
# Compiled at: 2020-08-06 21:24:49
# Size of source mod 2**32: 1535 bytes
from sims4.tuning.tunable import TunableTuple, Tunable

class TuningPrescribedWeatherType(TunableTuple):

    def __init__(self, **kwargs):
        (super().__init__)(rain=Tunable(description='\n                If checked this forecast will be unavailable if rain is disabled\n                ',
  tunable_type=bool,
  default=False), 
         storm=Tunable(description='\n                If checked this forecast will be unavailable if storm is disabled\n                ',
  tunable_type=bool,
  default=False), 
         snow=Tunable(description='\n                If checked this forecast will be unavailable if snow is disabled\n                ',
  tunable_type=bool,
  default=False), 
         blizzard=Tunable(description='\n                If checked this forecast will be unavailable if blizzard is disabled\n                ',
  tunable_type=bool,
  default=False), 
         thunder_snow_storms=Tunable(description='\n                If checked this forecast will be unavailable if thunder snow storms are disabled in the options menu.\n                ',
  tunable_type=bool,
  default=False), **kwargs)