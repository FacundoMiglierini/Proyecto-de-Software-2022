from src.core.database import db
from datetime import datetime

disciplina_instructor = db.Table('disciplina_instructor',
    db.Column('id_disciplina',db.ForeignKey('Disciplina.id'),primary_key=True), 
    db.Column('id_instructor', db.ForeignKey('Instructor.id'), primary_key=True)
)

disciplina_categoria = db.Table('disciplina_categoria', 
    db.Column('id_categoria', db.ForeignKey('Categoria.id'), primary_key=True),
    db.Column('id_disciplina', db.ForeignKey('Disciplina.id'), primary_key=True))

class Disciplina(db.Model):
    __tablename__ = "Disciplina"
    id = db.Column(db.Integer, primary_key=True)
    nombre_disciplina = db.Column(db.String(50), unique=True, nullable=False) 
    habilitada =  db.Column(db.Boolean, default = True, nullable = False)
    detalle = db.Column(db.String(256), nullable = False)
    costo = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False)
    instructores = db.relationship('Instructor', secondary=disciplina_instructor,lazy='subquery')
    categorias = db.relationship('Categoria', secondary=disciplina_categoria,lazy='subquery')

class Instructor(db.Model):
    __tablename__ = "Instructor"
    id = db.Column(db.Integer, primary_key=True)
    nombre_instructor = db.Column(db.String(30), nullable=False)
    apellido_instructor = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False)

class Categoria(db.Model):
    __tablename__ = "Categoria"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(128), unique=True,nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False)