from src.core.business import delete_disciplina
from src.core.business import disciplina_exists
from src.core.business import load_disciplina
from src.core.business import get_disciplina

def test_new_discipline(context):
    """
    Dado un modelo de disciplina, 
    Cuando una disciplina es creada,
    Entonces se verifica que el nombre sea definido correctamente
    """

    discipline = load_disciplina(
        habilitada = True,
        detalle = "detalle_test",
        nombre_disciplina = "TEST",
        costo = 3000.5
    )
    
    assert discipline.nombre_disciplina == "TEST"

def test_existing_discipline(context):
    """
    Dado el nombre de una disciplina,
    Cuando se busca dicho nombre en la base de datos, 
    Entonces se verifica que la disciplina obtenida coincida con la adecuada
    """
    
    discipline = get_disciplina("TEST")

    assert discipline.detalle == "detalle_test"


def test_none_existing_discipline(context):
    """
    Dado el nombre de una disciplina, 
    Cuando se consulta si dicho nombre corresponde a una disciplina,
    Entonces se retorna True o False de acuerdo al resultado obtenido
    """

    assert disciplina_exists("TEST inexistente") == False


def test_delete_discipline(context):
    """
    Dada una disciplina,
    Cuando se elimina una disciplina,
    Entonces se verifica que la misma no se encuentre almacenada en la BD
    """

    discipline = get_disciplina("TEST")
    delete_disciplina(discipline)

    discipline = get_disciplina("TEST")
    assert discipline == None