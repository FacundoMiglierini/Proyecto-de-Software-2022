from src.core.auth import load_socio
from src.core.auth import get_socio
from src.core.auth import update_socio
from src.core.auth import get_socio_id
from src.core.auth import delete_socio

def test_new_socio(context):
    """
    Dado un modelo de socio, 
    Cuando un socio es creado, 
    Entonces se verifica que el nombre, apellido y teléfono sean definidos correctamente
    """

    socio = load_socio(
       tipo_identificacion="DNI",
       identificacion="20000000",
       genero="Masculino",
       telefono="",
       email="sociot@gmail.com",
       nombre="Juan",
       apellido="Perez",
       domicilio="7 y 50",
    )

    assert socio.nombre == "Juan"
    assert socio.apellido == "Perez"
    assert socio.telefono == ""


def test_existing_socio(context):
    """
    Dado el id de un socio, 
    Cuando se busca dicho id en la base de datos, 
    Entonces se verifica que el domicilio y el nombre de socio obtenidos correspondan con el mismo
    """

    socio = get_socio("20000000")

    assert socio.domicilio == "7 y 50"
    assert socio.nombre == "Juan"

def test_none_existing_socio(context):
    """
    Dado el id de un socio,
    Cuando se busca dicho id en la base de datos, 
    Entonces se verifica que el usuario obtenido sea None
    """

    socio = get_socio_id(9999999)

    assert socio == None

def test_updating_socio(context):
    """
    Dado un socio existente, 
    Cuando se modifican sus atributos,
    Entonces se verifica que el socio se encuentre con sus datos modificados
    """

    socio = get_socio("20000000")

    socio.identificacion = "20000001"
    socio.domicilio = "8 y 50"
    socio.email = "sociotest@gmail.com"

    update_socio(socio)

    socio = get_socio("20000001")

    assert socio.identificacion == "20000001"
    assert socio.email == "sociotest@gmail.com"
    assert socio.domicilio == "8 y 50"

def test_delete_socio(context):
    """
    Dado un socio existente,
    Cuando se elimina dicho socio
    Entonces se verifica que no exista en la base de datos
    """

    # verifico existencia de socio
    socio = get_socio("40000099")
    assert socio != None

    # delete
    delete_socio(socio.id)

    # verifico que haya sido eliminado correctamente
    socio = get_socio("40000099")
    assert socio == None