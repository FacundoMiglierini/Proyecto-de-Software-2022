from src.core.config.models import Config
from src.core.database import db

def load_configuration(**kwargs):
    config = Config(**kwargs)
    db.session.add(config)
    db.session.commit()

def get_configuration():
    """Retorna la configuracion actual de la página"""
    return db.session.query(Config).get(1)

def update_configuration(new_config):
    """Actualiza la configuracion en la bd"""
    db.session.add(new_config)
    db.session.commit()

def get_contact():
    contact = {"email": (Config.query.order_by(Config.email).first()).email,
                "phone": (Config.query.order_by(Config.phone).first()).phone}

    return contact

def ELEM_PER_PAGE():
    return (Config.query.order_by(Config.cant_elem).first()).cant_elem

def get_criterio():
    return (Config.query.order_by(Config.criterio).first()).criterio