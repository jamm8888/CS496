import webapp2
from google.appengine.ext import ndb
from google.appengine.api import datastore_errors
import base_page
import category
import re
import datetime
import os

class Product(ndb.Model):
	sku = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty(required=True)
	cost = ndb.FloatProperty(required=True)
	active = ndb.BooleanProperty(required=True)
	categories = ndb.KeyProperty(repeated=True)
	added = ndb.DateTimeProperty(required=True)
	lastmodified = ndb.DateTimeProperty(required=True)

	# from https://cloud.google.com/appengine/docs/python/ndb/queries
	# definition from https://docs.python.org/2/library/functions.html
	@classmethod
 	def query_product(cls, ndb_config):
 		return cls.query(ancestor=cls.query_key(ndb_config)).order(+cls.sku)

 	@classmethod
 	def query_key(cls, ndb_config):
 		return ndb.Key(cls, ndb_config)

 	@classmethod
 	def getProductKey(cls, key):
 		try:
			product_key = ndb.Key(key)
			product = product_key.get()
		except (TypeError, datastore_errors.BadRequestError):
			product = ''
		return product

	# https://github.com/googlecloudplatform/datastore-ndb-python/issues/143
	@classmethod
 	def getUrlProductKey(cls, key):
 		try:
 			product_key = ndb.Key(urlsafe=key)
	 		if cls.keyIsValid(product_key):
		 		try:
					product = product_key.get()
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
		return product

	@staticmethod
	def skuRegex():
		return "^[a-zA-Z0-9-]+$"

	@staticmethod
	def nameRegex():
		return "^[a-zA-Z0-9 ]+$"

	@staticmethod
	def descRegex():
		return "^[a-zA-Z0-9 \\.\\?\\-\\!\\#\\$\\(\\)\\+\\~\\`\\,\\:\\;\\']+$"

	@staticmethod
	def costRegex():
		return "^-?[\d]+(\.[\d]+)?$"

	# http://stackoverflow.com/questions/26233350/check-if-a-key-is-a-valid-key-for-the-current-app-id
	@staticmethod
	def keyIsValid(key):
		try:
			key.id()
  		except TypeError:
   			return False
  		return key.app() == os.getenv('APPLICATION_ID')

