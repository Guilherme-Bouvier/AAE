import requests
import time


class StreamAlertManager:

    def __init__(self, token: str, chat_id: str):

        self.token = token
        self.chat_id = chat_id

        self.thresholds = {
            10: True,
            30: True,
            50: True,
            100: True,
            500: False,
            1000: False
        }

        self.last_alert_level = None
        self.last_alert_time = 0

        self.cooldown_seconds = 8

    # ============================
    # ENVIO TELEGRAM
    # ============================

    def _send(self, text: str):

        if not self.token or not self.chat_id:
            print("[TELEGRAM] Token ou chat_id não configurado")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        try:
            requests.post(url, data=payload, timeout=5)
        except Exception as e:
            print("[TELEGRAM ERROR]", e)

    # ============================
    # CHECK DE ALERTA
    # ============================

    def check(self, value: float, confidence: float = 0.0):

        if value is None:
            return

        now = time.time()

        # anti-spam global
        if now - self.last_alert_time < self.cooldown_seconds:
            return

        for level in sorted(self.thresholds.keys(), reverse=True):

            if value >= level and self.thresholds[level]:

                if self.last_alert_level == level:
                    return

                self.last_alert_level = level
                self.last_alert_time = now

                message = (
                    "🚨 AAE ALERT SYSTEM\n\n"
                    f"📊 Vela detectada: {value}x\n"
                    f"🎯 Nível: {level}x\n"
                    f"🧠 Confiança IA: {confidence:.2%}\n"
                )

                self._send(message)
                return

    # ============================
    # CONFIG DINÂMICA
    # ============================

    def set_threshold(self, level: int, enabled: bool):

        if level in self.thresholds:
            self.thresholds[level] = enabled