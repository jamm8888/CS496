import webapp2
from google.appengine.ext import ndb
import db_defs
import re
from base_page import BaseHandler

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
		if self.request.get('limit') and re.match(self.intRegex(), self.request.get('limit')):
			limit = int(self.request.get('limit'))
			if limit == 0:
				limit = None
		else: 
			limit = self.default_limit

		if self.request.get('offset') and re.match(self.intRegex(), self.request.get('offset')):
			offset = int(self.request.get('offset'))
		else:
			offset = self.default_offset

		# if no pid specified get all the products
		q = db_defs.Product.query(ancestor=parent)
		keys = q.fetch(keys_only=True, limit=limit, offset=offset)
		results = { 'keys' : [x.id() for x in keys]}

		self.write_json(results)
		return

	def post(self, *args, **kwargs):
		''' Creates a Product Entity

		POST Body Variables:
		'''

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

					if self.request.get('quantity'):
						orderObj.quantity = int(self.request.get('quantity'))
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
		validated = self.validate(self.request, "create")

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		# if no order specified pull from pool of products
		duplicateSku = self.validateSku(self.request.get('sku'))

		if duplicateSku:
			self.write_error(self.status_bad_request, "Product already exists.")
			return

		prodObj = db_defs.Product()
		prodObj.sku = self.request.get('sku')
		prodObj.name = self.request.get('name')
		prodObj.description = self.request.get('description')
		prodObj.cost = float(self.request.get('cost'))
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
		if not str(prodObj.sku) == str(self.request.get('sku')):
			if self.validateSku(self.request.get('sku')):
				self.write_error(self.status_bad_request, "Sku cannot be duplicate of another sku")
				return
		
		if self.request.get('sku'):
			prodObj.sku = self.request.get('sku')
		if self.request.get('name'):
			prodObj.name = self.request.get('name')
		if self.request.get('description'):
			prodObj.description = self.request.get('description')
		if self.request.get('cost'):
			prodObj.cost = float(self.request.get('cost'))

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
	def get(self, *args, **kwargs):
		''' Searches a Customer Entity
		email - String.  Email Address
		'''

		if not self.check_status(self.request):
			return

		validated = self.validate(self.request)

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		q = db_defs.Product(parent=None).query()

		# check if the sku is valid to use in a filter
		if self.request.get('sku'):
			q = q.filter(db_defs.Product.sku == self.request.get('sku'))
		
		if self.request.get('name'):
			q = q.filter(db_defs.Product.name == self.request.get('name'))

		# check if the cost is valid to use in a filter
		if self.request.get('cost'):
			q = q.filter(db_defs.Product.cost == float(self.request.get('cost')))
			
		if self.request.get('quantity'):
			q = q.filter(db_defs.Product.quantity == int(self.request.get('quantity')))


		params = getLimits(self.request)
		keys = q.fetch(keys_only=True, limit=params['limit'], offset=params['offset'])
		results = { 'keys':[x.id() for x in keys]}

		self.write_json(results)
		return
