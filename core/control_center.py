import threading

# 🧠 IA EVOLUTIVA
from core.learning_engine import LearningEngine

# 📊 LOG SYSTEM
from core.log_system import LogSystem


class ControlCenter:

    def __init__(self, ia_engine, alert_manager, ocr_engine=None):

        # ============================
        # ENGINES BASE
        # ============================
        self.ia = ia_engine
        self.alerts = alert_manager
        self.ocr = ocr_engine

        # ============================
        # IA EVOLUTIVA
        # ============================
        self.learning = LearningEngine()

        # ============================
        # LOG SYSTEM (AUDITORIA)
        # ============================
        self.logger = LogSystem()

        # ============================
        # ESTADO GLOBAL
        # ============================
        self.stream_active = False
        self.ocr_active = False

        self.thread = None
        self.last_value = None

    # ==================================================
    # START STREAM
    # ==================================================

    def start_stream(self, stream_engine):

        if self.stream_active:
            return "Stream já ativo"

        self.stream_active = True

        def run():
            stream_engine.start()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

        return "Stream iniciado"

    # ==================================================
    # STOP STREAM
    # ==================================================

    def stop_stream(self):

        self.stream_active = False
        return "Stream parado"

    # ==================================================
    # PROCESSO CENTRAL (IA + LEARNING + LOGS)
    # ==================================================

    def process(self, value):

        if value is None:
            return None

        self.last_value = value

        # ============================
        # 🔮 IA PREDICTION
        # ============================
        prediction = self.ia.predict_next(steps=1)[0]

        confidence = self.ia.confidence_score()

        # ============================
        # 🧠 LEARNING ENGINE
        # ============================
        learning_state = self.learning.update(prediction, value)

        # ============================
        # 🚨 ALERT SYSTEM
        # ============================
        self.alerts.check(value, confidence)

        # ============================
        # 📊 LOG SYSTEM (AUDITORIA TOTAL)
        # ============================
        self.logger.add(
            value=value,
            prediction=prediction,
            confidence=confidence,
            learning_state=learning_state
        )

        # ============================
        # OUTPUT FINAL
        # ============================
        return {
            "value": value,
            "prediction": prediction,
            "confidence": confidence,
            "learning": learning_state
        }

    # ==================================================
    # STATUS COMPLETO DO SISTEMA
    # ==================================================

    def status(self):

        return {
            "stream_active": self.stream_active,
            "ocr_active": self.ocr_active,
            "last_value": self.last_value,

            # 🧠 IA EVOLUTIVA
            "learning": self.learning.status(),

            # 📊 LOGS
            "logs": self.logger.stats()
        }