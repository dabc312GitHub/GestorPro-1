from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,redirect,url_for,flash, request
from flask_login import UserMixin
from datetime import datetime
app=Flask(__name__)
app.secret_key='replace_later'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://acvkbvhdpkqdfx:cd1254236e14c2916acc8efcabe23abd59c3022f4fe52c3a2c0a12059f197ad4@ec2-54-163-47-62.compute-1.amazonaws.com:5432/de1bc8lmmb3b0s'
db= SQLAlchemy(app)
#TABLAS INTERMEDIARIAS DE LAS RELACIONES DE MUCHOS A MUCHOS
gestion_e =db.Table('gestion_e',
                    db.Column('id_usuario', db.Integer, db.ForeignKey('Usuarios.id'), primary_key=True),
                    db.Column('id_evento', db.Integer, db.ForeignKey('Evento.id_evento'),primary_key=True))
tiene_m=db.Table('tiene_m',
                db.Column('id_evento',db.Integer,db.ForeignKey('Evento.id_evento'),primary_key=True),
                db.Column('id_material',db.Integer,db.ForeignKey('Material.id_material'),primary_key=True))
#CREA LOS MODELOS EN LA BASE DE DATOS Y MANTIENE LAS INTERACCIONES DE:
#ML_01 Y ML_02
class User(UserMixin, db.Model):
    __tablename__= "Usuarios"
    id= db.Column(db.Integer, primary_key=True)
    usuario=db.Column(db.String(25),unique=True, nullable=False)
    contraseña=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(120),unique=True)
    eventos=db.relationship('Evento',secondary=gestion_e, backref=db.backref('Usuarios_r'), lazy='dynamic')
    #id_rol = db.Column(db.Integer, db.ForeignKey('Rol.id_rol'),nullable=False)
#CREA LOS MODELOS EN LA BASE DE DATOS Y MANTIENE LAS INTERACCIONES DE:
#MC_01, MC_02, MC_03.MC_04,MC_05
class Evento(db.Model):
    __tablename__= "Evento"
    id_evento= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    fecha_inicial=db.Column(db.DateTime,nullable=False)
    fecha_final=db.Column(db.DateTime,nullable=False)
    ubicacion=db.Column(db.String(100),nullable=False)
    descripcion=db.Column(db.String(280),nullable=False)
#CREA LOS MODELOS EN LA BASE DE DATOS Y MANTIENE LAS INTERACCIONES DE:
#MC_14, MC_15, MC_16.MC_17
class Material(db.Model):
    __tablename__="Material"
    id_material=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    stock=db.Column(db.Integer)
    descripcion=db.Column(db.String(280),nullable=False) 
#CREA LOS MODELOS EN LA BASE DE DATOS Y MANTIENE LAS INTERACCIONES DE:
#MG_04,MG_05
class Rol(db.Model):
    __tablename__="Rol"
    id_rol=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    descripcion=db.Column(db.String(280),nullable=False)
    id_permiso = db.Column(db.Integer, db.ForeignKey('Permiso_Acceso.id_permiso'),nullable=False)


class Permiso_Acceso(db.Model):
    __tablename__="Permiso_Acceso"
    id_permiso=db.Column(db.Integer, primary_key=True)
    modulos=db.Column(db.String(100),nullable=False)
    submodulos=db.Column(db.String(100),nullable=False)