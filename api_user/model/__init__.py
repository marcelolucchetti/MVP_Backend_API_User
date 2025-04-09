from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.base import Base
from model.user import User
import os

# Definição da URL única do banco de dados
db_url = 'sqlite:///database.db'

# Criando a engine
engine = create_engine(db_url, echo=False)

# Criando a sessão
Session = sessionmaker(bind=engine)

# Criando o banco de dados caso não exista
if not database_exists(engine.url):
    create_database(engine.url)

# Criando as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
