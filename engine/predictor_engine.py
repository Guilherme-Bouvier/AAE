import random
import numpy as np
from collections import Counter


class PredictorEngine:

    def __init__(self, df, learning_engine=None):

        self.df = df.copy()
        self.learning_engine = learning_engine

        if len(self.df) > 0:
            self.df = self.df.sort_values("id")

    # ==================================================
    # ESTADO BASE DO MERCADO
    # ==================================================

    def _get_state(self, multiplier):

        if multiplier < 2:
            return "FRIO"

        elif multiplier < 10:
            return "EQUILIBRADO"

        else:
            return "QUENTE"

    # ==================================================
    # SEQUÊNCIA DE ESTADOS
    # ==================================================

    def get_state_sequence(self, window=30):

        data = self.df.tail(window)["multiplier"]

        return [self._get_state(m) for m in data]

    # ==================================================
    # PROBABILIDADE SIMPLES
    # ==================================================

    def base_probability(self):

        sequence = self.get_state_sequence()

        count = Counter(sequence)

        total = len(sequence)

        return {
            state: count[state] / total
            for state in ["FRIO", "EQUILIBRADO", "QUENTE"]
        }

    # ==================================================
    # DETECÇÃO DE TRANSIÇÕES
    # ==================================================

    def transition_matrix(self):

        sequence = self.get_state_sequence()

        transitions = {
            "FRIO": Counter(),
            "EQUILIBRADO": Counter(),
            "QUENTE": Counter()
        }

        for i in range(len(sequence) - 1):

            current = sequence[i]
            next_state = sequence[i + 1]

            transitions[current][next_state] += 1

        matrix = {}

        for state in transitions:

            total = sum(transitions[state].values())

            if total == 0:
                matrix[state] = {"FRIO": 0, "EQUILIBRADO": 0, "QUENTE": 0}
                continue

            matrix[state] = {
                k: v / total
                for k, v in transitions[state].items()
            }

        return matrix

    # ==================================================
    # PREVISÃO DO PRÓXIMO ESTADO
    # ==================================================

    def predict_next(self):

        sequence = self.get_state_sequence()

        if not sequence:
            return None

        current_state = sequence[-1]

        transition = self.transition_matrix()

        probs = transition.get(current_state, {})

        if not probs:
            probs = self.base_probability()

        predicted = max(probs, key=probs.get)

        confidence = probs[predicted]

        return {
            "current_state": current_state,
            "prediction": predicted,
            "confidence": round(confidence, 3),
            "distribution": probs
        }

    # ==================================================
    # PREVISÃO MULTI-PASSO (5–10 FUTUROS)
    # ==================================================

    def predict_multi_step(self, steps=10):

        sequence = self.get_state_sequence()

        if not sequence:
            return []

        state = sequence[-1]

        transition = self.transition_matrix()

        predictions = []

        for i in range(steps):

            probs = transition.get(state, self.base_probability())

            next_state = max(probs, key=probs.get)

            confidence = probs[next_state]

            predictions.append({
                "step": i + 1,
                "prediction": next_state,
                "confidence": round(confidence, 3)
            })

            state = next_state

        return predictions

    # ==================================================
    # SCORE DE CONFIANÇA GLOBAL
    # ==================================================

    def model_confidence(self):

        predictions = self.predict_multi_step(5)

        if not predictions:
            return 0.0

        return round(
            np.mean([p["confidence"] for p in predictions]),
            3
        )