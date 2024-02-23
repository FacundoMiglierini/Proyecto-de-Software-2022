from src.core.config.models import Config
from src.core.database import ma

class ContactoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Config
        
    email = ma.auto_field()
    phone = ma.auto_field()