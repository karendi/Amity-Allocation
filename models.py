from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class AmityPopulation(Base):
    """ Table with all the people found in Amity """

    __tablename__ = 'AmityPopulation'

    Employee_id = Column(String, primary_key=True)
    Employee_Type = Column(String(25))


class AmityAllocation(Base):
    """ Table with the the room name and all the people allocated to the room """

    __tablename__ = 'AmityAllocation'

    Room_name = Column(String(25), primary_key=True)
    Allocated_People = Column(Text)

    def __init__(self, Room_name=None, Allocated_People=None):
        self.Room_name = Room_name
        self.Allocated_People = Allocated_People


class AmityOffices(Base):
    __tablename__ = 'AmityOffices'

    Room_name = Column(String(25), primary_key=True)


class AmityLivingSpace(Base):
    __tablename__ = 'AmityLivingSpace'

    Room_name = Column(String(25), primary_key=True)


class AmityFellows(Base):
    __tablename__ = 'AmityFellows'

    Employee_id = Column(String, primary_key=True)
    Fellow_name = Column(String(25))


class AmityStaff(Base):
    __tablename__ = 'AmityStaff'

    Employee_id = Column(String, primary_key=True)
    Staff_name = Column(String(25))

class AmityUnallocated(Base):
    __tablename__ = 'AmityUnallocated'

    Employee_id = Column(String, primary_key=True)
    Room = Column(String(25))


def create_db(database_name):
    directory = 'databases/'
    # create an engine that stores data in the local directory
    engine = create_engine('sqlite:///' + directory + database_name +'.db')
    # create all tables in the engine.It is the same as Create Table in sql
    return Base.metadata.create_all(engine)
