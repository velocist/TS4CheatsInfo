# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\jigs.py
# Compiled at: 2020-02-05 01:46:12
# Size of source mod 2**32: 1029 bytes
import objects.game_object, objects.object_enums, objects.persistence_groups, sims4.tuning.instances

class Jig(objects.game_object.GameObject):

    @property
    def persistence_group(self):
        return objects.persistence_groups.PersistenceGroups.NONE

    @persistence_group.setter
    def persistence_group(self, value):
        pass

    def save_object(self, object_list, *args, item_location=objects.object_enums.ItemLocation.ON_LOT, container_id=0, **kwargs):
        pass

    @property
    def is_valid_posture_graph_object(self):
        return False


sims4.tuning.instances.lock_instance_tunables(Jig, _persistence=(objects.object_enums.PersistenceType.NONE),
  _world_file_object_persists=False)