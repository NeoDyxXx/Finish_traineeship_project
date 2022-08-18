import sqlalchemy.sql.expression
from flask_login import UserMixin
from sqlalchemy import ForeignKey

from user_auth.flask_app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255), unique=True)
    otp_code = db.Column(db.String(6))
    is_verify = db.Column(db.Boolean())


class Advertising(db.Model):
    __tablename__ = 'advertising'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    country = db.Column(db.String(32))
    courses = db.Column(db.Boolean(), default=False, server_default=sqlalchemy.sql.expression.false())
    aviasales = db.Column(db.Boolean(), default=False, server_default=sqlalchemy.sql.expression.false())
    visa_places = db.Column(db.Boolean(), default=False, server_default=sqlalchemy.sql.expression.false())