from setuptools.package_index import Credential

__author__ = 'pde'

from models import User, Session
from flask import abort, jsonify
from database import db_session
import json
import datetime

class SessionManager():

    def create_session(hash):
        user = db_session.query(User).filter_by(hash=hash)
        if len(list(user)) == 0:
            return None
        session = Session(user[0].id)
        db_session.add(session)
        db_session.commit()
        return session


    def get_session(sessiontoken):
        session = db_session.query(Session).filter_by(sessiontoken=sessiontoken)
        if len(list(session)) == 0:
            session = None
        if session[0].active == 0 or session[0].logouttime is not None:
            session = None

        return session


    def logout_session(session_token):
        session = db_session.query(Session).filter_by(sessiontoken=sessiontoken)
        if len(list(session)) == 0:
            session = None
        if session.active == 0 or session.logouttime is not None:
            session = None

        session[0].logouttime = datetime.datetime.now()
        session[0].active = 0
        db_session.commit()
        
    def create_user(credentials, hash):
        credentialsObj = json.loads(credentials)
        user = db_session.query(User).filter_by(email=credentialsObj['email'])
        if len(list(user)) > 0:
            return None
        user = User(credentialsObj['email'],hash)
        db_session.add(user)
        db_session.commit()
        session = SessionManager.create_session(hash)

        return session
