import sqlite3
import os.path

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from models import Amity_Allocation, Amity_Population, Amity_Living_space, Amity_Offices, Amity_Fellows, Amity_Staff
from functions.amity_class import Amity



# for running native sql statements
connection = sqlite3.connect("amity_allocation.db")
cursor = connection.cursor()


class Database_sessions(object):

    def __init__(self, database_name):
            directory = 'databases/'
            engine = create_engine('sqlite:///' + directory + database_name + '.db')
            Session = sessionmaker(bind=engine)
            self.session = Session()

    def add_person(self, **data):
        """
        add a room with its occupants
        **data specifies that the data to be entered is a dict
        working with Amity.people (dictionary)
        works with the model Amity_Population
        """
        for k, v in Amity.people.items():
            # add data to the table
            # first check if the person already exists
            check_person = self.session.query(Amity_Population).filter_by(Employee_id=k).first()
            if check_person is None:
                person = Amity_Population(Employee_id=k, Employee_Type=v)
                self.session.add(person)
                self.session.commit()
            else:  # edit the already existing person
                check_person.Employee_id = k
                check_person.Employee_Type = v
                self.session.commit()

        return "The employees were added"

    def edit_room(self, **data):
        """ Edits an already existing column (existing room in the database)"""
        for room_name, people4 in Amity.rooms.items():
            number_of_people = len(people4)
            returned_data = self.session.query(Amity_Allocation).filter_by(Room_name=room_name).first()
            if number_of_people == 0:  # when no-one was allocated to that room again
                returned_data.Room_name = room_name
                returned_data.Allocated_People = None
                self.session.commit()
            elif number_of_people == 1:  # if one person was allocated to the room
                returned_data.Room_name = room_name
                returned_data.Allocated_People = people4[0]
                self.session.commit()
            else:  # if more than two people were allocated to the room
                returned_data.Room_name = room_name
                returned_data.Allocated_People = ','.join(map(str, people4))
                self.session.commit()
        return "The room data was added"

    def add_room(self, **data):
        """ works with the Amity.rooms (dictionary)
        enters the data to the model Amity_Allocation
        """

        for roomname, people_in in Amity.rooms.items():
            # add data to the table
            length_of_list = len(people_in)

            # check if the room already exists in the table
            room_object = self.session.query(Amity_Allocation).filter(Amity_Allocation.Room_name == roomname).first()
            if room_object is None:
                if length_of_list == 0:
                    allocation = Amity_Allocation(Room_name=roomname, Allocated_People=None)
                    self.session.add(allocation)
                    self.session.commit()

                elif length_of_list == 1:
                    allocation = Amity_Allocation(Room_name=roomname, Allocated_People=people_in[0])
                    self.session.add(allocation)
                    self.session.commit()

                elif length_of_list > 1:
                    # list is v (make the list a string)
                    people = ','.join(map(str, people_in))
                    allocation = Amity_Allocation(Room_name=roomname, Allocated_People=people)
                    self.session.add(allocation)
                    self.session.commit()
            else:
                return self.edit_room()
        return "The rooms were added"

    def add_office(self, *params):
        """ Function that takes the Amity.offices list and adds it to the database
        It uses the model Amity_Offices """
        for off in Amity.offices:
            office_object = self.session.query(Amity_Offices).filter(Amity_Offices.Room_name == off).first()
            if office_object is None:  # check if the office exists
                new_office = Amity_Offices(Room_name=off)
                self.session.add(new_office)
                self.session.commit()
            else:
                office_object.Room_name = off
                self.session.commit()
        return "The offices were added"

    def add_living_space(self, *params):
        """ Function that commits the data from Amity.living_spaces to the database
        It uses the model Amity_Living_space """
        for l_s in Amity.living_spaces:
            living_space_object = self.session.query(Amity_Living_space).filter(Amity_Living_space.Room_name == l_s).first()
            if living_space_object is None:  # check if the living_space exists
                new_living_space = Amity_Living_space(Room_name=l_s)
                self.session.add(new_living_space)
                self.session.commit()
            else:
                self.session.commit()
        return "The living spaces were added"

    def add_fellows(self, **data):
        """ Function that adds all the fellows from the fellows dict to the database,
         uses the model Amity_Fellows"""
        for fellow_id, fellow_name in Amity.fellows.items():
            # check if the fellow exists
            check_fellow = self.session.query(Amity_Fellows).filter(Amity_Fellows.Employee_id == fellow_id).first()
            if check_fellow is None:
                fellow_object = Amity_Fellows(Employee_id=fellow_id, Fellow_name=fellow_name)
                self.session.add(fellow_object)
                self.session.commit()
            else:
                self.session.commit()
        return "The fellows were added.."

    def add_staff(self, **data):
        """ Method that adds all the staff members from the staff dict to the database,
        uses the model Amity_Staff """
        for staff_id, staff_name in Amity.staff.items():
            # check if the staff exists
            check_staff = self.session.query(Amity_Staff).filter(Amity_Staff.Employee_id == staff_id).first()
            if check_staff is None:
                staff_object = Amity_Staff(Employee_id=staff_id, Staff_name=staff_name)
                self.session.add(staff_object)
                self.session.commit()
            else:
                self.session.commit()
        return "The staff members were added.."

    def return_rooms(self, **data):
        """ Returns the data from the database table Amity_Allocation """
        # returning all the data stored for rooms in the database
        print("Returning the rooms and the people in them .. \n")
        results = self.session.query(Amity_Allocation).all()
        new_list = []
        for i in results:
            room_name = i.Room_name
            people_in_room = i.Allocated_People
            if people_in_room is None:
                Amity.rooms[room_name] = new_list
            else:
                people_in_room = i.Allocated_People.split(',')  # returns a list of all the people in the room
                people_in_room_int = map(int , people_in_room) # change to integer
                Amity.rooms[room_name] = people_in_room_int # return the data

        return Amity.rooms

    def return_offices(self, *params):
        """ Returns all the offices from the database table Amity_Offices
            appends it to the list Amity.offices """
        print("Returning the offices...\n")
        query = self.session.query(Amity_Offices).all()
        for office in query:
            Amity.offices.append(office.Room_name)
        return Amity.offices

    def return_living_spaces(self, *params):
        print("Returning the living spaces")
        query2 = self.session.query(Amity_Living_space).all()
        for living_s in query2:
            Amity.living_spaces.append(living_s.Room_name)
        return Amity.living_spaces

    def return_fellows(self):
        print("Returning the fellows..")
        fellow_query = self.session.query(Amity_Fellows).all()
        for fellow in fellow_query:
            fellow_id = int(fellow.Employee_id)
            fellow_name = fellow.Fellow_name
            Amity.fellows[fellow_id] = fellow_name  # add data to the Amity.fellows dict
        print (Amity.fellows)

    def return_staff(self):
        print("Returning the staff members..")
        staff_query = self.session.query(Amity_Staff).all()
        for staff in staff_query:
            staff_id = int(staff.Employee_id)
            staff_name = staff.Staff_name
            Amity.staff[staff_id] = staff_name  # add data to the Amity.staff dict
        print (Amity.staff)

    def return_population(self):
        print("Returning the Amity population..")
        people_query = self.session.query(Amity_Population).all()
        for employee in people_query:
            employee_id = int(employee.Employee_id)
            employee_type = employee.Employee_Type
            Amity.people[employee_id] = employee_type
        return Amity.people
