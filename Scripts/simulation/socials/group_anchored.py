# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\socials\group_anchored.py
# Compiled at: 2018-02-20 20:14:23
# Size of source mod 2**32: 2496 bytes
from sims4.tuning.instances import lock_instance_tunables
from sims4.utils import flexmethod
from socials.group import SocialGroup
import sims4.log
logger = sims4.log.Logger('Social Group')

class SocialGroupAnchored(SocialGroup):

    @classmethod
    def _get_social_anchor_object(cls, si, target_sim):
        if si.picked_object is None:
            logger.error('{} is being created with no picked object. Are you sure {} was pushed from a picker?', cls, si)
        return si.picked_object

    @classmethod
    def can_get_close_and_wait(cls, sim, target):
        return False

    @flexmethod
    def make_constraint_default(cls, inst, sim, target, position, routing_surface, *, picked_object=None, **kwargs):
        picked_object = inst.anchor if inst is not None else picked_object
        if picked_object is None:
            logger.error('{} is not being provided a picked object in make_constraint_default(). That is not supported.')
        else:
            position = picked_object.position
            routing_surface = picked_object.routing_surface
        return (super(__class__, inst if inst is not None else cls).make_constraint_default)(sim, target, position, routing_surface, picked_object=picked_object, **kwargs)


lock_instance_tunables(SocialGroupAnchored, adjust_sim_positions_dynamically=False,
  social_anchor_object=None)