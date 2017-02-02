import webapp2
import json
import urllib
from google.appengine.api import urlfetch
from base_page import BaseHandler
import unittest
#from testMethods import TestMethods

class TestCustomer(BaseHandler):

	#base_url = "http://localhost:8080"
	base_url = "https://cs496-assignment3-1288.appspot.com"
	customers_url = "/customers"
	orders_url = "/orders"
	products_url = "/products"

	good_customer_list = [
		{
			"firstname": "Jane",
			"lastname": "Doe",
			"email": "janedoe@gmail.com"
		},
		{
			"firstname": "John",
			"lastname": "Doe",
			"email": "johndoe1@gmail.com"
		},
		{
			"firstname": "Mary",
			"lastname": "Kay",
			"email": "mary.Kay@mary.kay.com"
		},
		{
			"firstname": "Jennifer",
			"lastname": "apiGuru",
			"email": "jennifer_Guru@guru.com"
		},
		{
			"firstname": "Jumble",
			"lastname": "Person",
			"email": "jumble.person.1@gmail.com"
		}
	]

	erronous_customer_dict = {
		'no_params':
		{},
		'firstname':
		{
			"firstname": "Jane*s",
			"lastname": "Doe",
			"email": "erronousjanedoe@gmail.com"
		},
		'lastname':
		{
			"firstname": "Jane*s",
			"lastname": "Doe*",
			"email": "erronousjanedoe@gmail.com"
		},
		'email':
		{
			"firstname": "Jane*s",
			"lastname": "Doe*",
			"email": "janedoe"
		}
	}

	def testAddCustomers(self, url):
		customers = []

		for x in self.good_customer_list:
			form_fields = x

			headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}

			response = self.returnUrl(url, headers, urlfetch.POST, form_fields)
			response_content = json.loads(response.content)

			message = "Test Customers POST\n"
			errors = False

			message += "Expected Status Content: " + str(self.status_success_code) + "\n"
			message += "Actual Status Content: " + str(response.status_code) + "\n"

			if not response.status_code == self.status_success_code:
				errors = True

			message += "Expected First Name in Response: " + x['firstname'] + "\n"
			if 'firstName' in response_content and response_content['firstName'] == x['firstname']:
				message += "Actual First Name Received: " + response_content['firstName'] + "\n"
			else:
				errors = True

			message += "Expected Last Name in Response: " + x['lastname'] + "\n"
			if 'lastName' in response_content and response_content['lastName'] == x['lastname']:
				message += "Actual Last Name Received: " + response_content['lastName'] + "\n"
			else:
				errors = True

			message += "Expected Email in Response: " + x['email'] + "\n"
			if 'email' in response_content and response_content['email'] == x['email'].lower():
				message += "Actual Email Received: " + response_content['email'] + "\n"
			else:
				errors = True

			if errors:
				message = "FAILED: " + message + "Returned Content: " + str(response.content) + "\n"
			else:
				message = "PASSED: " + message
				customers.append(response_content['_id'])

			message = message + "\n"
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write(message)

		return customers

	def returnUrl(self, url, headers, methodType, form_fields={}):

		form_data = urllib.urlencode(form_fields)

		return urlfetch.fetch(
			url=url,
    		payload=form_data,
    		method=methodType,
    		headers=headers
    	)
