"""
Usage:
    interface.py create_room <room_name> <room_type>
    interface.py add_person <First_name> <Last_name> <E_Type> <want_accomodation>
    interface.py save_state [--db=sqlite_database]
    interface.py quit
    interface.py check_data
    interface.py load_state <database>
    interface.py reallocate_person <employee_id> <room_name>
    interface.py load_from_text_file
    interface.py print_allocations [--o=file_name]
    interface.py print_unallocated
    interface.py print_room <room_name>


Arguments:
    <room_name> The name of the created room
    <First_name> The first name of the employee
    <Middle_name> The employee's middle name
    <Last_name> The employee's Last name
    <database> Database name
    <Employee_type> The employee  can either be FELLOW|STAFF
    <want_accommodation> For FELLOWS only can either be YES|NO(Y|N)
    [--o=file_name] Optional text file , where you can print allocations to
Options:
    -h , --help , Show this screen and exit

"""


from docopt import docopt, DocoptExit
import cmd
from functions import amity_class
from functions import sessions
from models import create_db


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def definition():
    print("This program is supposed to help allocate space to Amity's empolyees")
    print("the space can either be an office or Living_Space")
    print("------------------------------------------------------")
    print("\n")
    print(__doc__)


class Amity(cmd.Cmd):
    prompt = '<Amity_allocation>'

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name> <room_type> """

        room_name = arg['<room_name>']
        room_type = arg['<room_type>']

        if room_type.lower() == "office":
            added_office = amity_class.Office(room_name.lower(), room_type)
            print(added_office.add_office())

        elif room_type.lower() == "living_space":
            added_living_space = amity_class.Living_Space(room_name.lower(), room_type)
            print(added_living_space.add_living_space())
        else:
            print("That room category does not exist!")

        added_room = amity_class.Room(room_name.lower(), room_type)
        print(added_room.create_room())

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <First_name> <Last_name> <E_Type> <Employee_No> <want_accommodation>"""
        f_name = arg['<First_name>']
        l_name = arg['<Last_name>']
        e_type = arg['<E_Type>']
        e_id = int(arg['<Employee_No>'])
        a_status = arg['<want_accommodation>']

        if e_type.lower() == "fellow":
            # append the employee id to a list with fellows
            added_fellow = amity_class.Fellow(f_name, l_name, e_type, e_id, a_status)
            print(added_fellow.add_person())

        elif e_type.lower() == "staff":
            # append the employee id to a list with staff members
            a_status = "n"  # default for a staff member

            added_staff = amity_class.Staff(f_name, l_name, e_type, e_id)
            print(added_staff.add_person())

        # add the person to the amity population dictionary
        new_person = amity_class.Person(f_name, l_name, e_type, e_id)
        print(new_person.add_person())

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        db_name = arg['--db']

        if db_name is None:
            db_name = "amity_allocation.db"
            create_db(db_name)
            database_object = sessions.Database_sessions(db_name)
            print(database_object.add_person())
            print(database_object.add_room())
            print(database_object.add_office())
            print(database_object.add_living_space())
            print(database_object.add_fellows())
            print(database_object.add_staff())

        else:
            create_db(db_name)
            database_object = sessions.Database_sessions(db_name)
            print(database_object.add_person())
            print(database_object.add_room())
            print(database_object.add_office())
            print(database_object.add_living_space())
            print(database_object.add_fellows())
            print(database_object.add_staff())

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <database>"""
        database_name = arg['<database>']
        database_object2 = sessions.Database_sessions(database_name)
        database_object2.return_rooms()
        database_object2.return_offices()
        database_object2.return_living_spaces()
        database_object2.return_fellows()
        database_object2.return_staff()
        database_object2.return_population()

    @docopt_cmd
    def do_check_data(self, arg):
        """Usage: check_data"""
        print(sessions.check_data())

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <employee_id> <room_name>"""
        person_identifier = int(arg['<employee_id>'])
        room_name = arg['<room_name>']
        # test the employee type of the person
        if person_identifier in amity_class.Amity.staff:
            to_be_reallocated = amity_class.Staff()
            print(to_be_reallocated.reallocate_staff(person_identifier, room_name))

        elif person_identifier in amity_class.Amity.fellows:
            fellow_to_be_allocated=amity_class.Fellow()
            print(fellow_to_be_allocated.reallocate_fellow(person_identifier, room_name))

        elif person_identifier not in amity_class.Amity.people.keys():
            print("Sorry you cannot reallocate an employee who has not been saved ")


    @docopt_cmd
    def do_load_from_text_file(self, arg):
        """ Usage: load_from_text_file """
        person_from_text_file = amity_class.Person()
        print(person_from_text_file.load_from_text_file())

    @docopt_cmd
    def do_print_allocations(self, arg):
        """ Usage: print_allocations [--o=file_name]"""
        file_name = arg['--o']
        if file_name is None:
            amity_class.Amity.print_allocations()
        else:
            print(file_name)

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_room <room_name>"""
        r_name = arg['<room_name>']
        amity_class.Amity.print_room(r_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """ Usage: print_unallocated"""
        amity_class.Amity.print_unallocated_people()

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        exit()


if __name__ == "__main__":
    definition()
    Amity().cmdloop()
