# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: D:\dev\TS4\_deploy\Client\Releasex64\Python\Generated\protocolbuffers\WeatherSeasons_pb2.py
# Compiled at: 2020-12-13 14:24:12
# Size of source mod 2**32: 19037 bytes
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
import protocolbuffers.ResourceKey_pb2 as ResourceKey_pb2
import protocolbuffers.Localization_pb2 as Localization_pb2
import protocolbuffers.Lot_pb2 as Lot_pb2
DESCRIPTOR = descriptor.FileDescriptor(name='WeatherSeasons.proto',
  package='EA.Sims4.Network',
  serialized_pb='\n\x14WeatherSeasons.proto\x12\x10EA.Sims4.Network\x1a\x11ResourceKey.proto\x1a\x12Localization.proto\x1a\tLot.proto"±\x07\n!SeasonWeatherInterpolationMessage\x12g\n\x0cmessage_type\x18\x01 \x02(\x0e2Q.EA.Sims4.Network.SeasonWeatherInterpolationMessage.SeasonWeatherInterpolatedType\x12\x13\n\x0bstart_value\x18\x02 \x02(\x02\x12\x12\n\nstart_time\x18\x03 \x02(\x04\x12\x11\n\tend_value\x18\x04 \x02(\x02\x12\x10\n\x08end_time\x18\x05 \x02(\x04"Ô\x05\n\x1dSeasonWeatherInterpolatedType\x12\n\n\x06SEASON\x10\x00\x12\x15\n\x11LEAF_ACCUMULATION\x10\x01\x12\x11\n\rFLOWER_GROWTH\x10\x02\x12\x15\n\x11FOLIAGE_REDUCTION\x10\x03\x12\x16\n\x12FOLIAGE_COLORSHIFT\x10\x04\x12\r\n\x08RAINFALL\x10è\x07\x12\r\n\x08SNOWFALL\x10é\x07\x12\x16\n\x11RAIN_ACCUMULATION\x10ê\x07\x12\x16\n\x11SNOW_ACCUMULATION\x10ë\x07\x12\x11\n\x0cWINDOW_FROST\x10ì\x07\x12\x11\n\x0cWATER_FROZEN\x10í\x07\x12\t\n\x04WIND\x10î\x07\x12\x10\n\x0bTEMPERATURE\x10ï\x07\x12\x0c\n\x07THUNDER\x10ð\x07\x12\x0e\n\tLIGHTNING\x10ñ\x07\x12\x13\n\x0eSNOW_FRESHNESS\x10ò\x07\x12\x0e\n\tSTORY_ACT\x10ó\x07\x12\x12\n\rECO_FOOTPRINT\x10ô\x07\x12\x0e\n\tACID_RAIN\x10õ\x07\x12\x18\n\x13STARWARS_RESISTANCE\x10ö\x07\x12\x19\n\x14STARWARS_FIRST_ORDER\x10÷\x07\x12\x11\n\x0cSNOW_ICINESS\x10ø\x07\x12\x19\n\x14SKYBOX_PARTLY_CLOUDY\x10Ð\x0f\x12\x11\n\x0cSKYBOX_CLEAR\x10Ñ\x0f\x12\x1b\n\x16SKYBOX_LIGHTRAINCLOUDS\x10Ò\x0f\x12\x1a\n\x15SKYBOX_DARKRAINCLOUDS\x10Ó\x0f\x12\x1b\n\x16SKYBOX_LIGHTSNOWCLOUDS\x10Ô\x0f\x12\x1a\n\x15SKYBOX_DARKSNOWCLOUDS\x10Õ\x0f\x12\x12\n\rSKYBOX_CLOUDY\x10Ö\x0f\x12\x14\n\x0fSKYBOX_HEATWAVE\x10×\x0f\x12\x13\n\x0eSKYBOX_STRANGE\x10Ø\x0f\x12\x17\n\x12SKYBOX_VERYSTRANGE\x10Ù\x0f\x12\x16\n\x11SKYBOX_INDUSTRIAL\x10Ú\x0f"t\n\x1bSeasonWeatherInterpolations\x12U\n\x18season_weather_interlops\x18\x01 \x03(\x0b23.EA.Sims4.Network.SeasonWeatherInterpolationMessage"\x8e\x02\n\rRegionWeather\x12\x0e\n\x06region\x18\x01 \x02(\x06\x12>\n\x07weather\x18\x02 \x02(\x0b2-.EA.Sims4.Network.SeasonWeatherInterpolations\x12\x15\n\rweather_event\x18\x03 \x02(\x06\x12\x1b\n\x13forecast_time_stamp\x18\x04 \x02(\x04\x12\x1f\n\x17next_weather_event_time\x18\x05 \x02(\x04\x12\x15\n\tforecasts\x18\x06 \x03(\x04B\x02\x10\x01\x12\x19\n\x11override_forecast\x18\x07 \x01(\x04\x12&\n\x1eoverride_forecast_season_stamp\x18\x08 \x01(\x04"U\n\x19PersistableWeatherService\x128\n\x0fregion_weathers\x18\x01 \x03(\x0b2\x1f.EA.Sims4.Network.RegionWeather"1\n\x0fUiWeatherUpdate\x12\x1e\n\x12weather_type_enums\x18\x01 \x03(\x03B\x02\x10\x01"<\n\x17UiWeatherForecastUpdate\x12!\n\x15forecast_instance_ids\x18\x01 \x03(\x04B\x02\x10\x01')
