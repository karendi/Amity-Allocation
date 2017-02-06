import sys
from StringIO import StringIO
from mock import patch

import unittest
from functions.amity_class import Amity, Room, Office, Living_Space, Person, Fellow, Staff


class Test_Amity(unittest.TestCase):
    """ Tests for the amity_class.Amity class methods"""
    def setUp(self):
        self.amity = Amity()
        self.office = Room("Taveta", "office")
        self.living_space = Room("Ian", "living_space")
        self.test_staff = Person("Charles","Muthini", "staff", 67, "y")

    def test_check_available_rooms(self):
        """ Tests if the offices are not filled to capacity """
        self.amity.check_available_rooms()
        no_of_ls_before = len(self.amity.living_spaces)
        self.living_space.create_room()
        self.amity.check_available_rooms()
        no_of_ls_after = len(self.amity.available_offices)
        self.assertNotEqual(no_of_ls_after, no_of_ls_before, msg="There is an available living space")

    def test_print_room(self):
        """ Tests the print room function """
        self.amity.rooms = {} # when there are no rooms
        assert "The room does not exist" == self.amity.print_room("Kindaruma")

    def tearDown(self):
        del self.amity
        del self.office
        del self.living_space
        del self.test_staff


class TestRoom(unittest.TestCase):
    """ Tests for the amity_class.Room class """

    def setUp(self):
        self.amity = Amity()
        self.room = Room("Krypton", "office")
        self.room_2 = Room("Sharon", "living_space")

    def test_create_room_method(self):
        """ Test if the room is created when the create room method is called"""

        number_of_rooms = len(self.amity.rooms)
        self.room.create_room()
        current_rooms = len(self.amity.rooms)
        self.assertEqual(current_rooms, number_of_rooms + 1, msg="The room has been added")

    def test_if_room_exists(self):
        """ Test if the room added already exists ,the name of the room is unique"""
        self.room.create_room()
        self.assertNotIn(self.room.room_name, self.amity.rooms.keys(), msg="The room does not exist!")

    def test_office_maximum_capacity(self):
        """ Test if an office has more than 6 people"""
        self.room.create_room()
        no_of_people = len(self.amity.rooms[self.room.room_name.lower()])
        self.assertNotEqual(no_of_people, 6, msg="The max number of people an office can hold is 6")

    def test_living_space_max_capacity(self):
        """ Test if a living_space has more than 4 people """
        self.room_2.create_room()
        no_of_people = len(self.amity.rooms[self.room.room_name.lower()])
        self.assertNotEqual(no_of_people, 4, msg="The max number of people an office can hold is 6")

    def tearDown(self):
        del self.amity
        del self.room
        del self.room_2



class Test_Office(unittest.TestCase):
    """ Tests for the amity_class.Office """
    def setUp(self):
        self.amity = Amity()
        self.office = Office("Snow", "office")

    def test_if_add_office_works(self):
        """ Test if the add_office method works"""

        number_of_offices_before = len(self.amity.offices)
        self.office.add_office()
        number_of_offices_after = len(self.amity.offices)
        self.assertNotEqual(number_of_offices_after, number_of_offices_before, msg="The office has been added")

    def test_if_office_exists(self):
        """ Tests if the office to be added already exists """

        self.office.add_office()
        self.assertNotIn(self.office.room_name , self.amity.offices , msg = "The office does not already exist")

    def tearDown(self):
        del self.amity
        del self.office


class TestLiving_Space(unittest.TestCase):
    """ Tests for the amity_class.Living_Space"""
    def setUp(self):
        self.amity = Amity()
        self.living_s = Living_Space("Laravel", "living_space")

    def test_if_add_living_space_works(self):
        """ Test if the add_living_space method works """

        number_of_ls_before = len(self.amity.living_spaces)
        self.living_s.add_living_space()
        number_of_ls_after = len(self.amity.living_spaces)
        self.assertEqual(number_of_ls_after, number_of_ls_before + 1, msg="The living_space has been added")

    def test_if_living_space_exists(self):
        """ Tests if the living_space to be added already exists """

        self.living_s.add_living_space()
        self.assertNotIn(self.living_s.room_name, self.amity.living_spaces, msg="The living space does not exist yet")

    def tearDown(self):
        del self.amity
        del self.living_s


class TestPerson(unittest.TestCase):
    """ Tests for the amity_class.Person"""

    def setUp(self):
        self.test_person = Person()
        self.amity = Amity()
        self.new_person = Person("Sharon", "Wanjiku", "staff", 30390)
        self.new_room2 = Room("Hogwarts", "office")
        self.new_room3 = Room("Laravel", "living_space")

    def test_wrong_input(self):
        """ Test if the data entered is in the correct format"""

        self.assertIsInstance(self.new_person, Person, msg="You have to enter data in the correct format")

    def test_if_person_exists(self):
        """ Test if the employee to be added already exists ,
        the employee_id of the room is unique"""
        self.new_person.add_person()
        self.assertIn(self.new_person.employee_id, self.amity.people.keys(), msg="The person already exist")

    def test_if_add_person_method_works(self):
        """ Test if the add_person method works """

        self.amity.offices = ['hogwarts', 'shire']
        no_of_people_before = len(self.amity.people)
        self.new_person.add_person()
        no_of_people_after = len(self.amity.people)
        self.assertEqual(no_of_people_after, no_of_people_before+1, msg="The person has been added")

    def test_load_from_text_file(self):
        """ Tests if adding from text file method works """
        self.new_room2.create_room()
        self.new_room3.create_room()
        len_of_people_before = len(self.amity.people)
        self.test_person.load_from_text_file()
        len_of_people_after = len(self.amity.people)
        self.assertNotEqual(len_of_people_after, len_of_people_before, msg="A person was added")

    def tearDown(self):
        del self.test_person
        del self.amity
        del self.new_person
        del self.new_room2
        del self.new_room3

class TestFellow(unittest.TestCase):
    """ Tests for the amity_class.Fellow class """
    def setUp(self):
        self.room = Room("Sharon", "office")
        self.office = Office('Sharon', 'office')
        self.new_fellow = Fellow("Kim", "Tim", "fellow", 4509)

    def test_if_fellow_exists(self):
        """ Tests if the fellow to be added already exists.
        The employee_id is the unique identifier """

        self.office.add_office()
        self.new_fellow.add_person()
        self.assertNotIn(self.new_fellow.employee_id, Amity.people.keys(), msg="The fellow doesnot exist yet")

    def test_add_person_in_fellow_class(self):
        """ Tests if the add_person method in the Fellow class works """
        self.room.create_room()
        self.office.add_office()
        no_of_fellows_before = len(Amity.fellows)
        self.new_fellow.add_person()
        no_of_fellows_after = len(Amity.fellows)
        self.assertEqual(no_of_fellows_after, no_of_fellows_before + 1, msg="The fellow has been added")

    def tearDown(self):
        del self.room
        del self.office
        del self.new_fellow


class TestStaff(unittest.TestCase):
    """ Tests for amity_class.Staff class """
    def setUp(self):
        self.new_office2 = Room("Sharon", "office")  # there must be a room created before adding a person
        self.amity = Amity()
        self.new_staff = Staff("Lydia", "Nyawira", "staff", 9001)

    def test_if_staff_exists(self):
        """ Test if the staff being added already exists.
        The employee_id is the unique identifier """
        self.new_office2.create_room()
        self.new_staff.add_person()
        self.assertNotIn(self.new_staff.employee_id, self.amity.people.keys(),
                         msg="The staff member does not already exists")

    def tearDown(self):
        del self.new_office2
        del self.amity
        del self.new_staff
