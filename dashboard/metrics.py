# ==========================================================
# MÉTRICAS DO DASHBOARD
# ==========================================================

import pandas as pd

# ==========================================================
# CARREGAR DADOS
# ==========================================================

def build_metrics(df):

    # ======================================================
    # MÉDIA DOS MULTIPLICADORES
    # ======================================================

    avg_multiplier = round(df["multiplier"].mean(), 2)

    # ======================================================
    # MAIOR MULTIPLICADOR
    # ======================================================

    max_multiplier = round(df["multiplier"].max(), 2)

    # ======================================================
    # TOTAL DE RODADAS
    # ======================================================

    total_rounds = len(df)

    return {
        "avg_multiplier": avg_multiplier,
        "max_multiplier": max_multiplier,
        "total_rounds": total_rounds
    }