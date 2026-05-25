import requests


class TelegramAlerts:

    def __init__(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id

        # níveis padrão (editáveis depois no dashboard)
        self.thresholds = {
            "10x": True,
            "30x": True,
            "50x": True,
            "100x": True,
            "500x": False,
            "1000x": False
        }

        self.last_sent = None

    # ============================
    # CONFIGURAR ALERTAS
    # ============================

    def set_threshold(self, key, value: bool):

        if key in self.thresholds:
            self.thresholds[key] = value

    # ============================
    # ENVIAR MENSAGEM
    # ============================

    def send_message(self, message: str):

        if not self.token or not self.chat_id:
            print("[TELEGRAM] Config não definida")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"[TELEGRAM ERROR] {e}")

    # ============================
    # VERIFICAR ALERTA
    # ============================

    def check_alert(self, value: float, confidence: float = 0):

        if value is None:
            return

        alert_levels = [
            (1000, "1000x"),
            (500, "500x"),
            (100, "100x"),
            (50, "50x"),
            (30, "30x"),
            (10, "10x"),
        ]

        for threshold, label in alert_levels:

            if value >= threshold and self.thresholds.get(label):

                # evita spam repetido
                if self.last_sent == label:
                    return

                self.last_sent = label

                msg = (
                    f"🚨 ALERTA AAE SYSTEM\n\n"
                    f"Vela detectada: {value}x\n"
                    f"Nível: {label}\n"
                    f"Confiança IA: {confidence:.2%}\n"
                )

                self.send_message(msg)

                return