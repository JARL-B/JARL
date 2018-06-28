from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, unique=True)
    message = Column(String(2000))
    channel = Column(Integer)
    time = Column(Integer)
    interval = Column(Integer)

    def __repr__(self):
        return '<Reminder "{}" <#{}> {}s>'.format(self.message, self.channel, self.time)

import json

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, unique=True)
    prefix = Column( String(5) )
    language = Column( String(2) )
    timezone = Column( String(30) )
    blacklist = Column( String(1000) )
    restrictions = Column( String(1000) )
    tags = Column( String(1000) )
    autoclears = Column( String(1000) )

    def __repr__(self):
        return '<Server ' + str(self.__dict__) + ' >'
