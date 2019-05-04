# Producto
from google.appengine.ext import ndb

class User(ndb.Model):
    id_user = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
