import json

# from base import HassBase

from appdaemon.apps.base import HassBase


class Occupancy(HassBase):
    async def initialize(self):
        self.log(f"hello")
        #await self._find_entities()
