# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\crafting_component.py
# Compiled at: 2020-05-28 02:35:44
# Size of source mod 2**32: 36307 bytes
import operator, random
from protocolbuffers import SimObjectAttributes_pb2 as protocols, UI_pb2 as ui_protocols
from crafting.crafting_process import CraftingProcess, logger
from crafting.crafting_tunable import CraftingTuning
from event_testing import test_events
from notebook.notebook_entry import SubEntryData
from objects.components import Component, componentmethod, types, componentmethod_with_fallback
from objects.game_object_properties import GameObjectProperty
from objects.hovertip import TooltipFieldsComplete
from retail.retail_component import RetailComponent
from sims4.callback_utils import CallableList
from sims4.localization import LocalizationHelperTuning
from singletons import DEFAULT
import services, sims4.math, zone_types

class CraftingComponent(Component, component_name=types.CRAFTING_COMPONENT, persistence_key=protocols.PersistenceMaster.PersistableData.CraftingComponent, allow_dynamic=True):

    def __init__(self, owner):
        super().__init__(owner)
        self._crafting_process = None
        self._use_base_recipe = False
        self.object_mutated_listeners = CallableList()
        self._servings_statistic_tracker_handle = None
        self._quality_change_callback_added = False
        self._spoil_listener_handle = None
        self._is_final_product = False
        self._last_spoiled_time = None
        self._spoil_timer_state_value = CraftingTuning.SPOILED_STATE_VALUE

    @property
    def is_final_product(self):
        return self._is_final_product

    def set_final_product(self, is_final_product):
        self._is_final_product = is_final_product

    @componentmethod_with_fallback(lambda : (DEFAULT, DEFAULT))
    def get_template_content_overrides(self):
        is_final_product = self._crafting_process.phase is None or self._crafting_process.phase.object_info_is_final_product
        if is_final_product or self.owner.name_component is None:
            return (
             DEFAULT, DEFAULT)
        name_component = self._crafting_process.recipe.final_product_definition.cls.tuned_components.name
        if name_component is not None:
            if name_component.templates:
                selected_template = random.choice(name_component.templates)
                return (selected_template.template_name, selected_template.template_description)
        return (
         DEFAULT, DEFAULT)

    def on_add(self, *_, **__):
        tracker = self.owner.get_tracker(CraftingTuning.SERVINGS_STATISTIC)
        self._servings_statistic_tracker_handle = tracker.add_watcher(self._on_servings_change)
        if tracker.has_statistic(CraftingTuning.SERVINGS_STATISTIC):
            current_value = tracker.get_value(CraftingTuning.SERVINGS_STATISTIC)
            if current_value is not None:
                self.owner.update_tooltip_field((TooltipFieldsComplete.servings), (max(int(current_value), 0)), should_update=True)
        if self.owner.state_component is not None:
            self.owner.add_state_changed_callback(self._on_object_state_change)
            self._quality_change_callback_added = True
            consumable_state_value = self.owner.get_state_value_from_stat_type(CraftingTuning.CONSUME_STATISTIC)
            if consumable_state_value is not None:
                self._on_object_state_change(self.owner, consumable_state_value.state, consumable_state_value, consumable_state_value)
            quality_state_value = self.owner.get_state_value_from_stat_type(CraftingTuning.QUALITY_STATISTIC)
            if quality_state_value is not None:
                self._on_object_state_change(self.owner, quality_state_value.state, quality_state_value, quality_state_value)
            freshness_state = CraftingTuning.LOCK_FRESHNESS_STATE_VALUE.state
            if self.owner.has_state(freshness_state):
                freshness_locked_state_value = self.owner.get_state(freshness_state)
                if freshness_locked_state_value is CraftingTuning.LOCK_FRESHNESS_STATE_VALUE:
                    self._on_object_state_change(self.owner, freshness_locked_state_value.state, freshness_locked_state_value, freshness_locked_state_value)

    def on_remove(self, *_, **__):
        if self._servings_statistic_tracker_handle is not None:
            tracker = self.owner.get_tracker(CraftingTuning.SERVINGS_STATISTIC)
            if tracker.has_watcher(self._servings_statistic_tracker_handle):
                tracker.remove_watcher(self._servings_statistic_tracker_handle)
            self._servings_statistic_tracker_handle = None
        if self._quality_change_callback_added:
            self.owner.remove_state_changed_callback(self._on_object_state_change)
            self._quality_change_callback_added = False
        if self._spoil_listener_handle is not None:
            spoil_tracker = self.owner.get_tracker(self._spoil_timer_state_value.state.linked_stat)
            spoil_tracker.remove_listener(self._spoil_listener_handle)
        self._remove_hovertip()

    def on_mutated(self):
        self.object_mutated_listeners()
        self.object_mutated_listeners.clear()
        self.owner.remove_component(types.CRAFTING_COMPONENT)
        self.on_remove()

    @property
    def crafter_sim_id(self):
        if self._crafting_process.crafter_sim_id:
            return self._crafting_process.crafter_sim_id
        return 0

    def _on_servings_change(self, stat_type, old_value, new_value):
        if stat_type is CraftingTuning.SERVINGS_STATISTIC:
            owner = self.owner
            self.owner.update_tooltip_field((TooltipFieldsComplete.servings), (max(int(new_value), 0)), should_update=True)
            current_inventory = owner.get_inventory()
            if current_inventory is not None:
                current_inventory.push_inventory_item_update_msg(owner)
            if new_value <= 0:
                if old_value != new_value:
                    self.on_mutated()

    def _on_object_state_change(self, owner, state, old_value, new_value):
        state_value = None
        if state is CraftingTuning.QUALITY_STATE:
            state_value = new_value
        else:
            if state is CraftingTuning.FRESHNESS_STATE:
                if new_value in CraftingTuning.QUALITY_STATE_VALUE_MAP:
                    state_value = new_value
                else:
                    self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, None)
                    if self.owner.has_state(CraftingTuning.QUALITY_STATE):
                        state_value = self.owner.get_state(CraftingTuning.QUALITY_STATE)
                    elif state_value is not None:
                        value_quality = CraftingTuning.QUALITY_STATE_VALUE_MAP.get(state_value)
                        if value_quality is not None:
                            self.owner.update_tooltip_field(TooltipFieldsComplete.quality, value_quality.state_star_number)
                            self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, None)
                    if owner.has_state(CraftingTuning.SPOILED_STATE_VALUE.state) and owner.get_state(CraftingTuning.SPOILED_STATE_VALUE.state) is CraftingTuning.SPOILED_STATE_VALUE:
                        if self._crafting_process is not None:
                            recipe = self._get_recipe()
                            if recipe.show_spoiled_quality_description:
                                self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, CraftingTuning.SPOILED_STRING)
                    else:
                        self.owner.update_tooltip_field(TooltipFieldsComplete.spoiled_time, 0)
            else:
                if owner.has_state(CraftingTuning.MASTERWORK_STATE) and owner.get_state(CraftingTuning.MASTERWORK_STATE) is CraftingTuning.MASTERWORK_STATE_VALUE and self._crafting_process is not None:
                    recipe = self._get_recipe()
                    if recipe is not None:
                        if recipe.masterwork_name is not None:
                            self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, recipe.masterwork_name)
                    if state is CraftingTuning.CONSUMABLE_STATE:
                        value_consumable = CraftingTuning.CONSUMABLE_STATE_VALUE_MAP.get(new_value)
                        if value_consumable is not None:
                            self.owner.update_tooltip_field(TooltipFieldsComplete.percentage_left, value_consumable)
                else:
                    if new_value is CraftingTuning.CONSUMABLE_EMPTY_STATE_VALUE:
                        if old_value is not CraftingTuning.CONSUMABLE_EMPTY_STATE_VALUE:
                            self._remove_hovertip()
                    if new_value is CraftingTuning.LOCK_FRESHNESS_STATE_VALUE:
                        self.owner.update_tooltip_field(TooltipFieldsComplete.spoiled_time, 0)
                        if self._spoil_listener_handle is not None:
                            spoil_tracker = self.owner.get_tracker(self._spoil_timer_state_value.state.linked_stat)
                            spoil_tracker.remove_listener(self._spoil_listener_handle)
                            self._spoil_listener_handle = None
                self.owner.update_object_tooltip()

    def _add_hovertip(self):
        if self._is_final_product:
            if self._is_finished():
                self._add_consumable_hovertip()

    def _is_finished(self):
        crafting_process = self._crafting_process
        tracker = None
        stat = CraftingTuning.PROGRESS_STATISTIC
        if crafting_process.current_ico is not None:
            tracker = crafting_process.current_ico.get_tracker(stat)
        if tracker is None:
            tracker = self.owner.get_tracker(stat)
        if not (tracker is None or tracker.has_statistic(stat)):
            tracker = crafting_process.get_tracker(stat)
        if tracker.has_statistic(stat):
            if tracker.get_value(stat) != stat.max_value:
                return crafting_process.is_complete
        return True

    def _get_recipe(self):
        recipe = self._crafting_process.recipe
        if self._use_base_recipe:
            recipe = recipe.get_base_recipe()
        return recipe

    def _add_consumable_hovertip(self):
        owner = self.owner
        owner.hover_tip = ui_protocols.UiObjectMetadata.HOVER_TIP_CONSUMABLE_CRAFTABLE
        crafting_process = self._crafting_process
        recipe = self._get_recipe()
        if recipe is None:
            return
            self.owner.update_tooltip_field(TooltipFieldsComplete.recipe_name, recipe.get_recipe_name(crafting_process.crafter))
            crafted_by_text = crafting_process.get_crafted_by_text(is_from_gallery=(self.owner.is_from_gallery))
            crafted_with_text = crafting_process.get_crafted_with_text()
            if crafted_by_text is not None:
                if crafted_with_text is not None:
                    crafted_by_text = LocalizationHelperTuning.NEW_LINE_LIST_STRUCTURE(crafted_by_text, crafted_with_text)
                crafter_sim_id = crafting_process.crafter_sim_id
                if crafter_sim_id is not None:
                    self.owner.update_tooltip_field(TooltipFieldsComplete.crafter_sim_id, crafter_sim_id)
        elif crafted_with_text is not None:
            crafted_by_text = crafted_with_text
        self.owner.update_tooltip_field(TooltipFieldsComplete.crafted_by_text, crafted_by_text)
        if owner.has_state(CraftingTuning.QUALITY_STATE):
            value_quality = CraftingTuning.QUALITY_STATE_VALUE_MAP.get(owner.get_state(CraftingTuning.QUALITY_STATE))
            if value_quality is not None:
                self.owner.update_tooltip_field(TooltipFieldsComplete.quality, value_quality.state_star_number)
        if owner.has_state(CraftingTuning.MASTERWORK_STATE):
            if owner.get_state(CraftingTuning.MASTERWORK_STATE) is CraftingTuning.MASTERWORK_STATE_VALUE:
                if recipe.masterwork_name is not None:
                    self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, recipe.masterwork_name)
        inscription = crafting_process.inscription
        if inscription is not None:
            self.owner.update_tooltip_field(TooltipFieldsComplete.inscription, inscription)
        self._add_spoil_listener(state_override=(recipe.spoil_time_commodity_override))
        if recipe.time_until_spoiled_string_override is not None:
            self.owner.update_tooltip_field(TooltipFieldsComplete.spoiled_time_text, recipe.time_until_spoiled_string_override)
        subtext = self.owner.get_state_strings()
        if subtext is not None:
            self.owner.update_tooltip_field(TooltipFieldsComplete.subtext, subtext)
        recipe.update_hovertip((self.owner), crafter=(crafting_process.crafter))
        current_inventory = owner.get_inventory()
        if current_inventory is not None:
            current_inventory.push_inventory_item_update_msg(owner)
        self.owner.update_object_tooltip()

    def update_simoleon_tooltip(self):
        self._crafting_process.apply_simoleon_value(self.owner)
        recipe = self._get_recipe()
        recipe.update_hovertip((self.owner), crafter=(self._crafting_process.crafter))
        self.owner.update_object_tooltip()

    def update_quality_tooltip(self):
        owner = self.owner
        recipe = self._get_recipe()
        if owner.has_state(CraftingTuning.QUALITY_STATE):
            value_quality = CraftingTuning.QUALITY_STATE_VALUE_MAP.get(owner.get_state(CraftingTuning.QUALITY_STATE))
            if value_quality is not None:
                self.owner.update_tooltip_field(TooltipFieldsComplete.quality, value_quality.state_star_number)
        if owner.has_state(CraftingTuning.MASTERWORK_STATE):
            quality_description = recipe.masterwork_name if owner.get_state(CraftingTuning.MASTERWORK_STATE) is CraftingTuning.MASTERWORK_STATE_VALUE else None
            if quality_description is not None:
                self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, quality_description)

    def _remove_hovertip(self):
        owner = self.owner
        owner.hover_tip = ui_protocols.UiObjectMetadata.HOVER_TIP_DISABLED
        self.owner.update_tooltip_field(TooltipFieldsComplete.recipe_name, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.recipe_description, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.crafter_sim_id, 0)
        self.owner.update_tooltip_field(TooltipFieldsComplete.crafted_by_text, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.quality, 0)
        self.owner.update_tooltip_field(TooltipFieldsComplete.servings, 0)
        self.owner.update_tooltip_field(TooltipFieldsComplete.spoiled_time, 0)
        self.owner.update_tooltip_field(TooltipFieldsComplete.percentage_left, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.style_name, None)
        if self.owner.get_tooltip_field(TooltipFieldsComplete.simoleon_value) is not None:
            self.owner.update_tooltip_field(TooltipFieldsComplete.simoleon_value, owner.current_value)
        self.owner.update_tooltip_field(TooltipFieldsComplete.main_icon, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.sub_icons, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.quality_description, None)
        self.owner.update_tooltip_field(TooltipFieldsComplete.subtext, None)
        self.owner.update_object_tooltip()

    def _on_spoil_time_changed(self, _, spoiled_time):
        if self._last_spoiled_time is None or self._last_spoiled_time != spoiled_time:
            self._last_spoiled_time = spoiled_time
        else:
            if RetailComponent.SOLD_STATE is not None:
                if self.owner.has_state(RetailComponent.SOLD_STATE.state):
                    if self.owner.get_state(RetailComponent.SOLD_STATE.state) is RetailComponent.SOLD_STATE:
                        self.owner.update_tooltip_field((TooltipFieldsComplete.spoiled_time), 0, should_update=True)
                        return
            if spoiled_time is not None:
                time_in_ticks = spoiled_time.absolute_ticks()
                self.owner.update_tooltip_field((TooltipFieldsComplete.spoiled_time), time_in_ticks, should_update=True)
                logger.debug('{} will get spoiled at {}', self.owner, spoiled_time)
            else:
                self.owner.update_tooltip_field((TooltipFieldsComplete.spoiled_time), 0, should_update=True)

    def _on_spoiled(self, _):
        self._last_spoiled_time = None

    def _add_spoil_listener(self, state_override=None):
        check_operator = operator.lt
        if state_override is not None:
            self._spoil_timer_state_value = state_override.state_to_track
            check_operator = state_override.commodity_check_operator
        elif self._spoil_listener_handle is None and self.owner.has_state(self._spoil_timer_state_value.state):
            linked_stat = self._spoil_timer_state_value.state.linked_stat
            tracker = self.owner.get_tracker(linked_stat)
            if tracker is None:
                return
            threshold = sims4.math.Threshold()
            threshold.value = self._spoil_timer_state_value.range.upper_bound
            threshold.comparison = check_operator
            self._spoil_listener_handle = tracker.create_and_add_listener(linked_stat, threshold, (self._on_spoiled), on_callback_alarm_reset=(self._on_spoil_time_changed))

    def _on_crafting_process_updated(self):
        if self._crafting_process.recipe is not None:
            self._add_hovertip()
            self.owner.update_component_commodity_flags()

    @componentmethod
    def set_crafting_process(self, crafting_process, use_base_recipe=False, is_final_product=False, from_load=False):
        if is_final_product and (from_load or self._crafting_process) is not None and crafting_process.multiple_order_process:
            new_process = crafting_process.copy_for_serve_interaction(crafting_process.get_order_or_recipe())
            self._crafting_process.linked_process = new_process
            self._crafting_process = new_process
        else:
            self._crafting_process = crafting_process
        self._use_base_recipe = use_base_recipe
        self._is_final_product = is_final_product
        self._on_crafting_process_updated()

    @componentmethod
    def get_crafting_process(self):
        return self._crafting_process

    @componentmethod
    def on_crafting_process_finished(self):
        self._add_hovertip()
        self.owner.update_component_commodity_flags()
        crafting_process = self._crafting_process
        if crafting_process is None:
            return
        crafting_process.clear_refundables()
        if crafting_process.current_ico is None:
            crafting_process.current_ico = self.owner
        recipe = crafting_process.recipe
        if self._use_base_recipe:
            recipe = recipe.get_base_recipe()
        skill_test = recipe.skill_test
        if crafting_process.crafter_sim_id is None:
            return
        sim_info = services.sim_info_manager().get(crafting_process.crafter_sim_id)
        if sim_info is not None:
            created_object_quality = self.owner.get_state(CraftingTuning.QUALITY_STATE) if self.owner.has_state(CraftingTuning.QUALITY_STATE) else None
            created_object_masterwork = self.owner.get_state(CraftingTuning.MASTERWORK_STATE) if self.owner.has_state(CraftingTuning.MASTERWORK_STATE) else None
            services.get_event_manager().process_event((test_events.TestEvent.ItemCrafted), sim_info=sim_info,
              crafted_object=(self.owner),
              skill=(skill_test.skill if skill_test is not None else None),
              quality=created_object_quality,
              masterwork=created_object_masterwork)

    @componentmethod
    def get_recipe(self):
        if self._crafting_process.recipe is None:
            return
        if self.owner.definition is not self._crafting_process.recipe.final_product.definition:
            for linked_recipe in self._crafting_process.recipe.linked_recipes_map.values():
                if self.owner.definition is linked_recipe.final_product.definition:
                    return linked_recipe

        return self._crafting_process.recipe

    @componentmethod
    def get_photo_definition(self):
        recipe = self.get_recipe()
        if recipe is None:
            return
        return recipe.photo_definition

    @componentmethod_with_fallback(lambda *_, **__: None)
    def get_craftable_property(self, property_type):
        recipe = self._get_recipe()
        crafting_process = self._crafting_process
        if crafting_process is None:
            return
        if property_type == GameObjectProperty.RECIPE_NAME:
            return recipe.get_recipe_name(crafting_process.crafter)
        if property_type == GameObjectProperty.RECIPE_DESCRIPTION:
            return recipe.recipe_description(crafting_process.crafter)
        logger.error(('Requested crafting property_type {} not found on game_object'.format(property_type)), owner='camilogarcia')

    @componentmethod
    def get_consume_affordance--- This code section failed: ---

 L. 516         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _is_final_product
                4  POP_JUMP_IF_TRUE     20  'to 20'

 L. 517         6  LOAD_GLOBAL              logger
                8  LOAD_METHOD              warn
               10  LOAD_STR                 "Attempting to get consume affordances for something that isn't final product."
               12  CALL_METHOD_1         1  '1 positional argument'
               14  POP_TOP          

 L. 518        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM             4  '4'

 L. 520        20  BUILD_MAP_0           0 
               22  STORE_FAST               'error_dict'

 L. 522        24  LOAD_FAST                'self'
               26  LOAD_ATTR                owner
               28  LOAD_ATTR                consumable_component
               30  STORE_FAST               'consumable_component'

 L. 523        32  LOAD_FAST                'consumable_component'
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE   126  'to 126'

 L. 526        40  LOAD_FAST                'context'
               42  LOAD_CONST               None
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE    98  'to 98'

 L. 527        48  SETUP_LOOP          126  'to 126'
               50  LOAD_FAST                'consumable_component'
               52  LOAD_ATTR                consume_affordances
               54  GET_ITER         
               56  FOR_ITER             94  'to 94'
               58  STORE_FAST               'consume_affordance'

 L. 528        60  LOAD_FAST                'consume_affordance'
               62  LOAD_ATTR                test
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                owner
               68  LOAD_FAST                'context'
               70  LOAD_CONST               ('target', 'context')
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  STORE_FAST               'result'

 L. 529        76  LOAD_FAST                'result'
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 530        80  LOAD_FAST                'consume_affordance'
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'

 L. 531        84  LOAD_FAST                'result'
               86  LOAD_FAST                'error_dict'
               88  LOAD_FAST                'consume_affordance'
               90  STORE_SUBSCR     
               92  JUMP_BACK            56  'to 56'
               94  POP_BLOCK        
               96  JUMP_FORWARD        126  'to 126'
             98_0  COME_FROM            46  '46'

 L. 534        98  LOAD_GLOBAL              next
              100  LOAD_GLOBAL              iter
              102  LOAD_FAST                'consumable_component'
              104  LOAD_ATTR                consume_affordances
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  LOAD_CONST               None
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  STORE_FAST               'consume_affordance'

 L. 535       114  LOAD_FAST                'consume_affordance'
              116  LOAD_CONST               None
              118  COMPARE_OP               is-not
              120  POP_JUMP_IF_FALSE   126  'to 126'

 L. 536       122  LOAD_FAST                'consume_affordance'
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'
            126_1  COME_FROM            96  '96'
            126_2  COME_FROM_LOOP       48  '48'
            126_3  COME_FROM            38  '38'

 L. 542       126  SETUP_LOOP          178  'to 178'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                owner
              132  LOAD_METHOD              super_affordances
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  GET_ITER         
            138_0  COME_FROM           168  '168'
            138_1  COME_FROM           162  '162'
              138  FOR_ITER            176  'to 176'
              140  STORE_FAST               'affordance'

 L. 543       142  LOAD_CONST               0
              144  LOAD_CONST               ('GrabServingSuperInteraction',)
              146  IMPORT_NAME_ATTR         crafting.crafting_interactions
              148  IMPORT_FROM              GrabServingSuperInteraction
              150  STORE_FAST               'GrabServingSuperInteraction'
              152  POP_TOP          

 L. 544       154  LOAD_GLOBAL              issubclass
              156  LOAD_FAST                'affordance'
              158  LOAD_FAST                'GrabServingSuperInteraction'
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  POP_JUMP_IF_FALSE   138  'to 138'

 L. 545       164  LOAD_FAST                'affordance'
              166  LOAD_ATTR                consume_affordances_override
              168  POP_JUMP_IF_TRUE    138  'to 138'

 L. 546       170  LOAD_FAST                'affordance'
              172  RETURN_VALUE     
              174  JUMP_BACK           138  'to 138'
              176  POP_BLOCK        
            178_0  COME_FROM_LOOP      126  '126'

 L. 547       178  LOAD_FAST                'error_dict'
              180  POP_JUMP_IF_FALSE   194  'to 194'

 L. 548       182  LOAD_GLOBAL              logger
              184  LOAD_METHOD              error
              186  LOAD_STR                 'Failed to find valid consume affordance. Consumable component affordances tested as follows:\n\n{}'
              188  LOAD_FAST                'error_dict'
              190  CALL_METHOD_2         2  '2 positional arguments'
              192  POP_TOP          
            194_0  COME_FROM           180  '180'

