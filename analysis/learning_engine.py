import sqlite3
from datetime import datetime

class LearningEngine:

    def __init__(self, db_path="data/rounds.db"):
        self.db_path = db_path

        self.init_state_if_not_exists()


    # ==================================================
    # CONEXÃO
    # ==================================================

    def connect(self):
        return sqlite3.connect(self.db_path)


    # ==================================================
    # CRIAR ESTADO INICIAL (SE NÃO EXISTIR)
    # ==================================================

    def init_state_if_not_exists(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            low_weight REAL,
            medium_weight REAL,
            high_weight REAL,
            hits INTEGER,
            errors INTEGER,
            accuracy REAL,
            updated_at TEXT
        )
        """)

        # cria linha inicial se não existir nenhuma
        cursor.execute("SELECT COUNT(*) FROM learning_state")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
            INSERT INTO learning_state (
                low_weight,
                medium_weight,
                high_weight,
                hits,
                errors,
                accuracy,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                1.0, 1.0, 1.0,
                0, 0,
                0.0,
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()


    # ==================================================
    # PEGAR ESTADO ATUAL
    # ==================================================

    def get_state(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT low_weight, medium_weight, high_weight, hits, errors, accuracy
        FROM learning_state
        ORDER BY id DESC
        LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        return {
            "low_weight": row[0],
            "medium_weight": row[1],
            "high_weight": row[2],
            "hits": row[3],
            "errors": row[4],
            "accuracy": row[5]
        }


    # ==================================================
    # ATUALIZAR COM ACERTO / ERRO
    # ==================================================

    def update(self, prediction, real):

        state = self.get_state()

        hit = prediction == real

        hits = state["hits"]
        errors = state["errors"]

        if hit:
            hits += 1
        else:
            errors += 1

        total = hits + errors
        accuracy = hits / total if total > 0 else 0

        lw = state["low_weight"]
        mw = state["medium_weight"]
        hw = state["high_weight"]

        # ==================================================
        # AJUSTE DE PESOS
        # ==================================================

        if not hit:

            if real == "LOW":
                lw *= 1.05
            elif real == "MEDIUM":
                mw *= 1.05
            elif real == "HIGH":
                hw *= 1.05

        else:

            if prediction == "LOW":
                lw *= 1.01
            elif prediction == "MEDIUM":
                mw *= 1.01
            elif prediction == "HIGH":
                hw *= 1.01


        # ==================================================
        # NORMALIZAÇÃO
        # ==================================================

        total_w = lw + mw + hw

        lw /= total_w
        mw /= total_w
        hw /= total_w


        # ==================================================
        # SALVAR NOVO ESTADO
        # ==================================================

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO learning_state (
            low_weight,
            medium_weight,
            high_weight,
            hits,
            errors,
            accuracy,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lw, mw, hw,
            hits, errors,
            accuracy,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()


    # ==================================================
    # ACURÁCIA ATUAL
    # ==================================================

    def accuracy(self):

        state = self.get_state()
        return state["accuracy"]