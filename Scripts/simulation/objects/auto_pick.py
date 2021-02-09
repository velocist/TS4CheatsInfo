# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\auto_pick.py
# Compiled at: 2018-03-30 20:27:38
# Size of source mod 2**32: 2565 bytes
import operator, random
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, TunableVariant
from sims4.utils import flexmethod
import services, sims4.log
logger = sims4.log.Logger('AutoPick', default_owner='jdimailig')

class AutoPick(TunableVariant):

    def __init__(self, **kwargs):
        (super().__init__)(randomized_pick=AutoPickRandom.TunableFactory(), 
         best_object_relationship=AutoPickBestObjectRelationship.TunableFactory(), 
         locked_args={'disabled': False}, 
         default='disabled', **kwargs)


class AutoPickRandom(HasTunableSingletonFactory, AutoFactoryInit):

    @flexmethod
    def perform_auto_pick(cls, inst, choices):
        return random.choice(choices)


class AutoPickBestObjectRelationship(HasTunableSingletonFactory, AutoFactoryInit):

    @flexmethod
    def perform_auto_pick(cls, inst, choices):
        household = services.active_household()
        if household is None:
            return
        else:
            sim_ids = tuple((sim_info.id for sim_info in household.sim_info_gen()))
            obj_rel_tuples_list = []
            for choice in choices:
                obj_rel_tuples_list.extend(cls._get_obj_rel_tuples_for_sims(choice, sim_ids))

            return obj_rel_tuples_list or None
        return max(obj_rel_tuples_list, key=(operator.itemgetter(1)))[0]

    @classmethod
    def _get_obj_rel_tuples_for_sims(cls, obj, sim_ids):
        tuple_list = []
        comp = obj.objectrelationship_component
        if comp is None:
            return tuple_list
        for sim_id in sim_ids:
            if comp.has_relationship(sim_id):
                tuple_list.append((obj, comp.get_relationship_value(sim_id)))

        return tuple_list