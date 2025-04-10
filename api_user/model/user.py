from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from model.base import Base, engine  # Base já foi definida corretamente

# Criando a sessão corretamente
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
