import cv2

from src.common import config, utils
import numpy as np

from src.common.gdi_capture import gdi_capture
from src.common.gdi_capture.gdi_capture import CaptureWindow
from src.common.utils import convert_image, show_image

# These are colors taken from the mini-map in BGRA format.
PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)

# The distance between the top of the minimap and the top of the screen
MINIMAP_TOP_BORDER = 5

# The thickness of the other three borders of the minimap
MINIMAP_BOTTOM_BORDER = 9

# Offset in pixels to adjust for windowed mode
WINDOWED_OFFSET_TOP = 36
WINDOWED_OFFSET_LEFT = 10

# The top-left and bottom-right corners of the minimap
MM_TL_TEMPLATE = cv2.imread('assets/minimap_tl_template.png', 0)
MM_BR_TEMPLATE = cv2.imread('assets/minimap_br_template.png', 0)

MMT_HEIGHT = max(MM_TL_TEMPLATE.shape[0], MM_BR_TEMPLATE.shape[0])
MMT_WIDTH = max(MM_TL_TEMPLATE.shape[1], MM_BR_TEMPLATE.shape[1])

# The player's symbol on the minimap
PLAYER_TEMPLATE = cv2.imread('assets/player_template.png', 0)
PT_HEIGHT, PT_WIDTH = PLAYER_TEMPLATE.shape


class Game:
    def __init__(self, region=None):
        config.game = self
        self.hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        self.capture = CaptureWindow(self.hwnd)

        # These values should represent pixel locations on the screen of the mini-map.
        if region:
            pass
        self.minimap = self.get_minimap()

    def get_rune_image(self):
        """
        Takes a picture of the application window.
        """
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                print("MapleStory.exe was not found.")
                return None
            return img.copy()

    def locate(self, *color):
        """
        Returns the median location of BGRA tuple(s).
        """
        # Crop the image to show only the mini-map.
        # img_cropped = img[self.left:self.right, self.top:self.bottom]
        locations = []
        img_cropped = self.get_minimap()
        height, width = img_cropped.shape[0], img_cropped.shape[1]
        # Reshape the image from 3-d to 2-d by row-major order.
        img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
        for c in color:
            sum_x, sum_y, count = 0, 0, 0
            # Find all index(s) of np.ndarray matching a specified BGRA tuple.
            matches = np.where(np.all((img_reshaped == c), axis=1))[0]
            for idx in matches:
                # Calculate the original (x, y) position of each matching index.
                sum_x += idx % width
                sum_y += idx // width
                count += 1
            if count > 0:
                x_pos = sum_x / count
                y_pos = sum_y / count
                locations.append((x_pos, y_pos))
        show_image(img_cropped)
        # TODO 找色失败问题
        return locations

    def get_player_location(self):
        """
        Returns the (x, y) position of the player on the mini-map.
        """
        # location = self.locate(PLAYER_BGRA)
        # return location[0] if len(location) > 0 else None
        self.minimap = self.get_minimap()
        # show_image(self.minimap)
        player = utils.multi_match(self.minimap, PLAYER_TEMPLATE, threshold=0.8)
        if player:
            return player[0]

    def get_rune_location(self):
        """
        Returns the (x, y) position of the rune on the mini-map.
        """
        location = self.locate(RUNE_BGRA)
        return location[0] if len(location) > 0 else None

    def get_other_location(self):
        """
        Returns a boolean value representing the presence of any other players on the mini-map.
        """
        location = self.locate(ENEMY_BGRA, GUILD_BGRA, BUDDY_BGRA)
        return len(location) > 0

    def get_minimap_var(self):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            return convert_image(self.minimap, img)

    def get_minimap(self):
        frame = self.capture.screenshot()
        # with gdi_capture.CaptureWindow(self.hwnd) as frame:
        if frame is None:
            print("MapleStory.exe was not found.")
            return None
        else:
            tl, _ = utils.single_match(frame, MM_TL_TEMPLATE)
            _, br = utils.single_match(frame, MM_BR_TEMPLATE)
            mm_tl = (
                tl[0] + MINIMAP_BOTTOM_BORDER,
                tl[1] + MINIMAP_TOP_BORDER
            )
            mm_br = (
                max(mm_tl[0] + PT_WIDTH, br[0] - MINIMAP_BOTTOM_BORDER),
                max(mm_tl[1] + PT_HEIGHT, br[1] - MINIMAP_BOTTOM_BORDER)
            )
            # minimap_ratio = (mm_br[0] - mm_tl[0]) / (mm_br[1] - mm_tl[1])

            minimap_sample = frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
            self.minimap = minimap_sample
            return minimap_sample
        # return convert_image(minimap_img, img)
