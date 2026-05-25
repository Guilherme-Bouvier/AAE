# ==========================================================
# CRIADOR DO BANCO DE DADOS
# ==========================================================

# Este arquivo será executado apenas UMA vez.
#
# Objetivo:
# criar automaticamente:
#
# - banco SQLite;
# - tabelas;
# - estrutura inicial.
#
# O SQLAlchemy lerá os modelos definidos
# em database/models.py
#
# e converterá tudo em tabelas reais.

# ==========================================================
# IMPORTA ENGINE
# ==========================================================

# engine = conexão principal com banco

from database.connection import engine

# ==========================================================
# IMPORTA BASE DOS MODELOS
# ==========================================================

# Base contém todas as tabelas registradas

from database.models import Base

# ==========================================================
# CRIA TODAS AS TABELAS
# ==========================================================

Base.metadata.create_all(bind=engine)

# ==========================================================
# MENSAGEM FINAL
# ==========================================================

print("=" * 50)
print("BANCO CRIADO COM SUCESSO")
print("=" * 50)