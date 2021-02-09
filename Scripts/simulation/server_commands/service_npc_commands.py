# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\service_npc_commands.py
# Compiled at: 2014-03-27 19:38:10
# Size of source mod 2**32: 3419 bytes
from date_and_time import create_time_span
from sims4.commands import CommandType
import services, sims4.commands

@sims4.commands.Command('service_npc.request_service', command_type=(CommandType.Cheat))
def request_service(service_npc_type: str, household_id=None, _connection=None):
    service_npc_tuning = services.service_npc_manager().get(service_npc_type)
    if service_npc_tuning is not None:
        tgt_client = services.client_manager().get(_connection)
        if tgt_client is None:
            return False
        if household_id is None:
            household = tgt_client.household
        else:
            household_id = int(household_id)
            manager = services.household_manager()
            household = manager.get(household_id)
            if household is None:
                household = tgt_client.household
        services.current_zone().service_npc_service.request_service(household, service_npc_tuning)
        sims4.commands.output('Requesting service {0}'.format(service_npc_type), _connection)
        return True
    return False


@sims4.commands.Command('service_npc.fake_perform_service')
def fake_perform_service(service_npc_type: str, _connection=None):
    service_npc_tuning = services.service_npc_manager().get(service_npc_type)
    if service_npc_tuning is not None:
        tgt_client = services.client_manager().get(_connection)
        if tgt_client is None:
            return False
        household = tgt_client.household
        service_npc_tuning.fake_perform(household)
        return True
    return False


@sims4.commands.Command('service_npc.cancel_service', command_type=(CommandType.Automation))
def cancel_service(service_npc_type: str, max_duration: int=240, _connection=None):
    service_npc_tuning = services.service_npc_manager().get(service_npc_type)
    if service_npc_tuning is not None:
        tgt_client = services.client_manager().get(_connection)
        if tgt_client is None:
            return False
        household = tgt_client.household
        services.current_zone().service_npc_service.cancel_service(household, service_npc_tuning)
        return True
    return False


@sims4.commands.Command('service_npc.toggle_auto_scheduled_services', command_type=(CommandType.Automation))
def toggle_auto_scheduled_services(enable: bool=None, max_duration: int=240, _connection=None):
    service_npc_service = services.current_zone().service_npc_service
    enable_auto_scheduled_services = enable if enable is not None else not service_npc_service._auto_scheduled_services_enabled
    service_npc_service._auto_scheduled_services_enabled = enable_auto_scheduled_services
    return True