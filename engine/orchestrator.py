from engine.pattern_detector import PatternDetector
from engine.predictor_engine import PredictorEngine
from engine.learning_engine import LearningEngine
from engine.feedback_loop import FeedbackLoop


class Orchestrator:

    def __init__(self, df, db_path="data/rounds.db"):

        self.df = df

        self.learning = LearningEngine(db_path)
        self.feedback = FeedbackLoop(db_path)

        self.pattern = PatternDetector(df)
        self.predictor = PredictorEngine(df, self.learning)

    # ==================================================
    # EXECUÇÃO COMPLETA DO CICLO
    # ==================================================

    def run_cycle(self, actual_state=None):

        # 1. PREVISÃO
        prediction = self.predictor.predict_next()

        if not prediction:
            return None

        predicted_state = prediction["prediction"]
        confidence = prediction["confidence"]

        # 2. SALVA PREVISÃO
        prediction_id = self.learning.save_prediction(
            predicted_state,
            confidence
        )

        result = None

        # 3. AVALIA SE EXISTIR DADO REAL
        if actual_state:

            result = self.learning.evaluate_prediction(
                prediction_id,
                actual_state
            )

        # 4. ATUALIZA EVOLUÇÃO DO MODELO
        evolution = self.feedback.save_evolution()

        # 5. RETORNA ESTADO COMPLETO
        return {
            "prediction": prediction,
            "prediction_id": prediction_id,
            "evaluation": result,
            "evolution": evolution
        }