from datetime import datetime
from src.core.database import db

socio_disciplina = db.Table('socio_disciplina',
    db.Column('id_socio',db.ForeignKey('Socios.id'), primary_key=True), 
    db.Column('id_disciplina', db.ForeignKey('Disciplina.id',ondelete='CASCADE'), primary_key=True)
)

usuario_roles = db.Table('usuario_roles',
    db.Column('role_id', db.ForeignKey('Roles.id'), primary_key=True),
    db.Column('user_id', db.ForeignKey('Usuarios.id', ondelete='CASCADE'), primary_key=True))

class User(db.Model):

    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nombre = db.Column(db.String(36), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    estado = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=usuario_roles, lazy='subquery', back_populates="users")


class Socio(db.Model):

    __tablename__ = "Socios"
    id = db.Column(db.Integer, primary_key=True) #Número de socio
    username = db.Column(db.String(256), unique=True, nullable=True)
    password = db.Column(db.String(256), nullable=True)
    tipo_identificacion = db.Column(db.String(50), nullable=False)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    nombre = db.Column(db.String(36), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    estado_act_block = db.Column(db.Boolean(), default=True)
    genero = db.Column(db.String(15), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    domicilio = db.Column(db.String(255), nullable=False)
    fecha_alta = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    disciplinas = db.relationship('Disciplina', secondary=socio_disciplina)
    cuotas = db.relationship('Cuota', backref='socio', lazy=True, cascade="all, delete")
    #carnet = db.relationship('Carnet', backref='socio', uselist=False)
    image = db.relationship('Image', backref='socio', uselist=False)