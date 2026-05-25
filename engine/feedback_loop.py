import sqlite3
from datetime import datetime


class FeedbackLoop:

    def __init__(self, db_path="data/rounds.db"):

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self._create_table()

    # ==================================================
    # TABELA DE EVOLUÇÃO DO MODELO
    # ==================================================

    def _create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accuracy REAL,
            error_rate REAL,
            confidence_avg REAL,
            score REAL,
            created_at TEXT
        )
        """)

        self.conn.commit()

    # ==================================================
    # CALCULAR PERFORMANCE GERAL
    # ==================================================

    def evaluate_model(self):

        self.cursor.execute("""
        SELECT
            AVG(is_correct),
            AVG(error_margin)
        FROM learning_results
        """)

        result = self.cursor.fetchone()

        if not result or result[0] is None:
            return None

        accuracy = result[0]
        error_rate = result[1]

        return accuracy, error_rate

    # ==================================================
    # CALCULAR CONFIANÇA DAS PREVISÕES
    # ==================================================

    def evaluate_confidence(self):

        self.cursor.execute("""
        SELECT AVG(confidence)
        FROM predictions
        """)

        result = self.cursor.fetchone()[0]

        return result if result else 0.0

    # ==================================================
    # SCORE FINAL DO MODELO
    # ==================================================

    def compute_score(self, accuracy, error_rate, confidence):

        score = (
            (accuracy * 100)
            - (error_rate * 50)
            + (confidence * 20)
        )

        return round(score, 2)

    # ==================================================
    # REGISTRAR EVOLUÇÃO
    # ==================================================

    def save_evolution(self):

        accuracy, error_rate = self.evaluate_model()

        if accuracy is None:
            return None

        confidence = self.evaluate_confidence()

        score = self.compute_score(
            accuracy,
            error_rate,
            confidence
        )

        self.cursor.execute("""
        INSERT INTO model_evolution (
            accuracy,
            error_rate,
            confidence_avg,
            score,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            accuracy,
            error_rate,
            confidence,
            score,
            datetime.now().isoformat()
        ))

        self.conn.commit()

        return {
            "accuracy": accuracy,
            "error_rate": error_rate,
            "confidence": confidence,
            "score": score
        }

    # ==================================================
    # HISTÓRICO DE EVOLUÇÃO
    # ==================================================

    def get_history(self, limit=50):

        self.cursor.execute("""
        SELECT *
        FROM model_evolution
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    # ==================================================
    # FECHAR CONEXÃO
    # ==================================================

    def close(self):
        self.conn.close()