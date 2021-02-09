# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\pools\pool_utils.py
# Compiled at: 2019-05-01 19:05:07
# Size of source mod 2**32: 1155 bytes
from _weakrefset import WeakSet
import services, sims4.log, sims4.reload
logger = sims4.log.Logger('Pools', default_owner='bhill')
with sims4.reload.protected(globals()):
    cached_pool_objects = WeakSet()
POOL_LANDING_SURFACE = 'Water'

def get_main_pool_objects_gen():
    yield from cached_pool_objects
    if False:
        yield None


def get_pool_by_block_id(block_id):
    for pool in get_main_pool_objects_gen():
        if pool.block_id == block_id:
            return pool

    zone = services.current_zone()
    if zone is not None:
        if not services.current_zone().is_in_build_buy:
            logger.error('No Pool Matching block Id: {}', block_id, owner='camilogarcia')