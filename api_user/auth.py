# Importações de bibliotecas
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta


# CONFIGURAÇÃO DO APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = "sua_chave_secreta"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)


# Inicializa extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


# DEFINIÇÃO DO MODELO USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# ROTA DE REGISTRO DE USUÁRIO
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Usuário já existe'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

# ROTA DE LOGIN DE USUÁRIO
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Credenciais inválidas'}), 401

# ROTA PROTEGIDA COM JWT
@app.route('/plano', methods=['GET'])
@jwt_required()
def get_plano():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    return jsonify({'message': 'Bem-vindo ao plano financeiro!', 'username': user.username})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
