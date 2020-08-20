import mongoengine as me

class Booking(me.EmbeddedDocument):
    guest_owner_id = me.ObjectIdField()
    guest_dog_id = me.ObjectIdField()

    booked_date = me.DateTimeField()
    checkin_date = me.DateTimeField(required=True)
    checkout_date = me.DateTimeField(required=True)

    review = me.StringField()
    rating = me.IntField(default=0, max_value=5)