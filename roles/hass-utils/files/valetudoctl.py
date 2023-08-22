# distributed from ansible

import argparse
import json
from functools import lru_cache

import requests
from loguru import logger

class ValetudoConfig:

    def __init__(self, **kwargs):
        self._config = kwargs.copy()

    def __getattr__(self, name):
        try:
            value = self._config[name]
            if isinstance(value, dict):
                return ValetudoConfig(**value)
            else:
                return value
        except KeyError:
            raise

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __contains__(self, key):
        return key in self._config

    def __setitem__(self, key, value):
        logger.error("config is readonly")
        raise SystemExit

    def __repr__(self):
        return json.dumps(self._config, indent=4)

    @classmethod
    @lru_cache()
    def get(cls, config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return cls(**config)
        except FileNotFoundError:
            return cls(**{})

class ValetudoSession(requests.Session):
    def __init__(self, valetudo_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valetudo_url = valetudo_url

    def _make_url(self, path=""):
        if path.startswith("/"):
            path = path[1:]
        return f"{self.valetudo_url}/{path}"

    def get(self, path, *args, **kwargs):
        url = self._make_url(path)
        r = super().get(url, *args, **kwargs)
        r.raise_for_status()
        return r.json()
    def put(self, path, *args, **kwargs):
        url = self._make_url(path)
        r = super().put(url, *args, **kwargs)
        # logger.debug(url)
        # logger.debug(kwargs.get("json"))
        try:
            r.raise_for_status()
            return r.status_code
            #return r.json()
        except requests.exceptions.HTTPError as e:
            logger.error(r.text)
            raise SystemExit
        # except requests.exceptions.JSONDecodeError as e:
        #     return

class ValetudoClient:
    def __init__(self, config_path):
        self.config = ValetudoConfig.get(config_path)
        self.s = ValetudoSession(self.config.url)
        self.s.headers.update({
            "accept": "application/json"
        })
        # logger.debug("ValetudoClient.__init__")

    # def __enter__(self):
    #     return self

    # def __exit(self):
    #     self

    def get_rooms(self):
        path = "/api/v2/robot/capabilities/MapSegmentationCapability"
        r = self.s.get(path)
        rooms = {item['name']: item['id'] for item in r}
        return rooms

    def clean_room(self, room_name, iterations):
        try:
            room_id = self.config.rooms[room_name]
        except KeyError:
            logger.error(f"room not in config: '{room_name}'")
            raise SystemExit

        payload = {
            "action": "start_segment_action",
            "segment_ids": [str(room_id)],
            "iterations": iterations
        }
        path = "/api/v2/robot/capabilities/MapSegmentationCapability"
        self.s.put(path, json=payload)


    @classmethod
    @lru_cache()
    def get(cls, config_path):
        config = ValetudoConfig.get(config_path)
        return cls(config)

def make_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["show", "clean", "return"])
    parser.add_argument("-c", "--config", help="config file", default="valetudo.json")
    parser.add_argument("-r", "--room")
    parser.add_argument("-i", "--iterations", type=int, default=1)
    return parser

def cli():
    args = make_argparser().parse_args()
    client = ValetudoClient(args.config)

    if args.action == "show":
        rooms = client.get_rooms()
        logger.info(json.dumps(rooms, indent=4))
    elif args.action == "clean" and args.room is not None:
        client.clean_room(args.room, args.iterations)
        logger.success(f"robot is starting to clean {args.room}")

    else:
        raise NotImplementedError



if __name__ == "__main__":
    cli()
