import random


class Amity(object):
    """ Contains dictionaries or lists as class variable
     that hold the people and rooms in the facility"""

    rooms = {}  # dict that holds room and people in it {"room_names":[emp_1 , emp_2] ,}
    offices = []  # list that holds office_names [Hogwarts , Shire , Kindaramu]
    living_spaces = []  # list that holds living_space_names [Joy , Peace ]
    people = {}  # dict that holds all people {"emp_id": emp_type , }
    fellows = []  # list that holds the fellow [emp_id1 , emp_id2]
    staff = []  # list that holds the staff [emp_id1 , emp_id2]
    unallocated_people = {}  # a dict of all the people who havenot been allocated a room{emp_id : room_type}

    def __init__(self):
        pass


class Room(Amity):
    """Contains all the rooms found in Amity facility.
    It uses the Amity.rooms dictionary"""

    def __init__(self, room_name="None", room_type="None"):

        """ The room name must be unique"""

        self.room_name = room_name
        self.room_type = room_type

    def create_room(self):

        """ Add a room to the dictionary Amity.rooms"""

        if self.room_name.lower() in Amity.rooms.keys():  # check if the room exists
            return "Sorry the room already exists!"

        else:
            # add the rooms to the dictionary{"room_name": [emp_1 , emp_2]}
            r_name = self.room_name.lower()
            Amity.rooms[r_name] = list()
            return Amity.rooms


class Office(Room):
    """ Subclass of the Room class for rooms with room_type == office.
    It use the Amity.offices list """

    def add_office(self):
        """ Append room_name to Amity.offices List """

        if self.room_name.lower() in Amity.offices:  # check if the office exists
            return "That office already exists"

        else:  # append to the office list(Amity.offices)
            Amity.offices.append(self.room_name.lower())
            return Amity.offices


class Living_Space(Room):
    """ Subclass of the Room class for rooms with room_type == living_space.
    It uses the Amity.living_spaces list """

    def add_living_space(self):
        """ Appends room_name to Amity.living_spaces List """
        if self.room_name.lower() in Amity.living_spaces:
            # check if living_space exists
            return "That Living_space already exists"

        else:
            # append to the Amity.living_spaces list
            Amity.living_spaces.append(self.room_name.lower())
            return Amity.living_spaces


class Person(Amity):
    """ Class that inherits from Amity class uses the Amity.people dict.
    Contain a dict with all the people found in Amity facility"""

    def __init__(self, First_name="none", Last_name="none",
                 employee_type="none", employee_id="none", want_accomodation="n"):
        self.First_name = First_name
        self.Last_name = Last_name
        self.employee_type = employee_type
        self.employee_id = employee_id  # unique identifier for a person
        self.want_accomodation = want_accomodation

    def add_person(self):
        """ Adds data to the Amity.people dict """

        e_type = self.employee_type.lower()
        Amity.people[self.employee_id] = e_type
        return Amity.people  # return the dict {"emp_id":emp_type , "emp_id":emp_type}


class Fellow(Person):
    """ Subclass of Person , contain all the employees with employee_type == fellow.
    Uses Amity.fellows list"""

    def __init__(self, First_name, Last_name, employee_type, employee_id, want_accomodation="n", office="None",
                 living_space="None"):
        Person.__init__(self, First_name, Last_name, employee_type, employee_id, want_accomodation)
        self.office = office
        self.living_space = living_space

    def add_person(self):
        """ appends to the Amity.fellows list"""
        if self.want_accomodation.lower() == "y":
            r_name = random.choice(Amity.offices)  # choose a random office name

            # max_capacity of an office is 6
            if len(Amity.rooms[r_name.lower()]) < 6:
                # assign a fellow to an office
                Amity.rooms[r_name.lower()].append(self.employee_id)
            elif len(Amity.rooms[r_name.lower()]) == 6:
                Amity.unallocated_people[self.employee_id] = "office"  # append to the Amity.unallocated_people dict

            l_name = random.choice(Amity.living_spaces)  # choose a living space randomly

            # max_capacity of a living_space is 4
            if len(Amity.rooms[l_name.lower()]) < 4:
                # assign a fellow to a living space randomly
                Amity.rooms[l_name.lower()].append(self.employee_id)
            elif len(Amity.rooms[l_name.lower()]) == 4:
                Amity.unallocated_people[
                    self.employee_id] = "living_space"  # append to the Amity.unallocated_people dict

            # add the fellows to the fellow list
            Amity.fellows.append(self.employee_id)

            return Amity.rooms
            return Amity.fellows
            return Amity.unallocated_people

        elif self.want_accomodation.lower() == "n":
            r_name = random.choice(Amity.offices)  # choose a random office name

            # max_capacity of an office is 6
            if len(Amity.rooms[r_name.lower()]) < 6:
                # assign a fellow to an office
                Amity.rooms[r_name.lower()].append(self.employee_id)
            elif len(Amity.rooms[r_name.lower()]) == 6:
                Amity.unallocated_people[self.employee_id] = "office"  # append to the Amity.unallocated_people dict

            # append the fellow list with the employee_id
            Amity.fellows.append(self.employee_id)

            return Amity.rooms 
            return Amity.fellows
            return Amity.unallocated_people


class Staff(Person):
    # Class variable - A list with all the staff employee_id numbers
    staff_members = []

    def __init__(self, First_name, Last_name, employee_type, employee_id, office="None"):
        Person.__init__(self, First_name, Last_name, employee_type, employee_id)
        self.office = office

    def add_person(self):
        # choose a random office name from the list
        r_name = random.choice(Amity.offices)

        # max_capacity of an office is 6
        if len(Amity.rooms[r_name.lower()]) < 6:
            # assign the staff to an office
            Amity.rooms[r_name.lower()].append(self.employee_id)

        elif len(Amity.rooms[r_name.lower()]) == 6:
            Amity.unallocated_people[self.employee_id] = "office"  # append to the Amity.unallocated_people dict

        # append the staff list with the employee_id
        Amity.staff.append(self.employee_id)

        return Amity.rooms  # return the room dict
        return Amity.staff  # return the staff list
        return Amity.unallocated_people
