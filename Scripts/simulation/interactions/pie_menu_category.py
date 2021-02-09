# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\pie_menu_category.py
# Compiled at: 2015-03-10 21:12:11
# Size of source mod 2**32: 3896 bytes
from sims4.localization import TunableLocalizedStringFactory
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, Tunable, TunableResourceKey, TunableEnumEntry, TunableMapping, TunableTuple
from sims4.tuning.tunable_base import ExportModes
import enum, services, sims4.resources

class SpecialPieMenuCategoryType(enum.Int):
    NO_CATEGORY = 0
    MORE_CATEGORY = 1


class PieMenuCategory(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.PIE_MENU_CATEGORY)):
    INSTANCE_TUNABLES = {'_display_name':TunableLocalizedStringFactory(description='\n            Localized name of this category',
       export_modes=ExportModes.All), 
     '_icon':TunableResourceKey(description='\n            Icon to be displayed in the pie menu\n            ',
       resource_types=sims4.resources.CompoundTypes.IMAGE,
       default=None,
       allow_none=True,
       export_modes=ExportModes.All), 
     '_collapsible':Tunable(description='\n            If enabled, when this category only has one item inside, that item will show on the pie menu without going through this category.\n            If disabled, the user will always go through this category, regardless of the number of entries within.',
       tunable_type=bool,
       default=True,
       export_modes=ExportModes.All), 
     '_parent':TunableReference(description='\n            Parent category.\n            ',
       manager=services.get_instance_manager(sims4.resources.Types.PIE_MENU_CATEGORY),
       allow_none=True,
       export_modes=ExportModes.All), 
     '_special_category':TunableEnumEntry(description='\n            Designate this category as a special category.  Most will be NO_CATEGORY.\n            ',
       tunable_type=SpecialPieMenuCategoryType,
       default=SpecialPieMenuCategoryType.NO_CATEGORY,
       export_modes=ExportModes.All), 
     '_display_priority':Tunable(description='\n            The display priority of this category.\n            ',
       tunable_type=int,
       default=1,
       export_modes=ExportModes.All), 
     'mood_overrides':TunableMapping(description='\n            If sim matches mood, tooltip and display name of category will\n            be updated with tuned values.\n            ',
       key_type=TunableReference(manager=(services.get_instance_manager(sims4.resources.Types.MOOD))),
       value_type=TunableTuple(name_override=TunableLocalizedStringFactory(description='\n                   Localized name of this category\n                   ',
       allow_none=True),
       tooltip=TunableLocalizedStringFactory(description='\n                   Tooltip for the new category.\n                   ',
       allow_none=True),
       export_class_name='text_overrides'),
       key_value_type=None,
       key_name='mood',
       value_name='override_data',
       tuple_name='mood_to_override_data',
       export_modes=(
      ExportModes.ClientBinary,))}