# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\venues\gym_zone_director.py
# Compiled at: 2015-08-05 03:29:49
# Size of source mod 2**32: 542 bytes
from situations.complex.yoga_class import YogaClassScheduleMixin
from venues.scheduling_zone_director import SchedulingZoneDirector
from venues.visitor_situation_on_arrival_zone_director_mixin import VisitorSituationOnArrivalZoneDirectorMixin

class GymZoneDirector(YogaClassScheduleMixin, VisitorSituationOnArrivalZoneDirectorMixin, SchedulingZoneDirector):
    pass