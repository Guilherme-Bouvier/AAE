import json
import os
from datetime import datetime


class LogSystem:

    def __init__(self, path="data/logs.json"):

        self.path = path

        self.logs = []

        self.load()

    # ============================
    # CARREGAR LOGS
    # ============================

    def load(self):

        if os.path.exists(self.path):

            with open(self.path, "r") as f:
                self.logs = json.load(f)

    # ============================
    # SALVAR LOGS
    # ============================

    def save(self):

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with open(self.path, "w") as f:
            json.dump(self.logs, f, indent=4)

    # ============================
    # REGISTRAR EVENTO
    # ============================

    def add(self, value, prediction, confidence, learning_state):

        error = abs(prediction - value)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "value": value,
            "prediction": prediction,
            "error": error,
            "confidence": confidence,
            "learning": learning_state
        }

        self.logs.append(log_entry)

        # mantém limite de memória
        if len(self.logs) > 5000:
            self.logs = self.logs[-5000:]

        self.save()

    # ============================
    # ESTATÍSTICAS
    # ============================

    def stats(self):

        if not self.logs:
            return {}

        errors = [log["error"] for log in self.logs]

        return {
            "total_logs": len(self.logs),
            "avg_error": sum(errors) / len(errors),
            "max_error": max(errors),
            "min_error": min(errors)
        }

    # ============================
    # EXPORTAR
    # ============================

    def export(self):

        return self.logs