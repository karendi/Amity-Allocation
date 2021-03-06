import random
import os

from termcolor import cprint, colored


class Amity(object):
    """ Contains dictionaries or lists as class variable
     that hold the people and rooms in the facility"""

    rooms = {}  # dict that holds room and people in it {"room_names":[emp_1 , emp_2] ,}
    offices = []  # list that holds office_names [Hogwarts , Shire , Kindaramu]
    living_spaces = []  # list that holds living_space_names [Joy , Peace ]
    people = {}  # dict that holds all people {"emp_id": emp_type , }
    fellows = {}  # dict that holds the fellows [emp_id1: "first_name second_name" ,]
    staff = {}  # dict that holds the staff [emp_id1: "first_name second_name" , ]
    unallocated_people = {}  # a dict of all the people who have not been allocated a room{emp_id : room_type}
    available_offices = []  # list with all the offices that are not full
    available_living_spaces = []  # list with all the living spaces that are not full

    @staticmethod
    def check_available_rooms():
        """ Method that checks and returns rooms both living spaces and offices that aren't full"""
        for key, value in Amity.rooms.items():
            if key in Amity.offices:
                if len(value) < 6:
                    Amity.available_offices.append(key)
            elif key in Amity.living_spaces:
                if len(value) < 4:
                    Amity.available_living_spaces.append(key)
        return Amity.available_living_spaces, Amity.available_offices

    @staticmethod
    def print_allocations():
        """ Method that prints the rooms and people allocated to them """
        if len(Amity.rooms) != 0:
            for key, value in Amity.rooms.items():
                if key in Amity.offices:
                    print("\n")
                    print("---------------------------------------------")
                    cprint("AMITY OFFICES", 'red', attrs=['bold'])
                    print("---------------------------------------------")
                    cprint("Room Name: " + key, 'red', attrs=['bold'])
                    print("---------------------------------------------")
                    for person in value:
                        if person in Amity.fellows.keys():
                            print (Amity.fellows[person] + " " + str(person))
                        elif person in Amity.staff.keys():
                            print (Amity.staff[person] + " " + str(person))
                    print("---------------------------------------------")
                    print("\n")
                elif key in Amity.living_spaces:
                    print("\n")
                    print("---------------------------------------------")
                    cprint("AMITY LIVING SPACE", 'red', attrs=['bold'])
                    print("---------------------------------------------")
                    cprint("Room Name: " + key, 'red', attrs=['bold'])
                    print("---------------------------------------------")
                    for person in value:
                        if person in Amity.fellows.keys():
                            print (Amity.fellows[person] + " " + str(person))
                    print("---------------------------------------------")
                    print("\n")
        else:
            return "There are no allocations yet to be printed"

    @staticmethod
    def print_unallocated_people():
        """ Method that prints the people who have not been allocated to any room(living_space / office) """
        if len(Amity.unallocated_people) == 0:  # check if there are any people in the unallocated_people dict
            return "There are currently no unallocated people.."
        else:
            for key, value in Amity.unallocated_people.items():
                print("\n")
                cprint("Unallocated List of people", "red", attrs=['bold'])
                cprint("-----------------------------------------------", "white")
                if key in Amity.fellows.keys():
                    cprint(str(key) + ":" + Amity.fellows[key] + " " + "-" + value, "cyan")
                    print("\n")
                elif key in Amity.staff.keys():
                    cprint(str(key) + ":" + Amity.staff[key] + " " + "-" + value, "cyan")
                    print("\n")
            return Amity.unallocated_people

    @staticmethod
    def print_room(room_name):
        """ Method that prints the people in the room uses the Amity.rooms dict """
        if room_name in Amity.rooms:  # check if the room exists
            cprint("Room Name:" + room_name, "yellow", attrs=['bold'])
            print("-------------------------------------")

            for person in Amity.rooms[room_name]:
                if person in Amity.fellows.keys():
                    print(Amity.fellows[person])
                elif person in Amity.staff.keys():
                    print(Amity.staff[person])
            return Amity.rooms
        else:
            cprint("The room does not exist" , "red")

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
        if self.room_type.lower() in ["office", "living_space"]:  # check if the type is valid
            if self.room_name.lower() in Amity.rooms.keys():  # check if the room exists
                return "Sorry the room already exists!"

            else:
                # add the rooms to the dictionary{"room_name": [emp_1 , emp_2]}
                r_name = self.room_name.lower()
                Amity.rooms[r_name] = list()
                return "The room " + r_name + " has been created"
        else:  # when the room_type is not valid
            return "The room type is not valid"


