import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Amity_Allocation, Base


class TestDatabaseSessions(unittest.TestCase):
    """ Test for the database sessions """
    engine = create_engine('sqlite:///amity_allocation.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        # Connect to the database and create the schema within a transaction
        Base.metadata.create_all(self.engine)
        self.session.add(Amity_Allocation(id=100, Room_name="Kinda", Allocated_People=None))
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_add_room_to_database(self):
        pass
