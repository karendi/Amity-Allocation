import unittest
from functions.amity_class import Amity, Room, Office, LivingSpace, Person, Fellow, Staff


class Test_Amity(unittest.TestCase):
    """ Tests for the amity_class.Amity class methods"""
    def setUp(self):
        self.amity = Amity()
        self.office = Room("Taveta", "office")
        self.office_2 = Office("Taveta", "office")
        self.living_space = Room("Ian", "living_space")
        self.living_space_2 = LivingSpace("Ian", "living_space")
        self.test_staff = Person("Charles","Muthini", "staff", 67, "y")

    def test_check_available_rooms(self):
        """ Tests if the offices are not filled to capacity """
        self.amity.check_available_rooms()
        no_of_livingspaces_before = len(self.amity.available_living_spaces)
        self.living_space.create_room()
        self.living_space_2.add_living_space()
        self.amity.check_available_rooms()
        no_of_living_spaces_after = len(self.amity.available_living_spaces)
        self.assertNotEqual(no_of_living_spaces_after, no_of_livingspaces_before, msg="There is an available living space")

    def test_unavailable_rooms(self):
        self.amity.check_available_rooms()
        no_of_offices_before = len(self.amity.available_offices)
        self.office.create_room()
        self.office_2.add_office()
        self.amity.check_available_rooms()
        no_of_offices_after = len(self.amity.available_offices)
        self.assertNotEqual(no_of_offices_after , no_of_offices_before, msg="There is an available office")

    def test_print_allocations_when_there_are_no_unallocated_people(self):
        results = self.amity.print_allocations()
        self.assertNotEqual(results, "There are no allocations yet to be printed")

    def test_print_room(self):
        """ Test that a room is printed """
        results = self.amity.print_room("krypton")
        self.assertIn("krypton", self.amity.rooms.keys())

    def tearDown(self):
        del self.amity
        del self.office
        del self.office_2
        del self.living_space
        del self.living_space_2
        del self.test_staff


class TestRoom(unittest.TestCase):
    """ Tests for the amity_class.Room class """

    def setUp(self):
        self.amity = Amity()
        self.room = Room("Krypton", "office")
        self.room_2 = Room("Sharon", "living_space")
        self.invalid_room = Room("Lilac", "library")

    def test_create_room_method(self):
        """ Test if the room is created when the create room method is called"""
        new_test_room = Room("nandia", "office")
        new_test_room.create_room()
        self.assertIn(new_test_room.room_name, self.amity.rooms.keys())

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

    def test_create_invalid_room(self):
        """ Create a room with an invalid room_type"""
        results = self.invalid_room.create_room()
        self.assertEqual(results, "The room type is not valid")

    def tearDown(self):
        del self.amity
        del self.room
        del self.room_2


class Test_Office(unittest.TestCase):
    """ Tests for the amity_class.Office """
    def setUp(self):
        self.amity = Amity()
        self.office = Office("Snow", "office")
        self.office_2 = Office("Snow", "library")

    def test_if_add_office_method_works(self):
        """ Test if the add_office method works"""
        new_test_office=Office("php", "office")
        new_test_office.add_office()
        self.assertIn(new_test_office.room_name, self.amity.offices)

    def test_for_invalid_office_type(self):
        """ Tests if the office to be added has an invalid room_type """
        results = self.office_2.add_office()
        self.assertEqual(results, "You cannot enter that room")

    def tearDown(self):
        del self.amity
        del self.office
        del self.office_2


class TestLiving_Space(unittest.TestCase):
    """ Tests for the amity_class.LivingSpace"""
    def setUp(self):
        self.amity = Amity()
        self.living_s = LivingSpace("Laravel", "living_space")
        self.invalid_living_space = LivingSpace("Laravely", "hotel")

    def test_if_add_living_space_works(self):
        """ Test if the add_living_space method works """
        new_test_living_space = LivingSpace("amber","living_space")
        new_test_living_space.add_living_space()
        self.assertIn(new_test_living_space.room_name, self.amity.living_spaces)

    def test_if_living_space_exists(self):
        """ Tests if the living_space to be added already exists """

        self.living_s.add_living_space()
        self.assertNotIn(self.living_s.room_name, self.amity.living_spaces, msg="The living space does not exist yet")
    def test_if_living_space_is_invalid(self):
        """ Tests if the living_space to be added has invalid room_type """
        results = self.invalid_living_space.add_living_space()
        self.assertEqual(results, "You cannot enter that room")

    def tearDown(self):
        del self.amity
        del self.living_s


class TestPerson(unittest.TestCase):
    """ Tests for the amity_class.Person"""

    def setUp(self):
        self.test_person = Person()
        self.amity = Amity()
        self.new_person = Person("Sharon", "Wanjiku", "staff", 30390)
        self.new_staff = Staff("Sharon", "Wanjiku", "staff", 30390)
        self.new_room2 = Room("hogwarts", "office")
        self.new_room3 = Room("Laravel", "living_space")
        self.new_test_office = Office("hogwarts", "office")

    def test_if_person_exists(self):
        """ Test if the employee to be added already exists ,
        the employee_id of the room is unique"""
        self.new_person.add_person()
        self.assertIn(self.new_person.employee_id, self.amity.people.keys(), msg="The person already exist")

    def test_if_add_person_method_works(self):
        """ Test if the add_person method works """
        self.new_room2.create_room()
        self.new_test_office.add_office()
        self.new_staff.add_person()
        self.new_person.add_person()
        self.assertIn(self.new_person.employee_id, self.amity.people.keys())

    def tearDown(self):
        del self.test_person
        del self.amity
        del self.new_person
        del self.new_room2
        del self.new_room3

class TestFellow(unittest.TestCase):
    """ Tests for the amity_class.Fellow class """
    def setUp(self):
        self.room = Room("php", "office")
        self.office = Office('php', 'office')
        self.new_fellow = Fellow("Kim", "Tim", "fellow", 4509, "n")
        self.new_fellow_2 = Fellow("Sharon", "Njihia", "fellow", 4509, "n")

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
        results = self.new_fellow.add_person()
        self.assertEqual(results, "The fellow has been added")

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
