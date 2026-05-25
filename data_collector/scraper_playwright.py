from playwright.sync_api import sync_playwright
import re
import time


class URLScraper:
    """
    Captura de dados reais de sites com renderização completa (JS incluso)
    e extração de valores tipo "12.5x", "100x", etc.
    """

    def __init__(self, url: str):
        self.url = url

    # ==================================================
    # ABRE A PÁGINA (RENDER COMPLETO)
    # ==================================================

    def fetch_page(self):

        if not self.url:
            return None

        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                page.goto(self.url, timeout=60000)

                # espera mínima de renderização JS
                page.wait_for_timeout(2000)

                html = page.content()

                browser.close()

                return html

        except Exception as e:
            print(f"[SCRAPER ERROR] {e}")
            return None

    # ==================================================
    # EXTRAÇÃO DE VELAS (X)
    # ==================================================

    def extract_multipliers(self, html: str):

        if not html:
            return []

        # pega padrões tipo 1.5x, 10x, 100.2x
        pattern = r"(\d+(?:\.\d+)?)\s*x"

        values = re.findall(pattern, html, re.IGNORECASE)

        try:
            values = [float(v) for v in values]

            # filtro de segurança (evita lixo da página)
            values = [v for v in values if 1 <= v <= 10000]

            return values

        except:
            return []

    # ==================================================
    # PEGAR ÚLTIMO VALOR
    # ==================================================

    def get_latest(self):

        html = self.fetch_page()

        values = self.extract_multipliers(html)

        if values:
            return values[-1]

        return None

    # ==================================================
    # STREAM SIMPLES (SEM THREAD)
    # ==================================================

    def stream(self, callback, interval=2):

        """
        Loop simples para streaming contínuo.
        """

        while True:

            value = self.get_latest()

            if value is not None:
                callback(value)

            time.sleep(interval)