from re import split
from bottle import request, HTTPResponse
from utils.jwt import JwtHelper
from utils.exceptions import AuthorizationError
import jwt

BEARER_PREFIX = 'bearer'
AUTHORIZATION_HEADER_SIZE = 2


def get_access_token():
    param_authorization = request.headers.get('Authorization', None)

    if not param_authorization:
        raise AuthorizationError('Authorization header is missing')

    splitted_authorization = param_authorization.split(' ')

    if splitted_authorization[0].lower() != BEARER_PREFIX:
        raise AuthorizationError('Authorization header has invalid value')

    if len(splitted_authorization) != AUTHORIZATION_HEADER_SIZE:
        raise AuthorizationError('Token is not found')

    return splitted_authorization[1]


def authenticate(function):
    def wrapper(*args, **kwargs):
        try:
            access_token = get_access_token()
        except AuthorizationError as error:
            return HTTPResponse({'code': 401, 'name': 'NOT_AUTHENTICATED', 'message': str(error)}, 401)
        
        jwt_helper = JwtHelper()

        try:
            jwt_helper.decode(access_token)
        except jwt.ExpiredSignature:
            return HTTPResponse({'code': 401, 'name': 'NOT_AUTHENTICATED', 'message': 'Token is expired'}, 401)
        except jwt.DecodeError:
            return HTTPResponse({'code': 401, 'name': 'NOT_AUTHENTICATED', 'message': 'Invalid token'}, 401)
        return function(*args, **kwargs)

    return wrapper
