# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\postures\posture_animation_data.py
# Compiled at: 2020-10-16 01:15:21
# Size of source mod 2**32: 16844 bytes
from animation import get_throwaway_animation_context
from animation.animation_utils import StubActor
from animation.asm import create_asm
from interactions.constraint_variants import TunableConstraintVariant
from interactions.utils.animation_reference import TunableAnimationReference
from sims.occult.occult_enums import OccultType
from sims.sim_info_types import Species
from sims4.tuning.tunable import TunableTuple, TunableResourceKey, Tunable, AutoFactoryInit, HasTunableSingletonFactory, TunableMapping, TunableEnumEntry, TunableFactory, OptionalTunable, TunableList
from sims4.tuning.tunable_base import SourceQueries
import sims4.resources
logger = sims4.log.Logger('Posture Animation Data')

def build_boundary_conditions_for_posture--- This code section failed: ---

 L.  31         0  LOAD_CONST               None
                2  RETURN_VALUE     

 L.  36         4  FOR_ITER            138  'to 138'
                6  STORE_FAST               'actor_param_name_tuning'

 L.  37         8  LOAD_GLOBAL              getattr
               10  LOAD_FAST                'anim_data'
               12  LOAD_FAST                'actor_param_name_tuning'
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  STORE_FAST               'actor_param_name'

 L.  38        18  LOAD_GLOBAL              StubActor
               20  LOAD_CONST               1
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'stub_actor'

 L.  39        26  LOAD_GLOBAL              create_asm
               28  LOAD_FAST                'anim_data'
               30  LOAD_ATTR                _asm_key
               32  LOAD_GLOBAL              get_throwaway_animation_context
               34  CALL_FUNCTION_0       0  '0 positional arguments'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  STORE_FAST               'asm'

 L.  40        40  LOAD_FAST                'asm'
               42  LOAD_METHOD              set_actor
               44  LOAD_FAST                'actor_param_name'
               46  LOAD_FAST                'stub_actor'
               48  CALL_METHOD_2         2  '2 positional arguments'
               50  POP_TOP          

 L.  41        52  LOAD_FAST                'anim_data'
               54  LOAD_ATTR                _target_name
               56  STORE_FAST               'target_name'

 L.  42        58  LOAD_FAST                'target_name'
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE    90  'to 90'

 L.  43        66  LOAD_GLOBAL              StubActor
               68  LOAD_CONST               2
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  STORE_FAST               'posture_target'

 L.  44        74  LOAD_FAST                'asm'
               76  LOAD_METHOD              add_potentially_virtual_actor
               78  LOAD_FAST                'actor_param_name'
               80  LOAD_FAST                'stub_actor'
               82  LOAD_FAST                'target_name'
               84  LOAD_FAST                'posture_target'
               86  CALL_METHOD_4         4  '4 positional arguments'
               88  POP_TOP          
             90_0  COME_FROM            64  '64'

 L.  47        90  LOAD_FAST                'asm'
               92  LOAD_ATTR                get_boundary_conditions_list
               94  LOAD_FAST                'stub_actor'
               96  LOAD_FAST                'anim_data'
               98  LOAD_ATTR                _enter_state_name

 L.  48       100  LOAD_FAST                'posture_type'

 L.  49       102  LOAD_FAST                'target_name'
              104  LOAD_CONST               ('posture', 'base_object_name')
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          

 L.  51       110  LOAD_FAST                'asm'
              112  LOAD_ATTR                get_boundary_conditions_list
              114  LOAD_FAST                'stub_actor'
              116  LOAD_FAST                'anim_data'
              118  LOAD_ATTR                _exit_state_name

 L.  52       120  LOAD_FAST                'anim_data'
              122  LOAD_ATTR                _state_name

 L.  53       124  LOAD_CONST               False

 L.  54       126  LOAD_FAST                'posture_type'

 L.  55       128  LOAD_FAST                'target_name'
              130  LOAD_CONST               ('from_state_name', 'entry', 'posture', 'base_object_name')
              132  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              134  POP_TOP          
              136  JUMP_BACK             4  'to 4'
              138  POP_BLOCK        

