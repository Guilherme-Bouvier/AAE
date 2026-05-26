import requests


class TelegramService:

    def send_message(self, token: str, chat_id: str, text: str):

        if not token or not chat_id:
            print("[TELEGRAM] Configuração inválida")
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }

        try:
            requests.post(url, data=payload, timeout=5)
            return True
        except Exception as e:
            print("[TELEGRAM ERROR]", e)
            return False