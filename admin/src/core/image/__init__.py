from src.core.image.models import Image
from src.core.database import db


def load_image(**kwargs):
    image = Image(**kwargs)
    db.session.add(image)
    db.session.commit()

    return image

def get_image(id):
    '''Retorna una imagen con el id recibido por parametro'''
    
    return Image.query.get(id)