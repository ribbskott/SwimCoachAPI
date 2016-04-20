__author__ = 'dmczk'
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
import models
#params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=swimcoachdb;UID=pde;PWD=test123!")

#engine = create_engine("mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server Native Client 11.0};SERVER=localhost\SqlExpress;DATABASE=swimcoachdb;UID=pde;PWD=Test123!", convert_unicode=True)
engine = create_engine("mssql+pyodbc://pde1:Test123!@SqlExpress", convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    Base.metadata.create_all(bind=engine)

