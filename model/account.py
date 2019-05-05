
from google.appengine.ext import ndb


class Account(ndb.Model):
    name = ndb.StringProperty(required = True)
    description = ndb.StringProperty()
    id_user = ndb.StringProperty(required=True)
