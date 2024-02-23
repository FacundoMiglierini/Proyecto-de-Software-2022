from src.core.database import db
from src.core.auth.models import usuario_roles

rol_permisos = db.Table('rol_permisos',
    db.Column('permiso_id', db.Integer, db.ForeignKey('Permissions.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('Roles.id'), primary_key=True))

class Role(db.Model):

    __tablename__ = "Roles"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(), unique=True, nullable=False)
    users = db.relationship('User', secondary=usuario_roles, lazy='subquery', back_populates="roles")
    permisos = db.relationship('Permission', secondary=rol_permisos, lazy='subquery', backref=db.backref('Roles', lazy=True))

class Permission(db.Model):

    __tablename__ = "Permissions"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(), unique=True, nullable=False)
    