class Office(Room):
    """ Subclass of the Room class for rooms with room_type == office.
    It use the Amity.offices list """

    def add_office(self):
        """ Append room_name to Amity.offices List """
        if self.room_type == "office":  # check if the room_type is an office
            if self.room_name.lower() in Amity.offices:  # check if the office exists
                return "That office already exists"

            else:  # append to the office list(Amity.offices)
                Amity.offices.append(self.room_name.lower())
            return "The office " + self.room_name + " has been added"
        else:
            return "You cannot enter that room"


class LivingSpace(Room):
    """ Subclass of the Room class for rooms with room_type == living_space.
    It uses the Amity.living_spaces list """

    def add_living_space(self):
        """ Appends room_name to Amity.living_spaces List """
        if self.room_type == "living_space": # check if the room_type is an office

            if self.room_name.lower() in Amity.living_spaces:
                # check if living_space exists
                return "That Living_space already exists"

            else:
                # append to the Amity.living_spaces list
                Amity.living_spaces.append(self.room_name.lower())
                return "The living space " + self.room_name + " has been added"
        else:
            return "You cannot enter that room"


class Person(Amity):
    """ Class that inherits from Amity class uses the Amity.people dict.
    Contain a dict with all the people found in Amity facility"""

    def __init__(self, first_name="none", last_name="none",
                 employee_type="none", employee_id="none", want_accomodation="n"):
        self.first_name = first_name
        self.last_name = last_name
        self.employee_type = employee_type
        self.employee_id = employee_id  # unique identifier for a person
        self.want_accomodation = want_accomodation

    def add_person(self):
        """ Adds data to the Amity.people dict """
        if self.employee_id in Amity.people.keys():
            return "Sorry an employee with the same ID already exists"
        elif self.employee_type in ["staff", "fellow"]:
            e_type = self.employee_type.lower()
            Amity.people[self.employee_id] = e_type
            return " The employee with the id '{0}' has been added ".format(self.employee_id)

        else:
            return "Invalid employee type"

    @staticmethod
    def load_from_text_file():
        """ Adds a person from a specified text file """
        src_dir = "files/"
        new_file_2 = os.path.join(src_dir, "load.txt")
        new_file = open(new_file_2)
        for add_person in new_file.readlines():
            new_person = add_person.split(' ')
            if new_person[2].lower() == 'staff':
                Person.first_name = new_person[0]
                Person.last_name = new_person[1]
                Person.employee_type = new_person[2].lower()
                Person.employee_id = new_person[3].strip('\n')
                new_staff2 = Staff(Person.first_name, Person.last_name, Person.employee_type, Person.employee_id)
                cprint(new_staff2.add_person(), "cyan", attrs=['bold'])
                # add the person to the people list
                Amity.people[Person.employee_id] = Person.employee_type

            elif new_person[2].lower() == 'fellow':

                Person.first_name = new_person[0]
                Person.last_name = new_person[1]
                Person.employee_type = new_person[2].lower()
                Person.employee_id = new_person[3]
                Person.want_accomodation = new_person[4].strip('\n')
                new_fellow2 = Fellow(Person.first_name,Person.last_name, Person.employee_type, Person.employee_id,
                                     Person.want_accomodation)
                new_fellow2.add_person()
                # add the person to the people list
                Amity.people[Person.employee_id] = Person.employee_type

            else:
                cprint("The person you are trying to add is not categorized correctly", "red", attrs=['bold'])
        return Amity.people  # return the dict with all the people


