import datetime
from typing import List
from data.owners import Owner
from data.rooms import Room
from data.bookings import Booking
from data.dogs import Dog


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def register_room(active_account: Owner,
                  room_name, room_price, square_meters, is_carpeted,
                  has_toys, allow_barker) -> Room:
    room = Room()

    room.name = room_name
    room.price = room_price
    room.square_meters = square_meters
    room.is_carpeted = is_carpeted
    room.has_toys = has_toys
    room.allow_barking_dogs = allow_barker

    room.save()

    account = find_account_by_email(active_account.email)
    account.room_ids.append(room.id)
    account.save()

    return room


def find_rooms_for_user(active_account: Owner) -> List[Room]:
    db_query = Room.objects(id__in=active_account.room_ids).all()
    rooms = list(db_query)

    return rooms


def add_availability(active_account: Owner, selected_room: Room,
                     start_date: datetime.datetime, available_days) -> Room:
    booking = Booking()

    booking.checkin_date = start_date
    booking.checkout_date = start_date + datetime.timedelta(days=available_days)

    room = Room.objects(id=selected_room.id).first()
    room.bookings.append(booking)
    room.save()

    return room


def add_dog(active_account: Owner,
            dog_name, length, weight,
            species, is_barking) -> Dog:
    dog = Dog()

    dog.name = dog_name
    dog.length = length
    dog.weight = weight
    dog.species = species
    dog.is_barking = is_barking

    dog.save()

    account = find_account_by_email(active_account.email)
    account.dog_ids.append(dog.id)
    account.save()

    return dog


def find_dogs_for_user(active_account: Owner) -> List[Dog]:
    db_query = Dog.objects(id__in=active_account.dog_ids).all()
    dogs = list(db_query)

    return dogs


def get_available_rooms(checkin: datetime.datetime, checkout: datetime.datetime,
                        dog: Dog) -> List[Room]:
    minimum_size = dog.length / 3

    db_query = Room.objects() \
        .filter(square_meters__gte=minimum_size) \
        .filter(bookings__checkin_date__lte=checkin) \
        .filter(bookings__checkout_date__gte=checkout)

    if dog.is_barking:
        db_query = db_query.filter(allow_barking_dogs=True)

    rooms = db_query.order_by('price', 'square_meters')

    available_rooms = []

    for room in rooms:
        for booking in room.bookings:
            if booking.checkin_date <= checkin and booking.checkout_date >= checkout and booking.guest_dog_id is None:
                available_rooms.append(room)

    return available_rooms


def book_room(active_account: Owner, checkin, checkout, dog, room):
    booking = Booking()

    for bkng in room.bookings:
        if bkng.checkin_date <= checkin and bkng.checkout_date >= checkout and bkng.guest_dog_id is None:
            booking = bkng

    booking.guest_owner_id = active_account.id
    booking.guest_dog_id = dog.id
    booking.booked_date = datetime.datetime.now()

    room.save()


def get_dogs_for_user(active_account: Owner) -> List[Dog]:
    #owner = Owner.objects(id__in=active_account.id).first()
    dogs = Dog.objects(id__in=active_account.dog_ids).all()

    return list(dogs)


def get_bookings_for_user(active_account: Owner) -> List[Booking]:
    booked_rooms = Room.objects() \
        .filter(bookings__guest_owner_id=active_account.id) \
        .only('bookings', 'name', 'price')

    def reverse_map_room_to_booking(room, booking):
        booking.room = room
        return booking

    bookings = [
        reverse_map_room_to_booking(room, booking)
        for room in booked_rooms
        for booking in room.bookings
        if booking.guest_owner_id == active_account.id
    ]

    return bookings
