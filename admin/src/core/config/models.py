from src.core.database import db

class Config(db.Model):
    __tablename__ = 'Configuracion'
    id = db.Column(db.Integer, primary_key=True)
    cant_elem = db.Column(db.Integer(), nullable=False, default=10)
    criterio = db.Column(db.String(4), nullable=False, default="asc")
    pagos = db.Column(db.String(12), nullable=False)
    cant_pagos_permitidos = db.Column(db.Integer(), nullable=False, default=3)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    recibo_txt = db.Column(db.String(256), nullable=True, default="")
    cuota_base = db.Column(db.Float, nullable=False)
    recargo = db.Column(db.Float, nullable=False, default=0)
