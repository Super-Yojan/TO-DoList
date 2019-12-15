from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

class item(Base):
    __tablename__ ='tolist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    items = Column(String(300))


engine = create_engine('sqlite:///todolist.db')

Base.metadata.create_all(engine)