# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\server_commands\zone_commands.py
# Compiled at: 2019-06-26 01:22:28
# Size of source mod 2**32: 2834 bytes
from event_testing.test_events import TestEvent
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target, OptionalSimInfoParam
from sims4.utils import create_csv
import services, sims4.commands

@sims4.commands.Command('zone.current_region')
def current_region(_connection=None):
    current_region = services.current_region()
    sims4.commands.output(f"Current Region: {current_region}", _connection)


@sims4.commands.Command('zone.loading_screen_animation_finished', command_type=(sims4.commands.CommandType.Live))
def loading_screen_animation_finished(_connection=None):
    services.current_zone().on_loading_screen_animation_finished()


@sims4.commands.Command('zone.trigger_test_event', command_type=(sims4.commands.CommandType.Live))
def trigger_test_event(event: int=0, opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    services.get_event_manager().process_event((TestEvent(event)), sim_info=sim_info)


@sims4.commands.Command('zone.gather_tick_metrics.start', command_type=(sims4.commands.CommandType.Automation))
def gather_tick_metrics_start(_connection=None):
    services.current_zone().start_gathering_tick_metrics()


@sims4.commands.Command('zone.gather_tick_metrics.stop', command_type=(sims4.commands.CommandType.Automation))
def gather_tick_metrics_stop(_connection=None):

    def callback(file):
        zone = services.current_zone()
        tick_data = zone.tick_data
        zone.stop_gathering_tick_metrics()
        file.write('ABSOLUTE TICKS,SIM NOW READABLE, SIM NOW TICKS,CLOCK SPEED ENUM,CLOCK SPEED MULTIPLIER,GAME TIME READABLE,GAME TIME TICKS,MULTIPLIER TYPE\n')
        for data in tick_data:
            file.write('{},{},{},{},{},{},{},{}\n'.format(data.absolute_ticks, data.sim_now, data.sim_now.absolute_ticks(), data.clock_speed, data.clock_speed_multiplier, data.game_time, data.game_time.absolute_ticks(), data.multiplier_type))

    create_csv('tick_metrics', callback=callback, connection=_connection)