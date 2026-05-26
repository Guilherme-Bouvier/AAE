import requests
import time
from database.users import UserDB


class StreamAlertManager:

    def __init__(self, token: str):

        self.token = token
        self.user_db = UserDB()

        self.cooldown = {}

    def _send(self, chat_id, text):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            requests.post(url, data={
                "chat_id": chat_id,
                "text": text
            }, timeout=5)
        except:
            pass

    def check(self, chat_id, value, confidence=0.7):

        user = self.user_db.get_user(chat_id)

        if not user:
            return

        plan = user.plan
        risk = float(user.risk)

        now = time.time()

        if chat_id in self.cooldown:
            if now - self.cooldown[chat_id] < 5:
                return

        # 🎯 lógica de risco IA
        threshold = 50 * risk

        if value >= threshold:

            msg = (
                f"📊 AAE ALERT\n"
                f"Vela: {value}x\n"
                f"Plano: {plan}\n"
                f"Risco: {risk:.2f}\n"
                f"Confiança: {confidence:.2f}"
            )

            self._send(chat_id, msg)

            self.cooldown[chat_id] = now