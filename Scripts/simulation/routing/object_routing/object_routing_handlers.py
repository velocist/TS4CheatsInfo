# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\object_routing\object_routing_handlers.py
# Compiled at: 2019-07-27 01:21:31
# Size of source mod 2**32: 1990 bytes
from objects.object_enums import ObjectRoutingBehaviorTrackingCategory
from sims4.gsi.dispatcher import GsiHandler
from sims4.gsi.schema import GsiGridSchema
import gsi_handlers, services
object_routing_schema = GsiGridSchema(label='Object Routing')
object_routing_schema.add_field('tracking_category', label='Tracking Category')
with object_routing_schema.add_has_many('active_objects', GsiGridSchema) as (active_objects_schema):
    active_objects_schema.add_field('objId', label='Object Id', width=3, unique_field=True)
    active_objects_schema.add_field('classStr', label='Class', width=3)
    active_objects_schema.add_field('definitionStr', label='Definition', width=3)

@GsiHandler('object_routing_view', object_routing_schema)
def generate_object_routing_view():
    categories = []
    routing_service = services.get_object_routing_service()
    if routing_service:
        for tracking_category in ObjectRoutingBehaviorTrackingCategory:
            if tracking_category is not ObjectRoutingBehaviorTrackingCategory.NONE:
                objects = []
                object_refs = routing_service.get_routing_object_set(tracking_category)
                for obj in object_refs:
                    class_str = gsi_handlers.gsi_utils.format_object_name(obj)
                    definition_str = str(obj.definition.name)
                    object_dict = {'objId':hex(obj.id), 
                     'classStr':class_str, 
                     'definitionStr':definition_str}
                    objects.append(object_dict)

                category_dict = {'tracking_category':tracking_category.name,  'active_objects':objects}
                categories.append(category_dict)

    return categories