import webapp2
from google.appengine.ext import ndb
import db_defs
import re
from base_page import BaseHandler

class OrderHandler(BaseHandler):

	def __init__(self, request, response):
		BaseHandler.__init__(self)
		self.initialize(request, response)

	# gets a single order by order ID.
	def getOrder(self, order_id):
		check = db_defs.Order.query(db_defs.Order.indexID == order_id).get()

		if not check: 
			self.write_error(self.status_not_found, "Order not found.")
			return

		return check


class Orders(OrderHandler):

	@ndb.transactional
	def add_order(self, cid_key, new_order):
		key = new_order.put()
		new_order = key.get()
		new_order.indexID = str(new_order.key.id())
		key = new_order.put()
		cid_key = cid_key.put()
		return new_order

	def post(self, *args, **kwargs):
		''' Creates a Customer Entity

		POST Body Variables:
		firstName - Required. First Name
		lastName - Required. Last Name
		email - Required. Email
		'''
		if not self.check_status(self.request):
			return

		if 'cid' in kwargs and not 'oid' in kwargs:
			cid_key = ndb.Key(db_defs.Customer, int(kwargs['cid']))
			cid = cid_key.get()
			if not cid:
				self.response.status = self.status_bad_request
				self.response.status_message = "Invalid Request.  Customer key not found."
				return
		else:
			self.response.status = 405
			self.response.status_message = "Invalid Request.  Customer key required."
			return

		#k = ndb.Key(db_defs.Customer, self.app.config.get('default-group'))
		cid.lastOID = cid.lastOID + 1
		new_order = db_defs.Order(parent=cid.key)
		new_order.orderId = kwargs['cid'] + "-" + str(cid.lastOID)
		new_order.created = self.get_now()
		new_order.lastModified = self.get_now()

		keys = self.add_order(cid, new_order)
		results = keys.to_dict()
		results['_id'] = keys.key.id()

		self.write_json(results)
		return

	def get(self, *args, **kwargs):

		# check if application/json identified in accept
		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		if 'cid' in kwargs:
			customer_key = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get()

			if customer_key:
				if 'oid' in kwargs:
					q = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid']), ancestor=customer_key.key)
					check = q.get()

					if not check: 
						self.write_error(self.status_not_found, "Order not found.")
						return
					results = check.to_dict()
				else:
					params = self.getLimits(self.request)

					q = db_defs.Order.query(ancestor=customer_key.key)
					keys = q.fetch(keys_only=True, limit=params['limit'], offset=params['offset'])
					results = { 'keys' : [x.id() for x in keys]}
			else: 
				self.write_error(self.status_not_found, "Customer not found.")
				return

		elif 'oid' in kwargs:
			check = self.getOrder(str(kwargs['oid']))
			if check:
				results = check.to_dict()
			else:
				self.write_error(self.status_not_found, "Order not found.")
				return
		else:
			params = self.getLimits(self.request)
		
			# process the query and return the keys only
			q = db_defs.Order.query()
			keys = q.fetch(keys_only=True, limit=params['limit'], offset=params['offset'])
			results = { 'keys' : [x.id() for x in keys]}

		self.write_json(results)
		return

	def delete(self, *args, **kwargs):
		# this will be the challenging one as we will need to delete orders and product children first.
		# check if application/json identified in accept
		# this will need a transaction and a tree search to delete all children.
		# if the tree search checks as many levels as needed this becomes viable for any number of future trees.

		if not self.check_status(self.request):
			return

		# check if cid if so we are querying a specific key otherwise we are querying all keys
		if 'oid' in kwargs:
			if 'cid' in kwargs: 
				check = ndb.Key(db_defs.Customer, int(kwargs['cid'])).get()
				if not check:
					self.write_error(self.status_not_found, "Invalid Customer ID.")
					return
				q = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid']), ancestor=check.key)
			else:
				q = db_defs.Order.query(db_defs.Order.indexID == str(kwargs['oid']))
			check = q.get()

			if not check: 
				self.write_error(self.status_not_found, "Order not found.")
				return

			# first check if there are children
			# need routine to recursively delete childrenj
			q = db_defs.Product.query(ancestor=check.key)
			keys = q.fetch(keys_only=True)

			deletedKeys = []

			for x in keys:
				deletedKeys.append(x.id())
				x.delete()

			key = check.key.delete()
			results = {'result':'success','deleted':str(kwargs['oid']),'deletedChildren':deletedKeys}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(results)

		else:
			if 'cid' in kwargs:
				self.write_error(self.status_not_allowed, "Invalid Order ID.")
				return
			self.write_error(self.status_not_allowed, "Invalid Method")
		return
