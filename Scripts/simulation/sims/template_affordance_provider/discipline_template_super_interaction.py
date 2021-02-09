# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\template_affordance_provider\discipline_template_super_interaction.py
# Compiled at: 2017-04-28 02:19:26
# Size of source mod 2**32: 2077 bytes
from interactions.base.super_interaction import SuperInteraction
from interactions.social.social_super_interaction import SocialSuperInteraction
from sims4.utils import flexmethod
from singletons import DEFAULT

class DisciplineTemplateMixin:

    def __init__(self, *args, template_display_name=None, template_outcome_basic_extras=None, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._display_name_override = template_display_name
        self._additional_outcome_basic_extra = template_outcome_basic_extras

    def build_basic_extras(self, sequence=()):
        sequence = super().build_basic_extras(sequence=sequence)
        if self._additional_outcome_basic_extra:
            for factory in reversed(self._additional_outcome_basic_extra):
                sequence = factory(self, sequence=sequence)

        return sequence

    @flexmethod
    def _get_name(cls, inst, target=DEFAULT, context=DEFAULT, template_display_name=None, **interaction_parameters):
        if template_display_name is not None:
            inst_or_cls = inst if inst is not None else cls
            target = inst.target if inst is not None else target
            return (super(SuperInteraction, inst_or_cls).create_localized_string)(template_display_name, target=target, context=context, **interaction_parameters)
        return (super(SuperInteraction, inst if inst is not None else cls)._get_name)(target=target, context=context, **interaction_parameters)


class DisciplineTemplateSuperInteraction(DisciplineTemplateMixin, SuperInteraction):
    pass


class DisciplineTemplateSocialSuperInteraction(DisciplineTemplateMixin, SocialSuperInteraction):
    pass