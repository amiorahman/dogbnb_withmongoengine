from colorama import Fore
from infrastructure.switchlang import switch
from validate_email import validate_email
from dateutil import parser
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome Host to Dog-BnB **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_rooms)
            s.case('r', register_room)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('b', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('Login to your [A]ccount')
    print('[L]ist your Rooms')
    print('[R]egister a Room')
    print('[U]pdate room availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('[B]ack to Main Menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER ACCOUNT **************** ')

    name = input('Enter you Full-Name: ')
    email = input('Enter your Email Address: ').strip().lower()

    valid_email = validate_email(email)
    if not valid_email:
        error_msg(f"Email not valid. Please try again.")
        return

    existing_account = svc.find_account_by_email(email)
    if existing_account:
        error_msg(f"ERROR: An account already exists with {email}.")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Account created successfully with Account ID: {state.active_account.id}")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('Enter your Email Address: ').strip().lower()

    valid_email = validate_email(email)
    if not valid_email:
        error_msg("Email not valid. Please try again.")
        return

    logged_account = svc.find_account_by_email(email)
    if not logged_account:
        error_msg(f"Account does not exist with email {email}")
        return

    state.active_account = logged_account
    success_msg(f"Logged in Succesfully!")


def register_room():
    print(' ****************** REGISTER ROOM **************** ')

    if not state.active_account:
        error_msg(f"You must login to continue.")
        return

    square_meters = input("How big is your room? (In Square Meter): ")
    if not square_meters:
        error_msg(f"Room size can not be empty!")

    square_meters = float(square_meters)
    is_carpeted = input("Is the room carpeted? [y, n]: ").lower().startswith('y')
    has_toys = input("Has dog toys? [y, n]: ").lower().startswith('y')
    allow_barker = input("Barking dogs allowed? [y, n]: ").lower().startswith('y')
    room_name = input("Enter anm attractive room name: ")
    room_price = input("Enter your asking price for this room: ")

    if not room_price:
        error_msg(f"Price can not be empty!")

    room_price = float(room_price)

    new_room = svc.register_room(
        state.active_account, room_name, room_price, square_meters, is_carpeted, has_toys, allow_barker
    )

    success_msg(f"Room registered successfully with Room ID: {new_room.id}")

    state.reload_account()


def list_rooms(supress_header=False):
    if not supress_header:
        print(' ******************     Your Registered Rooms     **************** ')

    if not state.active_account:
        error_msg(f"You must login to continue.")
        return

    rooms = svc.find_rooms_for_user(state.active_account)

    print(f"You have {len(rooms)} registered rooms.")
    for index, room in enumerate(rooms):
        print(f" {index + 1}. {room.name} is priced at {room.price}")

        for booking in room.bookings:
            print("     * Booking: {}, {} days. Booked?: {}".format(
                booking.checkin_date,
                (booking.checkout_date - booking.checkin_date).days,
                'YES' if booking.booked_date is not None else 'NO'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg(f"You must login to continue.")
        return

    list_rooms(supress_header=True)

    room_number = input("Enter Room Number: ")
    if not room_number.strip():
        error_msg(f"Operation Cancelled!")
        print()
        return

    room_number = int(room_number)

    rooms = svc.find_rooms_for_user(state.active_account)
    selected_room = rooms[room_number - 1]

    success_msg("Selected Room: {}".format(selected_room.name))

    start_date = parser.parse(input("Enter starting available date [yyyy-mm-dd]: "))
    available_days = int(input("For how many days the room is available: "))

    svc.add_availability(
        state.active_account, selected_room,
        start_date, available_days
    )

    state.reload_account()

    success_msg(f"Availability Updated for Room {selected_room.name}")


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg(f"You must login to continue.")
        return

    rooms = svc.find_rooms_for_user(state.active_account)

    bookings = [
        (room, booking)
        for room in rooms
        for booking in room.bookings
        if booking.booked_date is not None
    ]

    print(f"You have {len(bookings)} bookings.")
    for room, booking in bookings:
        print(" * Room: {}, Booked Date: {}, from {} to {}, for {} days.".format(
            room.name, booking.booked_date,
            booking.checkin_date, booking.checkout_date,
            (booking.checkout_date - booking.checkin_date).days
        ))


def exit_app():
    print()
    print('Good-Bye, See you again!')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
