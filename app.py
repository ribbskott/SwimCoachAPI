__author__ = 'dmczk'
#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request, session
from flask.ext.httpauth import HTTPBasicAuth
from models import Club, User, Session, Profile, Athlete, Group, GroupMember,TrainingResult
from database import db_session
from application_cache import ApplicationCache
from session_manager import SessionManager
from sloach_object_provider import SloachObjectProvider
from sqlalchemy import or_
import datetime
import json


auth = HTTPBasicAuth()
application_cache  = ApplicationCache()
application_cache.load_user_cache()
application_cache.load_active_sessions()
app = Flask(__name__)
app.config['SECRET_KEY'] = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(hours=24)

def check_auth(request):
    # TODO fixa sessionshanteringen så att check_auth returnerar en session (med iduser och liknande)

    if request.headers.get('sessiontoken') is None:
        return False

    sessiontoken = request.headers.get('sessiontoken')
    user_session = SessionManager.get_session(sessiontoken)
    if user_session is None:
        return False
    else:
        return True

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
           'description': result.description,
           'postaladdress': result.postaladdress,
           'postalzipcode': result.postalzipcode,
           'postalcity': result.postalcity,
           'visitingaddress': result.visitingaddress,
           'visitingzipcode': result.visitingzipcode,
           'visitingcity': result.visitingcity,
           'rowkey': result.rowkey}
      json_results.append(d)

    return jsonify({'clubs': json_results})

@app.route('/clubs/<string:rowkey>', methods=['POST','GET'])
def get_club(rowkey):
    if not check_auth(request):
        abort(403)
    club = db_session.query(Club).filter_by(rowkey=rowkey).first()
    if club is None:
        abort(404)
    if request.method =='GET':
        return jsonify({'idclub': club.idclub, 'name': club.name, 'description': club.description,
                        'postaladdress': club.postaladdress,
                        'postalzipcode': club.postalzipcode,
                        'postalcity': club.postalcity,
                        'visitingaddress': club.visitingaddress,
                        'visitingzipcode': club.visitingzipcode,
                        'visitingcity': club.visitingcity,
                        'rowkey': club.rowkey})

    if request.method =='POST':
        club.visitingaddress = request.json["visitingaddress"]
        club.visitingzipcode = request.json["visitingzipcode"]
        club.visitingcity = request.json["visitingcity"]
        club.name = request.json["name"]
        club.postaladdress = request.json["postaladdress"]
        club.postalzipcode = request.json["postalzipcode"]
        club.postalcity = request.json["postalcity"]
        db_session.commit()

    return jsonify({'idclub': club.idclub, 'name': club.name, 'description': club.description,
                        'postaladdress': club.postaladdress,
                        'postalzipcode': club.postalzipcode,
                        'postalcity': club.postalcity,
                        'visitingaddress': club.visitingaddress,
                        'visitingzipcode': club.visitingzipcode,
                        'visitingcity': club.visitingcity,
                        'rowkey': club.rowkey})


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
        session = SessionManager.create_session(hash, request.remote_addr)
        if session is None:
            return make_response("User not found or password is invalid", 404)
        profile = SloachObjectProvider.get_profile(session.iduser)
        if profile is None:
            return make_response("Couldn't find your profile", 500)
        loginResult = {'iduser': session.iduser, 'token': str(session.sessiontoken), 'profile': {"firstname": profile.firstname, "lastname": profile.lastname, "email": profile.email, "clubkey": profile.clubkey}}

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

@app.route('/clubs', methods=['PUT'])
def create_club():
    if not check_auth(request):
        abort(403)
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

@app.route('/clubs/<int:idclub>', methods=['POST', 'GET'])
def update_club(idclub):
    if not check_auth(request):
        abort(403)
    if request.method == 'GET':
        club = db_session.query(Club).filter_by(idclub=idclub)
        if len(list(club)) == 0:
            abort(404)
    if request.method == 'POST':
        if not request.json:
            abort(400)

    return jsonify({'club': club[0]})


@app.route('/clubs/<rowkey>/athletes', methods=['GET'])
def get_athletes(rowkey):
    if not check_auth(request):
        abort(403)
    if request.method == 'GET':
        athletes = db_session.query(Athlete).filter_by(club=rowkey)
        if len(list(athletes)) == 0:
            abort(404)
        else:
            retAthletes = []
            for athlete in athletes:
                retAthlete = {'firstname': athlete.firstname, 'lastname': athlete.lastname}
                retAthletes.append(retAthlete)
            return make_response(jsonify({'athletes': retAthletes}))


@app.route('/athletes/<rowkey>/results', methods=['GET'])
def get_results(idathlete):
    if not check_auth(request):
        abort(403)

    results = db_session.query_property(TrainingResult).filter_by(id=idathlete)

@app.route('/athletes/<rowkey>/trainingresults',methods=['GET','POST'])
def get_or_update_trainingresult(rowkey):
    if not check_auth(request):
        abort(403)



@app.route('/users/<int:iduser>/profile', methods=['GET', 'POST'])
def get_profile(iduser):
    if not check_auth(request):
        abort(403)

    retprofile = None

    if request.method == 'GET':
        retprofile = db_session.query(Profile).filter_by(user=iduser)
    if request.method == 'POST':
        # Todo: Check the code below.
        profile = request.get_json()
        retprofile = SloachObjectProvider.create_profile(iduser, profile)

    else:
        return make_response("Only POST and GET calls are allowed")

    if not retprofile:
        return make_response("No profile found", 404)
    else:
        return make_response(jsonify(profile), 200)

# USER BEGIN
# USER END


# AUTH

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


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
    password = request.json.get('password')
    email = request.json.get('email')
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

#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#@app.errorhandler(400)
#def custom400(error):
#    return make_response(jsonify({'message': error.description['message']}), 400)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)

