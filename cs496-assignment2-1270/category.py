import webapp2
from google.appengine.ext import ndb
import base_page
import re
import datetime
import os

class Category(ndb.Model):
	name = ndb.StringProperty(required=True)
	active = ndb.BooleanProperty(required=True)
	added = ndb.DateTimeProperty(required=True)
	lastmodified=ndb.DateTimeProperty(required=True)

	# from https://cloud.google.com/appengine/docs/python/ndb/queries
	# definition from https://docs.python.org/2/library/functions.html
	@classmethod
	def query_category(cls, ndb_config):
		return cls.query(ancestor=cls.query_key(ndb_config)).order(+cls.name)

 	@classmethod
 	def query_key(cls, ndb_config):
 		return ndb.Key(cls, ndb_config)

 	@classmethod
 	def getCategoryKey(cls, key):
 		try:
			category_key = ndb.Key(urlsafe=key)
			category = category_key.get()
		except (TypeError, datastore_errors.BadRequestError):
			category = ''
		return category

	# https://github.com/googlecloudplatform/datastore-ndb-python/issues/143
	@classmethod
 	def getUrlCategoryKey(cls, key):
 		try:
 			category_key = ndb.Key(urlsafe=key)
	 		if cls.keyIsValid(category_key):
		 		try:
					category = category_key.get()
				except (TypeError, datastore_errors.BadRequestError):
					return ''
			else:
				return ''
		except Exception, e:
			# if it returns ProtocolBufferDecodeError
			if e.__class__.__name__ == 'ProtocolBufferDecodeError':
				return ''
			else:
				# otherwise reraise the error as it is something else.
				raise
		return category

	# http://stackoverflow.com/questions/26233350/check-if-a-key-is-a-valid-key-for-the-current-app-id
	@staticmethod
	def keyIsValid(key):
		try:
			key.id()
  		except TypeError:
   			return False
  		return key.app() == os.getenv('APPLICATION_ID')

	@staticmethod
	def nameRegex():
		return "^[a-zA-Z0-9 ]+$"

