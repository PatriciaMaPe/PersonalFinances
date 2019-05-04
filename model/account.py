# Producto
from google.appengine.ext import ndb
from transaction import Transaction
from user import User


class Account(ndb.Model):
    name = ndb.StringProperty(required = True)
    description = ndb.StringProperty()
    id_user = ndb.StringProperty(required=True)
