import numpy as np


class PatternDetector:

    def __init__(self, data):

        # ==========================================
        # ACEITA LISTA OU DATAFRAME
        # ==========================================

        if isinstance(data, list):
            self.values = np.array(data, dtype=float)

        else:
            try:
                self.values = np.array(data["multiplier"], dtype=float)
            except Exception:
                self.values = np.array([], dtype=float)

    # ==========================================
    # VOLATILIDADE
    # ==========================================

    def volatility(self):

        if len(self.values) < 2:
            return 0.0

        return float(np.std(self.values))

    # ==========================================
    # LOW STREAK
    # ==========================================

    def low_streak(self):

        streak = 0

        for v in reversed(self.values):

            if v < 2:
                streak += 1
            else:
                break

        return streak

    # ==========================================
    # SCORE SIMPLES
    # ==========================================

    def risk_score(self):

        if len(self.values) == 0:
            return 0.0

        volatility = np.std(self.values)
        mean = np.mean(self.values)

        return float(round(volatility + (1 / (mean + 0.1)), 3))