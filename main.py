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
from model.user import User

from handlers.accounts import AccountHandler
from handlers.accounts import AddAccountHandler
from handlers.accounts import DeleteAccountHandler
from handlers.transactions import ViewTransactionsHandler
from handlers.transactions import AddTransactionHandler
from handlers.transactions import EditTransactionHandler
from handlers.transactions import DeleteTransactionHandler

from enviroment import JINJA_ENVIRONMENT


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/accounts")
        else:
            template_values = {
                "title": "Login",
                "login": "Please login",
                "user_login": users.create_login_url("/"),
                "content": "login"
            }

            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(template_values))


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        msg = self.request.GET['msg']

        template_values = {
            "title": "Error",
            "error_msg": msg,
            "content": "error"
        }

        self.render(template_values)


app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/accounts', AccountHandler),
    ('/addAccount', AddAccountHandler),
    ('/viewAccount', ViewTransactionsHandler),
    ('/deleteAccount', DeleteAccountHandler),
    ('/addTransaction', AddTransactionHandler),
    ('/editTransaction', EditTransactionHandler),
    ('/deleteTransaction', DeleteTransactionHandler),
    ('/error', ErrorHandler)
], debug=True)
