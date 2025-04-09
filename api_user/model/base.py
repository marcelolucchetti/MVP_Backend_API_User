from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


# Define a URL de conexão com o banco de dados SQLite
DATABASE_URL = "sqlite:///database.db" 

# Cria o motor (engine) de conexão com o banco
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma classe Base para o instanciamento de novos obetos/tabelas
Base = declarative_base()