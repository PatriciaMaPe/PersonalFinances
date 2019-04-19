# Producto
from google.appengine.ext import ndb

class Eco(ndb.Model):
    nombre = ndb.StringProperty(required=True)