__author__ = 'dmczk'
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time
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
    postaladdress = Column("postaladdress", String(100))
    postalzipcode = Column("postalzipcode", String(13))
    postalcity = Column("postalcity",String(50))
    visitingaddress = Column("visitingaddress", String(100))
    visitingzipcode = Column("visitingzipcode", String(13))
    visitingcity = Column("visitingcity",String(50))
    rowkey = Column("rowkey", String(40), unique=True)
    groups = relationship("Group",back_populates="club")
    profile_picture = Column("profilepicture", Integer)



    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Club %r>' % self.name

class UserFile(Base):
    __tablename__ = 'userfile'
    id = Column("id", Integer, primary_key=True)
    file_type = Column("filetype", String(40))
    owner = Column("owner", String(40))
    file_name = Column("filename", String(128))


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
    workstation = Column("workstation", String(20))

    def __init__(self, iduser=None):
        self.iduser = iduser
        self.logintime = datetime.datetime.now()
        self.active = 1
        self.sessiontoken = str(uuid.uuid4())
        self.workstation = ""

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




class TrainingSession(Base):
    __tablename__ = "trainingsession"
    id = Column("id",primary_key=True)
    name = Column("name", String(100))
    description = Column("description", String(250))
    fromtime = Column("fromtime", DateTime)
    totime = Column("totime", DateTime)
    group = Column("group", ForeignKey("group.id"))
    traininggroup = relationship("Group", back_populates="sessions")

    results = relationship("TrainingResult", back_populates="achievedonsession")
    participants = relationship("SessionParticipant", back_populates="trainingsession")

    def __repr__(self):
        return '<TrainingSession %r>' % self.name + ' ' + self.fromtime + '-' + self.totime

class GroupMember(Base):
    __tablename__ = "groupmember"
    id = Column("id",primary_key=True)
    athlete_id = Column("athlete", Integer, ForeignKey("athlete.id"))
    group_id = Column("group", Integer, ForeignKey("group.id"))
    group = relationship("Group", back_populates="members")
    athlete = relationship("Athlete", back_populates="memberofgroups")


class Group(Base):
    __tablename__ = "group"
    id = Column("id", primary_key=True)
    name = Column("name",String(100))
    description = Column("description", String(512))
    owner = Column("owner", Integer, ForeignKey("club.idclub"))
    members = relationship("GroupMember", back_populates = "group")
    club = relationship("Club", back_populates="groups")
    sessions = relationship("TrainingSession", back_populates="traininggroup")

    def __repr__(self):
        return '<Group %r>' % self.name


class Athlete(Base):
    __tablename__ = 'athlete'
    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname",String(100))
    lastname = Column("lastname",String(100))
    dateofbirth = Column("dateofbirth", Date)
    club = Column("club", UNIQUEIDENTIFIER)
    memberofgroups = relationship("GroupMember", back_populates="athlete")
    results = relationship("TrainingResult",back_populates="athlete")
    participates = relationship("SessionParticipant", back_populates="athlete")

    def __repr__(self):
        return '<Athlete %r>' % self.firstname + ' ' + self.lastname

class TrainingResult(Base):
    __tablename__ = "trainingresult"
    id = Column("id", Integer, primary_key=True)
    resulttype = Column("resulttype", Integer)
    athlete_id = Column("athlete_id",ForeignKey("athlete.id"),nullable=False)
    timeresult = Column("timeresult_ms", Integer) #Result stored in milliseconds

    trainingsession = Column("trainingsession", ForeignKey("trainingsession.id"))
    achievedonsession = relationship("TrainingSession", back_populates="results")
    athlete = relationship("Athlete",back_populates="results")

class SessionParticipant(Base):
    __tablename__ = "sessionparticipant"
    id = Column("id", Integer,primary_key=True)
    athlete_id = Column("athlete_id", ForeignKey("athlete.id"), nullable=False)
    trainingsession_id = Column("trainingsession", ForeignKey("trainingsession.id"), nullable=False)
    athlete = relationship("Athlete", back_populates="participates")
    trainingsession = relationship("TrainingSession", back_populates="participants")