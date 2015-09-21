from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime)
import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
