# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\interactions\picker\picker_pie_menu_interaction.py
# Compiled at: 2020-03-10 19:32:55
# Size of source mod 2**32: 4606 bytes
from event_testing.results import TestResult
from objects.base_interactions import ProxyInteraction
from sims4.utils import flexmethod, classproperty
from singletons import DEFAULT

class _PickerPieMenuProxyInteraction(ProxyInteraction):
    INSTANCE_SUBCLASSES_ONLY = True

    @classproperty
    def proxy_name(cls):
        return '[PickerRow]'

    @classmethod
    def generate(cls, proxied_affordance, picker_row_data):
        result = super().generate(proxied_affordance)
        result.picker_row_data = picker_row_data
        if hasattr(proxied_affordance, 'funds_source'):
            result.register_cost_gain_strings_callbacks(proxied_affordance.funds_source.get_cost_string, proxied_affordance.funds_source.get_gain_string)
        return result

    @classmethod
    def potential_interactions(cls, target, context, **kwargs):
        yield (cls.generate_aop)(target, context, **kwargs)

    @classmethod
    def _test(cls, target, context, **kwargs):
        result = (super()._test)(target, context, **kwargs)
        if not result:
            return result
        elif cls.picker_row_data.is_enable:
            tooltip = None
        else:
            tooltip = cls.picker_row_data.row_tooltip if cls.pie_menu_option.show_disabled_item else None
        return TestResult((cls.picker_row_data.is_enable), influence_by_active_mood=(cls.picker_row_data.pie_menu_influence_by_active_mood),
          tooltip=tooltip)

    @flexmethod
    def get_display_tooltip(cls, inst, override=None, context=DEFAULT, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        context = inst.context if context is DEFAULT else context
        tooltip = inst_or_cls.display_tooltip
        if override is not None:
            if override.new_display_tooltip is not None:
                tooltip = override.new_display_tooltip
        if tooltip is None:
            tooltip = inst_or_cls.picker_row_data.row_tooltip
        if tooltip is not None:
            tooltip = (inst_or_cls.create_localized_string)(tooltip, context=context, **kwargs)
        return tooltip

    @flexmethod
    def get_pie_menu_category(cls, inst, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        if inst_or_cls.pie_menu_option.force_pie_menu_category:
            return inst_or_cls.pie_menu_option.pie_menu_category
        return inst_or_cls.picker_row_data.pie_menu_category or inst_or_cls.pie_menu_option.pie_menu_category

    @flexmethod
    def _get_name(cls, inst, target=DEFAULT, context=DEFAULT, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        display_name = inst_or_cls.pie_menu_option.pie_menu_name
        override_tunable, _ = inst_or_cls.get_name_override_and_test_result(target=target, context=context)
        if override_tunable is not None:
            if override_tunable.new_display_name is not None:
                display_name = override_tunable.new_display_name
        display_name = (inst_or_cls.create_localized_string)(display_name, inst_or_cls.picker_row_data.name, target=target, 
         context=context, **kwargs)
        price = getattr(inst_or_cls.picker_row_data, 'price', 0)
        if price > 0:
            if inst_or_cls.picker_row_data.is_discounted:
                price = inst_or_cls.picker_row_data.discounted_price
            cost_name_factory = inst_or_cls.get_cost_name_factory()
            display_name = cost_name_factory(display_name, price)
        return display_name

    def _run_interaction_gen(self, timeline):
        yield from super()._run_interaction_gen(timeline)
        ingredient_data = self._kwargs.get('recipe_ingredients_map')
        self.on_choice_selected((self.picker_row_data.tag), ingredient_data=ingredient_data, ingredient_check=(ingredient_data is not None))
        return True
        if False:
            yield None