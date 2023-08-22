import hassapi
from appdaemon.entity import Entity

import requests
from pydantic import BaseModel

#
# GLaDOS TTS
#
# Args:
#


# https://community.home-assistant.io/t/how-do-you-call-sonos-for-tts-and-to-play-media-files/47076/2


class PlayerState(BaseModel):
    player_entity_id: str
    player_state: str
    owntone_entity_id: str
    owntone_playing: bool

    @classmethod
    async def from_entities(cls, player, owntone_output):
        # self.name = player.get_state(attribute="friendly_name")
        # self.entity_id = player.get_state(attribute="entity_id")
        player_state = await player.get_state()
        owntone_state = await owntone_output.get_state()
        if owntone_state == "on" and player_state == "playing":
            owntone_playing = True
        else:
            owntone_playing = False

        return cls(
            player_entity_id=player.entity_id,
            player_state=player_state,
            owntone_entity_id=owntone_output.entity_id,
            owntone_playing=owntone_playing
        )


class GLaDOS(hassapi.Hass):

    async def initialize(self):

        # message = "hello how are you there"
        # r = requests.post("https://hass.sudo.is/glados/tts", json={'message': message, 'use_cache': True})
        # r.raise_for_status()
        # j = r.json()
        # audiofile_name = j['audiofile_name']
        # audiofile_name = "GLaDOS-test_a34fc3b6d2cce8beb3216c2bbb5e55739e8121ed.mp3"
        self.run_in(
            self.usual_lights,
            0,
            room_name="study"
        )

        self.log("init: GLaDOS")


    async def get_player_state(self, player: Entity) -> PlayerState:
        player_name = player.entity_id.split(".", 2)[1].split("_")[0]
        owntone_output = self.get_entity(f"media_player.owntone_output_{player_name}")
        return await PlayerState.from_entities(player, owntone_output)

    async def usual_lights(self, room_name, **kwargs):
        usual = await self.get_state("light.the_usual_lights")
        self.log(usual)
        members = await self.get_state("light.the_usual_lights", attribute='entity_id')
        self.log(members)

        lights_ = ". ".join([a.split('.')[1].replace("_", " ") for a in members])
        msg = "\n\n\n".join([
            f"the usual lights are: {usual}."
            "        ",
            'and the quote un-quote usual lights, are the following: ',
            f"{lights_}.",
            "but you know that dont you?. ",
            "i mean, its your flat after all."
        ])
        self.log(msg)
        await self.say(message=msg, room_name=room_name)


    async def say(self, message: str, room_name: str):
        r = requests.post("https://hass.sudo.is/glados/tts", json={'message': message, 'use_cache': True})
        r.raise_for_status()
        j = r.json()
        audiofile_name = j['audiofile_name']
        audio_url = f"https://hass.sudo.is/glados/audio/{audiofile_name}"
        self.log(f"audio file: {audiofile_name}")
        await self.play(audio_url, room_name)


    async def play(self, audio_url, room_name: str):
        media_player = f"media_player.{room_name}"
        player = self.get_entity(media_player)
        before = await self.get_player_state(player)
        owntone_output = self.get_entity(before.owntone_entity_id)
        self.log(before)


        if before.owntone_playing:
            self.log("turning off owntone in '{before.player_entity_id}'")
            #await owntone_output.turn_off()
            await self.turn_off(before.owntone_entity_id)
            await owntone_output.wait_state("off")
            await player.wait_state("paused")
            self.log("owntone output is off")
        else:
            self.log("owntone was not playing")

        self.log(await self.get_player_state(player))

        self.call_service(
            "media_player/play_media",
            entity_id=before.player_entity_id,
            media_content_id=audio_url,
            media_content_type="music",
            announce=True
        )

        self.log(f"waiting for tts to finish on {before.player_entity_id}")
        await player.wait_state("playing")
        self.log(await self.get_player_state(player))
        await player.wait_state("paused")
        self.log(await self.get_player_state(player))

        if before.owntone_playing:
            self.log("turning owntone back on")
            #owntone_output.turn_on()
            await self.turn_on(before.owntone_entity_id)
            await owntone_output.wait_state("on")
            self.log("owntone is back on")
        else:
            self.log("owntone was not playing, not turning it back on")
