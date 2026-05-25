# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

# Aqui configuramos:
# - engine;
# - sessão;
# - conexão.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

# ==========================================================
# ENGINE PRINCIPAL
# ==========================================================

engine = create_engine(DATABASE_URL)

# ==========================================================
# SESSÃO
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)