from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = '67049ce9faacc9f10c352d4bfb70cdbb'  # utilizei o secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db?charset=utf8'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.login_message = 'COLOCA A MENSAGEM AQUI'
login_manager.login_message_category = 'alert-info'

from sitecomunidade import routes
