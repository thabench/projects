from enum import unique
from sqlalchemy import Column, Integer, Float, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///users.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column("User name", String, unique=True)

    
class Loans(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    name = Column("Loan name", String)
    amount = Column("Amount", Integer)
    interest = Column("Interest rate", Float)
    term = Column('Term', Integer)
    user_id = Column(Integer, ForeignKey('user.id'))


Base.metadata.create_all(engine)


def get_loans():
    loan_list = session.query(Loans).all()
    for i in loan_list:
        print(i)
        
def get_user_id(username):
    q = session.query(User).filter(User.name == username).one()
    return q.id
