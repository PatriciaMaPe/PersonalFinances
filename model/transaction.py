
from google.appengine.ext import ndb


class Transaction(ndb.Model):
    category = ndb.StringProperty(required = True, choices=["Educacion", "Entretenimiento", "Familia", "Comida", "Viaje", "Deuda", "Regalo", "Otros"])
    quantity = ndb.FloatProperty(required = True)
    type = ndb.StringProperty(required = True, choices=["Ingreso", "Gasto"])
    description = ndb.StringProperty()
    date = ndb.DateProperty()
    account = ndb.KeyProperty(kind='Account')