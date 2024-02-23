from src.core.database import db

class Image(db.Model):

    __tablename__ = "Image"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(6))
    socio_id = db.Column(db.Integer, db.ForeignKey("Socios.id"))