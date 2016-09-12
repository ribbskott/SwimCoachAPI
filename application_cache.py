__author__ = 'pde'

from database import db_session
from models import Profile, User,Session


class ApplicationCache:

    def __init__(self):
        self.session_cache = {}
        self.user_cache = {}

    def load_user_cache(self):
        for result in db_session.query(Profile, User).filter(Profile.user == User.id).all():
            self.user_cache[result[1].id] = result[0].clubkey

    def load_active_sessions(self):
        for result in db_session.query(Session).\
                filter((Session.active==1)):
            self.session_cache[result.sessiontoken] = result.iduser

    def add_session_to_cache(self, user_session):
        self.session_cache[user_session.sessiontoken] = user_session.iduser

    def remove_session_from_cache(self,sessiontoken):
        if sessiontoken in self.session_cache:
            del self.session_cache[sessiontoken]

    def get_club_by_sessiontoken(self, sessiontoken):
        club = self.user_cache[self.session_cache[sessiontoken]]
        return club