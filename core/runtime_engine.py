import threading
import time
import sqlite3
import random
from datetime import datetime


DB_PATH = "data/rounds.db"


# ==================================================
# GERADOR DE DADOS SIMULADOS
# ==================================================

def generate_multiplier():

    r = random.random()

    if r < 0.70:
        return round(random.uniform(1.0, 3.0), 2)

    elif r < 0.95:
        return round(random.uniform(3.0, 15.0), 2)

    else:
        return round(random.uniform(15.0, 100.0), 2)


# ==================================================
# SALVAR NO BANCO
# ==================================================

def save_round(multiplier):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rounds (
        multiplier,
        volatility,
        low_streak,
        distribution,
        score,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        multiplier,
        0.0,
        0,
        "AUTO",
        0.0,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# ==================================================
# LOOP PRINCIPAL (IA VIVA)
# ==================================================

def run_loop():

    print("🧠 IA em tempo real iniciada...")

    while True:

        multiplier = generate_multiplier()
        save_round(multiplier)

        print(f"[REALTIME] Novo valor gerado: {multiplier}x")

        time.sleep(1)


# ==================================================
# START EM THREAD
# ==================================================

def start_runtime():

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()

    return thread