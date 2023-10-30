from src.common import utils
from src.common.interception.stroke import *
import time

# Scancodes for arrow and alphanumeric/modifier keys should be separated. They have different key-states.
SC_DECIMAL_ARROW = {
    "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
}

SC_DECIMAL = {
    "ALT": 56, "SPACE": 57, "CTRL": 29, "SHIFT": 42,
    "A": 30, "S": 31, "D": 32, "F": 33,
    "Q": 16, "W": 17, "E": 18, "R": 19,
    "1": 2, "2": 3, "3": 4, "4": 5
}

# Change these to your own settings.
JUMP_KEY = "ALT"
ROPE_LIFT_KEY = "Q"
ATTACK = "A"


class Player:
    def __init__(self, context, device, game):
        self.game = game
        # interception
        self.context = context
        self.device = device

    def release_all(self):
        for key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        for key in SC_DECIMAL:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def press(self, key):
        """
        Mimics a human key-press.
        Delay between down-stroke and up-stroke was tested to be around 50 ms.
        """
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def release(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def hold(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))

    # @utils.run_if_enabled
    def go_to(self, target, delay=0.2, player_location=None):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        while True:
            player_location = player_location or self.game.get_player_location()
            if player_location is None:
                continue

            x1, y1 = player_location
            x2, y2 = target

            print(f"player_location:{player_location}")
            print(f"target:{target}")

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                # Player has reached target x-destination, release all held keys.
                self.release_all()
                if abs(y2 - y1) < 7:
                    # Player has reached target y-destination, release all held keys.
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    self.to_down()
                # Player is below target y-position.
                else:
                    if y1 - y2 > 30:
                        self.press(ROPE_LIFT_KEY)
                    else:
                        self.to_top()
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    self.hold("LEFT")
                if abs(x2 - x1) > 30:
                    self.flash_jump()
            time.sleep(delay)

    def to_down(self):
        self.hold("DOWN")
        time.sleep(0.2)
        self.press(JUMP_KEY)
        time.sleep(0.2)
        self.attack()

    def to_top(self):
        self.press(JUMP_KEY)
        self.press("UP")
        self.press("UP")
        time.sleep(0.2)
        self.attack()
        # time.sleep(0.2)

    def flash_jump(self):
        self.press(JUMP_KEY)
        self.press(JUMP_KEY)
        self.attack()

    def attack(self):
        self.hold(ATTACK)
        time.sleep(0.2)
        self.release(ATTACK)
