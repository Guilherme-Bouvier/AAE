class RiskEngine:

    def calculate_risk(self, history):

        if not history:
            return 0.5

        avg = sum(history[-20:]) / min(len(history), 20)

        if avg < 2:
            return 0.2  # conservador

        if avg < 10:
            return 0.5  # médio

        return 0.8  # agressivo