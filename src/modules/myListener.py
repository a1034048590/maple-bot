"""A keyboard listener to track user inputs."""

import time
import threading
import winsound
import keyboard as kb
from src.common.interfaces import Configurable
from src.common import config, utils
from datetime import datetime


class Listener(Configurable):
    DEFAULT_CONFIG = {
        'Start/stop': 'f5'
    }
    BLOCK_DELAY = 1  # Delay after blocking restricted button press

    def __init__(self):
        """Initializes this Listener object's main thread."""

        super().__init__("controls")
        config.listener = self

        self.enabled = False
        self.ready = False
        self.block_time = 0
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """
        Starts listening to user inputs.
        :return:    None
        """

        print('\n[~] Started keyboard listener')
        self.thread.start()

    def _main(self):
        """
        Constantly listens for user inputs and updates variables in config accordingly.
        :return:    None
        """
        self.ready = True
        while True:
            if self.enabled:
                if kb.is_pressed(self.config['Start/stop']):
                    Listener.toggle_enabled()
            else:
                print(f"press {self.config['Start/stop']} for start")
            time.sleep(0.01)

    @staticmethod
    def toggle_enabled():
        """Resumes or pauses the current routine. Plays a sound to notify the user."""
        config.enabled = not config.enabled
        utils.print_state()

        if config.enabled:
            winsound.Beep(784, 333)  # G5
        else:
            winsound.Beep(523, 333)  # C5
        time.sleep(0.267)
