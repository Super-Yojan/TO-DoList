from sqlalchemy import Column, Integer, String , ForeignKey , BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(50))
    password = Column(String(20))
    #verified = Column(BOOLEAN, default=False)


class item(Base):
    __tablename__ ='tolist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    items = Column(String(300))
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship(User)




engine = create_engine('sqlite:///todolist.db')

Base.metadata.create_all(engine)