from src.core.auth.models import Socio
from src.core.database import ma


class SocioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Socio
    
    id = ma.auto_field()
    tipo_identificacion = ma.auto_field()
    identificacion = ma.auto_field()
    nombre = ma.auto_field()
    apellido = ma.auto_field()
    fecha_alta = ma.DateTime(format='%d-%m-%Y')
    estado_act_block = ma.auto_field()


