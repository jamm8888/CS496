import webapp2
from google.appengine.ext import ndb
import db_defs
import re
from base_page import BaseHandler
import json

class ProductHandler(BaseHandler):

	def __init__(self, request, response):
		# this carreis down values from BaseHandler
		BaseHandler.__init__(self)
		# this overrides values in BaseHandler
		self.initialize(request, response)

	def validateSku(self, sku, indexID = None):

		if re.match(db_defs.Product.skuRegex(), sku):
			# check sku does not already exist
			q = db_defs.Product.query()
			q = q.filter(db_defs.Product.sku == sku)

			if indexID:
				q = q.filter(db_defs.Product.sku == sku)

			# if the sku already exists return it otherwise return None
			if q.fetch(parent=None):
				return q
		return None

	def validate(self, request, val=None):

		error = False
		message = ''
		validated = {}

		# if we are creating a product we need to verify all fields are filled in
		if val == "create":
			if not request.get('sku'):
				error = True
				message += "Sku missing. "
			if not request.get('name'):
				error = True
				message += "Name missing. "
			if not request.get('description'):
				error = True
				message += "Description Missing. "
			if not request.get('cost'):
				error = True
				message += "Cost missing. "


		# for both search and create we need to check the value
		if request.get('sku') and not re.match(db_defs.Product.skuRegex(), request.get('sku')):
			error = True
			message += "Sku invalid. "

		if request.get('name') and not re.match(db_defs.Product.nameRegex(), request.get('name')):
			error = True
			message += "Name invalid. "

		if request.get('description') and not re.match(db_defs.Product.descRegex(), request.get('description')):
			error = True
			message += "Description invalid. "

		if request.get('cost') and not re.match(db_defs.Product.costRegex(), request.get('cost')):
			error = True
			message += "Cost invalid. "

		if request.get('quantity') and not re.match(db_defs.Product.quantityRegex(), request.get('quantity')):
			error = True
			message += "Quntity invalid. "

		validated['error'] = error
		validated['message'] = message
		return validated

	def getValues(self, request):

		requestValues = db_defs.Product()
		limitValues = db_defs.Limits()

		try:
			request = json.loads(self.request.body)
			if 'sku' in request:
				requestValues.sku = request['sku']
			if 'name' in request:
				requestValues.name = request['name']
			if 'description' in request:
				requestValues.description = request['description']
			if 'cost' in request:
				try:
					requestValues.cost = float(request['limit'])
				except ValueError, e:
					requestValues.cost = None
			if 'quantity' in request:
				try:
					requestValues.quantity = int(request['quantity'])
				except ValueError, e:
					requestValues.quantity = None
			if 'limit' in request:
				try:
					limitValues.limit = int(request['limit'])
				except ValueError, e:
					limitValues.limit = self.default_limit
			if 'offset' in request: 
				try:
					limitValues.offset = int(request['offset'])
				except ValueError, e:
					limitValues.offset = self.default_offset
			
		except ValueError, e:
			if self.request.get('sku'):
				requestValues.firstName = self.request.get('sku')

			if self.request.get('name'):
				requestValues.lastName = self.request.get('name')

			if self.request.get('description'):
				requestValues.email = self.request.get('description')

			if self.request.get('cost'):
				try:
					requestValues.cost = float(self.request.get('cost'))
				except ValueError, e:
					requestValues.cost = None

			if self.request.get('quantity'):
				try:
					requestValues.quantity = int(self.request.get('quantity'))
				except ValueError, e:
					requestValues.quantity = None

			if self.request.get('limit'):
				try:
					limitValues.limit = int(self.request.get('limit'))
				except ValueError, e:
					limitValues.limit = self.default_limit
			else:
				limitValues.limit = None

			if self.request.get('offset'):
				try:
					limitValues.offset = int(self.request.get('offset'))
				except ValueError, e:
					limitValues.offset = self.default_offset
			else:
				limitValues.offset = self.default_offset

		if limitValues.limit < 0:
			limitValues.limit = self.default_limit

		if limitValues.offset < 0:
			limitValues.offset = self.default_offset

		return requestValues, limitValues

