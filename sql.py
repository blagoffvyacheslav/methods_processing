from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(255))
    fullname = Column(String)
    password = Column(String)
    age = Column(Integer)

    def __init__(self,name,fullname,password,age):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.age = age

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

session.add_all([User('vasia2', 'Vasiliy Pupkin2', 'Vasia20002', 192),
                 User('vasia3', 'Vasiliy Pupki3n', 'Vasia20003', 193)])
# vasia = User('vasia', 'Vasiliy Pupkin', 'Vasia2000', 19)
# session.add(vasia)

session.commit()
session.close()