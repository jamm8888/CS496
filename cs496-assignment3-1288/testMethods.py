import webapp2
import json
import urllib
from google.appengine.api import urlfetch
from testDefinitions import TestDefinitions
import time
from google.appengine.ext import ndb
import db_defs

class TestMethods(TestDefinitions):
	sleep = False

	def testSetup(self):
		'''
		testSetup 
		Deletes all the data in the datastore
		'''
		ndb.delete_multi(db_defs.Customer.query().fetch(keys_only=True))
		ndb.delete_multi(db_defs.Order.query().fetch(keys_only=True))
		ndb.delete_multi(db_defs.Product.query().fetch(keys_only=True))

	def check_status(self, expected, actual):
		errors = False
		message = "<br>Expected Status Code: " + str(expected)
		message += "<br>Actual Status Code: " + str(actual)

		if not expected == actual:
			errors = True

		return errors,message

	def checkInResponse(self, message, response_content, field, expected, actual):
		errors = False
		message += "<br>Expected " + field + " in Response: " + str(expected)

		if field in response_content and expected == actual:
			message += "<br>Actual " + field + " Received: " + str(actual)
		else:
			errors = True
		return errors, message



	def testPutValidCustomers(self, url):
		# get a customer let's use the first one in the series as there are 5
		customer = db_defs.Customer.query()
		customer = customer.filter(db_defs.Customer.email == self.good_customer_list[1]['email'])
		customer = customer.get(use_cache=False, use_memcache=False)

		if customer:
			newurl = url + "/" + str(customer.key.id())

			self.response.write("<p>Updating customer url: " + newurl + "</p>")
			self.response.write("Updating customer firstname: " + str(customer.firstName))
			self.response.write("<br>Updating customer lastname: " + str(customer.lastName))
			self.response.write("<br>Updating customer email: " + str(customer.email))
			self.response.write("<br><br><b>Valid Firstname Update: </b> - ")

			response = self.actionObject(newurl, urlfetch.PUT, self.good_update_list['firstname'])
			response_content = json.loads(response.content)
			
			# firstname checks
			if response_content['firstName'] == self.good_update_list['firstname']['firstname']:
				self.response.write("<span class='passed'>SUCCESS</span>")
			else: 
				self.response.write("<span class='failed'>FAILED</span>")

			self.response.write("<br>Expected First Name: " + self.good_update_list['firstname']['firstname'])
			self.response.write("<br>Actual First Name: " + response_content['firstName'])
			self.response.write("<br>Expected Last Name: " + customer.lastName)
			self.response.write("<br>Actual Last Name: " + response_content['lastName'])
			self.response.write("<br>Expected Email: " + customer.email)
			self.response.write("<br>Actual Email: " + response_content['email'])

			# second to update lastname
			customer = db_defs.Customer.query()
			customer = customer.filter(db_defs.Customer.email == self.good_customer_list[1]['email'])
			customer = customer.get(use_cache=False, use_memcache=False)
			self.response.write("<br><br><b>Valid Lastname Update: </b> - ")
			response = self.actionObject(newurl, urlfetch.PUT, self.good_update_list['lastname'])
			response_content = json.loads(response.content)

			# firstname checks
			if response_content['lastName'] == self.good_update_list['lastname']['lastname']:
				self.response.write("<span class='passed'>SUCCESS</span>")
			else: 
				self.response.write("<span class='failed'>FAILED</span>")

			self.response.write("<br>Expected First Name: " + self.good_update_list['firstname']['firstname'])
			self.response.write("<br>Actual First Name: " + response_content['firstName'])
			self.response.write("<br>Expected Last Name: " + self.good_update_list['lastname']['lastname'])
			self.response.write("<br>Actual Last Name: " + response_content['lastName'])
			self.response.write("<br>Expected Email: " + customer.email)
			self.response.write("<br>Actual Email: " + response_content['email'])



			# third to update email
			customer = db_defs.Customer.query()
			customer = customer.filter(db_defs.Customer.email == self.good_customer_list[0]['email'])
			customer = customer.get(use_cache=False, use_memcache=False)
			old_email = customer.email
			self.response.write("<br><br><b>Valid Non-duplicate Email Update: </b> - ")

			response = self.actionObject(newurl, urlfetch.PUT, self.good_update_list['email'])
			response_content = json.loads(response.content)

			# email checks
			if response_content['email'] == self.good_update_list['email']['email']:
				self.response.write("<span class='passed'>SUCCESS</span>")
			else: 
				self.response.write("<span class='failed'>FAILED</span>")

			self.response.write("<br>Expected First Name: " + self.good_update_list['firstname']['firstname'])
			self.response.write("<br>Actual First Name: " + response_content['firstName'])
			self.response.write("<br>Expected Last Name: " + self.good_update_list['lastname']['lastname'])
			self.response.write("<br>Actual Last Name: " + response_content['lastName'])
			self.response.write("<br>Expected Email: " + self.good_update_list['email']['email'])
			self.response.write("<br>Actual Email: " + response_content['email'])
		else:
			self.response.write("<span class='failed'>FAILED - Something wrong</span>")
		return

	def testPutInvalidCustomers(self, url):
		# get a customer let's use the first one in the series as there are 5
		customer = db_defs.Customer.query()
		customer = customer.filter(db_defs.Customer.email == self.good_customer_list[0]['email'])
		customer = customer.get(use_cache=False, use_memcache=False)

		if customer:
			newurl = url + "/" + str(customer.key.id())

			self.response.write("<p>Updating customer url: " + newurl + "</p>")
			self.response.write("Updating customer firstname: " + str(customer.firstName))
			self.response.write("<br>Updating customer lastname: " + str(customer.lastName))
			self.response.write("<br>Updating customer email: " + str(customer.email))
			self.response.write("<br><br><b>Invalid Firstname Update: </b> - ")
			response = self.actionObject(newurl, urlfetch.PUT, self.bad_update_list['firstname'])

			response_content = json.loads(response.content)

			errors,message = self.check_status(self.status_bad_request, response.status_code)
			message += "<br>Sent First Name: " + self.bad_update_list['firstname']['firstname']

			if not errors:
				message = "<span class='passed'>SUCCESS</span>" + message
			else: 
				message = "<span class='failed'>FAILED</span>" + message
			
			self.response.write(message)

			
			# second to update lastname
			customer = db_defs.Customer.query()
			customer = customer.filter(db_defs.Customer.email == self.good_customer_list[0]['email'])
			customer = customer.get(use_cache=False, use_memcache=False)

			self.response.write("<br><br><b>Invalid Lastname Update: </b> - ")
			newurl = url + "/" + str(customer.key.id())

			response = self.actionObject(newurl, urlfetch.PUT, self.bad_update_list['lastname'])
			response_content = json.loads(response.content)
			
			errors,message = self.check_status(self.status_bad_request, response.status_code)

			message += "<br>Sent Last Name: " + self.bad_update_list['lastname']['lastname']

			if not errors:
				message = "<span class='passed'>SUCCESS</span>" + message
			else: 
				message = "<span class='failed'>FAILED</span>" + message
			
			self.response.write(message)


			# third to update email
			customer = db_defs.Customer.query()
			customer = customer.filter(db_defs.Customer.email == self.good_customer_list[0]['email'])
			customer = customer.get(use_cache=False, use_memcache=False)
			
			self.response.write("<br><br><b>Invalid email Update: </b> - ")
			newurl = url + "/" + str(customer.key.id())
			response = self.actionObject(newurl, urlfetch.PUT, self.bad_update_list['email'])
			response_content = json.loads(response.content)
			
			errors,message = self.check_status(self.status_bad_request, response.status_code)

			message += "<br>Sent Email: " + self.bad_update_list['email']['email']
			if not errors:
				message = "<span class='passed'>SUCCESS</span>" + message
			else: 
				message = "<span class='failed'>FAILED</span>" + message
			
			self.response.write(message)

			# third to update duplicate email
			customer = db_defs.Customer.query()
			customer = customer.filter(db_defs.Customer.email == self.good_customer_list[0]['email'])
			customer = customer.get(use_cache=False, use_memcache=False)
			
			self.response.write("<br><br><b>Duplicate email Update: </b> - ")
			newurl = url + "/" + str(customer.key.id())
			response = self.actionObject(newurl, urlfetch.PUT, self.bad_update_list['duplicateemail'])
			response_content = json.loads(response.content)
			
			# check status and write message
			errors,message = self.check_status(self.status_bad_request, response.status_code)

			message += "<br>Sent Duplicate Email: " + self.bad_update_list['duplicateemail']['email']
			if not errors:
				message = "<span class='passed'>SUCCESS</span>" + message
			else: 
				message = "<span class='failed'>FAILED</span>" + message
			
			self.response.write(message)
		else:
			self.response.write("<span class='failed'>FAILED - Something wrong</span>")
		return


	def testAddObject(self, url, objectType, parentID=None, childID=None, status_code=200):

		parentUrl = ""
		childUrl = ""

		if objectType == db_defs.Order:
			if not childID:
				results = db_defs.Product.query(ancestor=None).fetch(limit=1, offset=2)
				if results:
					childID = str(results[0].key.id())
				else:
					childID = ""
			parentUrl = self.orders_url
			childUrl = self.products_url + "/" + childID
			
		if objectType == db_defs.Customer:
			parentUrl = self.customers_url
			childUrl = self.orders_url

		if not parentID:

			for x in range(0,5):
				results = objectType.query().fetch(limit=1, offset=x)
				if results:
					objectID = results[0].key.id()
				else:
					objectID = None
				add_url = self.base_url + parentUrl + "/" + str(objectID) + childUrl

				for y in range(-1,x):
					message = "<br>POST " + add_url
					response = self.actionObject(add_url, urlfetch.POST)

					if response.status_code == status_code:
						message += "<br><span class='passed'>SUCCESS</span>"
					else:
						message += "<br><span class='failed'>FAILED</span>"
						
					message += "<br>Expected Response Code: " + str(status_code)
					message += "<br>Actual Response Code: " + str(response.status_code)
					message += "<br>Actual Response" + str(response.content)

		else: 
			add_url = self.base_url + parentUrl + "/" + str(parentID) + childUrl

			message = "<br>POST " + add_url
			response = self.actionObject(add_url, urlfetch.POST)

			if response.status_code == status_code:
				message += "<br><span class='passed'>SUCCESS</span>"
			else:
				message += "<br><span class='failed'>FAILED</span>"
			message += "<br>Expected Response Code: " + str(status_code)
			message += "<br>Actual Response Code: " + str(response.status_code)
			message += "<br>Actual Response" + str(response.content)
		self.response.write(message)
		self.response.write("<br>")
		return

	def testAddObjects(self, url, objectType, objectList):
		objects = []
		self.response.write("<p>URL: " + url + "</p>")

		for x in objectList:
			payload = x
			response = self.actionObject(url, urlfetch.POST, payload)
			response_content = json.loads(response.content)
			
			errors = False

			errors,message = self.check_status(self.status_success_code, response.status_code)

			if objectType == "customers":
				if 'firstName' in response_content:
					fname = response_content['firstName']
				else:
					fname = None

				if 'lastName' in response_content:
					lname = response_content['lastName']
				else:
					lname = None

				if 'email' in response_content:
					email = response_content['email']
				else:
					email = None
				errors,message = self.checkInResponse(message, response_content, "firstName", x['firstname'], fname)
				errors,message = self.checkInResponse(message, response_content, "lastName", x['lastname'], lname)
				errors,message = self.checkInResponse(message, response_content, "email", x['email'].lower(), email)
			elif objectType == "products":
				if 'sku' in response_content:
					sku = response_content['sku']
				else:
					sku = None

				if 'name' in response_content:
					pname = response_content['name']
				else:
					pname = None

				if 'description' in response_content:
					pdesc = response_content['description']
				else:
					pdesc = None

				if 'cost' in response_content:
					cost = response_content['cost']
				else:
					cost = 0

				errors,message = self.checkInResponse(message, response_content, "sku", x['sku'], sku)
				errors,message = self.checkInResponse(message, response_content, "name", x['name'], pname)
				errors,message = self.checkInResponse(message, response_content, "description", x['description'], pdesc)
				errors,message = self.checkInResponse(message, response_content, "cost", float(x['cost']), float(cost))
				
			if errors:
				message = "<span class='failed'>FAILED: </span>" + message + "<br>Returned Content: " + str(response.content)
			else:
				message = "<span class='passed'>SUCCESS</span>" + message
				objects.append(int(response_content['_id']))

			message = message + "<br><br>"
			self.response.write(message)

			if self.sleep:
				time.sleep(1)

		return objects


	def testPostValidObjects(self, url, objType, objList):

		if objType == "products":
			object_keys = self.testAddObjects(url, "products", objList)
		elif objType == "customers":
			object_keys = self.testAddObjects(url, "customers", objList)
		else:
			self.response.write("Couldn't understand request.")

		self.response.write("<p><b>Test GET Added " + str(len(objList)) + " Objects</b></p>")
		
		if len(objList) == len(object_keys):
			message = "<span class='passed'>SUCCESS:</span>"
		else:
			message = "<span class='failed'>FAILURE:</span>"

		message += "<br>Expected Response: " + str(len(objList))
		message += "<br>Actual Response: " + str(len(object_keys))

		self.response.write(message)
		return object_keys

	def testPutNoDataObject(self, url, objectType):

		# get a customer let's use the first one in the series as there are 5
		customer = objectType.query().fetch(limit=1)

		if customer:
			customer = customer[0].key.get(use_cache=False, use_memcache=False)
			newurl = url + "/" + str(customer.key.id())

			self.response.write("<p>Updating customer url: " + newurl + "</p>")

			self.response.write("<b>No Data Update: </b> - ")
			response = self.actionObject(newurl, urlfetch.PUT, {})
			response_content = json.loads(response.content)
			
			# firstname checks
			if response.status_code == self.status_success_code:
				self.response.write("<span class='passed'>SUCCESS</span>")
			else: 
				self.response.write("<span class='failed'>FAILED</span>")

			self.response.write("<br>Expected status: " + str(self.status_success_code))
			self.response.write("<br>Actual Status: " + str(response.status_code))
		else:
			self.response.write("<span class='failed'>FAILED - No Customers Returned</span>")

	'''
	These Tests are not dependant on type of object and can be reused
	'''
	def returnUrl(self, url, headers, methodType, form_fields={}):

		form_data = urllib.urlencode(form_fields)

		return urlfetch.fetch(
			url=url,
    		payload=form_data,
    		method=methodType,
    		headers=headers
    	)

	def getHeaders(self, appType="json"):
		if appType == "json":
			return {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}
		else:
			return {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/xml'}		

	def actionObject(self, url, actionType, payload={}, appType="json"):
		headers = self.getHeaders(appType)
		return self.returnUrl(url, headers, actionType, payload)

	def testGetBadMime1(self, url):
		response = self.actionObject(url, urlfetch.GET, {}, "xml")
		self.response.write("<p>URL: " + url + "</p>")
		# verify data correct
		if response.status_code == self.status_not_acceptable:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"
		message += "<br>Expected Status Code: " + str(self.status_not_acceptable) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testGetObjects(self, url, expectedQty, objects={}, status_code = 200):
		errors = False
		self.response.write("<p>URL: " + url + "</p>")
		response = self.actionObject(url, urlfetch.GET)

		try:
			response_content = json.loads(response.content)
		except ValueError, e:
			response_content = response.content

		errors,message = self.check_status(status_code, response.status_code)

		if 'keys' in response_content:
			if not len(response_content['keys']) == expectedQty:
				errors = True
		elif expectedQty > 1:
			errors = True

		if errors:
			message = "<br><span class='failed'>FAILED</span>" + message
		else:
			message = "<br><span class='passed'>SUCCESS</span>" + message	

		message = message + "<br><br>"	
		self.response.write(message)

	def testGetBadObjects(self, url):
		errors = False
		self.response.write("<p>URL: " + url + "</p>")

		response = self.actionObject(url, urlfetch.GET)
		response_content = json.loads(response.content)

		errors,message = self.check_status(self.status_not_found, response.status_code)

		message += "<br>Actual Response Content: " + str(response.content)

		if errors:
			message = "<br><span class='failed'>FAILED</span>" + message
		else:
			message = "<br><span class='passed'>SUCCESS</span>" + message	

		message = message + "<br><br>"	
		self.response.write(message)

	def testGetSingleObject(self, url, objectType):
		obj_key = objectType.query().fetch(limit=1)
		if len(obj_key) > 0:
			obj_input = json.dumps(obj_key[0].to_dict(), default=self.date_handler)
			newurl = url + "/" + str(obj_key[0].key.id())
			self.testGetObjects(newurl, 1, obj_input)
		else: 
			self.response.write("<br>Something went wrong<br>")
		

	def testGetBadSingleObject(self, url):
		newurl = url + "/" + self.bad_key
		self.testGetBadObjects(newurl)

	def testGetAllObjects(self, url, expectedQty, object_keys):
		object_input = {}
		object_input['keys'] = object_keys
		self.testGetObjects(url, expectedQty, object_input)

	def testPostBadMime1(self, url):
		self.response.write("<p>URL: " + url + "</p>")
		response = self.actionObject(url, urlfetch.POST, {}, "xml")

		# verify data correct
		if response.status_code == self.status_not_acceptable:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"
		message += "<br>Expected Status Code: " + str(self.status_not_acceptable) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testPutBadMime1(self, url, status_code=406):
		self.response.write("<p>URL: " + url + "</p>")
		response = self.actionObject(url, urlfetch.PUT, {}, "xml")

		# verify data correct
		if response.status_code == status_code:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"
		message += "<br>Expected Status Code: " + str(status_code) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testDeleteObject(self, url, appType, status=200):
		self.response.write("<p>URL: " + url + "</p>")
		response = self.actionObject(url, urlfetch.DELETE, {}, appType)

		# verify data correct
		if response.status_code == status:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"
		message += "<br>Expected Status Code: " + str(status) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testPostInvalidObject(self, url, objectType, payloadDict, parent=None):

		# count the objects in the database before the test
		expectedCount = len(objectType.query(ancestor=parent).fetch())

		# post the objects
		message = self.testPostBadObject(url, payloadDict)
		message += "<p><b>Test Count Not Changed</b></p>"
		
		# count the objects in the database after the text
		actualCount = len(objectType.query(ancestor=parent).fetch())

		# check pass or fail
		if expectedCount == actualCount:
			message += "<span class='passed'>SUCCESS:</span>"
		else:
			message += "<span class='failed'>FAILURE:</span>"

		message += "<br>Expected Response: " + str(expectedCount)
		message += "<br>Actual Response: " + str(actualCount)

		self.response.write(message)
		return 

	def testPostNoData(self, url, status_code = 400):
		self.response.write("<p>URL: " + url + "</p>")
		response = self.actionObject(url, urlfetch.PUT)

		if response.status_code == status_code:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"

		message += "<br>Expected Status Code: " + str(status_code) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testPostNotAllowedData(self, url, ActionType, status_code):
		self.response.write("<p>URL: " + url + "</p>")

		if ActionType == "post":
			methodType = urlfetch.POST
		elif ActionType == "put":
			methodType = urlfetch.PUT
		else:
			methodType = urlfetch.GET

		headers = self.getHeaders("json")
		response = urlfetch.fetch(
			url=url,
    		method=methodType,
    	)

		if response.status_code == status_code:
			message = "<span class='passed'>SUCCESS</span>"
		else: 
			message = "<span class='failed'>FAILED</span>"

		message += "<br>Expected Status Code: " + str(status_code) + "<br>Actual Status Code: " + str(response.status_code)

		self.response.write(message)
		return

	def testPostBadObject(self, url, payloadDict):
		message = ""
		self.response.write("<p>URL: " + url + "</p>")
		for payload in payloadDict:
			response = self.actionObject(url, urlfetch.POST, payloadDict[payload])
			response_content = json.loads(response.content)
			
			errors = False

			message1 = "<br>Testing: " + str(payload)
			message1 += "<br>Payload Sent: " + str(payloadDict[payload])
			message1 += "<br>Expected Status Code: " + str(self.status_bad_request)
			message1 += "<br>Actual Status Code: " + str(response.status_code)

			if not response.status_code == self.status_bad_request:
				errors = True

			if errors:
				message += "<br><span class='failed'>FAILED: </span>" + message1 + "<br>Returned Content: " + str(response.content)
			else:
				message += "<br><span class='passed'>SUCCESS</span>" + message1
				
			message = message + "<br><br>"
			if self.sleep:
				time.sleep(1)

		return message

	def testDeleteAllObjects(self, objectType):
		url = self.base_url
		self.response.write("<p>URL: " + url + "</p>")
		if cmp(objectType, db_defs.Customer) == 0:
		 	url += self.customers_url
		elif cmp(objectType, db_defs.Order) == 0:
			url += self.orders_url
		elif cmp(objectType, db_defs.Product) == 0:
			url += self.products_url
		else:
			self.response.write("<span class='failed'>ERROR With Type</span>")
			return

		response = self.actionObject(url, urlfetch.GET)
		response_content = json.loads(response.content)
		
		object_keys = response_content['keys']
		self.response.write(object_keys)
		self.response.write("<br>")

		for x in object_keys:
			newurl = url + "/" + str(x)

			self.response.write("<br>DELETE " + newurl + " ")

			headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}
			response = self.returnUrl(newurl, headers, urlfetch.DELETE)

			cid_key = ndb.Key(objectType, x)
			cid = cid_key.get(use_cache=False, use_memcache=False)
			if cid: 
				self.response.write("<span class='failed'>FAILED</span>")
			else:
				self.response.write("<span class='passed'>SUCCESS</span>")
			if self.sleep:
				time.sleep(1)

		self.response.write("<br>DELETED")

	def testDeleteBadObject(self, url, objectType):

		url = self.base_url
		errors = False
		message = ""

		if not cmp(objectType, db_defs.Customer) == 0 and not cmp(objectType, db_defs.Order) == 0 and not cmp(objectType, db_defs.Product) == 0:

			self.response.write("<span class='failed'>ERROR With Type</span>")
			return

		url += "/" + str(self.bad_key)
		self.response.write("<br>DELETE " + url + " ")

		headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}
		response = self.returnUrl(url, headers, urlfetch.DELETE)

		if not response.status_code == self.status_not_found:
			error = True

		message1 = "<br>Expected Status Code: " + str(self.status_not_found)
		message1 += "<br>Actual Status Code: " + str(response.status_code)

		if errors:
			message += "<br><span class='failed'>FAILED: </span>" + message1 + "<br>Returned Content: " + str(response.content)
		else:
			message += "<br><span class='passed'>SUCCESS</span>" + message1
				
		message = message + "<br><br>"
		if self.sleep:
				time.sleep(1)

		self.response.write(message)

	def testGetOrders(self, url):
		results = db_defs.Order.query().fetch(keys_only=True)
		count = len(results)
		objects = {}
		objects['keys'] = [int(x.id()) for x in results]
		self.testGetObjects(url, count, objects)

	def testGetCustomerOrders(self, url, status_code=200, customerkey = None):
		results = []
		objects = {}
		
		if not customerkey:
			results = db_defs.Customer.query().fetch(keys_only=True, limit=1, offset=1)
			if results:
				customerID = results[0].id()

				results = db_defs.Order.query(ancestor=results[0]).fetch(keys_only=True)
				count = len(results)
				objects['keys'] = [int(x.id()) for x in results]
			else:
				self.response.write("<br><span class='failed'>FAILED: No Customers Returned</span>")
				return
		else:
			customerID = customerkey
			count = 0

		newurl = url + "/" + str(customerID) + self.orders_url
		self.testGetObjects(newurl, count, objects, status_code)

	def testActionSingleObject(self, url, objectType, actionType, status = 200, childkind=None):	

		results = objectType.query().fetch(keys_only=True,limit=1)

		if results:
			if childkind:
				newurl = url + "/" + str(results[0].id()) + "/" + childkind
			else:
				newurl = url + "/" + str(results[0].id())
			self.response.write(newurl)

			#self.testDeleteObject(newurl, "json", status)
			response = self.actionObject(newurl, actionType, payload={}, appType="json")
			errors,message = self.check_status(status, response.status_code)

			if not errors:	
				results = results[0].get(use_cache=False, use_memcache=False)

				if results and response.status_code == status:
					self.response.write("<br><span class='passed'>PASSED: Confirmed not in DB</span>")
				else:
					self.response.write("<br><span class='failed'>FAILED: Found Object in datastore</span>")
				self.response.write(message)
				return
			else:
				self.response.write("<br><span class='failed'>FAILED:</span>")
				self.response.write(message)
				return
		else:
			self.response.write("<br><span class='failed'>FAILED: NO IDS to delete</span>")
			return

	def testActionObjectParent(self, parentUrl, parentType, childUrl, childType, actionType, status, invalid=None, offset=1):

		if invalid:
			newurl = self.base_url + parentUrl + "/" + self.bad_key + childUrl + "/" + self.bad_key
			response = self.actionObject(newurl, actionType, payload={}, appType="json")
			errors,message = self.check_status(status, response.status_code)

			if not errors:	
				self.response.write("<br><span class='passed'>SUCCESS: </span>")
			else:
				self.response.write("<br><span class='failed'>FAILED: </span>")
			self.response.write(message)
			return

		else:
			parent = parentType.query().fetch(keys_only=True, limit=1)
			if parent:
				parent = parent[0]
				childres = childType.query(ancestor=parent).fetch(keys_only=True, limit=1, offset=0)
				if childres:
					parent = parent.id()
					child = childres[0].id()
					childData = childres[0].get(use_cache=False, use_memcache=False)
					childData = json.dumps(childData.to_dict(), default=self.date_handler)

					newurl = self.base_url + parentUrl + "/" + str(parent) + childUrl + "/" + str(child)
					response = self.actionObject(newurl, actionType, payload={}, appType="json")
					errors,message = self.check_status(status, response.status_code)

					if not errors:	
						if actionType == urlfetch.DELETE:
							validate = childres[0].get(use_cache=False, use_memcache=False)
							if not validate:
								self.response.write("<br><span class='passed'>SUCCESS: </span>")
							else:
								self.response.write("<br><span class='failed'>FAILED: Confirmed not deleted from datastore</span>")
						else:
							self.response.write("<br><span class='passed'>SUCCESS: </span>")
					else:
						self.response.write("<br><span class='failed'>FAILED: </span>")
					self.response.write(message)
					self.response.write("<br>Expected: " + str(childData))
					self.response.write("<br>Actual: " + str(response.content))
					return

				else:
					self.response.write("<br><span class='failed'>FAILED: NO IDS for child</span>")
					return
			else:
				self.response.write("<br><span class='failed'>FAILED: NO IDS for parent</span>")
				return

	
