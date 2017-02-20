"""
Usage:
    interface.py create_room <room_name>...
    interface.py add_person <First_name> <Last_name> <E_Type> <want_accomodation>
    interface.py save_state [--db=sqlite_database]
    interface.py quit
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

import cmd
import os.path

from docopt import docopt, DocoptExit
from termcolor import cprint, colored
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
    greetings = os.environ.get('SECRET_KEY')
    print(greetings)
    print("This program is supposed to help allocate space to Amity's empolyees")
    print("the space can either be an office or Living_Space")
    print("------------------------------------------------------")
    print("\n")
    print(__doc__)


class Amity(cmd.Cmd):
    prompt = '<Amity_allocation>'

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name>..."""

        room_name = arg['<room_name>']

        if room_name[-1].lower() == "office":
            for off in room_name[:-1]:
                added_office = amity_class.Office(off.lower(), "office")
                print("\n")
                cprint(added_office.add_office(), 'cyan', attrs=['bold'])
                added_room = amity_class.Room(off.lower(), "office")
                cprint(added_room.create_room(), 'magenta', attrs=['bold'])
                print("\n")

        elif room_name[-1].lower() == "living_space":
            for l_space in room_name[:-1]:
                added_living_space = amity_class.LivingSpace(l_space.lower(), "living_space")
                print("\n")
                cprint(added_living_space.add_living_space(), 'yellow', attrs=['bold'])
                added_room = amity_class.Room(l_space.lower(), "living_space")
                cprint(added_room.create_room(), 'magenta', attrs=['bold'])
                print("\n")
        else:
            print("\n")
            cprint("That room category does not exist!", 'red', attrs=['bold'])
            print("\n")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <First_name> <Last_name> <E_Type> <Employee_No> <want_accommodation>"""
        f_name = arg['<First_name>']
        l_name = arg['<Last_name>']
        e_type = arg['<E_Type>']
        e_id = arg['<Employee_No>']
        a_status = arg['<want_accommodation>']

        if len(amity_class.Amity.rooms) != 0:
            if e_type.lower() == "fellow":
                # append the employee id to a list with fellows
                added_fellow = amity_class.Fellow(f_name, l_name, e_type, e_id, a_status)
                print("\n")
                added_fellow.add_person()

            elif e_type.lower() == "staff":
                # append the employee id to a list with staff members
                a_status = "n"  # default for a staff member
                print("\n")
                added_staff = amity_class.Staff(f_name, l_name, e_type, e_id, a_status)
                added_staff.add_person()

            # add the person to the amity population dictionary
            new_person = amity_class.Person(f_name, l_name, e_type, e_id)
            cprint(new_person.add_person(), "red")
            print("\n")
        else:
            print(" \n You must create rooms first! \n")



    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        db_name = arg['--db']

        if db_name is None:
            db_name = "amity_default"
            create_db(db_name)
            database_object = sessions.DatabaseSessions(db_name)
            cprint(database_object.add_person(), "cyan")
            cprint(database_object.add_room(), "cyan")
            cprint(database_object.add_office(), "cyan")
            cprint(database_object.add_living_space(), "cyan")
            cprint(database_object.add_fellows(), "cyan")
            cprint(database_object.add_staff(), "cyan")
            cprint(database_object.add_unallocated(), "cyan")

        else:
            create_db(db_name)
            database_object = sessions.DatabaseSessions(db_name)
            cprint(database_object.add_person(), "cyan")
            cprint(database_object.add_room(), "cyan")
            cprint(database_object.add_office(), "cyan")
            cprint(database_object.add_living_space(), "cyan")
            cprint(database_object.add_fellows(), "cyan")
            cprint(database_object.add_staff(), "cyan")
            cprint(database_object.add_unallocated(), "cyan")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <database>"""
        database_name = arg['<database>']
        # check if the database exists
        if os.path.exists("./databases/" + database_name + ".db"):
            print("\n")
            database_object2 = sessions.DatabaseSessions(database_name)
            database_object2.return_rooms()
            database_object2.return_offices()
            database_object2.return_living_spaces()
            database_object2.return_fellows()
            database_object2.return_staff()
            database_object2.return_population()
            database_object2.return_unallocated()
            print("\n")
        else:
            print("\n")
            cprint("The database doesn't exist!", "red", attrs=['bold'])
            print("\n")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <employee_id> <room_name>"""
        person_identifier = arg['<employee_id>']
        room_name = arg['<room_name>']
        # test the employee type of the person
        if person_identifier in amity_class.Amity.staff.keys():
            to_be_reallocated = amity_class.Staff()
            print("\n")
            cprint(to_be_reallocated.reallocate_staff(person_identifier, room_name), "cyan", attrs=['bold'])
            print("\n")

        elif person_identifier in amity_class.Amity.fellows.keys():
            fellow_to_be_allocated=amity_class.Fellow()
            print("\n")
            cprint(fellow_to_be_allocated.reallocate_fellow(person_identifier, room_name), "cyan", attrs=['bold'])
            print("\n")

        elif person_identifier not in amity_class.Amity.people.keys():
            print("\n Sorry you cannot reallocate an employee who has not been saved \n")

    @docopt_cmd
    def do_load_from_text_file(self, arg):
        """ Usage: load_from_text_file """
        if len(amity_class.Amity.rooms) != 0:
            person_from_text_file = amity_class.Person()
            print("\n")
            person_from_text_file.load_from_text_file()
            print("\n")
        else:
            print("\n")
            cprint("\n You have to have/create rooms first! \n", 'red', attrs=['bold'])
            print("\n")

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
        if len(amity_class.Amity.unallocated_people) == 0:
            print("\n")
            cprint("There are no people in the unallocated list", "red", attrs=['bold'])
            print("\n")
        amity_class.Amity.print_unallocated_people()


    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        exit()


if __name__ == "__main__":
    definition()
    Amity().cmdloop()
