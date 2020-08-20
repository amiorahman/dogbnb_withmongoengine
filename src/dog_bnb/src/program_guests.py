from colorama import Fore
from infrastructure.switchlang import switch
import services.data_service as svc
import program_hosts as hosts
import infrastructure.state as state


def run():
    print(' ****************** Welcome Guest **************** ')
    print()

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_a_dog)
            s.case('y', view_your_dogs)
            s.case('b', book_a_room)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[B]ook a Room')
    print('[A]dd a Dog')
    print('View [y]our dogs')
    print('[V]iew your bookings')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_a_dog():
    print(' ****************** Add a Dog **************** ')

    if not state.active_account:
        error_msg("You must login to continue.")
        return

    dog_name = input("Enter your Dog's name: ")
    if not dog_name:
        error_msg("Dog name can not be empty!")
        return

    length = float(input("Enter your dog's length (In Meters): "))
    weight = float(input("Enter your dog's weight (In KGs): "))
    species = input("Enter your dog's species: ")
    is_barking = input("Is your dog aa barker? [y, n]: ").lower().startswith('y')

    new_dog = svc.add_dog(state.active_account, dog_name,
                          length, weight,
                          species, is_barking)

    success_msg("You Dog {} with ID {} has been added!".format(new_dog.name, new_dog.id))

    state.reload_account()


def view_your_dogs():
    print(' ****************** Your Dogs **************** ')

    if not state.active_account:
        error_msg("You must login to continue.")
        return

    dogs = svc.find_dogs_for_user(state.active_account)

    print(f"You have {len(dogs)} dogs registered.")
    for index, dog in enumerate(dogs):
        print(" * Dog {}: {} is a {} and {} a barker".format(
            index + 1, dog.name, dog.species,
            '' if dog.is_barking else 'not'
        ))


def book_a_room():
    print(' ****************** Book a Room for your Dog **************** ')
    # TODO: Require an account
    # TODO: Verify they have a snake
    # TODO: Get dates and select snake
    # TODO: Find cages available across date range
    # TODO: Let user select cage to book.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_bookings():
    print(' ****************** Your bookings **************** ')
    # TODO: Require an account
    # TODO: List booking info along with snake info

    print(" -------- NOT IMPLEMENTED -------- ")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
