from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '67049ce9faacc9f10c352d4bfb70cdbb'  # utilizei o secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db?charset=utf8'

database = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from sitecomunidade import routes
