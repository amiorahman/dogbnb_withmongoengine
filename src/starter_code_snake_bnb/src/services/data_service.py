import datetime
from typing import List
from data.owners import Owner
from data.rooms import Room
from data.bookings import Booking


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
    db_query = Room.objects(id__in = active_account.room_ids).all()
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