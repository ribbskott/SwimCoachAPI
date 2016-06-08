__author__ = 'dmczk'
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from database import Base
import uuid
import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash



class Club(Base):
    __tablename__ = 'club'

    idclub = Column("idclub", Integer, primary_key=True)
    name = Column("name", String(150))
    description = Column("description", String(500))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Club %r>' % self.name




class User(Base):
    __tablename__ = 'user'
    id = Column("iduser", Integer, primary_key=True)
    email = Column("email", String(200))
    hash = Column("hash", String(50))

    def __init__(self, email="", hash=""):
        self.hash = hash
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.email



class Session(Base):
    __tablename__ = 'session'
    id = Column("id", Integer, primary_key=True)
    iduser = Column("iduser", Integer)
    logintime = Column("logintime", DateTime)
    logouttime = Column("logouttime", DateTime)
    active = Column("active", Integer)
    sessiontoken = Column("sessiontoken", String(40))

    def __init__(self, iduser=None):
        self.iduser = iduser
        self.logintime = datetime.datetime.now()
        self.active = 1
        self.sessiontoken = str(uuid.uuid4())

    def __repr__(self):
        return '<Session %r>' % self.sessiontoken

class Profile(Base):
    __tablename__ = 'profile'
    id = Column("id", Integer, primary_key=True)
    user = Column("user", Integer)
    firstname = Column("firstname", String(100))
    lastname = Column("lastname", String(100))
    email = Column("email", String(200))
    clubkey = Column("clubkey", UNIQUEIDENTIFIER)


    def __init__(self, user=None):
        self.user = user

    def __repr__(self):
        return '<Profile %r>' % self.firstname + ' ' + self.lastname

class Athlete(Base):
    __tablename__ = 'athlete'
    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname",String(100))
    lastname = Column("lastname",String(100))
    owner = Column("club", UNIQUEIDENTIFIER)

    def __repr__(self):
        return '<Athlete %r>' % self.firstname + ' ' + self.lastname
