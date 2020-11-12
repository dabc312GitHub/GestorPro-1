from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db= SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__= "Usuarios"
    id= db.Column(db.Integer, primary_key=True)
    usuario=db.Column(db.String(25),unique=True, nullable=False)
    contraseña=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(120),unique=True)
