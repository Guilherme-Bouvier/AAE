import numpy as np
import cv2
import mss
import re
import easyocr


class OCREngine:

    def __init__(self, region=None):

        """
        region = {
            "top": 100,
            "left": 100,
            "width": 300,
            "height": 200
        }
        """

        self.region = region
        self.reader = easyocr.Reader(['en'], gpu=False)

    # ============================
    # ATUALIZAR REGIÃO DO OVERLAY
    # ============================

    def set_region(self, region):
        self.region = region

    # ============================
    # CAPTURA DE TELA
    # ============================

    def capture_screen(self):

        if not self.region:
            return None

        with mss.mss() as sct:
            screenshot = sct.grab(self.region)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            return img

    # ============================
    # OCR (LEITURA)
    # ============================

    def read_text(self, image):

        if image is None:
            return []

        results = self.reader.readtext(image)

        texts = [res[1] for res in results]

        return texts

    # ============================
    # EXTRAIR MULTIPLICADOR
    # ============================

    def extract_multiplier(self, texts):

        pattern = r"(\d+(?:\.\d+)?)\s*x"

        for text in texts:

            match = re.findall(pattern, text.lower())

            if match:
                return float(match[-1])

        return None

    # ============================
    # PIPELINE COMPLETO
    # ============================

    def get_value(self):

        img = self.capture_screen()
        texts = self.read_text(img)
        value = self.extract_multiplier(texts)

        return value