# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\picker\filtered_object_picker.py
# Compiled at: 2018-03-09 03:32:23
# Size of source mod 2**32: 2513 bytes
from interactions.base.picker_interaction import ObjectPickerInteraction
from interactions.utils.object_definition_or_tags import ObjectDefinitonsOrTagsVariant
from sims4.tuning.tunable import TunableVariant
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import flexmethod
import services, sims4.log
logger = sims4.log.Logger('FilteredObjectPickerInteraction', default_owner='jdimailig')

class FilteredObjectPickerInteraction(ObjectPickerInteraction):
    ON_LOT_ONLY = 'on_lot'
    OFF_LOT_ONLY = 'off_lot'
    ANYWHERE = 'anywhere'
    INSTANCE_TUNABLES = {'object_filter':ObjectDefinitonsOrTagsVariant(description='\n            Filter to use to find an object.\n            ',
       tuning_group=GroupNames.PICKERTUNING), 
     'on_off_lot_requirement':TunableVariant(description='\n            Whether to accept objects on the active lot.\n            ',
       default=ON_LOT_ONLY,
       locked_args={ON_LOT_ONLY: ON_LOT_ONLY, 
      OFF_LOT_ONLY: OFF_LOT_ONLY, 
      ANYWHERE: ANYWHERE},
       tuning_group=GroupNames.PICKERTUNING)}

    @flexmethod
    def _get_objects_gen(cls, inst, target, context, **kwargs):
        object_manager = services.object_manager()
        if cls.on_off_lot_requirement == cls.ANYWHERE:
            yield from object_manager.get_objects_with_filter_gen(cls.object_filter)
        else:
            if cls.on_off_lot_requirement == cls.ON_LOT_ONLY:
                for obj in object_manager.get_objects_with_filter_gen(cls.object_filter):
                    if obj.is_on_active_lot():
                        yield obj

            else:
                for obj in object_manager.get_objects_with_filter_gen(cls.object_filter):
                    if not obj.is_on_active_lot():
                        yield obj