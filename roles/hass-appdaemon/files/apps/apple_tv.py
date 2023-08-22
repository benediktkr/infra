import json

import loguru

import hassapi

LOG_FORMAT = [
    "<green><dim>{time:YYYY-MM-DDT}</dim>{time:HH:mm:ss}<dim>{time:Z}</dim></green>",
    "<dim><blue>{extra[handler]: >7} </blue></dim>",
    "<yellow>{extra[entity_id]: >21}</yellow>",
    "<green><dim>state=</dim>{extra[entity_state]}</green>",
    #"<level>{message}</level>"
]

class AppleTV(hassapi.Hass):

    async def initialize(self):
        loguru.logger.configure(
            handlers=[{
                "sink": "/var/log/appdaemon/apple_tv.log",
                "format": " ".join(LOG_FORMAT),
                "level": "INFO",
                "diagnose": False,
                "colorize": True,
                "enqueue": True,
                "colorize": True
            }],
            extra={}
        )
        self.atv_entity_ids = [
            "media_player.apple_tv",
            "remote.apple_tv",
            "switch.nad_c370"
        ]

        for item in self.atv_entity_ids:
            # listener for events for each entity_id
            self.listen_event(self.cb_listen_event, None, namespace="default", **{'entity_id': 'item'})

            # get the entity, assert that it exists and lsiten for all state changes
            entity = self.get_entity(item)
            assert entity is not None
            entity.listen_state(self.cb_listen_state, attribute="all")

            # and log their current states
            state_ = await entity.get_state(attribute="all")
            self.loguru_state("init", item, state_['state'])

        self.log("AppleTV: ready")

    def loguru_state(self, handler, entity_id, state):
        loguru.logger.bind(handler=handler, entity_id=entity_id, entity_state=state).info("")

    def remove_source_list(self, state):
        state_ = dict(state).copy()
        if state_.get('attributes', None) is not None:
            if state_['attributes'].get('source_list', None) is not None:
                source_list = state_['attributes'].pop('source_list')
                state_['attributes']['source_list'] = {'len': len(source_list)}
        return state_

    def states(self, **kwargs):
        return {k: self.remove_source_list(v) for k,v in kwargs.items()}

    def log_state(self, entity, **states):
        #j_entity = json.dumps(entity, indent=2)
        j_states = json.dumps(self.states(**states), indent=2)

        self.log("\n".join([
            f'[state] entity="{entity}"',
            f"{j_states}",
        ]))

    def cb_listen_state(self, entity, attribute, old, new, **kwargs):
        #states = self.states(old, new, **kwargs)
        #self.log_state(entity, old=old, new=new, kwargs=kwargs)
        self.loguru_state("state", entity, new['state'])


    def cb_listen_event(self, *args, **kwargs):
        if not any(a in f"{args} {kwargs}" for a in self.atv_entity_ids):
            return

        event_name = args[0]
        entity_id = args[1].get('entity_id', None)

        if event_name == "state_changed" and entity_id.startswith("media_player."):
            # if its a state_changed event, the event_data dict has 'new_state' and 'old_state'
            # keys, which contain a state dict that has 'source_' list in 'attributes', that needs
            # to be cleaned.
            event_data = {
                k: self.remove_source_list(v) if k.endswith("_state") else v for k,v in args[1].items()
            }
        else:
            event_data = args[1]

        # self.log("\n".join([
        #     f'[event] event_name="{event_name}" entity_id="{entity_id}"',
        #     json.dumps(event_data, indent=2)
        # ]))

        if event_name == "state_changed":
            old_state = event_data['old_state']['state']
            new_state = event_data['new_state']['state']
            self.loguru_state("event", entity_id, new_state)