class add(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def render(self, page, template_values={}):
		base_page.BaseHandler.render(self, page, template_values)

	def getCategories(self, template_values):
		k = ndb.Key(Category, self.app.config.get('default-group'))
		category_query = Category.query(ancestor=ndb.Key(Category, self.app.config.get('default-group'))).order(-Category.name)
		category_result = category_query.fetch()

		categories = []
		for c in category_query:
			categories.append({'category': c})
		return categories

	def get(self, template_values = {}):
		template_values['formaction'] = 'add_category'
		template_values['button_text'] = 'Add Category'
		template_values['pageaction'] = 'add'
		template_values['formpost'] = '/admin?paction=add&type=category'

		template_values['categories'] = self.getCategories(template_values)
		self.render('category/category.html', template_values)

		# should not talk to strangers children.... hmmmmm
		#methodInstance = view(self.request, self.response)
		#methodInstance.get(template_values, 'view')

	def post(self, request, template_values={}):
		error = False

		k = ndb.Key(Category, self.app.config.get('default-group'))
		obj = Category(parent=k)

		duplicate = Category.query_category(self.app.config.get('default-group')).filter(ndb.GenericProperty("name") == self.request.get('category-name')).fetch(1)

		if len(duplicate) > 0:
			error = True
			template_values['catnameerror'] = 'That Category already exists in the datastore'
			obj.name = self.request.get('category-name')
		elif not self.request.get('category-name'):
			error = True
			template_values['catnameerror'] = 'Name cannot be blank'
			obj.name = ''
		elif not re.match(obj.nameRegex(), self.request.get('category-name')):
			error = True
			template_values['catnameerror'] = 'Name must contain letters, numbers and - only'
			obj.name = self.request.get('category-name')
		else:
			obj.name = self.request.get('category-name')

				# set the boolean active
		if self.request.get('category-active'):
			practive = self.request.get('category-active')
			if practive == "True":
				obj.active = True
				template_values['catacttrue'] = 'checked'
				template_values['catactfalse'] = ''
			else: 
				obj.active = False
				template_values['catacttrue'] = ''
				template_values['catactfalse'] = 'checked'
		else:
			error = True
			template_values['catacttrue'] = ''
			template_values['catactfalse'] = ''
			template_values['catactiveerror'] = 'Choose active or inactive.'	

		# if no errors exist put the entity in the database
		if not error:
			now = datetime.datetime.utcnow()
			obj.added = now
			obj.lastmodified = now
			obj.put()
			template_values['catacttrue'] = ''
			template_values['catactfalse'] = ''
			template_values['message'] = 'Added Category ' + obj.name + ' to the database.'
			template_values.pop('category', None)
		else:
			template_values['category'] = obj
			template_values['message'] = 'Could not add category.  Errors Exist.'

		self.get(template_values)

class edit(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def render(self, page):
		base_page.BaseHandler.render(self, page, self.template_values)

	def getCategories(self, template_values):
		k = ndb.Key(Category, self.app.config.get('default-group'))
		category_query = Category.query(ancestor=ndb.Key(Category, self.app.config.get('default-group'))).order(-Category.name)
		category_result = category_query.fetch()

		categories = []
		for c in category_query:
			categories.append({'category': c})
		return categories

	def get(self, template_values = {}):
		self.template_values = template_values
		self.template_values['pageaction'] = 'edit'
		self.template_values['formaction'] = 'edit_category'
		self.template_values['button_text'] = 'Update'

		if(self.request.get('key')):

			obj = Category().getUrlCategoryKey(self.request.get('key'))

			if obj:
				self.template_values['formpost'] = '/admin?paction=edit&key=' + obj.key.urlsafe() + '&type=category'

				if obj.active:
					template_values['catacttrue'] = 'checked'
				else: 
					template_values['catactfalse'] = 'checked'

				self.template_values['category'] = obj		
			else:
				self.template_values['categories'] = self.getCategories(self.template_values)
		else:
			self.template_values['categories'] = self.getCategories(self.template_values)

		self.render('category/category.html')

	def post(self, request, template_values={}):
		error = False

		obj = Category().getUrlCategoryKey(self.request.get('key'))

		duplicate = Category.query_category(self.app.config.get('default-group')).filter(ndb.GenericProperty("name") == self.request.get('category-name'), ndb.GenericProperty("__key__") != obj.key).fetch(1)

		if len(duplicate) > 0:
			error = True
			template_values['catnameerror'] = 'That Category already exists in the datastore'
			obj.name = self.request.get('category-name')
		elif not self.request.get('category-name'):
			error = True
			template_values['catnameerror'] = 'Name cannot be blank'
		elif not re.match(obj.nameRegex(), self.request.get('category-name')):
			error = True
			template_values['catnameerror'] = 'Names contain letters, numbers and - only'
			obj.name = self.request.get('category-name')
		else:
			obj.name = self.request.get('category-name')

				# set the boolean active
		if self.request.get('category-active'):
			practive = self.request.get('category-active')
			if practive == "True":
				obj.active = True
				template_values['catacttrue'] = 'checked'
				template_values['catactfalse'] = ''
			else: 
				obj.active = False
				template_values['catacttrue'] = ''
				template_values['catactfalse'] = 'checked'
		else:
			error = True
			template_values['catacttrue'] = ''
			template_values['catactfalse'] = ''
			template_values['catactiveerror'] = 'Choose active or inactive.'	

		# if no errors exist put the entity in the database
		if not error:
			now = datetime.datetime.utcnow()
			obj.added = now
			obj.lastmodified = now
			obj.put()
			template_values['catacttrue'] = ''
			template_values['catactfalse'] = ''
			template_values['message'] = 'Added Category ' + obj.name + ' to the database.'
			template_values.pop('category', None)
		else:
			template_values['category'] = obj
			template_values['message'] = 'Could not add category.  Errors Exist.'

		if not error:
			now = datetime.datetime.utcnow()
			obj.lastmodified = now
			obj.put()
			template_values['message'] = 'Updated category ' + obj.name + ' to the database.'
		else:
			template_values['message'] = 'Could not update category.  Errors Exist.'

		template_values['categories'] = self.getCategories(template_values)
		self.get(template_values)


class view(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def render(self, page):
		base_page.BaseHandler.render(self, page, self.template_values)

	def getCategories(self, template_values):
		k = ndb.Key(Category, self.app.config.get('default-group'))
		category_query = Category.query(ancestor=ndb.Key(Category, self.app.config.get('default-group'))).order(-Category.name)
		category_result = category_query.fetch()

		categories = []
		for c in category_query:
			categories.append({'category': c})
		return categories

	def get(self, template_values = {}, pageaction = 'view'):
		self.template_values = template_values
		self.template_values['categories'] = self.getCategories(template_values)
		self.template_values['pageaction'] = 'view'
		self.render('category/category.html')