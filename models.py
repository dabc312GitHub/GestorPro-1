from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,redirect,url_for,flash, request
from flask_login import UserMixin
from datetime import datetime
app=Flask(__name__)
app.secret_key='replace_later'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://rafxar:password@localhost/gestor'
db= SQLAlchemy(app)

gestion_e =db.Table('gestion_e',
                    db.Column('id_usuario', db.Integer, db.ForeignKey('Usuarios.id'), primary_key=True),
                    db.Column('id_evento', db.Integer, db.ForeignKey('Evento.id_evento'),primary_key=True))
tiene_m=db.Table('tiene_m',
                db.Column('id_evento',db.Integer,db.ForeignKey('Evento.id_evento'),primary_key=True),
                db.Column('id_material',db.Integer,db.ForeignKey('Material.id_material'),primary_key=True))
class User(UserMixin, db.Model):
    __tablename__= "Usuarios"
    id= db.Column(db.Integer, primary_key=True)
    usuario=db.Column(db.String(25),unique=True, nullable=False)
    contraseña=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(120),unique=True)
    eventos=db.relationship('Evento',secondary=gestion_e, backref=db.backref('Usuarios_r'), lazy='dynamic')

class Evento(db.Model):
    __tablename__= "Evento"
    id_evento= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    fecha_inicial=db.Column(db.DateTime,nullable=False)
    fecha_final=db.Column(db.DateTime,nullable=False)
    ubicacion=db.Column(db.String(100),nullable=False)
    descripcion=db.Column(db.String(280),nullable=False)

class Material(db.Model):
    __tablename__="Material"
    id_material=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    stock=db.Column(db.Integer)
    descripcion=db.Column(db.String(280),nullable=False)