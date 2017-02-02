import webapp2
from google.appengine.ext import ndb
import json
import datetime
import re

class BaseHandler(webapp2.RequestHandler):

	invalid_mime_status = 406
	invalid_mime_status_message = "Not Acceptable.  application/json is the only acceptable MIME type"

	status_success_code = 200
	status_bad_request = 400
	status_not_found = 404
	status_not_allowed = 405
	status_not_acceptable = 406

	errors = {}
	errors[status_bad_request] = "Bad Request. "
	errors[status_not_found] = "Not Found. "
	errors[status_not_acceptable] = "Not Acceptable. "
	errors[status_not_allowed] = "Method Not Allowed. "

	default_limit = 20
	default_offset = 0

	@staticmethod
	def intRegex():
		return "^[0-9]+$"

	# http://stackoverflow.com/questions/14249115/serializing-output-to-json-valueerror-circular-reference-detected
	# converts items with attribute isoformat to obj.isoformat()
	def date_handler(self, obj):
		if hasattr(obj, 'isoformat'):
			return obj.isoformat()
		else:
			return obj

	def check_status(self, request):

		if 'application/json' not in request.accept:
			self.response.status = self.invalid_mime_status
			self.response.status_message = self.invalid_mime_status_message
			return False
		return True

	def write_json(self, results):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(results, default=self.date_handler))

	def get_now(self):
		return datetime.datetime.utcnow()

	def write_error(self, error_code, message=''):
		self.response.status = error_code
		self.response.status_message = self.errors[error_code] + message
		results = { 'status_int': self.response.status_int, 'status': self.response.status, 'status_message':self.response.status_message}
		self.write_json(results)
		return

	def getLimits(self, request):

		records = {}
		# check if a limit has been specified otherwise default is 10
		if request.get('limit') and re.match(self.intRegex(), request.get('limit')):
			records['limit'] = int(request.get('limit'))
			if int(request.get('limit')) == 0:
				records['limit'] = None
		else: 
			records['limit'] = self.default_limit

		if request.get('offset') and re.match(self.intRegex(), request.get('offset')):
			records['offset'] = int(request.get('offset'))
		else:
			records['offset'] = self.default_offset

		return records

