# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\sims\outfits\outfit_generator.py
# Compiled at: 2020-09-25 03:06:50
# Size of source mod 2**32: 2633 bytes
import services, sims4
from sims.outfits.outfit_utils import OutfitGeneratorRandomizationMixin
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, TunableSet, TunableEnumWithFilter
from snippets import define_snippet
from tag import Tag
with sims4.reload.protected(globals()):
    outfit_change_log_enabled = False

class OutfitGenerator(OutfitGeneratorRandomizationMixin, HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'tags': TunableSet(description='\n            The set of tags used to generate the outfit. Parts must match the\n            specified tag in order to be valid for the generated outfit.\n            ',
               tunable=TunableEnumWithFilter(tunable_type=Tag,
               filter_prefixes=('Uniform', 'OutfitCategory', 'Style', 'Situation'),
               default=(Tag.INVALID),
               invalid_enums=(
              Tag.INVALID,),
               pack_safe=True))}

    def __call__(self, *args, **kwargs):
        (self._generate_outfit)(args, tag_list=self.tags, **kwargs)

    @staticmethod
    def generate_outfit(outfit_generator, sim_info, outfit_category, **kwargs):
        (outfit_generator.generator)(sim_info, outfit_category, **kwargs)


TunableOutfitGeneratorReference, TunableOutfitGeneratorSnippet = define_snippet('Outfit', OutfitGenerator.TunableFactory())