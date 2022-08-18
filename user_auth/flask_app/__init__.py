import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('user_auth.config.DevelopmentConfig')
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
bcrypt = Bcrypt(app)
mail = Mail(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from routes import *