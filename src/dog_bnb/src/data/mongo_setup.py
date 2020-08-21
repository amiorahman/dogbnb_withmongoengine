import mongoengine
from mongoengine import connect


def global_init():
    DB_URI = "mongodb+srv://amiorahman:Madapagad48!@mongocluster.npmma.mongodb.net/dog_bnb?retryWrites=true&w=majority"
    connect(host=DB_URI)

    """ for local connection
    alias_core = 'core'
    db = 'dog_bnb'
    mongoengine.register_connection(alias=alias_core, name=db)"""
