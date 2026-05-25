import requests
import time
from bs4 import BeautifulSoup
import re


class URLScraper:

    def __init__(self, url):
        self.url = url

    # ==================================================
    # BAIXA HTML
    # ==================================================

    def fetch_html(self):

        try:
            response = requests.get(
                self.url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            return response.text

        except Exception as e:
            print("[SCRAPER ERROR]", e)
            return None

    # ==================================================
    # EXTRAÇÃO MAIS SEGURA DE MULTIPLICADORES
    # ==================================================

    def extract_multiplier(self, html):

        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator=" ")

        # 🔥 procura padrões tipo 1.5x, 10x, 100.2x
        pattern = r"(\d+(?:\.\d+)?)\s*x"

        matches = re.findall(pattern, text)

        if not matches:
            return None

        try:
            values = [float(m) for m in matches]

            # 🔥 remove valores absurdos inválidos
            filtered = [v for v in values if 1 <= v <= 10000]

            if not filtered:
                return None

            return filtered[-1]  # último valor

        except:
            return None

    # ==================================================
    # PEGAR ÚLTIMO VALOR
    # ==================================================

    def get_latest(self):

        html = self.fetch_html()

        return self.extract_multiplier(html)

    # ==================================================
    # STREAM SIMPLES
    # ==================================================

    def run_stream(self, callback, interval=2):

        while True:

            value = self.get_latest()

            if value:
                callback(value)

            time.sleep(interval)