import unittest
from functions.amity_class import Amity, Room , Office , Living_Space , Person , Fellow , Staff

class TestRoom(unittest.TestCase):
    """ Tests for the amity_class.Room class """
    def test_create_room_method(self):
        """ Test if the room is created when the create room method is called"""
        Amity.rooms = {"Ken" : [] , "Hogwarts" :[]} #dictionary with the rooms in Amity
        test_room = Room("Sharon" , "living_space")
        test_room.create_room()
        self.assertIn(test_room.room_name , Amity.rooms.keys() , msg="The room has not been added")

    def test_wrong_input(self):
        """ Test if the data entered is in the correct format"""
        self.assertEqual(Room(1 , 2) , Room("Sharon" , "Office"),msg= "You have to enter data in the correct form")

    def test_if_room_exists(self):
        """ Test if the room added already exists ,the name of the room is unique"""
        test_room = Room("Sharon" , "office")
        Amity.rooms = { "Sharon":[] , "Henry": [] }
        self.assertNotIn(test_room.room_name , Amity.rooms.keys() , msg = "The room already exists!")

    def test_office_maximum_capacity(self):
        """ Test if an office has more than 6 people"""
        office1 = Room("Joy" , "office")
        Amity.rooms ={"Joy": [12 , 132 , 56 , 57 , 12 ,11 ,45]}
        no_of_people = len(Amity.rooms["Joy"])
        self.assertEqual(no_of_people , 6 , msg="The maximum number an office can hold is 6")

    def test_living_space_max_capacity(self):
        """ Test if a living_space has more than 4 people """
        living_space1 = Room("Peace" , "living_space")
        Amity.rooms = {"Peace":[1 , 2 , 34 ,56 , 78]}
        no_of_people = len(Amity.rooms["Peace"])
        self.assertEqual(no_of_people , 4 , msg="The maximum number a living_space can hold is 4")

class Test_Office(unittest.TestCase):
    """ Tests for the amity_class.Office """
    def test_if_add_office_works(self):
        """ Test if the add_office method works"""
        Amity.offices = ["Hogwarts" , "Snow"] # List of all the offices in Amity
        test_office = Office("Shire" , "office") #instance of the office class
        test_office.add_office()
        self.assertIn( test_office.room_name , Amity.offices , msg = "The office has not been added yet")

    def test_if_office_exists(self):
        """ Tests if the office to be added already exists """
        test_office = Office("Hogwarts" , "office")
        Amity.offices = ["Hogwarts" , "Kindaruma"]
        self.assertNotIn(test_office.room_name , Amity.offices , msg = "The office already exists")

class TestLiving_Space(unittest.TestCase):
    """ Tests for the amity_class.Living_Space"""

    def test_if_add_living_space_works(self):
        """ Test if the add_living_space method works """
        Amity.living_spaces = ["Ken" , "Lood"]
        test_living_space = Living_Space("Oliver" , "living_space")
        test_living_space.add_living_space()
        self.assertIn(test_living_space.room_name , Amity.living_spaces , msg ="The living_space has not been added")

    def test_if_living_space_exists(self):
        """ Tests if the living_space to be added already exists """
        Amity.living_spaces = ["Peace" , "Joy"]
        test_living_space = Living_Space("Peace" , "living_space")
        test_living_space.add_living_space()
        self.assertNotIn(test_living_space.room_name , Amity.living_spaces , msg = "The living_space already exists")

class TestPerson(unittest.TestCase):
    """ Tests for the amity_class.Person"""

    def test_wrong_input(self):
        """ Test if the data entered is in the correct format"""

        self.assertEqual(Person(1 , 2 , 3 ,"Laravel") ,Person("Sharon", "Njihia" ,"fellow" , 98),
        msg= "You have to enter data in the correct format")

    def test_if_person_exists(self):
        """ Test if the employee to be added already exists ,
        the employee_id of the room is unique"""

        test_person = Person("Sharon", "Njihia" ,"fellow" , 98)
        Amity.people = { 98:"Fellow"  }
        self.assertNotIn(test_person.employee_id , Amity.people.keys() , msg = "The person already exists!")

    def test_if_add_person_method_works(self):
        """ Test if the add_person method works """
        Amity.people = {2345 : "fellow" , 456 : "staff"} #dictionary that holds all the employees{emp_id:emp_type}
        test_person = Person("Sharon" , "Njihia" , "fellow" , 567 ) #instance of the person class
        test_person.add_person()
        self.assertNotIn(test_person.employee_id , Amity.people.keys() , msg ="The person was not created!")

class TestFellow(unittest.TestCase):
    """ Tests for the amity_class.Fellow class """

    def test_if_fellow_exists(self):
        """ Tests if the fellow to be added already exists.
        The employee_id is the unique identifier """

        test_fellow = Fellow("Sharon", "Njihia" ,"fellow" , 98)
        Amity.fellows =[ 98 , 45]
        self.assertNotIn(test_fellow.employee_id , Amity.fellows , msg = "The fellow already exists!")

class TestStaff(unittest.TestCase):
    """ Tests for amity_class.Staff class """

    def test_if_staff_exists(self):
        """ Test if the staff being added already exists.
        The employee_id is the unique identifier """

        test_staff = Staff("Joy" , "Njihia" , "staff" , 198)
        Amity.staff = [ 65, 45 , 198]
        self.assertNotIn(test_staff.employee_id , Amity.staff , msg = "The staff member already exists")
