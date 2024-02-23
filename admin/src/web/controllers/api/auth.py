from flask import request
from flask import jsonify
from flask import Blueprint
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity, create_access_token, set_access_cookies #, create_refresh_token, set_refresh_cookies
from src.core.image.schemas import ImageSchema 
from src.core import auth
from src.core.auth.schemas import SocioSchema
from src.core.image import get_image

api_auth_blueprint = Blueprint("api_auth", __name__, url_prefix="/api/")

@api_auth_blueprint.post('/auth')
def login_jwt():
    data = request.get_json()
    username = data['username']
    password = data['password']
    socio = auth.find_socio_by_username_and_pass(username, password)
    
    if not socio:
        return jsonify(message="Unauthorized"), 401
    
    access_token = create_access_token(identity=socio.id)
    response = jsonify()
    set_access_cookies(response, access_token)
    return response, 201

@api_auth_blueprint.get('/auth/logout_jwt')
@jwt_required()
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200

@api_auth_blueprint.get('/auth/user_jwt')
@jwt_required()
def user_jwt():
    current_user = get_jwt_identity()
    user = auth.get_socio_id(current_user)
    user_dump = SocioSchema().dump(user)

    if user.image is not None:
        image = get_image(user.image.id)
        user_dump['image'] = ImageSchema().dump(image)
    else:
        user_dump['image'] = None
        
    return user_dump, 200