import webapp2
from google.appengine.ext import ndb
import db_defs
import base_page
import datetime

class AddHandler(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)
		self.tmeplate_values = {}

	def get(self):
		self.render('addproduct.html')