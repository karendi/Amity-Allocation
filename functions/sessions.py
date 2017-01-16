import sqlite3

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from models import Amity_Allocation, Amity_Population , Amity_Living_space , Amity_Offices
from functions.amity_class import Amity

engine = create_engine('sqlite:///amity_allocation.db')
Base = declarative_base()
Base.metadata.bind = engine

# for running native sql statements
connection = sqlite3.connect("amity_allocation.db")
cursor = connection.cursor()

Session = sessionmaker(bind=engine)

session = Session()


def check_data(*params):
    pass



def add_person(**data):
    """
    add a room with its occupants
    **data specifies that the data to be entered is a dict
    working with Amity.people (dictionary)
    works with the model Amity_Population
    """

    for k, v in Amity.people.items():
        # add data to the table
        person = Amity_Population(Employee_id=k, Employee_Type=v)
        session.add(person)
        session.commit()

    return "The data was added"


def edit_room(**data):
    """ Edits an already existing column (existing room in the database)"""
    for room_name , people4 in Amity.rooms.iteritems():
        number_of_people = len(people4)
        returned_data = session.query(Amity_Allocation).filter_by(Room_name=room_name).first()
        if number_of_people == 0: # when no-one was allocated to that room again
            returned_data.Room_name = room_name
            returned_data.Allocated_People = None
            session.commit()
        elif number_of_people == 1: # if one person was allocated to the room
            returned_data.Room_name = room_name
            returned_data.Allocated_People = people4[0]
            session.commit()
        else: # if more than two people were allocated to the room
            returned_data.Room_name = room_name
            returned_data.Allocated_People = ','.join(people4)
            session.commit()

def add_room(**data):
    """ works with the Amity.rooms (dictionary)
    enters the data to the model Amity_Allocation
    """

    for roomname, people_in in Amity.rooms.iteritems():
        # add data to the table
        length_of_list = len(people_in)

        # check if the room already exists in the table
        room_object = session.query(Amity_Allocation).filter(Amity_Allocation.Room_name == roomname).first()
        if room_object is None:
            if length_of_list == 0:
                allocation = Amity_Allocation(Room_name = roomname , Allocated_People = None)
                session.add(allocation)
                session.commit()

            elif length_of_list == 1:
                allocation = Amity_Allocation(Room_name=roomname, Allocated_People=people_in[0])
                session.add(allocation)
                session.commit()

            elif length_of_list > 1:
                # list is v (make the list a string)
                people = ','.join(people_in)
                allocation = Amity_Allocation(Room_name=roomname, Allocated_People=people)
                session.add(allocation)
                session.commit()
        else:
            return edit_room()

def add_office(*params):

    """ Function that takes the Amity.offices list and adds it to the database
    It uses the model Amity_Offices """

    for off in Amity.offices:
        new_office = Amity_Offices(Room_name = off)
        session.add(new_office)
        session.commit()

def add_living_space(*params):
    """ Function that commits the data from Amity.living_spaces to the database
    It uses the model Amity_Living_space """

    for l_s in Amity.living_spaces:
        new_living_space = Amity_Living_space(Room_name = l_s)
        session.add(new_living_space)
        session.commit()

def return_rooms(**data):
    """ Returns the data from the database """
        #returning all the data stored for rooms in the database
    results = session.query(Amity_Allocation).all()
    new_list = []
    for i in results:
        room_name = i.Room_name
        people_in_room = i.Allocated_People
        if people_in_room is None:
            Amity.rooms[room_name] = new_list
        else:
            people_in_room = i.Allocated_People.split(',') # returns a list of all the people in the room
            Amity.rooms[room_name] = people_in_room # return the data

    return Amity.rooms

def return_offices(*params):
    """ Returns all the living spaces from the database table Amity_Living_space
        appends it to the list Amity.living_spaces """
    query = session.query(Amity_Offices).all()
    for office in query:
        Amity.offices.append(office.Room_name)
    return Amity.offices

def return_living_spaces(*params):
    query2 = session.query(Amity_Living_space).all()
    for living_s in query2:
        Amity.living_spaces.append(living_s.Room_name)
    return Amity.living_spaces
