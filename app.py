__author__ = 'dmczk'
#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request, session, send_from_directory
from flask.ext.httpauth import HTTPBasicAuth

from werkzeug.utils import secure_filename
from models import Club, User, Session, Profile, Athlete, Group, GroupMember,TrainingResult, UserFile, TrainingSession
from database import db_session
from application_cache import ApplicationCache
from session_manager import SessionManager
from sloach_object_provider import SloachObjectProvider

from sqlalchemy import or_
import datetime
import json
import os


auth = HTTPBasicAuth()
application_cache  = ApplicationCache()
application_cache.load_user_cache()
application_cache.load_active_sessions()
app = Flask(__name__)
app.config['SECRET_KEY'] = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

app.config['CLUB_PICTURE_UPLOAD_FOLDER'] = 'static\\Sloach\\userdata\\clubpictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(hours=24)

def check_auth(request):
    if request.headers.get('sessiontoken') is None:
        return False

    sessiontoken = request.headers.get('sessiontoken')
    if sessiontoken in application_cache.session_cache:
        return True
    #Query the database for the user session
    user_session = SessionManager.get_session(sessiontoken)
    if user_session is None:
        application_cache.remove_session_from_cache(sessiontoken)
        return False
    else:
        if application_cache.session_cache[sessiontoken] is None:
            application_cache.session_cache[sessiontoken] = user_session.userid
        return True

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# CLUB BEGIN

@app.route('/clubs', methods=['GET'])
def get_clubs():
    if not check_auth(request):
        abort(403)
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


@app.route('/clubs/<string:rowkey>/groups', methods=['GET'])
def get_groups(rowkey):
    if not check_auth(request):
        abort(403)
    groups = db_session.query(Club).filter_by(rowkey=rowkey).join(Group)
    if len(list(groups)) == 0:
        return jsonify({"groups": []})

    retGroups = {"groups": []}

    if request.method =='GET':
        for group in groups[0].groups:
            retGroups["groups"].append({"id": group.id, "name": group.name, "description": group.description})
    return jsonify(retGroups)



@app.route('/clubs/<string:rowkey>/groups/<int:idgroup>/trainingsessions', methods=['GET'])
def get_sessions_for_group(rowkey,idgroup):
    if not check_auth(request):
        abort(403)
    sessions = db_session.query(TrainingSession).filter_by(group=idgroup)
    retSessions = {"groupSessions": []}
    for training_session in sessions:
        retSessions["groupSessions"].append(training_session.to_json())
        #"group": training_session.group,
         #                                    "name": training_session.name,
         #                                    "fromtime": str(training_session.fromtime.isoformat()),
         #                                     "totime": str(training_session.totime.isoformat()),
         #                                    "id": training_session.id
         #                                    })

    return jsonify(retSessions)

@app.route('/clubs/<string:rowkey>/groups/<int:idgroup>/athletes', methods=['GET'])
def get_athletes_in_group(rowkey, idgroup):
    if not check_auth(request):
        abort(403)
    athletes = db_session.query(Club).filter_by(rowkey=rowkey).join(Group).filter_by(id=idgroup).\
                join(GroupMember).join(Athlete)
    retAthletes = {"athletes": []}
    if len(list(athletes)) == 0:
        return jsonify(retAthletes)
    if request.method != 'GET':
        abort(405)
    if request.method =='GET':
        for athlete in athletes[0].groups[0].members:
            retAthletes["athletes"].append(athlete.athlete.to_json())

    return json.dumps(retAthletes)


@app.route('/signup', methods=['POST'])
def signup_user():

    userhash = str(request.headers.get("authorization"))

    if not userhash == "None":
        userhash = userhash.replace("Basic ", "")
        jsondata = json.dumps(request.json)

        session = SessionManager.create_user(jsondata, userhash)
        application_cache.add_session_to_cache({"sessiontoken": session, "userid": session.iduser})
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
        application_cache.add_session_to_cache(session)
        profile = SloachObjectProvider.get_profile(session.iduser)
        if profile is None:
            return make_response("Couldn't find your profile", 500)
        loginResult = {'iduser': session.iduser, 'token': str(session.sessiontoken), 'profile': {"firstname": profile.firstname, "lastname": profile.lastname, "email": profile.email, "clubkey": profile.clubkey}}

        return jsonify(loginResult)
    return make_response("",401)

