# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\stored_object_info_tuning.py
# Compiled at: 2018-07-13 01:10:46
# Size of source mod 2**32: 2398 bytes
from interactions import ParticipantTypeSingle
from objects.components import types
from sims4.tuning.dynamic_enum import DynamicEnum
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry
import services

class StoredObjectType(DynamicEnum):
    INVALID = 0
    SNOWPAL = 1


class _ObjectGeneratorFromStoredObjectComponent(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'participant':TunableEnumEntry(description='\n            The participant from which the stored object is returned.\n            ',
       tunable_type=ParticipantTypeSingle,
       default=ParticipantTypeSingle.Actor), 
     'stored_object_type':TunableEnumEntry(description='\n            The type of object to apply loot actions to.\n            ',
       tunable_type=StoredObjectType,
       default=StoredObjectType.INVALID,
       invalid_enums=(
      StoredObjectType.INVALID,))}

    def get_objects(self, resolver, *args, **kwargs):
        owner = (resolver.get_participant)(self.participant, *args, **kwargs)
        if owner is None:
            return ()
        else:
            return owner.is_sim or ()
        stored_object_component = owner.sim_info.get_component(types.STORED_OBJECT_INFO_COMPONENT)
        if stored_object_component is None:
            return ()
        obj_id = stored_object_component.get_stored_object_info_id(self.stored_object_type)
        stored_object = services.object_manager().get(obj_id)
        if stored_object is None:
            stored_object = services.inventory_manager().get(obj_id)
        if stored_object is not None:
            return (
             stored_object,)
        return ()