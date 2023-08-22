import json

from appdaemon.plugins.hass.hassapi import Hass


class BLEMonitor(Hass):
    async def initialize(self):
        self.ble_scanner = self.args["ble_scanner"]
        self.log(f"monitoring: '{self.ble_scanner['entity_id']}'")


    async def cb_ble_scanner(entity, attribute, old, new, **kwargs):
        pass
