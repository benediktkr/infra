import json

import appdaemon.plugins.hass.hassapi


def is_available(state):
    if state in ["unavailable", "unknown"]:
        return False
    else:
        return True

class ToothbrushManager(appdaemon.plugins.hass.hassapi.Hass):

    async def initialize(self):
        self.toothbrushes = await self.find_toothbrushes()
        for item in self.toothbrushes:
            self.log(f'found "{item}"')


        # set initial states and register callbacks
        for item in self.toothbrushes:
            #await self.listen_state(self.connected_state, signal_strenght, attributes=None)
            await self.set_initial_states(item)

        self.log(f"init: toothbrush")


    async def set_initial_states(self, name):
        signal_entity_id = f"sensor.{name}_signal_strength"
        signal_state = await self.get_state(signal_entity_id)
        self.log(f"{signal_entity_id}: {signal_state}")
        await self.connected_state(name, signal_state)


    async def connected_state(self, name, state):
        entity_id = f"binary_sensor.{name}_connected"
        new_state = is_available(state)
        await self.set_state(entity_id, state=new_state)
        self.log(f'entity_id="{entity_id}" state="{new_state}"')


    async def find_toothbrushes(self):
        """relying on our naming patterns instead of config
        """

        def id_to_name(t):
            return t.removeprefix("sensor.").removesuffix("_state")

        sensors = await self.get_state("sensor")
        #return {id_to_name(k): v for k,v in sensors.items() if k.endswith("_toothbrush_state")}
        return [id_to_name(t) for t in sensors.keys() if t.endswith("_toothbrush_state")]


class Toothbrush(appdaemon.plugins.hass.hassapi.Hass):
    async def initialize(self, **kwargs):
        self.name = kwargs.get("name")
        self.log(self.name)


#     async def __init__(self, name):
#         self.name = name
#         self.entity_ids = {
#             'signal_strength': f'sensor.{name}_signal_strenght',
#             'state': f'sensor.{name}_state',
#             'time': f'sensor.{name}_time',
#         }
#         self.friendly_name = await self.get_state(self.entity_ids['state'])['attributes'].get('friendly_name')

#         self._set_initial_states()

#     async def _initial_states(self):
#         signal_id = self.entity_ids['signal_strength']
#         signal_state = await self.get_state(signal_id)
#         new_state = is_available(signal_state)
#         await self.set_state(signal_id, state=new_state)
#         self.log(f"{signal_entity_id}: {signal_state}")
#         await self.connected_state(name, signal_state)

#     async def initialize(self):
#         self.log(f"init: {self.name}")
