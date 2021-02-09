# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\formation\formation_liability.py
# Compiled at: 2017-10-07 02:49:24
# Size of source mod 2**32: 727 bytes
from interactions.liability import ReplaceableLiability

class RoutingFormationLiability(ReplaceableLiability):
    LIABILITY_TOKEN = 'RoutingFormationLiability'

    def __init__(self, routing_formation_data, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._routing_formation_data = routing_formation_data

    def release(self):
        self._routing_formation_data.release_formation_data()