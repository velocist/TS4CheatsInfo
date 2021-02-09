# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\broadcasters\broadcaster_loot_op.py
# Compiled at: 2018-07-31 20:59:23
# Size of source mod 2**32: 2652 bytes
from broadcasters.broadcaster_request import BroadcasterRequest
from interactions import ParticipantType
from interactions.utils.loot_basic_op import BaseLootOperation
import element_utils, services, sims4.log
logger = sims4.log.Logger('Broadcaster Loots', default_owner='jdimailig')

def verify_immediate_broadcaster(instance_class, tunable_name, source, broadcaster_types=[], **kwargs):
    from broadcasters.broadcaster import Broadcaster
    for tested_broadcaster_tuple in broadcaster_types:
        broadcaster = tested_broadcaster_tuple.item
        if not broadcaster.frequency.frequency_type != Broadcaster.FREQUENCY_ENTER:
            broadcaster.immediate or logger.error('Only on-enter immediate broadcasters are allowed in this op found {}', broadcaster)


class BroadcasterOneShotLootOp(BaseLootOperation):
    FACTORY_TUNABLES = {'broadcaster_request': BroadcasterRequest.TunableFactory(description='\n            The broadcaster request to run.\n            ',
                              verify_tunable_callback=verify_immediate_broadcaster,
                              locked_args={'offset_time':None, 
                             'participant':ParticipantType.Object})}

    def __init__(self, *args, broadcaster_request=None, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.broadcaster_request = broadcaster_request

    def _apply_to_subject_and_target(self, subject, target, resolver):
        if subject.is_sim:
            if subject.sim_info is subject:
                subject = subject.get_sim_instance()
                if subject is None:
                    logger.error('Requested broadcaster for uninstanced Sim')
                    return
        sim_timeline = services.time_service().sim_timeline
        sim_timeline.schedule(self.broadcaster_request(subject,
          sequence=(element_utils.sleep_until_next_tick_element(),)))