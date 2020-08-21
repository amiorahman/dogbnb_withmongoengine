import datetime
import mongoengine as me

class Dog(me.Document):
    registered_date = me.DateTimeField(default=datetime.datetime.now())

    species = me.StringField(required=True)
    length = me.FloatField(required=True, max_value=6)
    weight = me.FloatField(required=True, max_value=25)
    name = me.StringField(required=True)
    is_barking = me.BooleanField(required=True)

    meta = {
        'collection': 'dogs'
    }