class Fellow(Person):
    """ Subclass of Person , contain all the employees with employee_type == fellow.
    Uses Amity.fellows list"""

    def __init__(self, first_name=None, last_name=None, employee_type=None,
                 employee_id=None, want_accomodation="n", office="None",
                 living_space="None"):
        Person.__init__(self, first_name, last_name, employee_type, employee_id, want_accomodation)
        self.office = office
        self.living_space = living_space

    def add_person(self):
        fellow_name = self.first_name + " " + self.last_name
        """ appends to the Amity.fellows list"""
        if self.employee_id in Amity.people.keys():
            cprint("Sorry a fellow with the same ID already exists!", "red")

        else:
            # adds the fellow to the fellow dict
            Amity.fellows[self.employee_id] = fellow_name
            if self.want_accomodation.lower() == "y":
                print('Adding fellow to office and living space ...')
                if len(Amity.offices) == 0:
                    return "There are no available offices yet , try and load state.."
                else:
                    r_name = random.choice(Amity.offices)  # choose a random office name

                    # max_capacity of an office is 6
                    if len(Amity.rooms[r_name.lower()]) < 6:
                        # assign a fellow to an office
                        Amity.rooms[r_name.lower()].append(self.employee_id)
                        cprint("The fellow has been added to {0}".format(r_name), "cyan")

                    elif len(Amity.rooms[r_name.lower()]) == 6:
                        # when the room is full , allocated the extra people to Amity.unallocated_people dict
                        cprint("the office is full placing the fellow in unallocated list..", "red", attrs=['bold'])
                        unallocated_fellows_offices = [self.employee_id]
                        for fellow in unallocated_fellows_offices:
                            Amity.unallocated_people[fellow] = "office"  # append to the Amity.unallocated_people dict

                if len(Amity.living_spaces) == 0:
                    return "There are no living spaces yet, try and load state.."

                else:
                    l_name = random.choice(Amity.living_spaces)  # choose a living space randomly

                    # max_capacity of a living_space is 4
                    if len(Amity.rooms[l_name.lower()]) < 4:
                        # assign a fellow to a living space randomly
                        Amity.rooms[l_name.lower()].append(self.employee_id)
                        cprint("The fellow has been added to {0}".format(l_name), "cyan")

                    elif len(Amity.rooms[l_name.lower()]) == 4:
                        # when the room is full , allocate the extra people to Amity.unallocated_people dict
                        cprint("the living space is full adding the fellow to the unallocated list...", 'red', attrs=['bold'])
                        unallocated_fellows_l_space = [self.employee_id]
                        for fellow in unallocated_fellows_l_space:
                            if fellow in Amity.unallocated_people.keys():
                                Amity.unallocated_people[fellow] = "office living_space"
                            else:
                                Amity.unallocated_people[fellow] = "living_space"  # append to the Amity.unallocated_people dict

            elif self.want_accomodation.lower() == "n":
                print("Adding the fellow to an office...")
                if len(Amity.offices) == 0:
                    return "There are no offices yet, try and load state.."
                else:
                    r_name = random.choice(Amity.offices)  # choose a random office name

                    # max_capacity of an office is 6
                    if len(Amity.rooms[r_name.lower()]) < 6:
                        # assign a fellow to an office
                        Amity.rooms[r_name.lower()].append(self.employee_id)
                        return "The fellow has been added"

                    elif len(Amity.rooms[r_name.lower()]) == 6:
                        # when the room is full , allocated the extra people to Amity.unallocated_people dict
                        unallocated_fellows_offices_2 = [self.employee_id]
                        for x in unallocated_fellows_offices_2:
                            Amity.unallocated_people[x] = "office"  # append to the Amity.unallocated_people dict
                        return "The fellow has been added to the unallocated_people list"

                # add the fellow to the fellows dict
                Amity.fellows[self.employee_id] = fellow_name

                return Amity.rooms, Amity.unallocated_people, Amity.fellows

    def reallocate_fellow(self, p_identifier, new_room):
        """ Reallocate the fellow to an Office or to a Living_Space"""

        # check if the fellow to be reallocated is from the unallocated dict(is not placed in any room)
        Amity.check_available_rooms()
        if p_identifier in Amity.unallocated_people.keys():
            if Amity.unallocated_people[p_identifier] == "office" and new_room in Amity.available_offices:
                Amity.rooms[new_room].append(p_identifier)  # allocate the fellow to an available office
                del Amity.unallocated_people[p_identifier]
                return "'{0}' has been reallocated to '{1}'".format(p_identifier, new_room)

            elif Amity.unallocated_people[p_identifier] == "living_space" and new_room in Amity.available_living_spaces:
                Amity.rooms[new_room].append(p_identifier)  # allocate the fellow to an available living space
                del Amity.unallocated_people[p_identifier]
                return "'{0}' has been reallocated to '{1}'".format(p_identifier, new_room)
            elif Amity.unallocated_people[p_identifier] == "office" and new_room not in Amity.available_offices:
                return "The fellow needs an office and you are reallocating to a living space"
            elif Amity.unallocated_people[p_identifier] == "living_space" and new_room not in Amity.available_living_spaces:
                return "The fellow needs a living space and you are reallocating them to an office"
            else:
                return "Sorry the fellow could not be reallocated"

        else:  # when the fellow already has already been allocated a room

            # check if the fellow is to be reallocated to an office
            if new_room in Amity.offices:
                cprint("reallocating fellow to another office...", "yellow", attrs=['bold'])
                # return a new dict with just the offices
                new_dict = {key: value for key, value in Amity.rooms.items() if key in Amity.offices}
                # Look for the person in the offices
                for room, list_of_people in new_dict.items():
                    if p_identifier in list_of_people:  # find the person in the office
                        Amity.rooms[room].remove(p_identifier)  # remove the person from the room
                        Amity.rooms[new_room].append(p_identifier)  # add them to the new room given
                        return "'{0}' has been reallocated to '{1}'".format(p_identifier, new_room)

            # check if the fellow is to be reallocated to a living_space
            elif new_room in Amity.living_spaces:
                print("reallocating fellow to a new living space...")
                # return a new dict with just the living_spaces
                new_dict2 = {key: value for key, value in Amity.rooms.items() if key in Amity.living_spaces}
                # Check for the person in the living_spaces
                for room2, list_of_people2 in new_dict2.items():
                    if p_identifier in list_of_people2:  # find the person in the living_spaces
                        Amity.rooms[room2].remove(p_identifier)  # remove the person from the living_space
                        Amity.rooms[new_room].append(p_identifier)  # add them to the new living_space
                        return "'{0}' has been reallocated to '{1}'".format(p_identifier,new_room)

            else:
                return "The room does not exist"


