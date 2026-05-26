import easyocr
import os


class ScreenOverlayOCR:
    """
    OCR seguro para captura de tela.
    Evita download automático de modelos (que causa erro SSL).
    """

    def __init__(self):

        # ==================================================
        # 🔥 EVITA ERROS DE PROXY / SSL
        # ==================================================
        os.environ["NO_PROXY"] = "*"

        # ==================================================
        # 🧠 OCR MODE (SEGURO)
        # ==================================================
        try:
            self.reader = easyocr.Reader(
                ['en'],
                gpu=False,
                download_enabled=False  # 🔥 EVITA CRASH DE SSL
            )

        except Exception as e:
            print("[OCR ERROR] Falha ao inicializar EasyOCR:", e)
            self.reader = None

    # ==================================================
    # SIMULA CAPTURA (BASE PARA FUTURO OVERLAY)
    # ==================================================
    def read_text(self, image):
        """
        Recebe imagem e retorna texto detectado
        """

        if self.reader is None:
            return None

        try:
            result = self.reader.readtext(image)

            texts = []

            for item in result:
                text = item[1]
                texts.append(text)

            return texts

        except Exception as e:
            print("[OCR ERROR] leitura falhou:", e)
            return None

    # ==================================================
    # STATUS DO OCR
    # ==================================================
    def status(self):
        return {
            "ocr_active": self.reader is not None,
            "mode": "safe_mode",
            "download_enabled": False
        }