"""
Usage:
    interface.py create_room <room_name> <room_type>
    interface.py add_person <First_name> <Last_name> <E_Type> <want_accomodation>
    interface.py save_state
    interface.py quit
    interface.py check_data
    interface.py load_state


Arguments:
    <room_name> The name of the created room
    <First_name> The first name of the employee
    <Middle_name> The emloyee's middle name
    <Last_name> The emloyee's Last name
    <Employee_type> The employee  can either be FELLOW|STAFF
    <want_accomodation> For FELLOWS only can either be YES|NO(Y|N)
Options:
    -h , --help , Show this screen and exit

"""


from docopt import docopt , DocoptExit
import cmd
from functions import amity_class
from functions import sessions




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

class Amity(cmd.Cmd):
    prompt = '<Amity_allocation>'

    @docopt_cmd
    def do_create_room(self , arg):
        """Usage: create_room <room_name> <room_type> """

        room_name = arg['<room_name>']
        room_type = arg['<room_type>']

        if room_type.lower() == "office":
            added_office = amity_class.Office(room_name , room_type)
            print(added_office.add_office())

        elif room_type.lower() == "living_space":
            added_living_space = amity_class.Living_Space(room_name , room_type)
            print(added_living_space.add_living_space())

        added_room = amity_class.Room(room_name , room_type)
        print(added_room.create_room())

    @docopt_cmd
    def do_add_person(self , arg):
        """Usage: add_person <First_name> <Last_name> <E_Type> <Employee_No> <want_accomodation>"""
        f_name = arg['<First_name>']
        l_name = arg['<Last_name>']
        e_type = arg['<E_Type>']
        e_id = arg['<Employee_No>']
        a_status = arg['<want_accomodation>']

        if e_type.lower() == "fellow":
             #append the employee id to a list with fellows
             added_fellow = amity_class.Fellow(f_name , l_name , e_type , e_id , a_status)
             print(added_fellow.add_person())

        elif e_type.lower() == "staff":
             #append the employee id to a list with staff members
             a_status = "n" #default for a staff member

             added_staff = amity_class.Staff(f_name , l_name , e_type , e_id)
             print(added_staff.add_person())


        #add the person the amity population dictionary
        new_person = amity_class.Person(f_name , l_name , e_type , e_id)
        print(new_person.add_person())



    @docopt_cmd
    def do_save_state(self , arg):
        """Usage: save_state"""
        print(sessions.add_person())
        print(sessions.add_room())
        print(sessions.add_office())
        print(sessions.add_living_space())

    @docopt_cmd
    def do_load_state(self , arg):
        """Usage: load_state"""

        print(sessions.return_rooms())
        print(sessions.return_offices())
        print(sessions.return_living_spaces())

    @docopt_cmd
    def do_check_data(self , arg):
        """Usage: check_data"""
        print(sessions.check_data())




    @docopt_cmd
    def do_quit(self , arg):
        """Usage: quit"""
        exit()



if __name__ == "__main__" :
    definition()
    Amity().cmdloop()
