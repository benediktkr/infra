import json

from loguru import logger

import hassapi

LOG_FORMAT = [
    "<green><dim>{time:YYYY-MM-DDT}</dim>{time:HH:mm:ss}<dim>{time:Z}</dim></green>",
    "<dim><blue>{extra[event_name]: >7} </blue></dim>",
    #"<yellow>{extra[entity_id]: >21}</yellow>",
    #"<green><dim>state=</dim>{extra[entity_state]}</green>",
    "<level>{message}</level>"
]

class Buttons(hassapi.Hass):

    async def initialize(self):
        logger.configure(
            handlers=[{
                "sink": "/var/log/appdaemon/buttons.log",
                "format": " ".join(LOG_FORMAT),
                "level": "INFO",
                "diagnose": False,
                "colorize": True,
                "enqueue": True,
                "colorize": True
            }],
            extra={}
        )

        self.device_ids = {
            'e6b5c5c6502ba5310d69f644f2e70a62': 'wallmote',
        }

        self.listen_event(self.cb_key_pressed, ["zwave_js_value_notification", "zwave_js_notification"])

        logger.info("ready", event_name="init")
        self.log("Buttons: ready")

    def cb_key_pressed(self, *args, **kwargs):
        event_name = args[0]
        j_event_data = json.dumps(args[1], indent=2)
        logger.bind(event_name=event_name).info(f'event_data={j_event_data}')
