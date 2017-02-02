import webapp2
from google.appengine.ext import ndb
import base_page
import datetime
import product
import category
import re

class AdminHandler(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}

	def get(self):
		if self.request.get('paction'):
			paction = self.request.get('paction')
			actor = self.request.get('type')

			if (paction == 'add' or paction == 'edit' or paction == 'view'):
				if actor == 'product':
					methodToCall = getattr(product, paction)
					methodToCall(self.request, self.response).get()
				elif actor == 'category':
					methodToCall = getattr(category, paction)
					methodToCall(self.request, self.response).get()
				else:
					self.template_values['message'] = "That type does not exist"
					self.render('error.html')
			else:
				self.template_values['message'] = "That action cannot be performed"
				self.render('error.html', self.template_values)
		else:
			self.render('admin.html')

	def post(self):
		paction = self.request.get('paction')
		action = self.request.get('action')
		if action == 'add_product':
			methodToCall = getattr(product, 'add')
			methodToCall(self.request, self.response).post(self.request, self.template_values)
		elif action == 'add_category':
			methodToCall = getattr(category, 'add')
			methodToCall(self.request, self.response).post(self.request, self.template_values)
		elif action == 'edit_product':
			methodToCall = getattr(product, 'edit')
			methodToCall(self.request, self.response).post(self.request, self.template_values)
		elif action == 'edit_category':
			methodToCall = getattr(category, 'edit')
			methodToCall(self.request, self.response).post(self.request, self.template_values)
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
			base_page.BaseHandler.render(self, 'admin.html', self.template_values)