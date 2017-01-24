import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Amity_Population(Base):
    """ Table with all the people found in Amity """

    __tablename__ = 'Amity_Population'

    Employee_id = Column(Integer, primary_key=True)
    Employee_Type = Column(String(25))


class Amity_Allocation(Base):
    """ Table with the the room name and all the people allocated to the room """

    __tablename__ = 'Amity_Allocation'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    Room_name = Column(String(25))
    Allocated_People = Column(Text)

    def __init__(self, Room_name=None, Allocated_People=None, id=None):
        self.id = id
        self.Room_name = Room_name
        self.Allocated_People = Allocated_People


class Amity_Offices(Base):
    __tablename__ = 'Amity_Offices'

    Room_name = Column(String(25), primary_key=True)


class Amity_Living_space(Base):
    __tablename__ = 'Amity_Living_space'

    Room_name = Column(String(25), primary_key=True)


# create an engine that stores data in the local directory
engine = create_engine('sqlite:///amity_allocation.db')

# create all tables is the engine.It is the same as Create Table in sql
Base.metadata.create_all(engine)
