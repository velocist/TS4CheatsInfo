# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\puddles\puddle_commands.py
# Compiled at: 2015-05-07 02:55:29
# Size of source mod 2**32: 1671 bytes
from objects.puddles import create_puddle, PuddleSize, PuddleLiquid
from objects.puddles.puddle import Puddle
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target, RequiredTargetParam
import sims4.commands

@sims4.commands.Command('puddles.create')
def puddle_create(count: int=1, size: PuddleSize=PuddleSize.MediumPuddle, liquid=PuddleLiquid.WATER, obj: OptionalTargetParam=None, _connection=None):
    obj = get_optional_target(obj, _connection)
    if obj is None:
        return False
    for _ in range(count):
        puddle = create_puddle(size, liquid)
        if puddle is None:
            return False
        puddle.place_puddle(obj, max_distance=8)

    return True


@sims4.commands.Command('puddles.evaporate')
def puddle_evaporate(obj_id: RequiredTargetParam, _connection=None):
    obj = obj_id.get_target()
    if obj is None:
        return False
    else:
        return isinstance(obj, Puddle) or False
    obj.evaporate(None)
    return True


@sims4.commands.Command('puddles.grow')
def puddle_grow(obj_id: RequiredTargetParam, _connection=None):
    obj = obj_id.get_target()
    if obj is None:
        return False
    else:
        return isinstance(obj, Puddle) or False
    obj.try_grow_puddle()
    return True