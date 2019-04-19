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

import datetime
import time

from model.transaction import Transaction
from model.eco import Eco
from model.category import Category

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("templates/respuesta.html")
        self.response.write(template);

class EcoHandler(webapp2.RequestHandler):
    def post(self):
        eco = self.request.get("eco", "noneco")

        # Store the answer
        nuevo_eco = Eco(nombre=eco)
        nuevo_eco.put()

        ecos = Eco.query()

        template_values = {
            'dato': eco,
            'ecos': ecos
        }

        template = JINJA_ENVIRONMENT.get_template("templates/respuesta.html")
        self.response.write(template.render(template_values));


class TransactionHandler(webapp2.RequestHandler):
    def post(self):
        category = self.request.get("category", "none")
        quantity = self.request.get("quantity", 0)
        type = self.request.get("type", "none")
        description = self.request.get("description", "none")
        date = self.request.get("date", "none")

        if category != "none":
            #Store the answer
            date_format = datetime.datetime.strptime(date, "%Y-%m-%d")
            new_transaction = Transaction(category=category, quantity=int(quantity), type=type, description=description,
                                  date=date_format)

            #new_transaction = Transaction(category="entretenimiento", quantity=123, type="ingreso", description="lala", date=datetime.date.today())

            new_transaction.put()
            time.sleep(1)


        transactions = Transaction.query().order(-Transaction.date)


        template_values = {
            'transactions': transactions
        }

        template = JINJA_ENVIRONMENT.get_template("templates/invoices.html")
        self.response.write(template.render(template_values));


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addTransaction', TransactionHandler),
    ('/eco', EcoHandler)
], debug=True)
