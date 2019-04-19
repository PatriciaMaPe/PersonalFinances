# Producto
from google.appengine.ext import ndb
from category import Category
from user import User


class Transaction(ndb.Model):
    #category = ndb.KeyProperty(kind='Category', required = True)
    category = ndb.StringProperty(required = True)
    quantity = ndb.IntegerProperty(required = True)
    type = ndb.StringProperty(required = True)
    description = ndb.StringProperty()
    date = ndb.DateProperty()
    #owner = ndb.KeyProperty(kind=User, required = True)