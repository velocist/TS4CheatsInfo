# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\role_commands.py
# Compiled at: 2013-04-11 03:16:07
# Size of source mod 2**32: 3310 bytes
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
import services, sims4.commands

@sims4.commands.Command('role.add_role')
def add_role(name: str=None, opt_target: OptionalTargetParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection)
    if target is None or name is None:
        return False
    else:
        role_state_type = services.role_state_manager().get(name)
        if role_state_type is None:
            sims4.commands.output('role({0}) is not a valid role'.format(name), _connection)
            return False
            role_state = target.add_role(role_state_type)
            if role_state is not None:
                sims4.commands.output('role({0}) has been added onto sim'.format(name), _connection)
        else:
            sims4.commands.output('role({0}) has FAILED to be added onto sim'.format(name), _connection)


@sims4.commands.Command('role.remove_role')
def remove_role(name: str=None, opt_target: OptionalTargetParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection)
    if target is None or name is None:
        return False
    role_state_type = services.role_state_manager().get(name)
    if role_state_type is None:
        sims4.commands.output('role({0}) is not a valid role'.format(name), _connection)
        return False
    if target.remove_role_of_type(role_state_type):
        sims4.commands.output('role({0}) has been removed'.format(name), _connection)
        return True
    sims4.commands.output('role({0}) was not in sims role list'.format(name), _connection)
    return False


@sims4.commands.Command('role.current_active_roles')
def current_active_role(opt_target: OptionalTargetParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection)
    if target is None:
        return False
    elif target.active_roles():
        sims4.commands.output('Active Roles: {}'.format(target.active_roles()), _connection)
    else:
        sims4.commands.output('Sim has no active role', _connection)


@sims4.commands.Command('qa.role.current_active_role', command_type=(sims4.commands.CommandType.Automation))
def automation_current_active_role(opt_target: OptionalTargetParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection)
    if target is None:
        sims4.commands.automation_output('SimRole; SimId:None', _connection)
        return False
    role = target.active_roles().__class__.__name__ if target.active_roles() is not None else 'None'
    sims4.commands.automation_output('SimRole; SimId:{}, Role:{}'.format(target.id, role), _connection)