from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, PickleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_json import NestedMutableJson, MutableJson
import configparser

config = configparser.SafeConfigParser()
config.read('../config.ini')
user = config.get('MYSQL', 'USER')
passwd = config.get('MYSQL', 'PASSWD')
host = config.get('MYSQL', 'HOST')
database = config.get('MYSQL', 'DATABASE')

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, unique=True)
    message = Column(String(2000))
    channel = Column(BigInteger)
    time = Column(Integer)
    interval = Column(Integer)

    def __repr__(self):
        return '<Reminder "{}" <#{}> {}s>'.format(self.message, self.channel, self.time)


class Server(Base):
    __tablename__ = 'servers'

    map_id = Column(Integer, primary_key=True)
    id = Column(BigInteger, unique=True)
    prefix = Column( String(5) )
    language = Column( String(2) )
    timezone = Column( String(30) )
    blacklist = Column( NestedMutableJson )
    restrictions = Column( NestedMutableJson )
    tags = Column( MutableJson )
    autoclears = Column( MutableJson )

    def __repr__(self):
        return '<Server {}>'.format(self.id)


engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{db}'.format(user=user, passwd=passwd, host=host, db=database))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

import sqlite3
import json

with sqlite3.connect('../DATA/calendar.db') as connection:
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row()

    cursor.execute('SELECT * FROM reminders;')

    for reminder in cursor.fetchall():
        session.add(Reminder(**dict(reminder)))

    session.commit()

    cursor.execute('SELECT * FROM servers;')

    for server in cursor.fetchall():
        s = dict(server)
        idx = s['id']
        prefix = s['prefix']
        language = s['language']
        timezone = s['timezone']

        blacklist = {'data': json.loads(s['blacklist'])}
        restrictions = {'data': json.loads(s['restrictions'])}

        tags = json.loads(s['tags'])
        autoclears = json.loads(s['autoclears'])

        session.add(Server(id=idx, prefix=prefix, language=language, timezone=timezone, blacklist=blacklist, restrictions=restrictions, tags=tags, autoclears=autoclears))
