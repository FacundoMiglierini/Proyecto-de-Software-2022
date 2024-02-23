from src.core.config import get_configuration
from src.core.config import update_configuration


def test_get_settings(context):
    """
    Dada una configuración, 
    Cuando se desea obtener sus parámetros,
    Entonces se verifica que se obtengan correctamente
    """

    settings = get_configuration()
    
    assert settings.criterio in ["asc", "desc"]
    assert settings.id == 1
    assert "@" in settings.email 

def test_update_settings(context):
    """
    Dada una configuración,
    Cuando se modifica dicha configuración,
    Entonces se verifica que los cambios fueron efectuados exitosamente
    """
    
    settings = get_configuration()
    settings.criterio = "desc"
    settings.email = "test@gmail.com"
    settings.recibo_txt = "Proyecto de Software"

    update_configuration(settings)

    settings = get_configuration()
    
    assert settings.criterio == "desc"
    assert settings.email == "test@gmail.com"
    assert settings.recibo_txt == "Proyecto de Software"
