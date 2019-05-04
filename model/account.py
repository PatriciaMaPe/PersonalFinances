# Producto
from google.appengine.ext import ndb
from transaction import Transaction
from user import User


class Account(ndb.Model):
    name = ndb.StringProperty(required = True)
    description = ndb.StringProperty()
    #owner = ndb.KeyProperty(kind=User)
