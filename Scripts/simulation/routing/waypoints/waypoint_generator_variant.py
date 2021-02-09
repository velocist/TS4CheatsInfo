# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\waypoints\waypoint_generator_variant.py
# Compiled at: 2020-04-21 05:39:21
# Size of source mod 2**32: 2162 bytes
from routing.waypoints.waypoint_generator_connected_points import _WaypointGeneratorConnectedPoints
from routing.waypoints.waypoint_generator_ellipse import _WaypointGeneratorEllipse
from routing.waypoints.waypoint_generator_footprint import _WaypointGeneratorFootprint
from routing.waypoints.waypoint_generator_lot import _WaypointGeneratorLotPoints
from routing.waypoints.waypoint_generator_pacing import _WaypointGeneratorPacing
from routing.waypoints.waypoint_generator_points import _WaypointGeneratorObjectPoints
from routing.waypoints.waypoint_generator_pool import _WaypointGeneratorPool
from routing.waypoints.waypoint_generator_spawn_points import _WaypointGeneratorSpawnPoints
from routing.waypoints.waypoint_generator_tags import _WaypointGeneratorMultipleObjectByTag
from routing.waypoints.waypoint_generator_unobstructed_line import _WaypointGeneratorUnobstructedLine
from sims4.tuning.tunable import TunableVariant

class TunableWaypointGeneratorVariant(TunableVariant):

    def __init__(self, *args, **kwargs):
        (super().__init__)(args, description='\n            Define how the waypoints are generated.\n            ', 
         spawn_points=_WaypointGeneratorSpawnPoints.TunableFactory(), 
         lot_points=_WaypointGeneratorLotPoints.TunableFactory(), 
         pool_laps=_WaypointGeneratorPool.TunableFactory(), 
         object_points=_WaypointGeneratorObjectPoints.TunableFactory(), 
         pacing=_WaypointGeneratorPacing.TunableFactory(), 
         multiple_objects_by_tag=_WaypointGeneratorMultipleObjectByTag.TunableFactory(), 
         ellipse=_WaypointGeneratorEllipse.TunableFactory(), 
         footprint=_WaypointGeneratorFootprint.TunableFactory(), 
         unobstructed_line=_WaypointGeneratorUnobstructedLine.TunableFactory(), 
         connected_points=_WaypointGeneratorConnectedPoints.TunableFactory(), 
         default='spawn_points', **kwargs)