# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Core\sims4\sim_irq_service.py
# Compiled at: 2014-02-15 00:22:04
# Size of source mod 2**32: 3338 bytes
import argparse
from sims4.service_manager import Service
import sims4.log
logger = sims4.log.Logger('SimIrqService')
try:
    import _sim_irq
except ImportError:

    class _sim_irq:

        @staticmethod
        def handle_sim_irq(zone_id):
            return 0


class SimIrqService(Service):
    _instance = None

    def __init__(self):
        self._is_active = False
        self._is_inprogress = False
        self._zone_id = -1
        parser = argparse.ArgumentParser()
        parser.add_argument('--simyield', dest='simyield', action='store_true')
        parser.add_argument('--no-simyield', dest='simyield', action='store_false')
        parser.set_defaults(simyield=True)
        args, unused_args = parser.parse_known_args()
        self._is_enabled = args.simyield

    def start(self):
        SimIrqService._instance = self

    def stop(self):
        SimIrqService._instance = None

    def on_client_connect(self, client):
        self._is_active = True

    def on_client_disconnect(self, client):
        self._is_active = False

    def _yield_to_irq(self):
        if self._is_enabled:
            if self._is_active:
                if not self._is_inprogress:
                    try:
                        self._is_inprogress = True
                        _sim_irq.handle_sim_irq(self._zone_id)
                    finally:
                        self._is_inprogress = False


def yield_zone_id(zone_id):
    SimIrqService._instance._zone_id = zone_id


def yield_to_irq():
    if SimIrqService._instance is None:
        return
    SimIrqService._instance._yield_to_irq()