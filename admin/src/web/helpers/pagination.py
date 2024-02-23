from flask import request

def pagination():
    '''Retorna número de página indicada en la URL para la vista de tablas.
    Si la página es un dígito, se accede a dicha página.
    Si la página no es un dígito, se accede a la página 1.'''
    
    page = request.args.get('page')

    if page and page.isdigit():
        return int(page)
    else:
        return 1