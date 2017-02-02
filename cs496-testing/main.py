import webapp2
from urlparse import urlparse
import json

config = {'default-group' : 'how-to-pages'}

class MainHandler(webapp2.RequestHandler):



	def get(self):
		url = urlparse(self.request.url)
		url1 = url.scheme + "://" + url.netloc
		base_url1 = str(url1)

		# get the base url - lets see if we can get this working this time.
		self.response.write(base_url1)

app = webapp2.WSGIApplication([
	('/', 'main.MainHandler'),
], debug=True, config=config)