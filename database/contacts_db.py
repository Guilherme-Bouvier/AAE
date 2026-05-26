import sqlite3


class ContactsDB:

    def __init__(self, db_path="data/contacts.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            token TEXT,
            chat_id TEXT
        )
        """)
        self.conn.commit()

    def add_contact(self, name, token, chat_id):

        self.conn.execute(
            "INSERT INTO contacts (name, token, chat_id) VALUES (?, ?, ?)",
            (name, token, chat_id)
        )
        self.conn.commit()

    def delete_contact(self, contact_id):

        self.conn.execute(
            "DELETE FROM contacts WHERE id=?",
            (contact_id,)
        )
        self.conn.commit()

    def get_contacts(self):

        cursor = self.conn.execute("SELECT * FROM contacts")
        return cursor.fetchall()