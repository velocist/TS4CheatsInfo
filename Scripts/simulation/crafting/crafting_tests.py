# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\crafting\crafting_tests.py
# Compiled at: 2019-05-16 20:23:18
# Size of source mod 2**32: 4267 bytes
import services
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from interactions import ParticipantType, ParticipantTypeObject
from objects.components.types import CRAFTING_COMPONENT
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableVariant, TunableReference, TunableSet, OptionalTunable, TunableEnumEntry
from tag import TunableTag
logger = Logger('Crafting_Tests')

class _TestRecipeByTag(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'required_tag': TunableTag(description='\n            The tag that must exist on the recipe\n            ',
                       filter_prefixes=('Recipe', ))}

    def test_recipe(self, recipe):
        if self.required_tag not in recipe.recipe_tags:
            return TestResult(False, f"{recipe} does not have required tag {self.required_tag}")
        return TestResult.TRUE


class _TestRecipeByDefinition(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'valid_recipes': TunableSet(description='\n            The set of recipes allowed.\n            ',
                        tunable=TunableReference(manager=(services.get_instance_manager(Types.RECIPE)),
                        class_restrictions=('Recipe', )),
                        minlength=1)}

    def test_recipe(self, recipe):
        if recipe not in self.valid_recipes:
            return TestResult(False, f"{recipe} not in valid recipes {self.valid_recipes}")
        return TestResult.TRUE


class CraftingRecipeTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    FACTORY_TUNABLES = {'recipe_test':TunableVariant(description='\n            How to test for the recipe.\n            ',
       by_recipe=_TestRecipeByDefinition.TunableFactory(),
       by_tag=_TestRecipeByTag.TunableFactory(),
       default='by_recipe'), 
     'subject':OptionalTunable(description='\n            Participant to look up the crafting process.  \n            Tuning this is not necessary if this loot is run within a crafting interaction.\n            ',
       tunable=TunableEnumEntry(tunable_type=ParticipantTypeObject,
       default=(ParticipantTypeObject.Object)))}

    def get_expected_args(self):
        if self.subject is None:
            return {'crafting_process': ParticipantType.CraftingProcess}
        return {'subject': self.subject}

    def __call__(self, subject=(), crafting_process=(), **kwargs):
        if self.subject is not None:
            subject = next(iter(subject), None)
            if not subject.has_component(CRAFTING_COMPONENT):
                error = f"{subject} has no crafting component!"
                logger.error(error)
                return TestResult(False, error, tooltip=(self.tooltip))
                crafting_process = subject.get_crafting_process()
            else:
                crafting_process = next(iter(crafting_process), None)
        else:
            if crafting_process is None:
                error = f"Crafting process not found when testing {self}"
                logger.error(error)
                return TestResult(False, error, tooltip=(self.tooltip))
            recipe = crafting_process.get_order_or_recipe()
            if recipe is None:
                return TestResult(False, 'No recipe on crafting process!', tooltip=(self.tooltip))
            recipe_result = self.recipe_test.test_recipe(recipe)
            return recipe_result or TestResult(False, (recipe_result.reason), tooltip=(self.tooltip))
        return TestResult.TRUE