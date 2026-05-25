# ==========================================================
# GERADOR FAKE DE RODADAS
# ==========================================================

# Este módulo simula um jogo real.
#
# Objetivo:
# permitir desenvolvimento SEM depender:
# - do site;
# - websocket;
# - scraping.
#
# Isso acelera MUITO o desenvolvimento.

import random
import time

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def generate_fake_round():

    # ======================================================
    # SIMULA TEMPO ENTRE RODADAS
    # ======================================================

    time.sleep(2)

    # ======================================================
    # GERA MULTIPLICADOR
    # ======================================================

    # A maioria será baixa.
    # Alguns médios.
    # Pouquíssimos extremos.

    chance = random.random()

    if chance < 0.70:
        multiplier = round(random.uniform(1.00, 2.00), 2)

    elif chance < 0.95:
        multiplier = round(random.uniform(2.00, 10.00), 2)

    elif chance < 0.995:
        multiplier = round(random.uniform(10.00, 100.00), 2)

    else:
        multiplier = round(random.uniform(100.00, 1000.00), 2)

    # ======================================================
    # RETORNO DA RODADA
    # ======================================================

    return {
        "multiplier": multiplier,
        "players": random.randint(100, 500),
        "bet_volume": round(random.uniform(1000, 100000), 2)
    }