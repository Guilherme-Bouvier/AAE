import sqlite3

class LearningDB:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction TEXT,
            real_value TEXT,
            correct INTEGER,
            volatility REAL,
            low_streak INTEGER,
            score REAL,
            created_at TEXT
        )
        """)

        self.conn.commit()

    def save(self, data):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO learning (
            prediction,
            real_value,
            correct,
            volatility,
            low_streak,
            score,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)

        self.conn.commit()

    def get_stats(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(correct) as hits
        FROM learning
        """)

        row = cursor.fetchone()

        total = row[0] or 0
        hits = row[1] or 0

        accuracy = hits / total if total > 0 else 0

        return {
            "total": total,
            "hits": hits,
            "errors": total - hits,
            "accuracy": round(accuracy, 3)
        }