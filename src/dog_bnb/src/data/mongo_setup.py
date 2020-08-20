import mongoengine

def global_init():
    alias_core = 'core'
    db = 'dog_bnb'
    mongoengine.register_connection(alias=alias_core, name=db)