# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\careers\detective\detective_commands.py
# Compiled at: 2020-06-12 18:02:18
# Size of source mod 2**32: 3735 bytes
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target
import services, sims4.commands

@sims4.commands.Command('detective.create_new_crime_data', command_type=(sims4.commands.CommandType.Automation))
def create_new_crime_data(opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    career = next(iter(sim_info.career_tracker.careers.values()))
    career.create_new_crime_data()


@sims4.commands.Command('detective.test_criminal_generation')
def test_criminal_generation(opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    career = next(iter(sim_info.career_tracker.careers.values()))
    clue_groups = career.text_clues
    clue_incompatibility = career.clue_incompatibility

    def format_clues(clues):
        return tuple((clue.__name__ for clue in clues))

    def try_generate_criminal(chosen_clues):
        try:
            filter_terms = tuple((clue.filter_term for clue in chosen_clues))
            criminal_filter = career.criminal_filter(filter_terms=filter_terms)
            filter_results = services.sim_filter_service().submit_matching_filter(sim_filter=criminal_filter, requesting_sim_info=sim_info,
              allow_yielding=False,
              gsi_source_fn=(lambda : 'DetectiveCommands: Generate criminal based on {}'.format(str(chosen_clues))))
            if not filter_results:
                sims4.commands.output('Failed to spawn with clues: {}'.format(format_clues(chosen_clues)), _connection)
            else:
                sims4.commands.output('Generated: {}, {}'.format(filter_results[0].sim_info, format_clues(chosen_clues)), _connection)
                for f in filter_results:
                    services.sim_info_manager().remove_permanently(f.sim_info)

        except Exception as e:
            try:
                sims4.commands.output('<exc> Failed to spawn with clues: {}, {}'.format(format_clues(chosen_clues), e), _connection)
            finally:
                e = None
                del e

    def test_build_clues(index, chosen_clues, incompatible_clues):
        if index >= len(clue_groups):
            try_generate_criminal(chosen_clues)
            return
        for clue in clue_groups[index]:
            if clue not in incompatible_clues:
                new_chosen_clues = chosen_clues.copy()
                new_chosen_clues.add(clue)
                new_incompatible_clues = incompatible_clues.copy()
                new_incompatible_clues.update(clue_incompatibility.get(clue, ()))
                test_build_clues(index + 1, new_chosen_clues, new_incompatible_clues)

        test_build_clues(index + 1, chosen_clues.copy(), incompatible_clues.copy())

    test_build_clues(0, set(), set())
    sims4.commands.output('Done', _connection)