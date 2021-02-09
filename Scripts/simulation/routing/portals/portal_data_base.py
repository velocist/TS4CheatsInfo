# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\portals\portal_data_base.py
# Compiled at: 2019-08-12 22:10:33
# Size of source mod 2**32: 4911 bytes
from routing.portals.portal_enums import PathSplitType
from routing.portals.portal_event import TunablePortalEventVariant
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableList

class _PortalTypeDataBase(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'portal_events': TunableList(description='\n            A list of portal events to add when a Sim uses the portal.\n            ',
                        tunable=TunablePortalEventVariant(description='\n                The tuning for a specific portal event.\n                '))}

    @property
    def portal_type(self):
        raise NotImplementedError

    @property
    def outfit_change(self):
        pass

    @property
    def requires_los_between_points(self):
        return True

    @property
    def lock_portal_on_use(self):
        return True

    def get_additional_required_portal_flags(self, entry_location, exit_location):
        return 0

    def notify_in_use(self, user, portal_instance, portal_object):
        pass

    def add_portal_data(self, actor, portal_instance, is_mirrored, walkstyle):
        pass

    def add_portal_events(self, portal, actor, obj, time, route_pb):
        for portal_event in self.portal_events:
            op = portal_event.get_portal_op(actor, obj)
            event = route_pb.events.add()
            event.time = max(0, time + portal_event.time)
            event.type = portal_event.get_portal_event_type()
            event.data = op.SerializeToString()

    def get_portal_asm_params(self, portal_instance, portal_id, sim):
        return {}

    def get_destination_objects(self):
        return ()

    def get_portal_duration(self, portal_instance, is_mirrored, walkstyle, age, gender, species):
        raise NotImplementedError

    def get_portal_locations(self, obj):
        raise NotImplementedError

    def get_posture_change(self, portal_instance, is_mirrored, initial_posture):
        return (
         initial_posture, initial_posture)

    def is_ungreeted_sim_disallowed(self):
        return False

    def split_path_on_portal(self):
        return PathSplitType.PathSplitType_DontSplit

    def provide_route_events(self, *args, **kwargs):
        pass