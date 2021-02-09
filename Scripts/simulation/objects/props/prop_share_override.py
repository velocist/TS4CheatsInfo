# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\props\prop_share_override.py
# Compiled at: 2016-08-15 17:57:05
# Size of source mod 2**32: 4760 bytes
import itertools
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, Tunable, TunableList, TunableVariant, OptionalTunable

class PropShareOverride(HasTunableSingletonFactory, AutoFactoryInit):

    class _PropShareKeyActor(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'actor_name': Tunable(description='\n                The actor that is to be used as a key.\n                ',
                         tunable_type=str,
                         default='x')}

        def get_resolved_key(self, asm):
            return asm.get_actor_by_name(self.actor_name)

    class _PropShareKeyParameter(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'actor_name':OptionalTunable(description="\n                The actor for which this parameter's value is to be used.\n                ",
           tunable=Tunable(description='\n                    The actor name.\n                    ',
           tunable_type=str,
           default='x'),
           enabled_name='Specified',
           disabled_name='Global'), 
         'parameter_name':Tunable(description='\n                The parameter whose value is to be used.\n                ',
           tunable_type=str,
           default=None)}

        def get_resolved_key(self, asm):
            for key, param_value in itertools.chain.from_iterable((d.items() for d in asm.get_all_parameters())):
                if not isinstance(key, str):
                    if key[1] != self.actor_name:
                        continue
                    key = key[0]
                if key != self.parameter_name:
                    continue
                return param_value

    class _PropShareKeyStringLiteral(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {'literal': Tunable(description='\n                The literal string that is to be used as a key.\n                ',
                      tunable_type=str,
                      default='')}

        def get_resolved_key(self, asm):
            return self.literal

    FACTORY_TUNABLES = {'key': TunableList(description='\n            A list of elements that form the key for this share. For keys that\n            are identical, props are shared.\n            ',
              tunable=TunableVariant(actor=(_PropShareKeyActor.TunableFactory()),
              parameter=(_PropShareKeyParameter.TunableFactory()),
              literal=(_PropShareKeyStringLiteral.TunableFactory()),
              default='actor'),
              minlength=1)}

    def get_prop_share_key(self, asm):
        return tuple((key.get_resolved_key(asm) for key in self.key))