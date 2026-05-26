from sqlalchemy import text
from database.db import engine


class UserDB:

    def create_table(self):
        with engine.begin() as conn:
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                chat_id TEXT UNIQUE,
                plan TEXT DEFAULT 'free',
                risk FLOAT DEFAULT 0.5
            )
            """))

    def add_user(self, chat_id, plan="free"):
        with engine.begin() as conn:
            conn.execute(text("""
            INSERT INTO users (chat_id, plan)
            VALUES (:chat_id, :plan)
            ON CONFLICT (chat_id) DO NOTHING
            """), {"chat_id": chat_id, "plan": plan})

    def get_user(self, chat_id):
        with engine.begin() as conn:
            result = conn.execute(text("""
            SELECT * FROM users WHERE chat_id = :chat_id
            """), {"chat_id": chat_id}).fetchone()

            return result

    def update_risk(self, chat_id, risk):
        with engine.begin() as conn:
            conn.execute(text("""
            UPDATE users SET risk = :risk WHERE chat_id = :chat_id
            """), {"risk": risk, "chat_id": chat_id})