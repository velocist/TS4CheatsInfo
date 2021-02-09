# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\venues\venue_object_test.py
# Compiled at: 2019-10-30 00:40:57
# Size of source mod 2**32: 8026 bytes
from event_testing.tests_object import NumberTaggedObjectsOwnedFactory
from sims4.localization import TunableLocalizedString
from sims4.math import MAX_INT32
from sims4.tuning.dynamic_enum import DynamicEnum
from sims4.tuning.tunable import TunableTuple, TunableRange, TunableList, TunableEnumEntry, Tunable
from sims4.tuning.tunable_base import ExportModes
import enum

class TunableVenueObjectTags(NumberTaggedObjectsOwnedFactory):

    def __init__(self, **kwargs):
        (
         (super().__init__)(locked_args={'desired_state': None}, **kwargs),)


class TunableVenueObject(TunableTuple):

    def __init__(self, **kwargs):
        (super().__init__)(object=TunableVenueObjectTags(description="\n                Specify object tag(s) that must be on this venue. Allows you to\n                group objects, i.e. weight bench, treadmill, and basketball\n                goals are tagged as\n                'exercise objects.'\n                ",
  export_modes=(ExportModes.All)), 
         number=TunableRange(description='\n                Number of the tuned object that have to be on the venue. Ex\n                Barstools 4 means you have to have at least 4 barstools before\n                it can be this venue.\n                ',
  tunable_type=int,
  default=1,
  minimum=1,
  export_modes=(ExportModes.All)), 
         object_display_name=TunableLocalizedString(description='\n                Name that will be displayed for the object(s)\n                ',
  allow_catalog_name=True,
  export_modes=(ExportModes.All)), **kwargs)


class VenueObjectTestTag(DynamicEnum):
    INVALID = 0


class VenueObjectTestType(enum.Int):
    INVALID = 0
    OBJECT = 1
    POOL = 2
    TILE = 3


class TunableVenueObjectWithPair(TunableTuple):

    def __init__(self, **kwargs):
        (super().__init__)(object=TunableVenueObjectTags(description="\n                Specify object tag(s) that must be on this venue. Allows you to\n                group objects, i.e. weight bench, treadmill, and basketball\n                goals are tagged as\n                'exercise objects.'\n                ",
  export_modes=(ExportModes.All)), 
         object_parent_pair_tests=TunableList(description="\n                Specify object tag(s) and/or parent attachment tags that\n                requires to be on this venue. Allows you to group objects, i.e.\n                weight bench, treadmill, and basketball goals are tagged as\n                'exercise objects.'\n                ",
  tunable=TunableTuple(object_tags=TunableVenueObjectTags(description='\n                        The objects (tag) that would count for the required items.\n                        ',
  export_modes=(ExportModes.All)),
  parent_tags=TunableVenueObjectTags(description='\n                        If set, the object tuned in object_tags would required\n                        to be slotted to the parent object tuned in\n                        parent_tags. \n                        \n                        E.g. in restaurant, a chair (with restaurant_chair tag)\n                        would need to slot to a table (with\n                        restaurant_table_tag) to count as a dining slot. But\n                        since bar will not has the restaurant_table_tag, so a\n                        high chair that slots to the bar will not count as\n                        dining spot.\n                        ',
  export_modes=(ExportModes.All)),
  count=TunableRange(description='\n                        How many required objects will be satisfied with this\n                        object(and/or with parent pair).\n                        \n                        E.g. a chair that slots to table will count as one\n                        dining spot, but booth slot to table will count as 2.\n                        ',
  tunable_type=int,
  default=1,
  minimum=1),
  required_object_test_tag=TunableEnumEntry(tunable_type=VenueObjectTestTag,
  default=(VenueObjectTestTag.INVALID)),
  export_class_name='VenueObjectParentPairTuple',
  export_modes=(ExportModes.All))), 
         min_number=TunableRange(description='\n                The lower bound above which the number of objects of this type on\n                the lot must be.\n                ',
  tunable_type=int,
  default=0,
  minimum=0,
  export_modes=(ExportModes.All)), 
         max_number=TunableRange(description='\n                The upper bound below which the number of objects of this type on\n                the lot must be.\n                ',
  tunable_type=int,
  default=MAX_INT32,
  minimum=0,
  export_modes=(ExportModes.All)), 
         object_display_name=TunableLocalizedString(description='\n                Name that will be displayed for the object(s)\n                ',
  allow_catalog_name=True,
  export_modes=(ExportModes.All)), 
         tooltip_override=TunableLocalizedString(description='\n                If tuned, the tooltip that will be shown when this requirement\n                is moused over in the venue configuration requirements UI.\n                ',
  export_modes=(ExportModes.All),
  allow_none=True), 
         is_optional=Tunable(description='\n                If True, this object requirement will be optional to this venue.\n                \n                E.g. Waiter station and host station for restaurant should set\n                this entry to True.\n                ',
  tunable_type=bool,
  default=False,
  export_modes=(ExportModes.All)), 
         object_test_type=TunableEnumEntry(description='\n                This option determines what test will be applied. To test the\n                number of objects of a certain type, select OBJECT. To test for\n                a pool, select pool. To test the number of tiles used by the\n                home, select tile (tiny home venues do this).\n                ',
  tunable_type=VenueObjectTestType,
  default=(VenueObjectTestType.OBJECT)), **kwargs)