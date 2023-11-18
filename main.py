import random

# from rune_solver import find_arrow_directions

import time

from src.command_book.bishop import Bishop
from src.common.interception import interception_filter_key_state
from src.common.interception.interception import Interception
from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.game import Game
from src.modules.notifier import Notifier
from src.modules.listener import Listener
from src.modules.gui import GUI
from src.modules.player import Player


def bind(context):
    context.set_filter(Interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if Interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(Interception.is_keyboard, 0)
            break
    return device


# def solve_rune(g, p, target):
#     """
#     Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
#     """
#     while True:
#         print("Pathing towards rune...")
#         p.go_to(target)
#         # Activate the rune.
#         time.sleep(1)
#         p.press("SPACE")
#         # Take a picture of the rune.
#         time.sleep(1)
#         img = g.get_rune_image()
#         print("Attempting to solve rune...")
#         directions = find_arrow_directions(img)
#
#         if len(directions) == 4:
#             print(f"Directions: {directions}.")
#             for d, _ in directions:
#                 p.press(d)
#
#             # The player dot will be blocking the rune dot, attempt to move left/right to unblock it.
#             p.hold("LEFT")
#             time.sleep(random.uniform(0.5, 1.25))
#             p.release("LEFT")
#
#             p.hold("RIGHT")
#             time.sleep(random.uniform(0.5, 1.25))
#             p.release("RIGHT")
#
#             rune_location = g.get_rune_location()
#             if rune_location is None:
#                 print("Rune has been solved.")
#                 break
#             else:
#                 print("Trying again...")


if __name__ == '__main__':

    bot = Bot()
    capture = Capture()
    notifier = Notifier()
    listener = Listener()
    # game = Game((5, 60, 180, 130))

    bot.start()
    while not bot.ready:
        time.sleep(0.01)

    capture.start()
    while not capture.ready:
        time.sleep(0.01)

    game = Game()
    c = Interception()
    d = bind(c)
    player = Player(c, d, game)

    listener.start()
    while not listener.ready:
        time.sleep(0.01)

    while True:
        # target = (60, 46) (82, 37)(125, 46) (125, 21) (36, 27) (33, 38) (20, 47) (20, 63) (55, 63) (96, 63) (126, 63)
        # 图书馆
        targets = [(140, 52), (82, 52), (20, 52), (49, 19), (100, 36), (100, 19), (129, 16)]
        # targets = [(130, 63), (10, 63), (25, 47), (55, 27), (98, 37), (75, 63)]
        for target in targets:
            print(f"goto:{target}")
            player.go_to(target)
            time.sleep(0.05)
            # player.press("CTRL")

    gui = GUI()
    gui.start()

# if __name__ == "__main__":
#     # This setup is required for Interception to mimic your keyboard.
#     c = interception()
#     d = bind(c)
#
#     # Example Script for Hayato @ SS4.
#     g = Game((5, 60, 180, 130))
#     p = Player(c, d, g)
#     target = (97, 32.5)
#
#     while True:
#         other_location = g.get_other_location()
#         if other_location > 0:
#             print("A player has entered your map.")
#
#         rune_location = g.get_rune_location()
#         if rune_location is not None:
#             print("A rune has appeared.")
#             solve_rune(g, p, rune_location)
#
#         print("Running...")
#         p.go_to(target)
#         p.press("Q")
#         time.sleep(0.5)
#         p.press("W")
#         time.sleep(3)
#         p.go_to(target)
#         p.press("LEFT")
#         time.sleep(0.5)
#         p.hold("E")
#         time.sleep(0.5)
#         p.release("E")
#         p.go_to(target)
#         p.press("RIGHT")
#         time.sleep(0.5)
#         p.hold("E")
#         time.sleep(0.5)
#         p.release("E")
#         time.sleep(3)
