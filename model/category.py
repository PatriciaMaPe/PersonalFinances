# Producto
from google.appengine.ext import ndb

class Category(ndb.Model):
    name = ndb.StringProperty(required = True)
    image = ndb.BlobProperty()

