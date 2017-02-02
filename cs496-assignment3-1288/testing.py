import webapp2
import json
import urllib
import time
import db_defs
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from base_page import BaseHandler
from testMethods import TestMethods


class TestCustomer(TestMethods):

	def get(self):

		""" 
		Check DELETE customers
		"""		
		customer_url = self.base_url + self.customers_url

		self.response.write("<h3>Preparing Datastore - deleting residual data</h3>")
		self.testSetup()

		# build a customer pool
		# foreach customer in the list create a customer twice make sure the second time does not succeed
		"""
		Customers Testing
		"""

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("<html>")
		self.response.write("<head>")
		self.response.write("<style>")
		self.response.write(".failed {")
		self.response.write("color: maroon;font-weight: bold;")
		self.response.write("}")
		self.response.write(".passed {")
		self.response.write("color: green;font-weight: bold;")
		self.response.write("}")
		self.response.write("</style>")
		self.response.write("</head>")
		self.response.write("<body>")
		self.response.write("<h1>Customers</h1>")
		self.response.write("<b>"+ customer_url +"</b>")

		self.response.write("<h2>Group URL: No data in datastore</h2>")
		'''
		Empty Customer GET Testing (no customers in datastore)
		'''
		# GET: No Customers in the database test with incorrect JSON
		self.response.write("<h3>GET Customers: Bad Mime Type</h3>")
		self.testGetBadMime1(customer_url)

		# GET: No Customers in the database
		self.response.write("<h3>GET Customers: Mime json - No Customers in datastore</h3>")
		self.testGetObjects(customer_url, 0)

		'''
		Empty Customer POST Testing
		'''
		# POST: No Customers in the database test with incorrect JSON
		self.response.write("<h3>POST Customers: Bad Mime Type</h3>")
		self.testPostBadMime1(customer_url)

		self.response.write("<h3>POST Customers: Mime json - No Data</h3>")
		self.testPostNoData(customer_url)


		'''
		Empty Customer PUT Testing
		'''
		# PUT: No Customers in the database test with incorrect JSON
		self.response.write("<h3>PUT Customers: Bad Mime Type</h3>")
		self.testPutBadMime1(customer_url)

		self.response.write("<h3>PUT Customers: Mime json - No Data</h3>")
		self.testPostNoData(customer_url)


		'''
		Empty Customer DELETE Testing
		'''

		# DELETE: No Customers in the database test with incorrect JSON
		self.response.write("<h3>DELETE Customers: Bad Mime Type</h3>")
		self.testDeleteObject(customer_url, "xml", self.status_not_acceptable)


		'''
		Customer POST Testing
		'''
		self.response.write("<h3>POST Customers: Mime json - Add Customers Valid Data</h3>")
		customer_keys = self.testPostValidObjects(customer_url, "customers", self.good_customer_list)
		
		self.response.write("<h3>POST Customers: Mime json - Add Customers Invalid Data</h3>")
		self.testPostInvalidObject(customer_url, db_defs.Customer, self.erronous_customer_dict)
		
		self.response.write("<h3>POST Customers: Mime json - Missing Required Fields</h3>")
		self.testPostInvalidObject(customer_url, db_defs.Customer, self.missing_customer_dict)

		""" 
		Check GET now has all customers returned
		"""
		self.response.write("<h3>GET Customers: Mime json - Customers in datastore</h3>")
		self.testGetAllObjects(customer_url, len(self.good_customer_list), customer_keys)

		'''
		CUSTOMERS/CID
		'''

		self.response.write("<h1>Customers/CID</h1>")
		self.response.write("<b>"+ customer_url +"/CID</b>")

		'''
		Single Customer GET Testing 
		'''
		self.response.write("<h3>GET Customers: Mime json - Single Customer</h3>")
		self.testGetSingleObject(customer_url, db_defs.Customer)

		'''
		Single Customer GET Testing 
		'''
		self.response.write("<h3>GET Customers: Mime json - Single Customer Bad ID</h3>")
		self.testGetBadSingleObject(customer_url)

		'''
		Single Customer PUT testing
		'''
		
		self.response.write("<h3>UPDATE Customers: Mime json - Update Customer Good Data</h3>")
		self.testPutValidCustomers(customer_url)
		
		'''
		Single Customer PUT testing - BAD DATA
		'''
		
		self.response.write("<h3>UPDATE Customers: Mime json - Update Customer Invalid Data</h3>")
		self.testPutInvalidCustomers(customer_url)	

		'''
		Single Customer PUT testing - NO DATA
		'''
		
		self.response.write("<h3>UPDATE Customers: Mime json - Update Customer No Data</h3>")
		self.testPutNoDataObject(customer_url, db_defs.Customer)


		""" 
		Check DELETE bad customer id
		"""		
		self.response.write("<h3>DELETE Customers: Mime json - Delete Bad ID from Datastore</h3>")
		self.testDeleteBadObject(customer_url, db_defs.Customer)

		""" 
		Check DELETE good customer id
		"""		
		self.response.write("<h3>DELETE Customers: Mime json - Delete Valid ID from Datastore</h3>")



		'''
		ORDERS
		'''
		order_url = self.base_url + self.orders_url
		self.response.write("<h1>Orders</h1>")
		self.response.write("<b>"+ self.orders_url +"</b>")

		'''
		Empty Orders GET Testing (no customers in datastore)
		'''
		# GET: No Customers in the database test with incorrect JSON
		self.response.write("<h3>GET Orders: Bad Mime Type</h3>")
		self.testGetBadMime1(order_url)

		# GET: No Customers in the database
		self.response.write("<h3>GET Orders: Mime json - No Customers in datastore</h3>")
		self.testGetObjects(order_url, 0)

		'''
		Empty Orders POST Testing
		'''
		# POST: No Customers in the database test with incorrect JSON
		self.response.write("<h3>POST Orders: Bad Mime Type</h3>")
		self.testPostBadMime1(order_url)

		self.response.write("<h3>POST Orders: Mime json - No Data</h3>")
		self.testPostNotAllowedData(order_url, "post", 400)


		'''
		Empty Orders PUT Testing
		'''
		# PUT: No Customers in the database test with incorrect JSON
		self.response.write("<h3>PUT Orders: Bad Mime Type</h3>")
		self.testPutBadMime1(order_url, 405)

		self.response.write("<h3>PUT Orders: Mime json - No Data</h3>")
		self.testPostNotAllowedData(order_url, "put", 405)


		'''
		Empty Orders DELETE Testing
		'''

		# DELETE: No Customers in the database test with incorrect JSON
		self.response.write("<h3>DELETE Orders: Bad Mime Type</h3>")
		self.testDeleteObject(order_url, "xml", self.status_not_acceptable)



		self.response.write("<h1>/Customer/CID/Orders</h1>")
		self.response.write("<b>"+ customer_url +"/CID/" + order_url + "</b>")		

		'''
		Orders ADD with valid customer id
		'''
		self.response.write("<h3>POST Orders: Mime json Valid Customer ID</h3>")
		self.testAddObject(customer_url, db_defs.Customer)

		'''
		Orders ADD with invalid customer id
		'''
		self.response.write("<h3>POST Orders: Mime json Invalid Customer ID</h3>")
		self.testAddObject(customer_url, db_defs.Customer, self.bad_key, None, self.status_bad_request)

		'''
		Orders GET with order data in the datastore
		'''
		self.response.write("<h3>GET Orders: Mime json - Orders in the datastore</h3>")
		self.testGetOrders(order_url)

		'''
		Orders GET all orders for a customer
		'''
		self.response.write("<h3>GET Orders: Mime json - Get all orders for a customer</h3>")
		self.testGetCustomerOrders(customer_url)

		'''
		Orders GET all orders for a customer bad id
		'''
		self.response.write("<h3>GET Orders: Mime json - Invalid Customer ID</h3>")
		self.testGetCustomerOrders(customer_url, 404, self.bad_key)

		'''
		Orders PUT - invalid action
		'''
		self.response.write("<h3>PUT Orders: Invalid Action</h3>")
		self.testActionSingleObject(customer_url, db_defs.Customer, urlfetch.PUT, self.status_not_allowed, "orders")

		''' 
		Orders DELETE - invalid action
		'''
		self.response.write("<h3>DELETE Orders: Invalid Action</h3>")
		self.testActionSingleObject(customer_url, db_defs.Customer, urlfetch.DELETE, self.status_not_allowed, "orders")


		'''
		/Customer/CID/Orders/OID _ WE ARE HERE
		'''
		self.response.write("<h1>/Customer/CID/Orders/OID</h1>")
		self.response.write("<b>"+ customer_url +"/CID/" + order_url + "/OID</b>")	

		'''
		Orders GET single order with valid id
		'''
		self.response.write("<h3>GET Orders: Mime json - Single order with valid id</h3>")
		self.testActionObjectParent(self.customers_url, db_defs.Customer, self.orders_url, db_defs.Order, urlfetch.GET, 200, False)

		'''
		Orders GET single order with invalid cid and invalid oid
		'''
		self.response.write("<h3>GET Orders: Mime json - Single order with invalid ids</h3>")
		self.testActionObjectParent(self.customers_url, db_defs.Customer, self.orders_url, db_defs.Order, urlfetch.GET, self.status_not_found, True)

		'''
		Orders POST single order with valid id
		'''
		self.response.write("<h3>POST Orders: Mime json - Single order with valid id</h3>")
		self.testActionObjectParent(self.customers_url, db_defs.Customer, self.orders_url, db_defs.Order, urlfetch.POST, self.status_bad_request, False)

		'''
		Orders PUT single order with valid id
		'''
		self.response.write("<h3>PUT Orders: Mime json - Single order with valid cid and oid</h3>")
		self.testActionObjectParent(self.customers_url, db_defs.Customer, self.orders_url, db_defs.Order, urlfetch.PUT, 405, False)

		'''
		Orders DELETE single order with valid id
		'''
		self.response.write("<h3>DELETE Orders: Mime json - Single order with valid cid and oid</h3>")
		self.testActionObjectParent(self.customers_url, db_defs.Customer, self.orders_url, db_defs.Order, urlfetch.DELETE, 200, False)

		""" 
		Check DELETE Orders - Invalid Customer ID
		"""		
		self.response.write("<h3>DELETE Order: Mime json - Invalid Customer ID</h3>")
		newurl = customer_url + "/" + self.bad_key + self.orders_url + "/" + self.bad_key
		self.testDeleteBadObject(newurl, db_defs.Order)

		'''
		PRODUCTS
		'''
		'''
		Empty Product GET Testing (no customers in datastore)
		'''
		# GET: No Customers in the database test with incorrect JSON
		product_url = self.base_url + self.products_url
		self.response.write("<h3>GET Products: Bad Mime Type</h3>")
		self.testGetBadMime1(product_url)

		# GET: No Customers in the database
		self.response.write("<h3>GET Products: Mime json - No Customers in datastore</h3>")
		self.testGetObjects(product_url, 0)
		
		'''
		Empty Product POST Testing
		'''
		# POST: No Customers in the database test with incorrect JSON
		self.response.write("<h3>POST Products: Bad Mime Type</h3>")
		self.testPostBadMime1(product_url)

		self.response.write("<h3>POST Products: Mime json - No Data</h3>")
		self.testPostNotAllowedData(product_url, "post", 400)


		'''
		Empty Product PUT Testing
		'''
		# PUT: No Customers in the database test with incorrect JSON
		self.response.write("<h3>PUT Products: Bad Mime Type</h3>")
		self.testPutBadMime1(product_url, self.status_not_acceptable)

		self.response.write("<h3>PUT Products: Mime json - No Data</h3>")
		self.testPostNotAllowedData(product_url, "put", 405)


		'''
		Empty Product DELETE Testing
		'''

		# DELETE: No Customers in the database test with incorrect JSON
		self.response.write("<h3>DELETE Products: Bad Mime Type</h3>")
		self.testDeleteObject(product_url, "xml", 406)

		'''
		Product POST - Add Products with valid Data
		'''
		self.response.write("<h3>POST Product: Mime json - Valid Product Data Sent</h3>")
		self.testPostValidObjects(product_url, "products", self.good_product_list)

		'''
		Product POST - Add Product with invalid data
		'''
		self.response.write("<h3>POST Product: Mime Type json Invalid Data</h3>")
		self.testPostInvalidObject(product_url, db_defs.Product, self.erronous_product_dict)

		'''
		Product POST - Add Product with missing data
		'''
		self.response.write("<h3>POST Products: Mime json - Missing Required Fields</h3>")
		self.testPostInvalidObject(customer_url, db_defs.Product, self.missing_product_dict)

		'''
		/orders/OID/products/PID
		'''

		'''
		Product POST - Add to order with valid order valid product
		'''
		self.response.write("<h3>POST Orders: Valid Order, Valid Project</h3>")
		self.testAddObject(product_url, db_defs.Order)

		'''
		Product POST - Add to order with valid order invalid product
		'''
		self.response.write("<h3>POST Orders: Valid Order, Invalid Project</h3>")
		self.testAddObject(product_url, db_defs.Order, None, self.bad_key, self.status_bad_request)

		'''
		Product POST - Add to order with invalid order valid product
		'''
		self.response.write("<h3>POST Orders: Invalid Order, Valid Project</h3>")
		self.testAddObject(product_url, db_defs.Order, self.bad_key, None, self.status_bad_request)

		'''
		Product POST - Add to order with invalid order invalid product
		'''
		self.response.write("<h3>POST Orders: Invalid Order, Invalid Project</h3>")
		self.testAddObject(product_url, db_defs.Order, self.bad_key, self.bad_key, self.status_bad_request)

		'''
		Product PUT - Update order with no data changed
		'''
		# get an order
		
		'''
		Product PUT - Update order with invalid data
		'''
		self.response.write("<h3>PUT Order Product invalid data</h3>")
		'''
		Product PUT - Update product on order with duplicate SKU
		'''
		self.response.write("<h3>PUT Order Product Duplicate SKU (allowed)</h3>")
		'''
		Product DELETE - Delete product on order with invalid produproduct on order
		'''
		self.response.write("<h3>DELETE Order Product - Invalid Product Key</h3>")
		'''
		Order DELETE - check products deleted.
		'''
		self.response.write("<h3>DELETE Order - with products</h3>")

		'''
		Customer DELETE - check products and orders deleted.
		'''
		self.response.write("<h3>DELETE Customer - with orders and products<h3>")

		""" 
		Check DELETE products
		"""		
		self.response.write("<h3>DELETE Products: Mime json - Products in datastore</h3>")
		self.testDeleteAllObjects(db_defs.Product)
		self.response.write("</body></html>")

		""" 
		Check DELETE Orders
		"""		
		self.response.write("<h3>DELETE Orders: Mime json - Orders in datastore</h3>")
		self.testDeleteAllObjects(db_defs.Order)
		self.response.write("</body></html>")

		""" 
		Check DELETE customers
		"""		
		self.response.write("<h3>DELETE Customers: Mime json - Delete single Customers in datastore</h3>")
		self.testDeleteAllObjects(db_defs.Customer)
		self.response.write("</body></html>")
		