class Staff(Person):
    def __init__(self, first_name=None, last_name=None, employee_type=None,
                 employee_id=None, want_accomodation="n", office="None"):
        Person.__init__(self, first_name, last_name, employee_type, employee_id, want_accomodation)
        self.office = office

    def add_person(self):
        staff_name = self.first_name + " " + self.last_name
        if self.employee_id in Amity.people.keys():
            return "Sorry a staff member with the same ID already exists"
        else:
            if len(Amity.offices) == 0:
                return "Sorry there are no offices try and load state.."
            else:
                print("adding the staff to a new office...")
                # choose a random office name from the list
                office_name = random.choice(Amity.offices)

                # max_capacity of an office is 6
                if len(Amity.rooms[office_name.lower()]) < 6:
                    # assign the staff to an office
                    Amity.rooms[office_name.lower()].append(self.employee_id)
                    # append the staff to the staff dict
                    Amity.staff[self.employee_id] = staff_name

                elif len(Amity.rooms[office_name.lower()]) == 6:
                    #  when the room is full , allocated the extra people to Amity.unallocated_people dict
                    unallocated_staff = [self.employee_id]
                    for x in unallocated_staff:
                        Amity.unallocated_people[x] = "office"  # append to the Amity.unallocated_people dict
                        # append the staff to the staff dict
                    Amity.staff[self.employee_id] = staff_name

                    return "The office is full, placing the staff member in the unallocated list..."

                return"\nThe staff member '{0}' was added to the office '{1}'".format(staff_name, office_name)

    def reallocate_staff(self, p_identifier, new_office):
        Amity.check_available_rooms()
        # check if the staff to be reallocated is in the unallocated people dict
        if p_identifier in Amity.unallocated_people.keys():
            if new_office.lower() in Amity.living_spaces:
                return "A staff member can not be assigned a Living Space"
            elif new_office in Amity.available_offices:
                # check if the office is available
                Amity.rooms[new_office].append(p_identifier)
                del Amity.unallocated_people[p_identifier]
                return "The staff member with the id " + str(p_identifier) + " has been reallocated "
            else:
                return "The staff could not be reallocated check that the room is available"

        else:
            # if the staff member already has been allocated a room
            if new_office not in Amity.offices:
                return "The room does not exist!"

            elif new_office.lower() in Amity.living_spaces:
                return "A staff member can not be assigned a living space"

            elif new_office in Amity.available_offices:
                print("reallocating the staff to a new office...")
                # Look for the person in the offices
                for room, list_of_people in Amity.rooms.items():
                    if p_identifier in list_of_people:  # find the person in the rooms
                        list_of_people.remove(p_identifier)  # remove the person from the room
                        Amity.rooms[new_office].append(p_identifier)  # add them to a new room
                return "'{0}' has been reallocated to '{1}'".format(p_identifier, new_office)

            elif new_office not in Amity.available_offices:
                return "Sorry the room is full"



        return Amity.rooms
