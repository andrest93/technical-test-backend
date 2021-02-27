from bottle import run, route, request, HTTPResponse
from models import Note, User
from schemas import note_schema, user_schema
from utils.auth import authenticate
from utils.exceptions import MissingField
from utils.jwt import JwtHelper
from helpers.commons import *

jwt_helper = JwtHelper()

@route('/notes', method=['GET', 'OPTIONS'])
@enable_cors
@authenticate
def get_notes():
    user_session = get_user_session()
    notes_query = Note.select().where(
        Note.user == user_session).order_by(Note.created_at.desc())
    notes_data = note_schema.dump(notes_query, many=True)
    return {'data': notes_data.data}

@route('/notes', method=['POST', 'OPTIONS'])
@enable_cors
@authenticate
def save_note():
    try:
        validate_post_data(request.json)
    except MissingField as error:
        return HTTPResponse({'code': 400, 'name': 'MISSING_VALUES', 'message': str(error)}, 401)

    text_note = request.json['text']
    user_session = get_user_session()
    note = Note.create(text=text_note, user=user_session)
    note.save()

    note_data = note_schema.dump(note)
    return note_data.data

@route('/notes/<id>', method=['DELETE', 'OPTIONS'])
@enable_cors
@authenticate
def delete_note(id):
    try:
        note_query = Note.get(Note.id == id)
        note_query.delete_instance()
        return {'id': id, 'deleted': True}
    except:
        return {'id': id, 'deleted': False}
   
@route('/users', method=['POST', 'OPTIONS'])
@enable_cors
def save_user():
    try:
        validate_login(request.json)
    except MissingField as error:
        return HTTPResponse({'code': 400, 'name': 'MISSING_VALUES', 'message': str(error)}, 401)

    user = request.json['user']
    password = request.json['password']

    try:
        user = User.create(user=user, password=password)
        user.save()
    except Exception as error:
        return HTTPResponse({'code': 400, 'name': 'GENERAL_ERROR', 'message': 'User already exist'}, 400)

    user_data = user_schema.dump(user)
    return user_data.data

@route('/authentication', method=['POST', 'OPTIONS'])
@enable_cors
def login():
    try:
        validate_login(request.json)
    except MissingField as error:
        return HTTPResponse({'code': 400, 'name': 'MISSING_VALUES', 'message': str(error)}, 401)

    user = request.json['user']
    password = request.json['password']
    try:
        user_query = User.get(User.user == user, User.password == password)
    except:
        return HTTPResponse({'code': 401, 'name': 'NOT_AUTHENTICATED', 'message': 'Invalid login'}, 401)

    user_id = user_query.get_id()
    payload = {'user': user_id}
    token = jwt_helper.encode(payload)
    response.headers['Content-Type'] = 'application/json'
    return {'token': token}


run(reloader=False, host='localhost', port=8000)
