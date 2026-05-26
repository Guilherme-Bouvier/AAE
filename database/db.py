from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:senha@localhost:5432/aae"

engine = create_engine(DATABASE_URL)