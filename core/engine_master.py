import threading


class EngineMaster:

    def __init__(self, control_center):

        self.control = control_center

        self.stream_thread = None

        self.running = False

    # ============================
    # START GLOBAL
    # ============================

    def start(self, stream_engine=None):

        if self.running:
            return "Sistema já ativo"

        self.running = True

        # ativa control center
        self.control.stream_active = True

        if stream_engine:

            def run():
                stream_engine.start()

            self.stream_thread = threading.Thread(target=run, daemon=True)
            self.stream_thread.start()

        return "Sistema iniciado com sucesso"

    # ============================
    # STOP GLOBAL
    # ============================

    def stop(self):

        self.running = False

        self.control.stream_active = False

        self.control.ocr_active = False

        return "Sistema parado com sucesso"

    # ============================
    # STATUS GERAL
    # ============================

    def status(self):

        return {
            "running": self.running,
            "stream": self.control.stream_active,
            "ocr": self.control.ocr_active,
            "last_value": self.control.last_value
        }