_SEASONWEATHERINTERPOLATIONMESSAGE_SEASONWEATHERINTERPOLATEDTYPE = descriptor.EnumDescriptor(name='SeasonWeatherInterpolatedType',
  full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.SeasonWeatherInterpolatedType',
  filename=None,
  file=DESCRIPTOR,
  values=[
 descriptor.EnumValueDescriptor(name='SEASON',
   index=0,
   number=0,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='LEAF_ACCUMULATION',
   index=1,
   number=1,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='FLOWER_GROWTH',
   index=2,
   number=2,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='FOLIAGE_REDUCTION',
   index=3,
   number=3,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='FOLIAGE_COLORSHIFT',
   index=4,
   number=4,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='RAINFALL',
   index=5,
   number=1000,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SNOWFALL',
   index=6,
   number=1001,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='RAIN_ACCUMULATION',
   index=7,
   number=1002,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SNOW_ACCUMULATION',
   index=8,
   number=1003,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='WINDOW_FROST',
   index=9,
   number=1004,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='WATER_FROZEN',
   index=10,
   number=1005,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='WIND',
   index=11,
   number=1006,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='TEMPERATURE',
   index=12,
   number=1007,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='THUNDER',
   index=13,
   number=1008,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='LIGHTNING',
   index=14,
   number=1009,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SNOW_FRESHNESS',
   index=15,
   number=1010,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='STORY_ACT',
   index=16,
   number=1011,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='ECO_FOOTPRINT',
   index=17,
   number=1012,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='ACID_RAIN',
   index=18,
   number=1013,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='STARWARS_RESISTANCE',
   index=19,
   number=1014,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='STARWARS_FIRST_ORDER',
   index=20,
   number=1015,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SNOW_ICINESS',
   index=21,
   number=1016,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_PARTLY_CLOUDY',
   index=22,
   number=2000,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_CLEAR',
   index=23,
   number=2001,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_LIGHTRAINCLOUDS',
   index=24,
   number=2002,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_DARKRAINCLOUDS',
   index=25,
   number=2003,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_LIGHTSNOWCLOUDS',
   index=26,
   number=2004,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_DARKSNOWCLOUDS',
   index=27,
   number=2005,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_CLOUDY',
   index=28,
   number=2006,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_HEATWAVE',
   index=29,
   number=2007,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_STRANGE',
   index=30,
   number=2008,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_VERYSTRANGE',
   index=31,
   number=2009,
   options=None,
   type=None),
 descriptor.EnumValueDescriptor(name='SKYBOX_INDUSTRIAL',
   index=32,
   number=2010,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=314,
  serialized_end=1038)
_SEASONWEATHERINTERPOLATIONMESSAGE = descriptor.Descriptor(name='SeasonWeatherInterpolationMessage',
  full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='message_type',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.message_type',
   index=0,
   number=1,
   type=14,
   cpp_type=8,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='start_value',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.start_value',
   index=1,
   number=2,
   type=2,
   cpp_type=6,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='start_time',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.start_time',
   index=2,
   number=3,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='end_value',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.end_value',
   index=3,
   number=4,
   type=2,
   cpp_type=6,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='end_time',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolationMessage.end_time',
   index=4,
   number=5,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[
 _SEASONWEATHERINTERPOLATIONMESSAGE_SEASONWEATHERINTERPOLATEDTYPE],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=93,
  serialized_end=1038)
_SEASONWEATHERINTERPOLATIONS = descriptor.Descriptor(name='SeasonWeatherInterpolations',
  full_name='EA.Sims4.Network.SeasonWeatherInterpolations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='season_weather_interlops',
   full_name='EA.Sims4.Network.SeasonWeatherInterpolations.season_weather_interlops',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1040,
  serialized_end=1156)
_REGIONWEATHER = descriptor.Descriptor(name='RegionWeather',
  full_name='EA.Sims4.Network.RegionWeather',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='region',
   full_name='EA.Sims4.Network.RegionWeather.region',
   index=0,
   number=1,
   type=6,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='weather',
   full_name='EA.Sims4.Network.RegionWeather.weather',
   index=1,
   number=2,
   type=11,
   cpp_type=10,
   label=2,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='weather_event',
   full_name='EA.Sims4.Network.RegionWeather.weather_event',
   index=2,
   number=3,
   type=6,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='forecast_time_stamp',
   full_name='EA.Sims4.Network.RegionWeather.forecast_time_stamp',
   index=3,
   number=4,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='next_weather_event_time',
   full_name='EA.Sims4.Network.RegionWeather.next_weather_event_time',
   index=4,
   number=5,
   type=4,
   cpp_type=4,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='forecasts',
   full_name='EA.Sims4.Network.RegionWeather.forecasts',
   index=5,
   number=6,
   type=4,
   cpp_type=4,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=(descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '\x10\x01'))),
 descriptor.FieldDescriptor(name='override_forecast',
   full_name='EA.Sims4.Network.RegionWeather.override_forecast',
   index=6,
   number=7,
   type=4,
   cpp_type=4,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 descriptor.FieldDescriptor(name='override_forecast_season_stamp',
   full_name='EA.Sims4.Network.RegionWeather.override_forecast_season_stamp',
   index=7,
   number=8,
   type=4,
   cpp_type=4,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1159,
  serialized_end=1429)
_PERSISTABLEWEATHERSERVICE = descriptor.Descriptor(name='PersistableWeatherService',
  full_name='EA.Sims4.Network.PersistableWeatherService',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='region_weathers',
   full_name='EA.Sims4.Network.PersistableWeatherService.region_weathers',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1431,
  serialized_end=1516)
_UIWEATHERUPDATE = descriptor.Descriptor(name='UiWeatherUpdate',
  full_name='EA.Sims4.Network.UiWeatherUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='weather_type_enums',
   full_name='EA.Sims4.Network.UiWeatherUpdate.weather_type_enums',
   index=0,
   number=1,
   type=3,
   cpp_type=2,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=(descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '\x10\x01')))],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1518,
  serialized_end=1567)
