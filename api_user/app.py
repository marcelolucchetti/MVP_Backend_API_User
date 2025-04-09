# Importações de bibliotecas externas
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from flask_cors import CORS
from urllib.parse import unquote
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Bibliotecas padrão do Python
import sys
import os

# Adiciona o diretório pai (MVP Plano de Controle Financeiro) ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações internas do projeto
from sqlalchemy.exc import IntegrityError
from model import Session
from model.user import User
from logger import logger
from model.user import *
from werkzeug.security import generate_password_hash, check_password_hash


# Configurações iniciais da API
info = Info(title="API User", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"
jwt = JWTManager(app)


# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
auth_tag = Tag(name="Autenticação", description="Rotas de autenticação de usuários")
plano_tag = Tag(name="Plano", description="Adição, visualização e remoção de planos à base")

# Rota: Registro de usuários
@app.route('/register', methods=['POST'])
def register():
    """Realiza o cadastro de um novo usuário na base de dados.
        Espera um JSON com os campos: 'username' e 'password'.
        Retorna mensagem de sucesso ou erro."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Usuário e senha são obrigatórios"}), 400

    hashed_password = generate_password_hash(password)

    try:
        session = SessionLocal()
        novo_usuario = User(username=username, password=hashed_password)
        session.add(novo_usuario)
        session.commit()
        session.close()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Nome de usuário já existe!"}), 400
    except Exception as e:
        return jsonify({"message": "Erro no servidor: " + str(e)}), 500


# Rota: Login de usuário
@app.post('/login', tags=[auth_tag])
def login():
    """Realiza login do usuário.
        Espera um JSON com 'username' e 'password'.
        Se as credenciais forem válidas, retorna um token JWT."""
    data = request.get_json()
    session = Session()
    
    user = session.query(User).filter_by(username=data["username"]).first()
    session.close()
    
    if not user or not check_password_hash(user.password, data["password"]):
        return {"message": "Credenciais inválidas"}, 401

    access_token = create_access_token(identity=user.username)
    return {"access_token": access_token}, 200


# Rota: Listagem de Planos
@app.get('/planos', tags=[plano_tag])
@jwt_required() 
def get_planos():
    """Faz a busca por todos os Planos cadastrados. 
       Retorna uma representação da listagem de planos."""
    current_user = get_jwt_identity() 
    logger.debug(f"Usuário {current_user} acessando planos")
    
    session = Session()
    planos = session.query(Plano).all()
    session.close()

    return apresenta_planos(planos), 200

# Rota: Página Inicial (Documentação)
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')