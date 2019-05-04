#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from webapp2_extras.users import users



import datetime
import time

from model.transaction import Transaction
from model.account import Account


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template("/accounts")
            self.response.write(template);
        else:
            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template);

        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render());


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            template_values = {
                "title": "Login",
                "login": "Please login",
                "access_link": users.create_login_url("/home"),
                "content": "login"
            }

            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect("/home")



class AccountHandler(webapp2.RequestHandler):
    def get(self):

        accounts = Account.query().order(Account.name)

        template_values = {
            'accounts': accounts
        }

        template = JINJA_ENVIRONMENT.get_template("templates/accounts.html")
        self.response.write(template.render(template_values));

class AddAccountHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("nameAccount", "none")
        description = self.request.get("descriptionAccount", "none")

        #Store the answer
        new_account = Account(name=name, description=description)
        new_account.put()
        time.sleep(1)

        self.redirect("/accounts")


class ViewAccountHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.GET['key']

        account_key = ndb.Key(urlsafe=key)

        transactions = Transaction.query(Transaction.account == account_key)

        template_values = {
            'account_key': account_key,
            'transactions': transactions
        }

        template = JINJA_ENVIRONMENT.get_template("templates/invoices.html")
        self.response.write(template.render(template_values));


class TransactionHandler(webapp2.RequestHandler):
    def post(self):
        key = self.request.GET['key']

        account_key = ndb.Key(urlsafe=key)

        transactions = Transaction.query().order(-Transaction.date)

        template_values = {
            'transactions': transactions
        }

        template = JINJA_ENVIRONMENT.get_template("templates/invoices.html")
        self.response.write(template.render(template_values));


class AddTransactionHandler(webapp2.RequestHandler):
    def post(self):
        category = self.request.get("category", "none")
        quantity = int(self.request.get("quantity", 0))
        type = self.request.get("type", "none")
        description = self.request.get("description", "none")
        date = self.request.get("date", "none")

        key = self.request.GET['key']
        account_key = ndb.Key(urlsafe=key)

        #Store the answer
        date_format = datetime.datetime.strptime(date, "%Y-%m-%d")
        new_transaction = Transaction(category=category, quantity=quantity, type=type, description=description,
                                  date=date_format, account=account_key)
        new_transaction.put()
        time.sleep(1)

        url = "/viewAccount?key=" + str(key)
        self.redirect(url)


class EditTransactionHandler(webapp2.RequestHandler):
    def post(self):
        key = self.request.get("key", "none")
        category = self.request.get("category", "none").strip()
        type = self.request.get("type", "none").strip()
        quantity = int(self.request.get("quantity", 0).strip())
        description = self.request.get("description", "none").strip()
        date = self.request.get("date", "none").strip()

        date_format = datetime.datetime.strptime(date, "%Y-%m-%d")

        transaction = ndb.Key(urlsafe=key).get()
        transaction.category = category
        transaction.type = type
        transaction.quantity = quantity
        transaction.description = description
        transaction.date = date_format

        account_key = transaction.account

        transaction.put()
        time.sleep(1)

        transactions = Transaction.query(Transaction.account == account_key).order(-Transaction.date)


        template_values = {
            'account_key': account_key,
            'transactions': transactions
        }

        template = JINJA_ENVIRONMENT.get_template("templates/invoices.html")
        self.response.write(template.render(template_values));




class DeleteTransactionHandler(webapp2.RequestHandler):
    def post(self):
        key = self.request.get("key", "none")

        transaction = ndb.Key(urlsafe=key).get()
        account_key = transaction.account
        transaction.key.delete()

        time.sleep(1)

        transactions = Transaction.query(Transaction.account == account_key).order(-Transaction.date)

        template_values = {
            'account_key': account_key,
            'transactions': transactions
        }

        template = JINJA_ENVIRONMENT.get_template("templates/invoices.html")
        self.response.write(template.render(template_values));




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

        template = JINJA_ENVIRONMENT.get_template("templates/accounts.html")
        self.response.write(template.render(template_values));


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/accounts', AccountHandler),
    ('/addAccount', AddAccountHandler),
    ('/viewAccount', ViewAccountHandler),
    ('/deleteAccount', DeleteAccountHandler),
    ('/login', TransactionHandler),
    ('/addTransaction', AddTransactionHandler),
    ('/editTransaction', EditTransactionHandler),
    ('/deleteTransaction', DeleteTransactionHandler)
], debug=True)
