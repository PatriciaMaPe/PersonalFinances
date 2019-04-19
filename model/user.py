# Producto
from google.appengine.ext import ndb

class User(ndb.Model):
    login = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
