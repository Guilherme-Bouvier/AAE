from analysis.pattern_detector import PatternDetector
from analysis.predictor_engine import PredictorEngine
from analysis.learning_engine import LearningEngine
from datetime import datetime


class IAEngine:

    def __init__(self, db_path):

        self.db_path = db_path

        self.learning = LearningEngine(db_path)

        self.last_prediction = None

        self.history = []

    # ============================
    # RECEBER NOVO DADO
    # ============================

    def process(self, value):

        if value is None:
            return None

        # salva histórico local
        self.history.append(value)

        if len(self.history) > 100:
            self.history = self.history[-100:]

        # ============================
        # DETECTOR
        # ============================

        detector = PatternDetector(
            type("obj", (), {"df": {"multiplier": self.history}})
        )

        volatility = detector.volatility()
        low_streak = detector.low_streak()
        score = detector.risk_score()

        # ============================
        # PREDICTOR
        # ============================

        predictor = PredictorEngine(
            type("obj", (), {"df": {"multiplier": self.history}})
        )

        prediction_list = predictor.predict_next(steps=1)
        prediction = prediction_list[0]

        confidence = predictor.confidence_score()

        # ============================
        # LEARNING (FEEDBACK LOOP)
        # ============================

        if self.last_prediction is not None:

            self.learning.update(
                prediction=self.last_prediction,
                real=value
            )

        self.last_prediction = prediction

        state = self.learning.get_state()

        # ============================
        # OUTPUT UNIFICADO
        # ============================

        result = {
            "value": value,
            "prediction": prediction,
            "confidence": confidence,
            "volatility": volatility,
            "low_streak": low_streak,
            "risk_score": score,
            "accuracy": state.get("accuracy", 0),
            "hits": state.get("hits", 0),
            "errors": state.get("errors", 0),
            "timestamp": datetime.now().isoformat()
        }

        return result