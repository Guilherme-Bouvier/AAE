# ==========================================================
# ENGINE RTP
# ==========================================================

# RTP = Return To Player
#
# Mede quanto foi pago
# em relação ao apostado.

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def calculate_rtp(total_bet, total_paid):

    if total_bet == 0:
        return 0

    return round((total_paid / total_bet) * 100, 2)