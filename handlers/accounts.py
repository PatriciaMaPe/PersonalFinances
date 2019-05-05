import webapp2
import time

from google.appengine.ext import ndb
from webapp2_extras.users import users

from model.account import Account
from model.user import User

from enviroment import JINJA_ENVIRONMENT


class AccountHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user == None:
            self.redirect("/")
        else:
            # Look for the user's information
            user_id = user.user_id()
            name_info = user.nickname()
            stored_user = User.query(User.id_user == user_id)

            if stored_user.count() == 0:
                # Store the information
                img = User(id_user=user_id, name=name_info)
                img.put()
                time.sleep(1)



            accounts = Account.query(Account.id_user == user_id).order(Account.name)

            template_values = {
                'title': "Accounts",
                'accounts': accounts,
                'user_logout': users.create_logout_url("/"),
                'user_id': user.user_id()
            }

            template = JINJA_ENVIRONMENT.get_template("accounts.html")
            self.response.write(template.render(template_values));


class AddAccountHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        name = self.request.get("nameAccount", "none")
        description = self.request.get("descriptionAccount", "none")

        #Store the answer
        new_account = Account(name=name, description=description, id_user=user.user_id())
        new_account.put()
        time.sleep(1)

        self.redirect("/accounts")


class DeleteAccountHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.GET['key']

        account = ndb.Key(urlsafe=key).get()
        account.key.delete()

        time.sleep(1)

        accounts = Account.query().order(Account.name)

        template_values = {
            'accounts': accounts
        }

        template = JINJA_ENVIRONMENT.get_template("accounts.html")
        self.response.write(template.render(template_values));



