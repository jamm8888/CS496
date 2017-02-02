import webapp2
import json
import re

class BaseHandler(webapp2.RequestHandler):

	#regex match for integers
	@staticmethod
	def intRegex():
		return "^[0-9]+$"

	