from utils.exceptions import MissingField
from utils.auth import get_access_token
from utils.jwt import JwtHelper
from models import User
from bottle import response, request

jwt_helper = JwtHelper()


def validate_login(login_data):
    if 'user' not in login_data:
        raise MissingField('user data is missing')
    if 'password' not in login_data:
        raise MissingField('password data is missing')


def validate_post_data(post_data):
    if 'text' not in post_data:
        raise MissingField('text data is missing')


def get_jwt_payload():
    access_token = get_access_token()
    payload = jwt_helper.decode(access_token)
    return payload


def get_user_session():
    payload = get_jwt_payload()
    user = User.get(User.id == payload['user'])
    return user


def enable_cors(fn):
    def wrapper(*args, **kwargs):
        response.set_header('Access-Control-Allow-Origin','*')
        response.set_header('Access-Control-Allow-Methods','GET, POST, PUT, DELETE, OPTIONS')
        response.set_header('Access-Control-Allow-Headers','Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization')
        
        if request.method == 'OPTIONS':
            return
        return fn(*args, **kwargs)

    return wrapper
