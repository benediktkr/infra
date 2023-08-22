"""Define an app for working with TTS (over Sonos)."""

# pylint: disable=attribute-defined-outside-init,too-few-public-methods
# pylint: disable=unused-argument,too-many-arguments

from datetime import timedelta
from typing import Tuple, Union

from app import App
from automation import Automation

OPENER_FILE_URL = '/local/tts_opener.mp3'


class TTS(App):
    """Define a class to represent the app."""

    # --- INITIALIZERS --------------------------------------------------------
    def initialize(self) -> None:
        """Initialize."""
        self._last_spoken_text = None
        self.living_room_tv = self.get_app('living_room_tv')
        self.presence_manager = self.get_app('presence_manager')
        self.sonos_manager = self.get_app('sonos_manager')
        self.utilities = self.get_app('utilities')

    # --- CALLBACKS -----------------------------------------------------------
    def _calculate_ending_duration_cb(self, kwargs: dict) -> None:
        """Calculate how long the TTS should play."""
        master_sonos_player = kwargs['master_sonos_player']

        duration = self.get_state(
            str(master_sonos_player), attribute='media_duration')
        if not duration:
            self.error("Couldn't calculate ending duration for TTS")
            return

        self.run_in(
            self._end_cb, duration, master_sonos_player=master_sonos_player)

    def _end_cb(self, kwargs: dict) -> None:
        """Restore the Sonos to its previous state after speech is done."""
        master_sonos_player = kwargs['master_sonos_player']

        master_sonos_player.play_file(OPENER_FILE_URL)
        self.run_in(self._restore_cb, 3.25)

    def _restore_cb(self, kwargs: dict) -> None:
        """Restore the Sonos to its previous state after speech is done."""
        if self.living_room_tv.current_activity_id:
            self.living_room_tv.play()
        self.sonos_manager.ungroup_all()
        self.sonos_manager.restore_all()

    def _speak_cb(self, kwargs: dict) -> None:
        """Restore the Sonos to its previous state after speech is done."""
        master_sonos_player = kwargs['master_sonos_player']
        text = kwargs['text']

        self.call_service(
            'tts/amazon_polly_say',
            entity_id=str(master_sonos_player),
            message=text)

        self.run_in(
            self._calculate_ending_duration_cb,
            2,
            master_sonos_player=master_sonos_player)

    # --- HELPERS -------------------------------------------------------------
    @staticmethod
    def _calculate_iterated_text(text: str, iterations: int = 1) -> str:
        """Return a string that equals itself times a number of iterations."""
        return ' Once again, '.join([text] * iterations)

    def _get_eta_time(self, travel_time: str) -> str:
        """Get an arrival time based upon travel time in minutes."""
        return (self.datetime() + timedelta(
            minutes=int(travel_time))).time().strftime('%I:%M %p')

    # --- APP API -------------------------------------------------------------
    def repeat(self, iterations: int = 1) -> None:
        """Repeat the last thing that was spoken."""
        if self._last_spoken_text:
            final_string = self._calculate_iterated_text(
                self._last_spoken_text, iterations)

            self.log('Repeating over TTS: {0}'.format(final_string))

            self.speak(final_string)

    def speak(self, text: str, iterations: int = 1) -> None:
        """Speak the provided text through the Sonos (pausing as needed)."""

        final_string = self._calculate_iterated_text(text, iterations)

        self.sonos_manager.snapshot_all()
        self.sonos_manager.set_all_volume()
        master_sonos_player = self.sonos_manager.group()
        master_sonos_player.play_file(OPENER_FILE_URL)

        if self.living_room_tv.current_activity_id:
            self.living_room_tv.pause()

        self.log('Speaking over TTS: {0}'.format(final_string))

        self.run_in(
            self._speak_cb,
            3.25,
            master_sonos_player=master_sonos_player,
            text='Good {0}. {1}'.format(self.utilities.relative_time_of_day(),
                                        final_string))

        self._last_spoken_text = text
