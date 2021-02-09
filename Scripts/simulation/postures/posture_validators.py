# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\postures\posture_validators.py
# Compiled at: 2016-02-19 02:15:02
# Size of source mod 2**32: 2071 bytes
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, TunableVariant, TunableReference
import services, sims4.resources

class _PostureValidator(HasTunableSingletonFactory, AutoFactoryInit):

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__)


class PostureValidatorTest(_PostureValidator):
    FACTORY_TUNABLES = {'test_set': TunableReference(description="\n            This test set is provided with a DoubleSimResolver. The Actor\n            participant is the transitioning Sim. The Object/TargetSim\n            participant is the posture container we're testing against.\n            \n            Should the test fail, the posture transition is deemed invalid and\n            is discarded.\n            ",
                   manager=(services.get_instance_manager(sims4.resources.Types.SNIPPET)),
                   class_restrictions=('TestSetInstance', ))}

    def __call__(self, resolver):
        return self.test_set(resolver)


class TunablePostureValidatorVariant(TunableVariant):

    def __init__(self, *args, **kwargs):
        (super().__init__)(args, test=PostureValidatorTest.TunableFactory(), 
         default='test', **kwargs)