_UIWEATHERFORECASTUPDATE = descriptor.Descriptor(name='UiWeatherForecastUpdate',
  full_name='EA.Sims4.Network.UiWeatherForecastUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 descriptor.FieldDescriptor(name='forecast_instance_ids',
   full_name='EA.Sims4.Network.UiWeatherForecastUpdate.forecast_instance_ids',
   index=0,
   number=1,
   type=4,
   cpp_type=4,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=(descriptor._ParseOptions(descriptor_pb2.FieldOptions(), '\x10\x01')))],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1569,
  serialized_end=1629)
_SEASONWEATHERINTERPOLATIONMESSAGE.fields_by_name['message_type'].enum_type = _SEASONWEATHERINTERPOLATIONMESSAGE_SEASONWEATHERINTERPOLATEDTYPE
_SEASONWEATHERINTERPOLATIONMESSAGE_SEASONWEATHERINTERPOLATEDTYPE.containing_type = _SEASONWEATHERINTERPOLATIONMESSAGE
_SEASONWEATHERINTERPOLATIONS.fields_by_name['season_weather_interlops'].message_type = _SEASONWEATHERINTERPOLATIONMESSAGE
_REGIONWEATHER.fields_by_name['weather'].message_type = _SEASONWEATHERINTERPOLATIONS
_PERSISTABLEWEATHERSERVICE.fields_by_name['region_weathers'].message_type = _REGIONWEATHER
DESCRIPTOR.message_types_by_name['SeasonWeatherInterpolationMessage'] = _SEASONWEATHERINTERPOLATIONMESSAGE
DESCRIPTOR.message_types_by_name['SeasonWeatherInterpolations'] = _SEASONWEATHERINTERPOLATIONS
DESCRIPTOR.message_types_by_name['RegionWeather'] = _REGIONWEATHER
DESCRIPTOR.message_types_by_name['PersistableWeatherService'] = _PERSISTABLEWEATHERSERVICE
DESCRIPTOR.message_types_by_name['UiWeatherUpdate'] = _UIWEATHERUPDATE
DESCRIPTOR.message_types_by_name['UiWeatherForecastUpdate'] = _UIWEATHERFORECASTUPDATE

class SeasonWeatherInterpolationMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SEASONWEATHERINTERPOLATIONMESSAGE


class SeasonWeatherInterpolations(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SEASONWEATHERINTERPOLATIONS


class RegionWeather(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _REGIONWEATHER


class PersistableWeatherService(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PERSISTABLEWEATHERSERVICE


class UiWeatherUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UIWEATHERUPDATE


class UiWeatherForecastUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UIWEATHERFORECASTUPDATE