@app.route('/logout', methods=['POST','GET'])
def logout_user():
    if not str(request.headers.get('sessiontoken')):
        abort(400)
    sessionid = request.headers.get('sessiontoken')

    session = db_session.query(Session).filter_by(sessiontoken=sessionid, active=1, logouttime=None)
    if len(list(session)) == 0:
        return make_response("",200)
    session[0].logouttime = datetime.datetime.now()
    session[0].active = 0
    db_session.commit()

    application_cache.remove_session_from_cache(sessionid)

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
        abort(401)
    if request.method == 'GET':
        club = application_cache.get_club_by_sessiontoken(request.headers.get('sessiontoken'))
        if rowkey != club:
            abort(401)
        athletes = db_session.query(Athlete).filter_by(club=rowkey).join(GroupMember).join(Group)
        if len(list(athletes)) == 0:
            abort(404)
        else:
            retAthletes = []
            for athlete in athletes:
                retAthlete = {'firstname': athlete.firstname, 'lastname': athlete.lastname, 'id':athlete.id}
                retAthletes.append(retAthlete)
            return make_response(jsonify({'athletes': retAthletes}))
    abort(403)


@app.route('/clubs/<rowkey>/athletes/<idathlete>/sessions', methods=['GET'])
def athlete_sessions(rowkey, idathlete):
    if not check_auth(request):
        abort(401)
    if request.method == 'GET':
        club = application_cache.get_club_by_sessiontoken(request.headers.get('sessiontoken'))
        if rowkey != club:
            abort(401)
        athlete = db_session.query(Athlete).filter_by(club=rowkey,id=idathlete)
        retSessions = {"athleteSessions": []}
        if len(list(athlete)) == 0:
            abort(404)
        else:
            training_sessions = db_session.query(TrainingSession)\
                .join(Group).join(GroupMember).join(Athlete).filter_by(id=idathlete).order_by(TrainingSession.fromtime.desc())

            if len(list(training_sessions)) > 0:
                for ts in training_sessions:
                    retSessions["athleteSessions"].append({"name":ts.name,
                                        "description": ts.description,
                                        "fromtime": str(ts.fromtime.isoformat()),
                                        "totime": str(ts.totime.isoformat()),
                                        "id": ts.id
                    })

        return jsonify(retSessions)

def allowed_file(filename):
    return '.' in filename and \
           str.lower(filename.rsplit('.', 1)[1]) in ALLOWED_EXTENSIONS

@app.route('/clubs/<rowkey>/picture', methods=['GET','POST'])
def club_pictures(rowkey):
    if not check_auth(request):
        abort(403)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response('No file part', 400)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return make_response('No file part', 400)
        if not allowed_file(file.filename):
            return make_response('The filetype is not allowed')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = rowkey + "." + filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['CLUB_PICTURE_UPLOAD_FOLDER'], filename))
            db_picture = db_session.query(UserFile).filter_by(owner=rowkey, file_type='ProfilePicture')
            if len(list(db_picture)) == 0:
                db_picture = UserFile()
                db_picture.file_type = 'ProfilePicture'
                db_picture.owner = rowkey
                db_session.add(db_picture)
                db_session.commit()
                return make_response("",200)
            db_picture.update({"file_name":filename})
            db_session.commit()
            return make_response("", 200)
    if request.method == 'GET':
        filename = db_session.query(UserFile).filter_by(file_type='ProfilePicture', owner=rowkey)[0].file_name
        return jsonify({"filename":  str.replace(app.config['CLUB_PICTURE_UPLOAD_FOLDER'], "static\\Sloach\\", "") + "/" + filename})

@app.route('/athletes/<idathlete>/results', methods=['GET','PUT'])
def get_results(idathlete):
    if not check_auth(request):
        abort(403)
    retResults = {"trainingresults": []}
    if request.method == 'GET':
        trainingresults = db_session.query(TrainingResult).filter_by(id=idathlete).join(TrainingSession).order_by(TrainingResult.resulttype)

        for training_result in trainingresults:
            retResults["trainingresults"].append({"result_type":training_result.resulttype,
                               "timeresult": training_result.timeresult,
                               "achievedonsession":training_result.achievedonsession.id,
                               "sessionname": training_result.achievedonsession.name,
                               "achievedondate":str(training_result.achievedonsession.fromtime.isoformat())})
    if request.method == 'PUT':
        if not request.json:
            abort(400)
        training_result = TrainingResult()
        training_result.achievedonsession = request.json["trainingsession"]
        training_result.athlete_id = request.json["athlete"]
        training_result.resulttype = request.json["resulttype"]
        training_result.timeresult = request.json["timeresult"]

        db_session.commit()

    return make_response(jsonify(retResults),200)

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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)

