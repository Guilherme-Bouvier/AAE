import numpy as np
import cv2
import mss
import re
import easyocr


class ScreenOverlayOCR:

    def __init__(self, region=None):

        """
        region exemplo:
        {
            "top": 200,
            "left": 500,
            "width": 300,
            "height": 200
        }
        """

        self.region = region
        self.reader = easyocr.Reader(['en'], gpu=False)

    # ============================
    # DEFINIR ÁREA DO OVERLAY
    # ============================

    def set_region(self, region):
        self.region = region

    # ============================
    # CAPTURA DE TELA
    # ============================

    def capture(self):

        if not self.region:
            return None

        with mss.mss() as sct:
            screen = sct.grab(self.region)

            img = np.array(screen)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            return img

    # ============================
    # OCR
    # ============================

    def read(self, image):

        if image is None:
            return []

        results = self.reader.readtext(image)

        return [r[1] for r in results]

    # ============================
    # EXTRAIR MULTIPLICADOR
    # ============================

    def extract(self, texts):

        pattern = r"(\d+(?:\.\d+)?)\s*x"

        for t in texts:

            match = re.findall(pattern, t.lower())

            if match:
                return float(match[-1])

        return None

    # ============================
    # PIPELINE COMPLETO
    # ============================

    def get_value(self):

        img = self.capture()
        texts = self.read(img)
        return self.extract(texts)