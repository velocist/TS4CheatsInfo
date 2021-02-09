# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\routing\route_events\route_event_commands.py
# Compiled at: 2018-03-31 05:28:07
# Size of source mod 2**32: 745 bytes
from sims4.commands import CommandType
import gsi_handlers, sims4.commands

@sims4.commands.Command('route_events.toggle_gsi_update_log', command_type=(CommandType.DebugOnly))
def route_events_toggle_gsi_update_log(_connection=None):
    enabled = not gsi_handlers.route_event_handlers.update_log_enabled
    gsi_handlers.route_event_handlers.update_log_enabled = enabled
    if enabled:
        sims4.commands.output('Route Event Update Log: Enabled', _connection)
    else:
        sims4.commands.output('Route Event Update Log: Disabled', _connection)
    return True