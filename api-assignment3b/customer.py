import webapp2
from google.appengine.ext import ndb
import db_defs
import re
from base_page import BaseHandler
import json

class CustomerHandler(BaseHandler):

	def __init__(self, request, response):
		BaseHandler.__init__(self)
		self.initialize(request, response)
		
	def validate(self, request, val=None):

		error = False
		message = ''
		validated = {}

		# if we are creating a product we need to verify all fields are filled in
		if val == "create":
			if not request.get('firstname'):
				error = True
				message += "First Name missing. "
			if not request.get('lastname'):
				error = True
				message += "Last Name missing. "
			if not request.get('email'):
				error = True
				message += "Email Missing. "

		# for both search and create we need to check the value
		if request.get('firstname') and not re.match(db_defs.Customer.nameRegex(), request.get('firstname')):
			error = True
			message += "First Name invalid. "

			if not re.match(db_defs.Customer.nameRegex(), str(request.get('firstname'))):
				error = True
				message += "First Name format issue. " + str(request.get('firstname'))

		if request.get('lastname') and not re.match(db_defs.Customer.nameRegex(), request.get('lastname')):
			error = True
			message += "Last Name invalid. "

			if not re.match(db_defs.Customer.nameRegex(), request.get('lastname')):
				error = True
				message += "First Name format issue. "

		if request.get('email') and not re.match(db_defs.Customer.emailRegex(), request.get('email')):
			error = True
			message += "Email invalid. "

		if not error and request.get('email') and (val == "create"):
			if re.match(db_defs.Customer.emailRegex(), request.get('email')):
				# check sku does not already exist
				q = db_defs.Customer.query()
				q = q.filter(db_defs.Customer.email == str(request.get('email')).lower())
			if q.fetch(keys_only=True):
				error = True
				message += "Email already exists. "

		validated['error'] = error
		validated['message'] = message
		return validated

	def getChildOrders(customer_id):
		q = db_defs.Order.query(db_defs.Order.indexID == order_id)
		check = q.get()

		if not check: 
			self.write_error(self.status_not_found, "Order not found.")
			return

		return check

	def getValues(self, request):

		requestValues = db_defs.Customer()
		limitValues = db_defs.Limits()

		try:
			request = json.loads(self.request.body)
			if 'firstname' in request:
				requestValues.firstName = request['firstname']
			if 'lastname' in request:
				requestValues.lastName = request['lastname']
			if 'email' in request:
				requestValues.email = request['email']
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
			if self.request.get('firstname'):
				requestValues.firstName = self.request.get('firstname')
			if self.request.get('lastname'):
				requestValues.lastName = self.request.get('lastname')
			if self.request.get('email'):
				requestValues.email = self.request.get('email')

			if self.request.get('limit'):
				try:
					limitValues.limit = int(self.request.get('limit'))
				except ValueError, e:
					limitValues.limit = self.default_limit

			if self.request.get('offset'):
				try:
					limitValues.offset = int(self.request.get('offset'))
				except ValueError, e:
					limitValues.offset = self.default_offset

		if limitValues.limit < 0:
			limitValues.limit = self.default_limit

		if limitValues.offset < 0:
			limitValues.offset = self.default_offset

		return requestValues, limitValues


