# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\notebook\notebook_commands.py
# Compiled at: 2019-06-14 18:46:43
# Size of source mod 2**32: 1923 bytes
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target, RequiredTargetParam
from sims4.commands import CommandType
from ui.notebook_tuning import NotebookCategories
import services, sims4

@sims4.commands.Command('notebook.generate_notebook', command_type=(CommandType.Live))
def generate_notebook(opt_sim: OptionalSimInfoParam=None, initial_category: int=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is not None:
        if sim_info.notebook_tracker is not None:
            initial_selected_category = None if initial_category is None else NotebookCategories(initial_category)
            sim_info.notebook_tracker.generate_notebook_information(initial_selected_category=initial_selected_category)
    return True


@sims4.commands.Command('notebook.mark_entry_as_seen', command_type=(CommandType.Live))
def mark_entry_as_seen(sim: RequiredTargetParam, subcategory_id: int, entry_id: int, _connection=None):
    sim_info = sim.get_target(manager=(services.sim_info_manager()))
    if sim_info is None:
        sims4.commands.output('Sim with id {} is not found to mark notebook entry as seen.'.format(sim.target_id), _connection)
        return False
    if sim_info.notebook_tracker is None:
        sims4.commands.output('Notebook tracker is not found on Sim {} to mark notebook entry as seen'.format(sim_info), _connection)
        return False
    sim_info.notebook_tracker.mark_entry_as_seen(subcategory_id, entry_id)
    return True