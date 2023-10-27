import cv2

from src.common import config
import numpy as np

from src.common.gdi_capture import gdi_capture
from src.common.utils import convert_image, show_image

# These are colors taken from the mini-map in BGRA format.
PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)


class Game:
    def __init__(self, region=None):
        config.game = self
        self.hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")

        # These values should represent pixel locations on the screen of the mini-map.
        if region:
            self.top, self.left, self.bottom, self.right = region[0], region[1], region[2], region[3]
        else:
            self.top, self.left, self.bottom, self.right = self.get_minimap_var(config.capture.minimap['minimap'])
        print(self.get_player_location())

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
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                print("MapleStory.exe was not found.")
            else:
                """
                The screenshot of the application window is returned as a 3-d np.ndarray, 
                containing 4-length np.ndarray(s) representing BGRA values of each pixel.
                """
                # Crop the image to show only the mini-map.
                # img_cropped = img[self.left:self.right, self.top:self.bottom]
                img_cropped = img[self.top:self.bottom, self.left:self.right]

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
            return locations

    def get_player_location(self):
        """
        Returns the (x, y) position of the player on the mini-map.
        """
        location = self.locate(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

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

    def get_minimap_var(self, minimap_img):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            show_image(img)
            show_image(minimap_img)
            return convert_image(minimap_img, img)
