from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import numpy as np

from analysis.predictor_engine import PredictorEngine

app = FastAPI(title="AAE IA API", version="1.0")


DB_PATH = "data/rounds.db"


# ==================================================
# MODELO DE RESPOSTA
# ==================================================

class PredictionResponse(BaseModel):
    previsoes: list
    confianca: float
    estado: str


# ==================================================
# CARREGAR DADOS
# ==================================================

def load_history(limit=100):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT multiplier FROM rounds
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [r[0] for r in rows][::-1]


# ==================================================
# ESTADO SIMPLES
# ==================================================

def get_state(values):

    if len(values) < 10:
        return "INSUFICIENTE"

    std = np.std(values)

    if std < 2:
        return "ESTÁVEL"
    elif std < 10:
        return "MODERADO"
    else:
        return "VOLÁTIL"


# ==================================================
# ENDPOINT PRINCIPAL
# ==================================================

@app.get("/predict", response_model=PredictionResponse)
def predict():

    history = load_history()

    predictor = PredictorEngine(
        type("obj", (), {"df": {"multiplier": history}})
    )

    preds = predictor.predict_next(steps=10)

    return {
        "previsoes": preds,
        "confianca": predictor.confidence_score(),
        "estado": get_state(history)
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "message": "AAE IA rodando corretamente"
    }