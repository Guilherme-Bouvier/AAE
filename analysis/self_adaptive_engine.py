import numpy as np


class SelfAdaptiveEngine:

    def __init__(self):
        self.baseline_std = None
        self.adaptation_level = 1.0
        self.drift_score = 0.0

    # ==================================================
    # DETECTA MUDANÇA DE PADRÃO (DRIFT)
    # ==================================================

    def detect_drift(self, values):

        if len(values) < 20:
            return 0.0

        recent = values[-10:]
        older = values[-30:-10]

        if len(older) == 0:
            return 0.0

        recent_std = np.std(recent)
        older_std = np.std(older)

        drift = abs(recent_std - older_std)

        self.drift_score = drift

        return round(drift, 4)

    # ==================================================
    # AJUSTE AUTOMÁTICO DE SENSIBILIDADE
    # ==================================================

    def adjust_sensitivity(self, values):

        drift = self.detect_drift(values)

        if drift > 10:
            self.adaptation_level = 1.5  # sistema instável
        elif drift > 5:
            self.adaptation_level = 1.2  # moderado
        else:
            self.adaptation_level = 1.0  # estável

        return self.adaptation_level

    # ==================================================
    # ESTADO DE SAÚDE DA IA
    # ==================================================

    def health_status(self):

        if self.drift_score > 10:
            return "CRÍTICO"
        elif self.drift_score > 5:
            return "INSTÁVEL"
        elif self.drift_score > 2:
            return "ATIVO"
        else:
            return "ESTÁVEL"