from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import uuid

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from sofa import APIResource

class Message(Base, APIResource):
    __tablename__ = 'messages'
    id = Column(String(32), primary_key=True)
    sender = Column(String(64))
    content = Column(String(1024))
    parent = Column(String(32), ForeignKey('messages.id'))
    tree = Column(String(16))
    attachment = Column(String(32))

    def __init__(self, sender, content, parent):
        self.id = uuid.uuid4().hex
        self.sender = sender
        self.content = content
        self.parent = parent

class User(Base, APIResource):
    __tablename__ = 'users'
    id = Column(String(32), primary_key=True)
    username = Column(String(64))
    password = Column(String(1024))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = uuid.uuid4().hex

Index('my_index', Message.id, unique=True, mysql_length=255)
