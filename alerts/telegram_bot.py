import requests


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message: str):

        if not self.token or not self.chat_id:
            print("[TELEGRAM] Configuração incompleta")
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