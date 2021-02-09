# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\crafting\photography_service.py
# Compiled at: 2017-06-14 07:18:31
# Size of source mod 2**32: 1184 bytes
from sims4.service_manager import Service
import sims4.log
logger = sims4.log.Logger('Photography', default_owner='shipark')

class PhotographyService(Service):

    def __init__(self):
        self._loots = []

    def add_loot_for_next_photo_taken(self, loot):
        self._loots.append(loot)

    def apply_loot_for_photo(self, siminfo):
        for photoloot in self._loots:
            photoloot.apply_loot(siminfo)

    def get_loots_for_photo(self):
        return self._loots

    def cleanup(self):
        self._loots = []

    def stop(self):
        self.cleanup()