Parse error at or near `FOR_ITER' instruction at offset 4


class _TunableAnimationData(TunableTuple):
    ASM_SOURCE = '_asm_key'
    ACTOR_PARAM_NAMES_LOCKED_ARGS = {'actor_param_name_list': ('_actor_param_name', )}

    def __init__(self, *args, locked_args=None, **kwargs):
        locked_args_merged = dict(self.ACTOR_PARAM_NAMES_LOCKED_ARGS)
        if locked_args:
            locked_args_merged.update(locked_args)
        (super.__init__)(args, _asm_key=TunableResourceKey(description='\n                The posture ASM.\n                ',
  default=None,
  resource_types=[
 sims4.resources.Types.STATEMACHINE],
  category='asm',
  pack_safe=True), 
         _actor_param_name=Tunable(description="\n                The name of the actor parameter in this posture's ASM. By\n                default, this is x, and you should probably not change it.\n                ",
  tunable_type=str,
  default='x',
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMActorSim)), 
         _target_name=Tunable(description="\n                The actor name for the target object of this posture. Leave\n                empty for postures with no target. In the case of a posture\n                that targets an object, it should be the name of the object\n                actor in this posture's ASM.\n                ",
  tunable_type=str,
  default=None,
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMActorAll)), 
         _jig_name=Tunable(description='\n                The actor name for the jig created by this posture, if a jig is\n                tuned.\n                ',
  tunable_type=str,
  default=None,
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMActorObject)), 
         _enter_state_name=Tunable(description='\n                The name of the entry state for the posture in the ASM. All\n                postures should have two public states, not including entry\n                and exit. This should be the first of the two states.\n                ',
  tunable_type=str,
  default=None,
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMState)), 
         _exit_state_name=Tunable(description='\n                The name of the exit state in the ASM. By default, this is\n                exit.\n                ',
  tunable_type=str,
  default='exit',
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMState)), 
         _state_name=Tunable(description='\n                The main state name for the looping posture pose in the\n                ASM. All postures should have two public states, not\n                including entry and exit. This should be the second of the\n                two states.\n                ',
  tunable_type=str,
  default=None,
  source_location=(self.ASM_SOURCE),
  source_query=(SourceQueries.ASMState)), 
         _idle_animation=TunableAnimationReference(description='\n                The animation for a Sim to play while in this posture and\n                waiting for interaction behavior to start.\n                ',
  callback=None,
  pack_safe=True), 
         _idle_animation_occult_overrides=TunableMapping(description='\n                A mapping of occult type to idle animation override data.\n                ',
  key_type=TunableEnumEntry(description='\n                    The occult type of the Sim.\n                    ',
  tunable_type=OccultType,
  default=(OccultType.HUMAN)),
  value_type=TunableAnimationReference(description='\n                    Idle animation overrides to use for a Sim based on their \n                    occult type.\n                    ',
  callback=None,
  pack_safe=True)), 
         _set_locomotion_surface=Tunable(description='\n                If checked, then the Sim\'s locomotion surface is set to the\n                target of this posture, if it exists.\n                \n                The locomotion surface affects the sound of the Sim\'s footsteps\n                when locomoting. Generally, this should be unset, since most\n                Sims don\'t route on objects as part of postures. For the cases\n                where they do, however, we need to ensure the sound is properly\n                overridden.\n                \n                e.g. The "Sit" posture for Cats includes sitting on objects.\n                Some of those transitions involve Cats walking across the sofa.\n                We need to ensure that the sound of the footsteps matches the\n                fabric, instead of the floor/ground.\n                ',
  tunable_type=bool,
  default=False), 
         _carry_constraint=OptionalTunable(description='\n                If enabled, Sims in this posture need to be picked up using this\n                specific constraint.\n                ',
  tunable=TunableList(tunable=TunableConstraintVariant(description='\n                        A constraint that must be fulfilled in order to pick up\n                        this Sim.\n                        ')),
  enabled_name='Override',
  disabled_name='From_Carryable_Component'), 
         locked_args=locked_args_merged, **kwargs)


class _AnimationDataBase(HasTunableSingletonFactory, AutoFactoryInit):

    def get_animation_data(self, sim, target):
        raise NotImplementedError

    def get_provided_postures_gen(self):
        raise NotImplementedError

    def get_supported_postures_gen(self):
        raise NotImplementedError

    def build_boundary_conditions(self, posture_type):
        raise NotImplementedError


class AnimationDataUniversal(_AnimationDataBase):

    @TunableFactory.factory_option
    def animation_data_options(locked_args=None, **tunable_data_entries):
        return {'_animation_data': _TunableAnimationData(locked_args=locked_args, **tunable_data_entries)}

    def get_animation_data(self, sim, target):
        return self._animation_data

    def get_provided_postures_gen(self):
        asm = create_asmself._animation_data._asm_keyget_throwaway_animation_context
        provided_postures = asm.provided_postures
        if provided_postures:
            for species in Species:
                if species == Species.INVALID:
                    continue
                yield (
                 species, provided_postures, asm)

    def get_supported_postures_gen(self):
        asm = create_asmself._animation_data._asm_keyget_throwaway_animation_context
        supported_postures = asm.get_supported_postures_for_actor(self._animation_data._actor_param_name)
        for species in Species:
            if species == Species.INVALID:
                continue
            yield (
             species, supported_postures, asm)

    def build_boundary_conditions(self, posture_type):
        build_boundary_conditions_for_postureself._animation_dataposture_type


class AnimationDataByActorSpecies(_AnimationDataBase):

    @TunableFactory.factory_option
    def animation_data_options(locked_args=None, **tunable_data_entries):
        return {'_actor_species_mapping': TunableMapping(description='\n                A mapping from actor species to animation data.\n                ',
                                     key_type=TunableEnumEntry(description='\n                    Species these animations are intended for.\n                    ',
                                     tunable_type=Species,
                                     default=(Species.HUMAN),
                                     invalid_enums=(
                                    Species.INVALID,)),
                                     value_type=_TunableAnimationData(locked_args=locked_args, **tunable_data_entries))}

    def get_animation_data(self, sim, target):
        return self._actor_species_mapping.get(sim.species)

    def get_animation_species(self):
        return self._actor_species_mapping.keys()

    def get_provided_postures_gen(self):
        for species, animation_data in self._actor_species_mapping.items():
            asm = create_asmanimation_data._asm_keyget_throwaway_animation_context
            provided_postures = asm.provided_postures
            if not provided_postures:
                continue
            yield (
             species, provided_postures, asm)

    def get_supported_postures_gen(self):
        for species, animation_data in self._actor_species_mapping.items():
            asm = create_asmanimation_data._asm_keyget_throwaway_animation_context
            supported_postures = asm.get_supported_postures_for_actor(animation_data._actor_param_name)
            yield (species, supported_postures, asm)

    def build_boundary_conditions(self, posture_type):
        for _species, animation_data in self._actor_species_mapping.items():
            build_boundary_conditions_for_postureanimation_dataposture_type


class AnimationDataByActorAndTargetSpecies(_AnimationDataBase):

    @TunableFactory.factory_option
    def animation_data_options(locked_args=None, **tunable_data_entries):
        return {'_actor_species_mapping': TunableMapping(description='\n                A mapping from actor species to target-based animation data\n                mappings.\n                ',
                                     key_type=TunableEnumEntry(description='\n                    Species these animations are intended for.\n                    ',
                                     tunable_type=Species,
                                     default=(Species.HUMAN),
                                     invalid_enums=(
                                    Species.INVALID,)),
                                     value_type=TunableMapping(description='\n                    A mapping of target species to animation data.\n                    ',
                                     key_type=TunableEnumEntry(description='\n                        Species these animations are intended for.\n                        ',
                                     tunable_type=Species,
                                     default=(Species.HUMAN),
                                     invalid_enums=(
                                    Species.INVALID,)),
                                     value_type=_TunableAnimationData(locked_args=locked_args, **tunable_data_entries)))}

    def get_animation_data(self, sim, target):
        actor_animation_data = self._actor_species_mapping.get(sim.species)
        if actor_animation_data is not None:
            return actor_animation_data.get(target.species)

    def get_provided_postures_gen(self):
        for species, target_species_data in self._actor_species_mapping.items():
            animation_data = next(iter(target_species_data.values()))
            asm = create_asmanimation_data._asm_keyget_throwaway_animation_context
            provided_postures = asm.provided_postures
            if not provided_postures:
                continue
            yield (
             species, provided_postures, asm)

    def get_supported_postures_gen(self):
        for species, target_species_data in self._actor_species_mapping.items():
            animation_data = next(iter(target_species_data.values()))
            asm = create_asmanimation_data._asm_keyget_throwaway_animation_context
            supported_postures = asm.get_supported_postures_for_actor(animation_data._actor_param_name)
            yield (species, supported_postures, asm)

    def build_boundary_conditions(self, posture_type):
        for _species, target_species_data in self._actor_species_mapping.items():
            for target_species_animation_data in target_species_data.values():
                build_boundary_conditions_for_posturetarget_species_animation_dataposture_type