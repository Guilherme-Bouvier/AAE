# ==========================================================
# ENGINE DE VOLATILIDADE
# ==========================================================

# Responsável por medir:
# - dispersão;
# - variação;
# - comportamento da mesa.

import numpy as np

# ==========================================================
# CALCULAR VOLATILIDADE
# ==========================================================

def calculate_volatility(data):

    # Evita erro em lista pequena
    if len(data) < 2:
        return 0

    # ======================================================
    # DESVIO PADRÃO
    # ======================================================

    return round(np.std(data), 2)