class Products(ProductHandler):

	# from http://stackoverflow.com/questions/23285558/datetime-date2014-4-25-is-not-json-serializable-in-djang
	@ndb.transactional
	def add_single_product(self, new_product):
		key = new_product.put()
		new_product = key.get()
		new_product.indexID = str(new_product.key.id())
		key = new_product.put()
		return new_product

	def get(self, *args, **kwargs):

		requestValues, limitValues = self.getValues(self.request)

		if not self.check_status(self.request):
			return

		parent = None

		# if order specified pull from those attached to parent
		if 'oid' in kwargs:
			order_key = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid'])).get()

			if not order_key:
				self.write_error(self.status_bad_request, "Order not found. ")
				return

			parent = order_key.key

		# if product specified
		if 'pid' in kwargs:
			results = db_defs.Product.query(db_defs.Product.indexID == str(kwargs['pid']), ancestor=parent).get()

			if results:
				results = results.to_dict()
				self.write_json(results)
				return
			else:
				self.write_error(self.status_bad_request, "Product not found in combination specified. ")
				return

		# check if a limit has been specified otherwise default is 10
		# check moved to initial area
		if limitValues.get('limit') == 0:
			limitValues.limit = None

		# if no pid specified get all the products
		q = db_defs.Product.query(ancestor=parent)
		keys = q.fetch(keys_only=True, limit=limitValues.limit, offset=limitValues.offset)
		results = { 'keys' : [x.id() for x in keys]}

		self.write_json(results)
		return

	def post(self, *args, **kwargs):
		''' Creates a Product Entity

		POST Body Variables:
		'''

		requestValues, limitValues = self.getValues(self.request)

		if not self.check_status(self.request):
			return

		if 'pid' in kwargs and not 'oid' in kwargs:
			self.write_error(self.status_not_allowed, "Not allowed.")
			return

		# if there is an oid there should only be a pid to go along with it
		if 'oid' in kwargs:
			q = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid']))
			good_oid = q.get()

			if 'pid' in kwargs and good_oid:
				checkpid = db_defs.Product.query(db_defs.Product.indexID == str(kwargs['pid']))
				checkpid = checkpid.get()

				if checkpid:
					orderObj = db_defs.Product(parent=good_oid.key)
					orderObj.sku = checkpid.sku
					orderObj.name = checkpid.name
					orderObj.description = checkpid.description
					orderObj.cost = checkpid.cost
					orderObj.created = self.get_now()
					orderObj.lastModified = self.get_now()

					if requestValues.get('quantity'):
						orderObj.quantity = int(requestValues.get('quantity'))
					else:
						orderObj.quantity = 1

					keys = self.add_single_product(orderObj)
					results = keys.to_dict()
					results['_id'] = keys.key.id()
					self.write_json(results)
					return
				else:
					self.write_error(self.status_bad_request, "Product ID does not exist to add to order")
					return
			else:
				self.write_error(self.status_not_allowed, "Order ID does not exist or product ID was not identified")
				return

		# otherwise if there is only a pid then we should add the product to the pool of products
		validated = self.validate(requestValues, "create")

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		# if no order specified pull from pool of products
		duplicateSku = self.validateSku(requestValues.get('sku'))

		if duplicateSku:
			self.write_error(self.status_bad_request, "Product already exists.")
			return

		prodObj = db_defs.Product()
		prodObj.sku = requestValues.get('sku')
		prodObj.name = requestValues.get('name')
		prodObj.description = requestValues.get('description')
		prodObj.cost = float(requestValues.get('cost'))
		prodObj.created = self.get_now()
		prodObj.lastModified = self.get_now()

		keys = self.add_single_product(prodObj)
		results = keys.to_dict()
		results['_id'] = keys.key.id()
		self.write_json(results)
		return

	def put(self, *args, **kwargs):

		if not self.check_status(self.request):
			return

		# otherwise if there is only a pid then we should add the product to the pool of products
		validated = self.validate(self.request)

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		if not 'pid' in kwargs:
			self.write_error(405, "Action not allowed")
			return

		# check the product exists
		prodObj = db_defs.Product.query(db_defs.Order.indexID == str(kwargs['pid']))
		prodObj = prodObj.get()

		if not prodObj:
			self.write_error(self.status_bad_request, "Product does not exist.")
			return

		# verify the sku does not exist anywhere but on this product
		if not str(prodObj.sku) == str(requestValues.get('sku')):
			if self.validateSku(requestValues.get('sku')):
				self.write_error(self.status_bad_request, "Sku cannot be duplicate of another sku")
				return
		
		if requestValues.get('sku'):
			prodObj.sku = requestValues.get('sku')
		if requestValues.get('name'):
			prodObj.name = requestValues.get('name')
		if requestValues.get('description'):
			prodObj.description = requestValues.get('description')
		if requestValues.get('cost'):
			prodObj.cost = float(requestValues.get('cost'))

		prodObj.lastModified = self.get_now()

		keys = self.add_single_product(prodObj)
		results = keys.to_dict()
		results['_id'] = keys.key.id()
		self.write_json(results)
		return

	def delete(self, *args, **kwargs):
		# todo:  institute a switch to allow deleting of all products from an order
		# todo:  institute a switch to allow deleting of one product from all orders by sku

		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		if 'pid' in kwargs:
			# if no order id just delete the product
			
			if 'oid' in kwargs:
				checkpid = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid'])).get()
				if checkpid:
					check = db_defs.Product.query(db_defs.Product.indexID == str(kwargs['pid']), ancestor=checkpid.key).get()
					if not check:
						self.write_error(self.status_not_found, "Product identified not found.  Products on orders must have Order Key identified.")
						return
				else:
					self.write_error(self.status_not_found, "Order identified not found.  Products on orders must have Order Key identified.")
					return
			else:
				check = db_defs.Product.query(db_defs.Product.indexID == str(kwargs['pid'])).get()

			if check:
				key = check.key.delete()
				results = {'result':'success','deleted':str(kwargs['pid'])}
				self.write_json(results)
			else:
				self.write_error(self.status_not_found, "Product identified not found.  Products on orders must have Order Key identified.")
				return
				
		else:
			self.write_error(self.status_bad_request, "Invalid Product ID.")
		return

