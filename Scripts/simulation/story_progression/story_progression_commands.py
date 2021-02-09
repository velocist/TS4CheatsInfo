# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\story_progression\story_progression_commands.py
# Compiled at: 2017-09-12 23:12:38
# Size of source mod 2**32: 3434 bytes
from server_commands.argument_helpers import get_optional_target, OptionalSimInfoParam
from story_progression.story_progression_service import StoryProgressionService
import services, sims4.commands

@sims4.commands.Command('story_progression.find_best_action')
def story_progression_find_best_action(opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        return False
    sim_info.story_progression_tracker.find_best_story_progression_action()
    return True


@sims4.commands.Command('story_progression.set_time_multiplier')
def story_progression_set_time_multiplier(time_multiplier: float=1, _connection=None):
    story_progression_service = services.get_story_progression_service()
    if story_progression_service is None:
        return False
    story_progression_service.set_time_multiplier(time_multiplier)
    return True


@sims4.commands.Command('story_progression.process_index', command_type=(sims4.commands.CommandType.Cheat))
def process_index(index: int=0, _connection=None):
    current_zone = services.current_zone()
    if current_zone is None:
        return False
    story_progression_service = current_zone.story_progression_service
    if story_progression_service is None:
        return False
    story_progression_service.process_action_index(index)


@sims4.commands.Command('story_progression.list_action_indexes')
def list_action_indexes(_connection=None):
    sims4.commands.output('Index: Action Type', _connection)
    for index, action in enumerate(StoryProgressionService.ACTIONS):
        sims4.commands.output('{}: {}'.format(index, action), _connection)


@sims4.commands.Command('story_progression.process_all')
def process_all_story_progression(times_to_process: int=1, _connection=None):
    current_zone = services.current_zone()
    if current_zone is None:
        return False
    story_progression_service = current_zone.story_progression_service
    if story_progression_service is None:
        return False
    while times_to_process > 0:
        story_progression_service.process_all_actions()
        times_to_process -= 1

    sims4.commands.output('All story progression processed.', _connection)