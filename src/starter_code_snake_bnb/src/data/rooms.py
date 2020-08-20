import datetime
import mongoengine as me
from data.bookings import Booking

class Room(me.Document):
    registered_date = me.DateTimeField(default=datetime.datetime.now())

    name = me.StringField(required=True)
    price = me.FloatField(required=True)
    square_meters = me.FloatField(required=True)
    is_carpeted = me.BooleanField(required=True)
    has_toys = me.BooleanField(required=True)
    allow_barking_dogs = me.BooleanField(default=False)

    bookings = me.EmbeddedDocumentListField(Booking)

    meta = {
        'db_alias': 'core',
        'collection': 'rooms'
    }