# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\weather\weather_enums.py
# Compiled at: 2020-06-19 01:38:49
# Size of source mod 2**32: 3700 bytes
from collections import namedtuple
from sims4.tuning.dynamic_enum import DynamicEnumLocked
import enum

class Temperature(enum.Int):
    FREEZING = -3
    COLD = -2
    COOL = -1
    WARM = 0
    HOT = 1
    BURNING = 2


class WeatherType(DynamicEnumLocked):
    Freezing = Temperature.FREEZING
    Cold = Temperature.COLD
    Cool = Temperature.COOL
    Warm = Temperature.WARM
    Hot = Temperature.HOT
    Burning = Temperature.BURNING
    UNDEFINED = 10
    AnySnow = 11
    AnyRain = 12
    Max_Snow_Accumulation = 13
    Max_Rain_Accumulation = 14
    AnyLightning = 15
    StruckByLightning = 16


WEATHER_TYPE_DEFINED_ENUMS_END = WeatherType.Max_Rain_Accumulation

class WeatherTypeGroup(enum.Int):
    UNGROUPED = 0
    WEATHER = 1
    TEMPERATURE = 2


class PrecipitationType(enum.Int):
    RAIN = 1000
    SNOW = 1001


class WeatherEffectType(enum.Int):
    WINDOW_FROST = 1004
    WATER_FROZEN = 1005
    WIND = 1006
    TEMPERATURE = 1007
    THUNDER = 1008
    LIGHTNING = 1009
    SNOW_FRESHNESS = 1010
    STRANGERVILLE_ACT = 1011
    ECO_FOOTPRINT = 1012
    ACID_RAIN = 1013
    STARWARS_RESISTANCE = 1014
    STARWARS_FIRST_ORDER = 1015
    SNOW_ICINESS = 1016


class CloudType(enum.Int):
    PARTLY_CLOUDY = 2000
    CLEAR = 2001
    LIGHT_RAINCLOUDS = 2002
    DARK_RAINCLOUDS = 2003
    LIGHT_SNOWCLOUDS = 2004
    DARK_SNOWCLOUDS = 2005
    CLOUDY = 2006
    HEATWAVE = 2007
    STRANGE = 2008
    VERY_STRANGE = 2009
    SKYBOX_INDUSTRIAL = 2010


class GroundCoverType(enum.Int):
    RAIN_ACCUMULATION = 1002
    SNOW_ACCUMULATION = 1003


class WeatherOption(enum.Int):
    WEATHER_ENABLED = 0
    DISABLE_STORMS = 1
    WEATHER_DISABLED = 2


class SnowBehavior(enum.Int):
    NO_SNOW = 0
    ACCUMULATE = 1
    PERMANENT = 2


WeatherElementTuple = namedtuple('WeatherElementTuple', 'start_value, start_time, end_value, end_time')