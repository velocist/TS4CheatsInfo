# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\portals\portal_data_dynamic_stairs.py
# Compiled at: 2020-09-14 16:58:25
# Size of source mod 2**32: 3559 bytes
from routing import Location
from routing.portals import portal_location
from routing.portals.portal_data_stairs import _PortalTypeDataStairs
from routing.portals.portal_tuning import PortalFlags
from sims4.tuning.tunable import TunableList, TunableTuple, TunableRange
import routing

class _PortalTypeDataDynamicStairs(_PortalTypeDataStairs):
    FACTORY_TUNABLES = {'lanes':TunableList(description='\n            The bones that describe each set of lanes (up and down).\n            ',
       tunable=TunableTuple(description='\n                Groups of bones that represent the up and down routes for this\n                lane.\n                ',
       up_begin=portal_location._PortalBoneLocation.TunableFactory(description='\n                    The bone for the beginning of the path up the stairs.\n                    '),
       up_end=portal_location._PortalBoneLocation.TunableFactory(description='\n                    The bone for the end of the path up the stairs.\n                    '),
       down_begin=portal_location._PortalBoneLocation.TunableFactory(description='\n                    The bone for the beginning of the path down the stairs.\n                    '),
       down_end=portal_location._PortalBoneLocation.TunableFactory(description='\n                    The bone for the end of the path down the stairs.\n                    '))), 
     'stair_count':TunableRange(description='\n            The number of stairs the Sim will traverse for this portal.\n            ',
       tunable_type=int,
       default=8,
       minimum=1)}

    def get_additional_required_portal_flags(self, entry_location, exit_location):
        return PortalFlags.STAIRS_PORTAL_LONG

    def get_stair_count(self, _):
        return self.stair_count

    def get_portal_locations(self, obj):
        locations = []
        portal_key_mask = routing.get_stair_portal_key_mask(obj.id, obj.zone_id)
        for lane in self.lanes:
            up_start = lane.up_begin(obj)
            up_end = lane.up_end(obj)
            down_start = lane.down_begin(obj)
            down_end = lane.down_end(obj)
            locations.append((Location((up_start.position), routing_surface=(up_start.routing_surface)),
             Location((up_end.position), routing_surface=(up_end.routing_surface)),
             Location((down_start.position), routing_surface=(down_start.routing_surface)),
             Location((down_end.position), routing_surface=(down_end.routing_surface)),
             portal_key_mask | PortalFlags.STAIRS_PORTAL_LONG))

        return locations