class Customers(CustomerHandler):

	def get(self, *args, **kwargs):

		requestValues, limitValues = self.getValues(self.request)

		# check if application/json identified in accept
		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		if 'cid' in kwargs:
			check = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get()
			if check: 
				results = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get().to_dict()
				results['id'] = kwargs['cid']
			else:
				self.write_error(self.status_not_found, "Customer not found.")
				return
		else:
			# process the query and return the keys only
			q = db_defs.Customer.query()

			if limitValues.get('limit') == 0:
				limitValues.limit = None

			keys = q.fetch(keys_only=True, limit=limitValues.limit, offset=limitValues.offset)
			results = { 'keys' : [x.id() for x in keys]}

		self.write_json(results)
		return

	def post(self, *args, **kwargs):
		''' Creates a Customer Entity

		POST Body Variables:
		firstName - Required. First Name
		lastName - Required. Last Name
		email - Required. Email
		'''

		requestValues, limitValues = self.getValues(self.request)

		if not self.check_status(self.request):
			return

		if 'cid' in kwargs:
			self.write_error(405, "Incorrect Action type specified.  To update a customer PUT is required.")
			return

		validated = self.validate(requestValues, "create")

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		#k = ndb.Key(db_defs.Customer, self.app.config.get('default-group'))
		new_customer = db_defs.Customer()
		new_customer.firstName = requestValues.get('firstname')
		new_customer.lastName = requestValues.get('lastname')
		new_customer.email = str(requestValues.get('email')).lower()
		new_customer.created = self.get_now()
		new_customer.lastModified = self.get_now()

		key = new_customer.put()
		results = new_customer.to_dict()
		results['_id'] = key.id()

		self.write_json(results)

		return

	def put(self, *args, **kwargs):

		requestValues, limitValues = self.getValues(self.request)

		# check if application/json identified in accept
		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		check = None

		if 'cid' in kwargs:
			check = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get()

		if check: 
			validated = self.validate(self.request)

			if re.match(db_defs.Customer.emailRegex(), requestValues.get('email')):
				# check sku does not already exist
				q = db_defs.Customer.query()
				q = q.filter(db_defs.Customer.email == str(requestValues.get('email')).lower())
				q = q.get(use_cache=False, use_memcache=False)

				if q and not int(kwargs['cid']) == q.key.id():
					validated['error'] = True
					validated['message'] += "Email already exists. "

			if validated['error']:
				self.write_error(self.status_bad_request, validated['message'])
				return

			if self.request.get('firstname'):
				check.firstName = requestValues.get('firstname')

			if self.request.get('lastname'):
				check.lastName = requestValues.get('lastname')

			if self.request.get('email'):
				check.email = str(requestValues.get('email')).lower()

			check.lastModified = self.get_now()
			key = check.put()
			results = check.to_dict()
			results['_id'] = key.id()
			self.write_json(results)
			return
			
		else:
			self.write_error(self.status_bad_request, "Invalid Customer ID.")
			return

	def delete(self, *args, **kwargs):
		# this will be the challenging one as we will need to delete orders and product children first.
		# check if application/json identified in accept
		# this will need a transaction and a tree search to delete all children.
		# if the tree search checks as many levels as needed this becomes viable for any number of future trees.

		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		if 'cid' in kwargs:
			#check = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get()
			check = db_defs.Customer.get_by_id(int(kwargs['cid']))

			if not check:
				self.write_error(self.status_not_found, "Customer not found.")
				return 

			# need routine to recursively delete childrenj
			q = db_defs.Product.query(ancestor=check.key)
			keys = q.fetch(keys_only=True)

			deletedProducts = []
			deletedOrders = []
			
			for x in keys:
				deletedProducts.append(str(x.id()))
				x.delete()

			q = db_defs.Order.query(ancestor=check.key)
			keys = q.fetch(keys_only=True)

			for x in keys:
				deletedOrders.append(str(x.id()))
				x.delete()

			key = check.key.delete()
			results = {'result':'success','deleted':str(kwargs['cid']),'deletedOrders':deletedOrders,'deletedProducts':deletedProducts}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(results)
			return
		else:
			self.write_error(self.status_bad_request, "Customer ID needs o be specified.")
			return

class CustomerSearch(CustomerHandler):

	def search(self, args, kwargs, request):
		''' Searches a Customer Entity
		email - String.  Email Address
		'''
		requestValues, limitValues = self.getValues(self.request)

		if not self.check_status(self.request):
			return

		validated = self.validate(requestValues)

		if validated['error']:
			self.write_error(self.status_bad_request, validated['message'])
			return

		q = db_defs.Customer.query()
		if requestValues.get('email'):
			q = q.filter(db_defs.Customer.email == str(requestValues.get('email')).lower())
		if requestValues.get('lastname'):
			q = q.filter(db_defs.Customer.lastName == requestValues.get('lastname'))
		if requestValues.get('firstname'):
			q = q.filter(db_defs.Customer.firstName == requestValues.get('firstname'))

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