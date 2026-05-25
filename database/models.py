# ==========================================================
# MODELOS DO BANCO
# ==========================================================

# Aqui definimos as tabelas.

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

# ==========================================================
# BASE PRINCIPAL
# ==========================================================

Base = declarative_base()

# ==========================================================
# TABELA DE RODADAS
# ==========================================================

class Round(Base):

    __tablename__ = "rounds"

    # ID interno
    id = Column(Integer, primary_key=True)

    # Multiplicador
    multiplier = Column(Float)

    # Quantidade de jogadores
    players = Column(Integer)

    # Volume apostado
    bet_volume = Column(Float)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)