import webapp2
import json
import urllib
import time
import db_defs
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from base_page import BaseHandler
from testMethods import TestMethods


class LoadData(TestMethods):

	def get(self):

		customer_url = self.base_url + self.customers_url
		order_url = self.base_url + self.orders_url
		product_url = self.base_url + self.products_url
		'''
		Customer POST Testing
		'''
		self.response.write("<h3>POST Customers: Mime json - Add Customers Valid Data</h3>")
		customer_keys = self.testPostValidObjects(customer_url, "customers", self.load_customer_list)

		'''
		Orders ADD with valid customer id
		'''
		self.response.write("<h3>POST Orders: Mime json Valid Customer ID</h3>")
		self.testAddObject(customer_url, db_defs.Customer)

		'''
		Product POST - Add Products with valid Data
		'''
		self.response.write("<h3>POST Product: Mime json - Valid Product Data Sent</h3>")
		self.testPostValidObjects(product_url, "products", self.load_product_list)