Parse error at or near `COME_FROM_LOOP' instruction at offset 126_2

    @componentmethod_with_fallback(lambda : None)
    def get_notebook_information(self, notebook_entry, notebook_sub_entries):
        recipe = self.get_recipe()
        if not recipe.use_ingredients:
            return
        sub_entries = (
         SubEntryData(recipe.guid64, False),)
        return (notebook_entry(None, sub_entries=sub_entries),)

    def _icon_override_gen(self):
        recipe = self.get_recipe()
        if recipe.icon_override is not None:
            yield recipe.icon_override

    @componentmethod
    def set_ready_to_serve(self):
        self._crafting_process.ready_to_serve = True

    def component_super_affordances_gen(self, **kwargs):
        recipe = self.get_recipe()
        if self._use_base_recipe:
            recipe = recipe.get_base_recipe()
        elif recipe is None:
            return
            if self._crafting_process.is_complete or self._crafting_process.ready_to_serve:
                for sa in recipe.final_product.super_affordances:
                    yield sa

                for linked_recipe in recipe.linked_recipes_map.values():
                    for sa in linked_recipe.final_product.super_affordances:
                        yield sa

            if recipe.resume_affordance:
                yield recipe.resume_affordance
        else:
            yield CraftingTuning.DEFAULT_RESUME_AFFORDANCE

    def component_interactable_gen(self):
        yield self

    def on_client_connect(self, client):
        if self._crafting_process.recipe is not None:
            self._add_hovertip()

    @componentmethod_with_fallback(lambda : False)
    def has_servings_statistic(self):
        tracker = self.owner.get_tracker(CraftingTuning.SERVINGS_STATISTIC)
        return tracker is None or tracker.has_statistic(CraftingTuning.SERVINGS_STATISTIC) or False
        return True

    def _on_households_loaded_update(self):
        self._add_hovertip()

    @componentmethod_with_fallback(lambda : None)
    def post_tooltip_save_data_stored(self):
        if self._last_spoiled_time is not None:
            self._on_spoil_time_changed(None, self._last_spoiled_time)

    def get_recipe_effect_overrides(self, effect_name):
        if self._crafting_process.recipe is not None:
            if self._crafting_process.recipe:
                effect_override = self._crafting_process.recipe.vfx_overrides.get(effect_name)
                if effect_override is not None:
                    return effect_override
        return effect_name

    def component_anim_overrides_gen(self):
        if self._crafting_process.recipe is not None:
            if self._crafting_process.recipe.anim_overrides is not None:
                yield self._crafting_process.recipe.anim_overrides

    def save(self, persistence_master_message):
        logger.info('[PERSISTENCE]: ----Start saving crafting component of {0}.', self.owner)
        self.owner.update_tooltip_field((TooltipFieldsComplete.spoiled_time), 0, should_update=True)
        persistable_data = protocols.PersistenceMaster.PersistableData()
        persistable_data.type = protocols.PersistenceMaster.PersistableData.CraftingComponent
        crafting_save = persistable_data.Extensions[protocols.PersistableCraftingComponent.persistable_data]
        self._crafting_process.save(crafting_save.process)
        crafting_save.use_base_recipe = self._use_base_recipe
        crafting_save.is_final_product = self._is_final_product
        persistence_master_message.data.extend([persistable_data])

    def load(self, crafting_save_message):
        logger.info('[PERSISTENCE]: ----Start loading crafting component of {0}.', self.owner)
        crafting_component_data = crafting_save_message.Extensions[protocols.PersistableCraftingComponent.persistable_data]
        crafting_process = CraftingProcess()
        crafting_process.load(crafting_component_data.process)
        self.set_crafting_process(crafting_process, (crafting_component_data.use_base_recipe), (crafting_component_data.is_final_product), from_load=True)
        recipe = self.get_recipe()
        if recipe is not None:
            if crafting_process.crafted_value is not None:
                self.owner.base_value = crafting_process.crafted_value
            services.current_zone().register_callback(zone_types.ZoneState.HOUSEHOLDS_AND_SIM_INFOS_LOADED, self._on_households_loaded_update)
            self.owner.append_tags(recipe.apply_tags)