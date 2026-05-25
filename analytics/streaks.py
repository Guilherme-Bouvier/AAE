# ==========================================================
# ENGINE DE STREAKS
# ==========================================================

# Detecta sequências consecutivas.

# ==========================================================
# STREAK BAIXO
# ==========================================================

def low_streak(data, limit=1.30):

    streak = 0

    # ======================================================
    # ANALISA DE TRÁS PARA FRENTE
    # ======================================================

    for value in reversed(data):

        if value <= limit:
            streak += 1

        else:
            break

    return streak