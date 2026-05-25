import sqlite3

conn = sqlite3.connect("data/rounds.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM rounds")

resultado = cursor.fetchone()

print(resultado)