# todo:  need to add query by order and query by customer (uniques maybe?)
class ProductSearch(ProductHandler):

	# queries all products in the product pool where parent = none
	def search(self, args, kwargs, request):
		''' Searches a Customer Entity
		email - String.  Email Address
		'''
		requestValues, limitValues = self.getValues(request)

		if not self.check_status(request):
			return

		validated = self.validate(requestValues)

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		q = db_defs.Product(parent=None).query()

		# check if the sku is valid to use in a filter
		if requestValues.get('sku'):
			q = q.filter(db_defs.Product.sku == requestValues.get('sku'))
		
		if requestValues.get('name'):
			q = q.filter(db_defs.Product.name == requestValues.get('name'))

		# check if the cost is valid to use in a filter
		if requestValues.get('cost'):
			q = q.filter(db_defs.Product.cost == float(requestValues.get('cost')))
			
		if requestValues.get('quantity'):
			q = q.filter(db_defs.Product.quantity == int(requestValues.get('quantity')))

		if limitValues.get('limit') == 0:
			limitValues.limit = None

		keys = q.fetch(keys_only=True, limit=limitValues.limit, offset=limitValues.offset)
		results = { 'keys':[x.id() for x in keys]}

		self.write_json(results)
		return

	def get(self, *args, **kwargs):
		self.search(args, kwargs, self.request)

	def post(self, *args, **kwargs):
		self.search(args, kwargs, self.request)


