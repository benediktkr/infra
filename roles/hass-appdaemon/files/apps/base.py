from appdaemon.plugins.hass.hassapi import Hass

from entity_ids import EntityName, EntityNames

class HassBase(Hass):
    async def _find_entities(self, **kwargs):
        """in home assistant, these functions are provided to look up
        areas:
          - areas()
          - area_id(lookup_value)
          - area_name(lookup_value)
          - area_entities(area_name_or_id)
          - area_devices(area_name_or_id)


        as far as i can tell, there is no equivalent available in appdaemon
        without signalling to/from hass. instead i'll rely on my naming
        standards to "find areas" with a specific kind of binary_sensor entity

        my naming schema for hass binary_sensor entities is rougly:
          binary_sensor.${kind}_${area_name}

        when needed, extra information is appended to the entity_id:
          binary_sensor.${kind}_${area_name}_foo_bar


        """

        #kinds = ["motion", "door", "human_presence"]
        #entity_patterns = [EntityName(domain="binary_sensor", kind=a) for a in kinds]
        entity_kinds = {
            "binary_sensor": [
                "motion",
                "radar"
                "door"
            ]
        }
        entity_ids = await self._filter_from_state(entity_kinds)
        return entity_ids


    async def _filter_from_state(self, entity_kinds):
        # as generator comprehension:
        #  all_ids = binary_sensor_states.keys()
        #  (a for a in all_ids if a.removeprefix(f"{domain}.").startswith(f"{kind}_"))

        for domain, kinds in entity_kinds.items():
            self.log(f"getting domain '{domain}' from state")
            states = await self.get_state(domain)
            self.log(f"found {len(states)} states in domain '{domain}'")

            for item in states.keys():
                # self.log(type(item))
                # self.log(item)
                entity_name = item.removeprefix(f"{domain}.")
                if any(entity_name.startswith(a) for a in kinds):
                    try:
                        area_name = entity_name.split('_', )[1]
                        self.log(f"found entity '{item}' in area '{area_name}'")

                        template_area_id = await self.render_template("{{ area_id('" + str(item) + "') }}")
                        self.log(f"render template area_id: {template_area_id}")

                    except IndexError:
                        self.log(f"entity_id '{item}' ignored")
        return []
