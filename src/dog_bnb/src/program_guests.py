from colorama import Fore
from dateutil import parser
import datetime
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

    if not state.active_account:
        error_msg("You must login to continue.")
        return

    dogs = svc.find_dogs_for_user(state.active_account)
    if not dogs:
        error_msg("You must add a dog first to book a room for you pet!")
        add_a_dog()

    print("Find rooms by availability....")
    checkin = parser.parse(input("Enter Checkin Date [yyyy-mm-dd]: "))
    if not checkin:
        error_msg("Checkin date can not be empty.")
        return

    checkout = parser.parse(input("Enter Checkout Date [yyyy-mm-dd]: "))
    if not checkout:
        error_msg("Checkout date can not be empty.")
        return

    if checkin >= checkout:
        error_msg("Checkout is not possible before checking in.")
        return

    for index, dog in enumerate(dogs):
        print(" * Dog {}: {} is a {} and {} a barker".format(
            index + 1, dog.name, dog.species,
            '' if dog.is_barking else 'not'
        ))

    selected_dog = dogs[int(input("Choose dog to book a room for: ")) - 1]
    rooms = svc.get_available_rooms(checkin, checkout, selected_dog)

    print(f"{len(rooms)} rooms found in the specified time.")
    for index, room in enumerate(rooms):
        print(" {}. {} with size {}, {} carpeted and {} toys.".format(
            index + 1, room.name, room.square_meters,
            '' if room.is_carpeted else 'not',
            'has' if room.has_toys else 'no'
        ))

    if not rooms:
        error_msg("Sorry, no rooms available in your specified dates.")
        return

    selected_room = rooms[int(input("Select a room to book:")) - 1]
    svc.book_room(state.active_account, checkin, checkout,
                  selected_dog, selected_room)

    success_msg("Booking succesfull for {} in {} for €{}/night.".format(
        selected_dog.name, selected_room.name, selected_room.price
    ))


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("You must login to continue.")
        return

    dogs = {dog.id: dog for dog in svc.get_dogs_for_user(state.active_account)}
    bookings = svc.get_bookings_for_user(state.active_account)

    print(f"You have {len(bookings)} bookings.")
    for booking in bookings:
        print(" * Dog: {} is booked at {} for {}/night from {} for {} nights.".format(
            dogs.get(booking.guest_dog_id).name,
            booking.room.name,
            booking.room.price,
            booking.checkin_date,
            (booking.checkout_date - booking.checkin_date).days
        ))


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
