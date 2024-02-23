from datetime import datetime

from src.core.database import db

class Cuota(db.Model):

    __tablename__ = "Cuotas"
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, default=0)
    estado = db.Column(db.String(9), nullable=False, default="Impaga")
    fecha_pago = db.Column(db.DateTime, nullable=True)
    detalle = db.Column(db.String, nullable=False)
    comprobante = db.Column(db.String, nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    socio_id = db.Column(db.Integer, db.ForeignKey("Socios.id"), nullable=False)

