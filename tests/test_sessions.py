import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functions.amity_class import Amity
from models import Amity_Allocation, Amity_Population , Amity_Living_space ,Base
from functions.sessions import Database_sessions


class TestDatabaseSessions(unittest.TestCase):
    """ Test for the database sessions """
    engine = create_engine('sqlite:///amity_allocation.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        # Connect to the database and create the schema within a transaction
        Base.metadata.create_all(self.engine)
        self.amity = Amity.rooms
        self.database_session_instance = Database_sessions("amity_allocation")
        self.add_rooms = self.database_session_instance.add_room()


    def test_add_a_room_to_the_database(self):
        no_of_rooms_before = self.session.query(Amity_Allocation).count()
        self.amity = { "Arizona":[],}
        self.add_rooms
        self.session.commit()
        no_of_rooms_after = self.session.query(Amity_Allocation).count()
        self.assertEqual(no_of_rooms_after , no_of_rooms_before + 1)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
