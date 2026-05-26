# alerts/contact_manager.py

import requests


class ContactManager:

    def __init__(self, bot_token: str):

        self.bot_token = bot_token
        self.contacts = []  # lista dinâmica

    # ============================
    # ADICIONAR CONTATO
    # ============================

    def add_contact(self, chat_id: str):

        if chat_id not in self.contacts:
            self.contacts.append(chat_id)
            self._send(chat_id, "✅ Você foi adicionado ao sistema AAE com sucesso!")

    # ============================
    # REMOVER CONTATO
    # ============================

    def remove_contact(self, chat_id: str):

        if chat_id in self.contacts:
            self.contacts.remove(chat_id)
            self._send(chat_id, "⚠️ Você foi removido do sistema AAE.")

    # ============================
    # ENVIO TELEGRAM
    # ============================

    def _send(self, chat_id: str, message: str):

        if not self.bot_token:
            return

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        try:
            requests.post(url, data={
                "chat_id": chat_id,
                "text": message
            }, timeout=5)

        except Exception as e:
            print("[TELEGRAM ERROR]", e)

    # ============================
    # BROADCAST ALERT
    # ============================

    def broadcast(self, message: str):

        for chat_id in self.contacts:
            self._send(chat_id, message)