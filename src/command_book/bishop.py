from src.modules.player import Player, JUMP_KEY

TP = "SPACE"


class Bishop(Player):

    def __init__(self, context, device, game):
        super().__init__(context, device, game)

    def to_down(self):
        self.hold("DOWN")
        self.press(JUMP_KEY)

    def to_top(self):
        self.press("ALT")
        self.hold("UP")
        self.press(TP)
        self.release("UP")

    def flash_jump(self):
        self.press(TP)
