from db.connection import Base
from sqlalchemy import Column,Integer,ForeignKey,String,Numeric,DateTime,Boolean,Time
from datetime import datetime

class Users(Base):
    __tablename__= "Users"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    name=Column(String,nullable=False)
    lastname=Column(String,nullable=False)
    email=Column(String,unique=True)
    phone=Column(Numeric(10),unique=True)
    password=Column(String,nullable=False)

class Categories(Base):
    __tablename__="Categories"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    name=Column(String,nullable=False)
    description=Column(String)
    schedulable=Column(Boolean,nullable=False)

class Transactions(Base):
    __tablename__="Transactions"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    user=Column(Integer,ForeignKey('Users.id'))
    amount=Column(Numeric(10,2),nullable=False)
    datetime=Column(DateTime,default=datetime.utcnow)
    description=Column(String,nullable=False)
    category=Column(Integer,ForeignKey('Categories.id'))

class ScheduledTransactions(Base):
    __tablename__="ScheduledTransactions"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    user=Column(Integer,ForeignKey('Users.id'))
    amount=Column(Numeric(10,2),nullable=False)
    day=Column(Integer, nullable=False)
    time=Column(Time,nullable=False)
    description=Column(String,nullable=False)
    category=Column(Integer,ForeignKey('Categories.id'))

class Budgets(Base):
    __tablename__="Budgets"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    user=Column(Integer,ForeignKey('Users.id'))
    amount=Column(Numeric(10,2),nullable=False)
    description=Column(String,nullable=False)
    year=Column(Integer,nullable=False)
    month=Column(Integer,nullable=False)
    category=Column(Integer,ForeignKey('Categories.id'))