class add(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def getCategoryBoxes(self, product):
		categories = category.Category.query(ancestor=ndb.Key(category.Category, self.app.config.get('default-group')))
		category_boxes = []
		for c in categories:
			if c.key in product.categories:
				category_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
			else: 
				category_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
		return category_boxes

	def getProducts(self, template_values):
		#k = ndb.Key(Product, self.app.config.get('default-group'))
		#product_query = Product.query(ancestor=ndb.Key(Product, self.app.config.get('default-group'))).order(-Product.name)
		productInstance = Product()
		product_query = productInstance.query_product(self.app.config.get('default-group')).fetch()

		product = []
		for p in product_query:
			categories = []
			for c in p.categories:
				ct = category.Category().getCategoryKey(c.urlsafe())
				categories.append({'category': ct})
			product.append({'product':p, 'categories': categories})
		return product

	def render(self, page, template_values={}):
		base_page.BaseHandler.render(self, page, template_values)

	def get(self, template_values = {}):

		dictkey = 'product'
		productInstance = Product()

		if not dictkey in template_values:
			template_values['categories'] = self.getCategoryBoxes(productInstance)

		template_values['formaction'] = 'add_product'
		template_values['button_text'] = 'Add Product'
		template_values['pageaction'] = 'add'
		template_values['formpost'] = '/admin?paction=add&type=product'
		template_values['products'] = self.getProducts(template_values)

		self.render('product/product.html', template_values)

	def post(self, request, template_values = {}):
		error = False

		k = ndb.Key(Product, self.app.config.get('default-group'))
		product = Product(parent=k)

		duplicate = Product.query_product(self.app.config.get('default-group')).filter(ndb.GenericProperty("sku") == self.request.get('product-sku')).fetch(1)

		if len(duplicate) > 0:
			error = True
			template_values['prodskuerror'] = 'That SKU already exists in the datastore'
			product.sku = self.request.get('product-sku')
		elif not self.request.get('product-sku'):
			error = True
			template_values['prodskuerror'] = 'Sku cannot be blank'
			product.sku = ''
		elif not re.match(product.skuRegex(), self.request.get('product-sku')):
			error = True
			template_values['prodskuerror'] = 'Sku must contain letters, numbers and - only'
			product.sku = self.request.get('product-sku')
		else:
			product.sku = self.request.get('product-sku')

		if not self.request.get('product-name'):
			error = True
			template_values['prodnameerror'] = 'Product name cannot be blank'
			product.name = ''
		elif not re.match(product.nameRegex(), self.request.get('product-name')):
			error = True
			template_values['prodnameerror'] = 'Product name can contain letters, numbers, - and space only'
			product.name = self.request.get('product-name')
		else: 
			product.name = self.request.get('product-name')

		if not self.request.get('product-desc'):
			error = True
			template_values['proddescerror'] = 'Description cannot be blank'
			product.description = ''
		elif not re.match(product.descRegex(), self.request.get('product-desc')):
			error = True
			template_values['proddescerror'] = 'Description can only contain letters, numbers, space and .-!#$()+~`,:;]+$'
			product.description = self.request.get('product-desc')
		else:
			product.description = self.request.get('product-desc')

		# verify the product cost
		if not self.request.get('product-cost'):
			error=True
			template_values['prodcosterror'] = 'Cost cannot be blank.'
			product.cost = None
		elif not re.match(product.costRegex(), self.request.get('product-cost')):
			error=True
			template_values['prodcosterror'] = 'Cost should be positive a dollar value'
			template_values['product.cost'] = self.request.get('product-cost').strip()
		else:
			product.cost = float(self.request.get('product-cost').strip())

		product.categories = [ndb.Key(urlsafe=x) for x in self.request.get_all('categories[]')]

		if len(product.categories) == 0:
			error = True
			template_values['prodcaterror'] = 'At least one category must be checked.'
		template_values['categories'] = self.getCategoryBoxes(product)

		# set the boolean active
		if self.request.get('product-active'):
			practive = self.request.get('product-active')
			if practive == "True":
				product.active = True
				template_values['prodacttrue'] = 'checked'
				template_values['prodactfalse'] = ''
			else: 
				product.active = False
				template_values['prodacttrue'] = ''
				template_values['prodactfalse'] = 'checked'
		else:
			error = True
			template_values['prodacttrue'] = ''
			template_values['prodactfalse'] = ''
			template_values['prodactiveerror'] = 'Choose active or inactive.'	

		# if no errors exist put the entity in the database
		if not error:
			now = datetime.datetime.utcnow()
			product.added = now
			product.lastmodified = now
			product.put()
			template_values['prodacttrue'] = ''
			template_values['prodactfalse'] = ''
			template_values['message'] = 'Added product ' + product.name + ' to the database.'
			template_values.pop('product', None)
		else:
			template_values['product'] = product
			template_values['message'] = 'Could not Add product.  Errors Exist.'

		template_values['products'] = self.getProducts(template_values)
		self.get(template_values)

class edit(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def render(self, page):
		base_page.BaseHandler.render(self, page, self.template_values)

	def getCategoryBoxes(self, product):
		categories = category.Category.query(ancestor=ndb.Key(category.Category, self.app.config.get('default-group')))
		category_boxes = []
		for c in categories:
			if c.key in product.categories:
				category_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
			else: 
				category_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
		return category_boxes

	def getProducts(self, template_values):
		#k = ndb.Key(Product, self.app.config.get('default-group'))
		#product_query = Product.query(ancestor=ndb.Key(Product, self.app.config.get('default-group'))).order(-Product.name)
		productInstance = Product()
		product_query = productInstance.query_product(self.app.config.get('default-group')).fetch()

		product = []
		for p in product_query:
			categories = []
			for c in p.categories:
				ct = category.Category().getCategoryKey(c.urlsafe())
				categories.append({'category': ct})
			product.append({'product':p, 'categories': categories})
		return product

	def get(self, template_values = {}):
		self.template_values = template_values
		self.template_values['pageaction'] = 'edit'
		self.template_values['formaction'] = 'edit_product'
		self.template_values['button_text'] = 'Update'

		if(self.request.get('key')):
			product = Product().getUrlProductKey(self.request.get('key'))

			if product:
				self.template_values['formpost'] = '/admin?paction=edit&key=' + product.key.urlsafe() + '&type=product'

				if product.active:
					template_values['prodacttrue'] = 'checked'
				else: 
					template_values['prodactfalse'] = 'checked'

				self.template_values['product'] = product		
				category_boxes = self.getCategoryBoxes(product)
				self.template_values['categories'] = category_boxes
			else:
				self.template_values['product'] = self.getProducts(self.template_values)
		else:
			self.template_values['product'] = self.getProducts(self.template_values)

		self.template_values['products'] = self.getProducts(template_values)
		self.render('product/product.html')

	def post(self, request, template_values = {}):
		error = False
		product = Product().getUrlProductKey(self.request.get('key'))

		duplicate = Product.query_product(self.app.config.get('default-group')).filter(ndb.GenericProperty("sku") == self.request.get('product-sku'), ndb.GenericProperty("__key__") != product.key).fetch(1)
		
		if len(duplicate) > 0:
			error = True
			template_values['prodskuerror'] = 'That SKU already exists in the datastore'
			product.sku = self.request.get('product-sku')
		elif not self.request.get('product-sku'):
			error = True
			template_values['prodskuerror'] = 'Sku cannot be blank'
		elif not re.match(product.skuRegex(), self.request.get('product-sku')):
			error = True
			template_values['prodskuerror'] = 'Skus contain letters, numbers and - only'
			product.sku = self.request.get('product-sku')
		else:
			product.sku = self.request.get('product-sku')

		if not self.request.get('product-name'):
			error = True
			template_values['prodnameerror'] = 'Product name cannot be blank'
		elif not re.match(product.nameRegex(), self.request.get('product-name')):
			error = True
			template_values['prodnameerror'] = 'Product names contain letters, numbers, -, and spaces only'
			product.name = self.request.get('product-name')
		else: 
			product.name = self.request.get('product-name')

		if not self.request.get('product-desc'):
			error = True
			template_values['proddescerror'] = 'Description cannot be blank'
		elif not re.match(product.descRegex(), self.request.get('product-desc')):
			error = True
			template_values['proddescerror'] = 'Descriptions contain letters, numbers, space and .-!#$()+~`,:;]+$'
			product.description = self.request.get('product-desc')
		else:
			product.description = self.request.get('product-desc')

		# verify the product cost
		if not self.request.get('product-cost'):
			error=True
			template_values['prodcosterror'] = 'Cost cannot be blank.'
		elif not re.match(product.costRegex(), self.request.get('product-cost')):
			error=True
			template_values['prodcosterror'] = 'Cost should be an integer or a decimal number'
			template_values['product.cost'] = self.request.get('product-cost').strip()
		else:
			product.cost = float(self.request.get('product-cost').strip())

		product.categories = [ndb.Key(urlsafe=x) for x in self.request.get_all('categories[]')]

		if len(product.categories) == 0:
			error = True
			template_values['prodcaterror'] = 'At least one category must be checked.'
		template_values['categories'] = self.getCategoryBoxes(product)

		# set the boolean active
		if self.request.get('product-active'):
			practive = self.request.get('product-active')
			if practive == "True":
				product.active = True
				template_values['prodacttrue'] = 'checked'
				template_values['prodactfalse'] = ''
			else: 
				product.active = False
				template_values['prodacttrue'] = ''
				template_values['prodactfalse'] = 'checked'
		else:
			error = True
			template_values['prodacttrue'] = ''
			template_values['prodactfalse'] = ''
			template_values['prodactiveerror'] = 'Choose active or inactive.'

		# if no errors exist put the entity in the database
		if not error:
			now = datetime.datetime.utcnow()
			product.lastmodified = now
			product.put()
			template_values['message'] = 'Updated product ' + product.name + ' to the database.'
		else:
			template_values['product'] = product
			template_values['message'] = 'Could not update product.  Errors Exist.'

		template_values['products'] = self.getProducts(template_values)
		self.get(template_values)

class view(base_page.BaseHandler):

	def __init__(self, request, response):
		self.initialize(request, response)

	def render(self, page):
		base_page.BaseHandler.render(self, page, self.template_values)

	def getProducts(self, template_values):
		#k = ndb.Key(Product, self.app.config.get('default-group'))
		#product_query = Product.query(ancestor=ndb.Key(Product, self.app.config.get('default-group'))).order(-Product.name)
		productInstance = Product()
		product_query = productInstance.query_product(self.app.config.get('default-group')).fetch()

		product = []
		for p in product_query:
			categories = []
			for c in p.categories:
				ct = category.Category().getCategoryKey(c.urlsafe())
				categories.append({'category': ct})
			product.append({'product':p, 'categories': categories})
		return product

	def get(self, template_values = {}, pageaction = 'view'):
		self.template_values = template_values
		self.template_values['pageaction'] = pageaction
		self.template_values['product'] = self.getProducts(self.template_values)
		self.render('product/product.html')