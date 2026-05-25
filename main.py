import time
import sqlite3
from datetime import datetime

from analysis.pattern_detector import PatternDetector
from analysis.predictor_engine import PredictorEngine
from analysis.learning_engine import LearningEngine
from analysis.self_adaptive_engine import SelfAdaptiveEngine

from core.runtime_engine import start_runtime


# ==================================================
# BANCO
# ==================================================

DB_PATH = "data/rounds.db"


def connect():
    return sqlite3.connect(DB_PATH)


# ==================================================
# CARREGAR HISTÓRICO
# ==================================================

def load_history(limit=100):

    conn = connect()
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
# MAIN LOOP
# ==================================================

def main():

    print("🧠 IA AAE iniciada em tempo real...")

    start_runtime()

    learning = LearningEngine(DB_PATH)
    adaptive = SelfAdaptiveEngine()

    last_prediction = None

    while True:

        history = load_history()

        if len(history) < 20:
            print("⏳ Aguardando dados...")
            time.sleep(2)
            continue

        # ==================================================
        # ANÁLISE
        # ==================================================

        detector = PatternDetector(history)

        volatility = detector.volatility()
        low_streak = detector.low_streak()
        score = detector.risk_score()

        # ==================================================
        # ADAPTATIVO
        # ==================================================

        drift = adaptive.detect_drift(history)
        adaptive.adjust_sensitivity(history)
        health = adaptive.health_status()

        # ==================================================
        # PREVISÃO
        # ==================================================

        predictor = PredictorEngine(history)
        prediction = predictor.predict_next(steps=1)[0]
        confidence = predictor.confidence_score()

        # ==================================================
        # CLASSIFICAÇÃO
        # ==================================================

        def classify(v):
            if v < 2:
                return "LOW"
            elif v < 10:
                return "MEDIUM"
            return "HIGH"

        real = history[-1]

        real_class = classify(real)
        pred_class = classify(prediction)

        # ==================================================
        # APRENDIZADO
        # ==================================================

        if last_prediction is not None:
            learning.update(last_prediction, real_class)

        last_prediction = pred_class

        state = learning.get_state()

        # ==================================================
        # OUTPUT
        # ==================================================

        print("\n" + "=" * 70)
        print(f"🎯 REAL: {real:.2f}x ({real_class})")
        print(f"🔮 PREVISÃO: {prediction:.2f}x ({pred_class})")
        print(f"🧠 CONFIANÇA: {confidence}")
        print(f"📊 VOLATILIDADE: {volatility:.2f}")
        print(f"⚡ LOW STREAK: {low_streak}")
        print(f"📈 SCORE: {score:.2f}")

        print("-" * 70)
        print(f"🧬 DRIFT: {drift:.2f}")
        print(f"⚙️ ADAPTAÇÃO: {adaptive.adaptation_level}")
        print(f"❤️ SAÚDE DA IA: {health}")

        print("-" * 70)
        print(f"🏆 ACURÁCIA: {state['accuracy']}")
        print(f"✔ ACERTOS: {state['hits']} | ❌ ERROS: {state['errors']}")
        print("=" * 70)

        time.sleep(2)


if __name__ == "__main__":
    main()