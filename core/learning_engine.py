import json
import os


class LearningEngine:

    def __init__(self, path="data/learning.json"):

        self.path = path

        self.state = {
            "weight_low": 1.0,
            "weight_medium": 1.0,
            "weight_high": 1.0,
            "accuracy": 0.5,
            "samples": 0
        }

        self.load()

    # ============================
    # CARREGAR MEMÓRIA
    # ============================

    def load(self):

        if os.path.exists(self.path):

            with open(self.path, "r") as f:
                self.state = json.load(f)

    # ============================
    # SALVAR MEMÓRIA
    # ============================

    def save(self):

        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=4)

    # ============================
    # REGISTRAR ERRO
    # ============================

    def update(self, prediction, real):

        error = abs(prediction - real)

        self.state["samples"] += 1

        # ajuste simples adaptativo
        if error > 10:

            self.state["weight_high"] *= 1.05

        elif error > 5:

            self.state["weight_medium"] *= 1.03

        else:

            self.state["weight_low"] *= 1.02

        # recalcula acurácia
        self.state["accuracy"] = max(
            0.1,
            1 - (error / (real + 1))
        )

        self.save()

        return self.state

    # ============================
    # ESTADO ATUAL
    # ============================

    def status(self):

        return self.state