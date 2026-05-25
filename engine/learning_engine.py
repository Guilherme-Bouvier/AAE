import sqlite3
from datetime import datetime


class LearningEngine:

    def __init__(self, db_path="data/rounds.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    # ==================================================
    # CRIA TABELAS NECESSÁRIAS
    # ==================================================

    def _create_tables(self):

        # Tabela de previsões feitas pelo sistema
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            predicted_state TEXT,
            confidence REAL,
            created_at TEXT
        )
        """)

        # Tabela de resultados reais avaliados
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            actual_state TEXT,
            is_correct INTEGER,
            error_margin REAL,
            created_at TEXT
        )
        """)

        self.conn.commit()

    # ==================================================
    # REGISTRAR PREVISÃO
    # ==================================================

    def save_prediction(self, predicted_state, confidence):

        self.cursor.execute("""
        INSERT INTO predictions (predicted_state, confidence, created_at)
        VALUES (?, ?, ?)
        """, (
            predicted_state,
            confidence,
            datetime.now().isoformat()
        ))

        self.conn.commit()

        return self.cursor.lastrowid

    # ==================================================
    # AVALIAR PREVISÃO
    # ==================================================

    def evaluate_prediction(self, prediction_id, actual_state):

        self.cursor.execute("""
        SELECT predicted_state, confidence
        FROM predictions
        WHERE id = ?
        """, (prediction_id,))

        row = self.cursor.fetchone()

        if not row:
            return None

        predicted_state, confidence = row

        is_correct = 1 if predicted_state == actual_state else 0
        error_margin = 0.0 if is_correct else 1.0

        self.cursor.execute("""
        INSERT INTO learning_results (
            prediction_id,
            actual_state,
            is_correct,
            error_margin,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            prediction_id,
            actual_state,
            is_correct,
            error_margin,
            datetime.now().isoformat()
        ))

        self.conn.commit()

        return {
            "prediction": predicted_state,
            "actual": actual_state,
            "correct": is_correct
        }

    # ==================================================
    # TAXA DE ACERTO
    # ==================================================

    def accuracy(self):

        self.cursor.execute("""
        SELECT AVG(is_correct)
        FROM learning_results
        """)

        result = self.cursor.fetchone()[0]

        return result if result else 0.0

    # ==================================================
    # SCORE EVOLUTIVO
    # ==================================================

    def learning_score(self):

        self.cursor.execute("""
        SELECT
            AVG(is_correct) * 100 -
            AVG(error_margin) * 10
        FROM learning_results
        """)

        result = self.cursor.fetchone()[0]

        return result if result else 0.0

    # ==================================================
    # FECHAR CONEXÃO
    # ==================================================

    def close(self):
        self.conn.close()