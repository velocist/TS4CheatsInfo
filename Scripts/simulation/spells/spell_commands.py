# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\spells\spell_commands.py
# Compiled at: 2019-06-17 22:19:03
# Size of source mod 2**32: 3251 bytes
import services, sims4.resources
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target, TunableInstanceParam
from sims4.resources import Types
from spells.spellbook import SpellbookHelper

@sims4.commands.Command('spells.generate_spell_book', command_type=(sims4.commands.CommandType.Live))
def generate_spell_book(opt_target: OptionalSimInfoParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)
    if target is None:
        return False
    SpellbookHelper(target).view_spellbook()


@sims4.commands.Command('spells.generate_spell_book.ui', command_type=(sims4.commands.CommandType.Live))
def generate_spell_book_ui(opt_target: OptionalSimInfoParam=None, context: str=None, _connection=None):
    target = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)
    if target is None:
        return False
    SpellbookHelper(target).view_spellbook(context=context)


@sims4.commands.Command('spells.mark_spellbook_entry_as_viewed', command_type=(sims4.commands.CommandType.Live))
def mark_as_viewed(tuning_guid: int, opt_target: OptionalSimInfoParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)
    if target is None:
        sims4.commands.output('No Sim with id {}'.format(opt_target), _connection)
        return False
    unlock_tracker = target.unlock_tracker
    if unlock_tracker is None:
        sims4.commands.output('No unlock tracker for {}. Invalid LOD?'.format(target), _connection)
        return False
    spells_manager = services.get_instance_manager(Types.SPELL)
    recipe_manager = services.get_instance_manager(Types.RECIPE)
    unlockable_class = spells_manager.get(tuning_guid) or recipe_manager.get(tuning_guid)
    if unlockable_class is None:
        sims4.commands.output('Invalid guid {}'.format(tuning_guid), _connection)
        return False
    unlock_tracker.unmark_as_new(unlockable_class)


@sims4.commands.Command('spells.unlock_spell', command_type=(sims4.commands.CommandType.DebugOnly))
def unlock_spell(spell_type: TunableInstanceParam(sims4.resources.Types.SPELL), opt_target: OptionalSimInfoParam=None, _connection=None):
    target = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)
    if target is None:
        return False
    unlock_tracker = target.unlock_tracker
    if unlock_tracker is None:
        return False
    unlock_tracker.add_unlock(spell_type, None, mark_as_new=True)