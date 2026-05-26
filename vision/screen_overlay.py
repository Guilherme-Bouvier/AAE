import pytesseract
import cv2
import numpy as np
import mss
import re

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Guilherme\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


class ScreenOverlayOCR:

    def __init__(self, region=None):

        self.region = region

    def set_region(self, region):
        self.region = region

    def capture(self):

        if not self.region:
            return None

        try:

            with mss.mss() as sct:

                screen = sct.grab(self.region)

                img = np.array(screen)

                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_BGRA2BGR
                )

                return img

        except:
            return None

    def read(self, image):

        if image is None:
            return ""

        try:

            text = pytesseract.image_to_string(image)

            return text

        except:
            return ""

    def extract(self, text):

        pattern = r"(\d+(?:\.\d+)?)\s*x"

        match = re.findall(
            pattern,
            text.lower()
        )

        if match:
            return float(match[-1])

        return None

    def get_value(self):

        img = self.capture()

        text = self.read(img)

        return self.extract(text)