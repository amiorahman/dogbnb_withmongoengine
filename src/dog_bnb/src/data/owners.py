import datetime
import mongoengine as me

class Owner(me.Document):
    registered_date = me.DateTimeField(default=datetime.datetime.now())
    name = me.StringField(required=True)
    email = me.StringField(required=True)

    dog_ids = me.ListField()
    room_ids = me.ListField()

    meta = {
        'collection': 'owners'
    }