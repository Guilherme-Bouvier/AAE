# ==========================================================
# CLASSIFICAÇÃO DE PERFIL DA MESA
# ==========================================================

# Objetivo:
# identificar se a mesa está:
# - fria;
# - normal;
# - quente.

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def classify_distribution(data):

    if len(data) == 0:
        return "NO DATA"

    average = sum(data) / len(data)

    # ======================================================
    # CLASSIFICAÇÃO
    # ======================================================

    if average < 1.7:
        return "COLD"

    elif average < 3:
        return "NORMAL"

    return "HOT"