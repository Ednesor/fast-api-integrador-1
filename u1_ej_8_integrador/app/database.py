from sqlmodel import create_engine, SQLModel, Session
from fastapi import FastAPI

DATABASE_URL = "postgresql://fastapi_user:fastapi_pass@127.0.0.1:5433/fastapi_db"

engine = create_engine(
  DATABASE_URL,
  echo=True, #SQL invisible en consola(obligatorio en dev)
)

def create_db():
  SQLModel.metadata.create_all(engine)

def get_session():
  with Session(engine) as session:
    yield session