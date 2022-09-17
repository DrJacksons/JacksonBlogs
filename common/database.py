from main import db
from sqlalchemy import MetaData

def dbconnect():
    ddd = db.engine
    dbsession = db.session
    metadata = MetaData(bind=db.engine)
    DBase = db.Model
    return dbsession,metadata,DBase