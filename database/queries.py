# ==========================================================
# QUERIES DO BANCO
# ==========================================================

# Aqui centralizamos:
# - inserts;
# - consultas;
# - filtros.

from database.models import Round

# ==========================================================
# SALVAR RODADA
# ==========================================================

def save_round(db, round_data):

    round_object = Round(
        multiplier=round_data["multiplier"],
        players=round_data["players"],
        bet_volume=round_data["bet_volume"]
    )

    db.add(round_object)

    db.commit()