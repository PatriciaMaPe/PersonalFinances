import webapp2
import datetime
import time

from google.appengine.ext import ndb
from webapp2_extras.users import users

from model.transaction import Transaction

from enviroment import JINJA_ENVIRONMENT


class ViewTransactionsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user.nickname()
        try:
            msg_error = self.request.GET['msg_error']
        except:
            msg_error = None

        key = self.request.GET['key']

        account_key = ndb.Key(urlsafe=key)

        transactions = Transaction.query(Transaction.account == account_key).order(-Transaction.date)

        template_values = {
            'title': "Transactions",
            'account_key': account_key,
            'transactions': transactions,
            'user_nickname': user.nickname(),
            'user_logout': users.create_logout_url("/"),
            'user_id': user.user_id(),
            'msg_error': msg_error
        }

        template = JINJA_ENVIRONMENT.get_template("invoices.html")
        self.response.write(template.render(template_values));


class AddTransactionHandler(webapp2.RequestHandler):
    def post(self):
        key = self.request.GET['key']
        try:
            category = self.request.get("category", "none")
            quantity = float(self.request.get("quantity", 0))
            type = self.request.get("type", "none")
            description = self.request.get("description", "none")
            date = self.request.get("date", "none")
            date_format = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            url = "/viewAccount?key=" + str(key) + ";msg_error=Formato de campo incorrecto"
            self.redirect(url)
            return


        account_key = ndb.Key(urlsafe=key)

        #Store the answer

        new_transaction = Transaction(category=category, quantity=quantity, type=type, description=description,
                                  date=date_format, account=account_key)
        new_transaction.put()
        time.sleep(1)

        url = "/viewAccount?key=" + str(key)
        self.redirect(url)


class EditTransactionHandler(webapp2.RequestHandler):
    def post(self):
        key_account = self.request.GET['key_account']

        try:
            key = self.request.get("key", "none")
            category = self.request.get("category", "none").strip()
            type = self.request.get("type", "none").strip()
            quantity = float(self.request.get("quantity", 0).strip())
            description = self.request.get("description", "none").strip()
            date = self.request.get("date", "none").strip()
            date_format = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            url = "/viewAccount?key=" + str(key_account) + ";msg_error=Formato de campo incorrecto"
            self.redirect(url)
            return



        transaction = ndb.Key(urlsafe=key).get()
        transaction.category = category
        transaction.type = type
        transaction.quantity = quantity
        transaction.description = description
        transaction.date = date_format

        transaction.put()
        time.sleep(1)

        url = "/viewAccount?key=" + str(key_account)
        self.redirect(url)


class DeleteTransactionHandler(webapp2.RequestHandler):
    def post(self):
        key_account = self.request.GET['key_account']

        key = self.request.get("key", "none")

        transaction = ndb.Key(urlsafe=key).get()
        transaction.key.delete()

        time.sleep(1)

        url = "/viewAccount?key=" + str(key_account)
        self.redirect(url)
