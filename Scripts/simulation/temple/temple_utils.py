# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\temple\temple_utils.py
# Compiled at: 2017-08-29 00:28:29
# Size of source mod 2**32: 738 bytes
import services

class TempleUtils:

    @classmethod
    def get_temple_zone_director(cls):
        zone_director = services.venue_service().get_zone_director()
        if hasattr(zone_director, '_temple_data'):
            return zone_director