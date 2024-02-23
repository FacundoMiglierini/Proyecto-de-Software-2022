from src.core.database import ma
from src.core.image import Image

class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Image
    
    data = ma.auto_field()