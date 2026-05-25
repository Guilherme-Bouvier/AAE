import numpy as np
import random


class PredictorEngine:

    def __init__(self, df):
        """
        Espera:
        df = objeto com atributo df["multiplier"]
        OU lista direta de valores (fallback seguro)
        """

        # ==================================================
        # NORMALIZAÇÃO DE ENTRADA (EVITA ERROS)
        # ==================================================

        if isinstance(df, list):
            self.values = np.array(df, dtype=float)

        else:
            try:
                self.values = np.array(df.df["multiplier"], dtype=float)
            except Exception:
                self.values = np.array([], dtype=float)

    # ==================================================
    # DISTRIBUIÇÃO DE PROBABILIDADE
    # ==================================================

    def probability_distribution(self):

        if len(self.values) < 10:
            return {
                "LOW": 0.33,
                "MEDIUM": 0.33,
                "HIGH": 0.34
            }

        low = np.mean(self.values < 2)
        medium = np.mean((self.values >= 2) & (self.values < 10))
        high = np.mean(self.values >= 10)

        total = low + medium + high

        return {
            "LOW": float(low / total),
            "MEDIUM": float(medium / total),
            "HIGH": float(high / total)
        }

    # ==================================================
    # PREVISÃO FUTURA
    # ==================================================

    def predict_next(self, steps=10):

        dist = self.probability_distribution()

        predictions = []

        for _ in range(steps):

            r = random.random()

            if r < dist["LOW"]:
                predictions.append(round(random.uniform(1.0, 2.5), 2))

            elif r < dist["LOW"] + dist["MEDIUM"]:
                predictions.append(round(random.uniform(2.5, 10.0), 2))

            else:
                predictions.append(round(random.uniform(10.0, 100.0), 2))

        return predictions

    # ==================================================
    # CONFIANÇA DO MODELO
    # ==================================================

    def confidence_score(self):

        if len(self.values) < 20:
            return 0.3

        volatility = np.std(self.values)
        trend = np.mean(np.diff(self.values[-10:]))

        score = (1 / (1 + volatility)) + abs(trend)

        return round(min(score, 1.0), 3)

    # ==================================================
    # BACKTEST SIMPLES
    # ==================================================

    def backtest(self, window=5):

        if len(self.values) < window + 5:
            return {
                "accuracy": 0,
                "hits": 0,
                "misses": 0
            }

        hits = 0
        misses = 0

        for i in range(window, len(self.values) - 1):

            past = self.values[i - window:i]
            prediction = np.mean(past)
            real = self.values[i]

            if real == 0:
                continue

            error = abs(prediction - real) / real

            if error < 0.35:
                hits += 1
            else:
                misses += 1

        total = hits + misses

        accuracy = hits / total if total > 0 else 0

        return {
            "accuracy": round(accuracy, 3),
            "hits": hits,
            "misses": misses
        }