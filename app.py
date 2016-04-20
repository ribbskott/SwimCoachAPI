__author__ = 'dmczk'
#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth
from models import Club, User, Session, Profile
from database import db_session

from session_manager import SessionManager
from sloach_object_provider import SloachObjectProvider
from sqlalchemy import or_
import datetime
import json


auth = HTTPBasicAuth()
app = Flask(__name__)


def check_auth(request):
    if request.headers.get('sessiontoken') is None:
        return False
    sessiontoken = request.headers.get('sessiontoken')
    session = SessionManager.get_session(sessiontoken)
    if sessiontoken is None:
        return False

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# CLUB BEGIN

@app.route('/clubs', methods=['GET'])
def get_clubs():
    if not check_auth(request):
        abort(401)
    results = Club.query.all()
    json_results = []
    for result in results:
      d = {'idclub': result.idclub,
           'name': result.name,
           'description': result.description}
      json_results.append(d)

    return jsonify({'clubs': json_results})

@app.route('/clubs/<int:idclub>', methods=['GET'])
def get_club(idclub):
    if not check_auth(request):
        abort(401)
    club = db_session.query(Club).filter_by(idclub=idclub)
    if len(list(club)) == 0:
        abort(404)
    return jsonify({'idclub': club[0].idclub, 'name': club[0].name, 'description': club[0].description})

@app.route('/signup', methods=['POST'])
def signup_user():

    userhash = str(request.headers.get("authorization"))

    if not userhash == "None":
        userhash = userhash.replace("Basic ", "")
        jsondata = json.dumps(request.json)

        session = SessionManager.create_user(jsondata, userhash)

        if session:
            profile = SloachObjectProvider.create_profile(session.iduser, {"firstname": "", "lastname": "", "address": "", "email": json.loads(jsondata)['email']})
            return jsonify({'iduser': session.iduser, 'token': str(session.sessiontoken), 'profile': {"firstname": profile.firstname, "lastname": profile.lastname, "email": profile.email}})
    return make_response("Username already exists", 400)

@app.route('/login', methods=['POST', 'GET'])
def login_user():
    hash = str(request.headers.get("authorization"))

    if not hash == 'None':
        hash = str.replace(hash, "Basic ", "")
        session = SessionManager.create_session(hash)
        if session is None:
            return make_response("User not found or password is invalid", 404)
        profile = SloachObjectProvider.get_profile(session.iduser)
        if profile is None:
            return make_response("Couldn't find your profile", 500)
        loginResult = {'iduser': session.iduser, 'token': str(session.sessiontoken), 'profile': {"firstname": profile.firstname, "lastname": profile.lastname, "email": profile.email}}

        return jsonify(loginResult)
    return make_response("",401)

@app.route('/logout', methods=['POST','GET'])
def logout_user():
    if not request.json or not 'token' in request.json:
        abort(400)
    sessionid = request.json['token']
    session = db_session.query(Session).filter_by(sessiontoken=sessionid, active=1, logouttime=None)
    if len(list(session)) == 0:
        abort(200)
    session[0].logouttime = datetime.datetime.now()
    session[0].active = 0
    db_session.commit()

    return make_response("",200)

@app.route('/clubs', methods=['POST'])
def create_club():
    if not check_auth(request):
        abort(401)
    idclub = "0"
    name = ""
    description = ""
    if not request.json or not 'name' in request.json:
        abort(400)
    if not request.json or not 'description' in request.json:
        abort(400)
    if 'idclub' in request.json:
        idclub = request.json['idclub']
    if 'name' in request.json:
        name = request.json['name']
    if 'description' in request.json:
        description = request.json['description']
    club = Club(name=name, description=description)
    if str(idclub) != "0":
        db_session.query(Club).filter_by(idclub=int(idclub)).update({"name": name, "description": description})
        db_session.commit()
    else:
        db_session.add(club)
        db_session.commit()

    return jsonify({"status": "OK"})

@app.route('/clubs/<int:idclub>', methods=['PUT'])
def update_club(idclub):
    if not check_auth(request):
        abort(401)
    club = db_session.query(Club).filter_by(idclub=idclub)
    if len(list(club)) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    club[0]['name'] = request.json.get('name', club[0]['name'])
    club[0]['description'] = request.json.get('description', club[0]['description'])

    return jsonify({'club': club[0]})

@app.route('/users/<int:iduser>/profile', methods=['GET', 'POST'])
def get_profile(iduser, profile):
    if not check_auth(request):
        abort(401)
    if request.method == 'GET':
        retProfile = db_session.query(Profile).filter_by(user=iduser)
    if request.method == 'POST':
        retProfile = SloachObjectProvider.create_profile(iduser, profile)
    else:
        return make_response("Only POST and GET calls are allowed")

    if not retProfile:
        return make_response("No profile found", 404)
    else:
        return make_response(retProfile,200)

# USER BEGIN
# USER END


# AUTH

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@auth.verify_password
def verify_password(username, password):
    user = db_session.query(User).filter_by(username=username).first()

    if not user:
        return False

    user.set_password(password)

    return user.check_password(password)

@app.route('/session', methods=['GET'])
def get_userSession():
    hash = request.headers.get('authorization')
    str.replace(hash, "Basic", "")


    return make_response("hej")


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or username == "":
    #    # missing arguments
        abort(400, {'message': 'Username is required'})
    if password is None or password == "":
        abort(400, {'message': 'Password is required'})
    if email is None or email == "":
    #    # missing arguments
        abort(400, {'message': 'Email is required'})
    if db_session.query(User).filter_by(username=username).first() is not None:
        # existing user
        # print("User exists already!!!")
        abort(400, {'message': 'User already exists'})
    user = User(username=username, email=email)
    user.set_password(password)

    db_session.add(user)
    db_session.commit()

    return jsonify({'username': user.username}), 201

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#@app.errorhandler(400)
#def custom400(error):
#    return make_response(jsonify({'message': error.description['message']}), 400)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)

