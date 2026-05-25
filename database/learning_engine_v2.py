import sqlite3

class LearningEngineV2:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.init_table()

    # ==================================================
    # TABELA DE EVOLUÇÃO DO MODELO
    # ==================================================

    def init_table(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight_low REAL,
            weight_medium REAL,
            weight_high REAL,
            accuracy REAL,
            last_update TEXT
        )
        """)

        self.conn.commit()

    # ==================================================
    # PEGAR ESTADO ATUAL
    # ==================================================

    def get_state(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT weight_low, weight_medium, weight_high, accuracy
        FROM model_state
        ORDER BY id DESC
        LIMIT 1
        """)

        row = cursor.fetchone()

        if row is None:
            return {
                "weight_low": 0.33,
                "weight_medium": 0.33,
                "weight_high": 0.34,
                "accuracy": 0.0
            }

        return {
            "weight_low": row[0],
            "weight_medium": row[1],
            "weight_high": row[2],
            "accuracy": row[3]
        }

    # ==================================================
    # ATUALIZAÇÃO INTELIGENTE DO MODELO
    # ==================================================

    def update(self, prediction, real, accuracy):

        state = self.get_state()

        correct = 1 if prediction == real else 0

        # ==========================================
        # AJUSTE DINÂMICO DE PESOS
        # ==========================================

        learning_rate = 0.05

        if real == "LOW":
            state["weight_low"] += learning_rate * (1 - correct)
        elif real == "MEDIUM":
            state["weight_medium"] += learning_rate * (1 - correct)
        else:
            state["weight_high"] += learning_rate * (1 - correct)

        # ==========================================
        # NORMALIZAÇÃO
        # ==========================================

        total = state["weight_low"] + state["weight_medium"] + state["weight_high"]

        state["weight_low"] /= total
        state["weight_medium"] /= total
        state["weight_high"] /= total

        # ==========================================
        # SALVAR NOVO ESTADO
        # ==========================================

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO model_state (
            weight_low,
            weight_medium,
            weight_high,
            accuracy,
            last_update
        ) VALUES (?, ?, ?, ?, datetime('now'))
        """, (
            state["weight_low"],
            state["weight_medium"],
            state["weight_high"],
            accuracy
        ))

        self.conn.commit()

    # ==================================================
    # ANALYTICS DO MODELO
    # ==================================================

    def model_stats(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT COUNT(*), AVG(accuracy)
        FROM model_state
        """)

        row = cursor.fetchone()

        return {
            "updates": row[0],
            "avg_accuracy": round(row[1] or 0, 3)
        }