from src.core.database import ma
from src.core.fees import Cuota

class CuotaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cuota

    id = ma.auto_field()
    monto = ma.auto_field()
    estado = ma.auto_field()
    created_at = ma.DateTime(format='%m-%Y')
    