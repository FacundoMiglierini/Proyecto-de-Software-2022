from src.core.auth import load_user
from src.core.auth import get_user_id
from src.core.auth import get_user_by_username
from src.core.auth import update_user
from src.core.auth import delete_user
import hashlib


def test_new_user(context):
    """
    Dado un modelo de usuario,
    Cuando un usuario es creado,
    Entonces se verifica que el username y la password hasheada sean definidas correctamente
    """

    user = load_user(
        password="1234",
        username="TEST",
        nombre="User",
        email= "user@test.com",
        apellido="Test"
    )

    assert user.username == "TEST"
    assert user.password != "1234"
    assert user.password == hashlib.sha256("1234".encode()).hexdigest() 


def test_existing_user(context):
    """
    Dado el id de un usuario,
    Cuando se busca dicho id en la base de datos,
    Entonces se verifica que el username y el mail obtenidos coincidan con los adecuados
    """

    user = get_user_by_username("TEST")

    assert user.apellido == "Test"
    assert user.email == "user@test.com"

def test_none_existing_user(context):
    """
    Dado el id de un usuario no creado,
    Cuando se busca dicho id en la base de datos,
    Entonces se verifica que el usuario obtenido sea None
    """

    user = get_user_id(99999)

    assert user == None

def test_updating_user(context):
    """
    Dado un usuario existente,
    Cuando se modifica el nombre y el estado
    Entonces se verifica que los nuevos datos sean definidos correctamente
    """

    # verifico el nombre y estado actual de user
    user = get_user_by_username("user3")
    assert user.nombre == "User"
    assert user.estado == True

    # update
    user.nombre = "test"
    user.estado = False
    update_user(user)
    
    # obtengo usuario y verifico que se hayan guardado las modificaciones
    user = get_user_by_username("user3")
    assert user.nombre == "test"
    assert user.estado == False

def test_delete_user(context):
    """
    Dado un usuario existente,
    Cuando se elimina dicho usuario
    Entonces se verifica que no exista en la base de datos
    """

    # verifico existencia de usuario
    user = get_user_by_username("user4")
    assert user != None

    # delete
    delete_user(user.id)

    # verifico que haya sido eliminado correctamente
    user = get_user_by_username("user4")
    assert user == None