from setuptools.package_index import Credential

__author__ = 'pde'

from models import User, Session
from flask import abort, jsonify
from database import db_session
from application_cache import ApplicationCache
import json
import datetime


class SessionManager():

    def user_has_active_session(userid, workstation):
        user = db_session.query(User).filter_by(id=userid).first()
        if user is None:
            return False
        sessions = db_session.query(Session).filter_by(Session.iduser == user.id, Session.active == 1)
        if len(list(sessions)) > 0:
            return True

        return False

    def user_has_active_session_other_workstation(userid, workstation):
        user = db_session.query(User).filter_by(id=userid).first()
        if user is None:
            return False
        sessions = db_session.query(Session).filter_by(Session.iduser == user.id, Session.active == 1, Session.workstation != workstation)

        if len(list(sessions)) > 0:
            return True

        return False

    def get_user_active_sessions(userid):
        return db_session.query(Session).filter(Session.iduser == userid, Session.active == 1)

    def create_session(hash, workstation):
        user = db_session.query(User).filter_by(hash=hash).first()
        if user is None:
            return None

        current_sessions = SessionManager.get_user_active_sessions(user.id)
        for session in current_sessions:
            session.active = 0

        db_session.commit()

        new_session = Session(user.id)

        db_session.add(new_session)
        db_session.commit()
        return new_session


    def get_session(sessiontoken):
        session = db_session.query(Session).filter_by(sessiontoken=sessiontoken)
        if len(list(session)) == 0:
            session = None
        if session[0].active == 0 or session[0].logouttime is not None:
            session = None

        return session


    def logout_session(session_token):
        session = db_session.query(Session).filter_by(sessiontoken=session_token)
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
