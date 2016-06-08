__author__ = 'pde'
from models import Profile, Club, Session, Athlete
from flask import abort, jsonify
from database import db_session
import json
import datetime


class SloachObjectProvider:

    def update_profile(iduser, existing_profile, profile):

        existing_profile.firstname = profile['firstname']
        existing_profile.lastname = profile['lastname']
        existing_profile.email = profile['email']

        db_session.add(existing_profile)
        db_session.commit()
        return existing_profile

    def create_profile(iduser, profile):
        existing_profile = db_session.query(Profile).filter_by(user=iduser)
        if(len(list(existing_profile))) > 0:
            retprofile = SloachObjectProvider.update_profile(iduser, existing_profile[0], profile)
            return retprofile

        db_profile = Profile(iduser)
        db_profile.firstname = profile['firstname']
        db_profile.lastname = profile['lastname']
        db_profile.email = profile['email']


        db_session.add(db_profile)
        db_session.commit()
        return db_profile


    def get_profile(iduser):
        profile = db_session.query(Profile).filter_by(user=iduser)
        if len(list(profile)) == 0:
            return None
        return profile[0]

    def get_club(self, sessiontoken, idclub):
        session = db_session.query(Session).filter_by(sessiontoken=sessiontoken)

        club = db_session.query(Club).filter_by(idclub=idclub)
        if len(list(club)) == 0:
            abort(404)
        return jsonify({'idclub': club[0].idclub, 'name': club[0].name, 'description': club[0].description})

    def get_athletes(self, sessiontoken):
        session = db_session.query(Session).filter_by(sessiontoken=sessiontoken)

        if session is None:
            abort(401)

