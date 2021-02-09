# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\tutorials\tutorial_tip_commands.py
# Compiled at: 2018-09-05 23:15:44
# Size of source mod 2**32: 1220 bytes
from server_commands.argument_helpers import TunableInstanceParam
import services, sims4

@sims4.commands.Command('tutorial.activate_tutorial_tip', command_type=(sims4.commands.CommandType.Live))
def activate_tutorial_tip(tutorial_tip: TunableInstanceParam(sims4.resources.Types.TUTORIAL_TIP), _connection=None):
    tutorial_tip.activate()
    return True


@sims4.commands.Command('tutorial.deactivate_tutorial_tip', command_type=(sims4.commands.CommandType.Live))
def deactivate_tutorial_tip(tutorial_tip: TunableInstanceParam(sims4.resources.Types.TUTORIAL_TIP), _connection=None):
    tutorial_tip.deactivate()
    return True


@sims4.commands.Command('tutorial.set_tutorial_mode', command_type=(sims4.commands.CommandType.Live))
def set_tutorial_mode(mode: int=0, _connection=None):
    tutorial_service = services.get_tutorial_service()
    if tutorial_service is not None:
        tutorial_service.set_tutorial_mode(mode)
    return True