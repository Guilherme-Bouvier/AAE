class DataRouter:

    def __init__(self, ia_engine):

        self.ia = ia_engine

        self.source_mode = "ocr"  # ocr | url | api | sim

    # ============================
    # DEFINIR FONTE
    # ============================

    def set_source(self, mode: str):

        self.source_mode = mode

    # ============================
    # RECEBER DADO (UNIFICADO)
    # ============================

    def push(self, value):

        if value is None:
            return None

        # manda direto para IA Engine
        return self.ia.process(value)