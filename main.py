from google.appengine.api import users
from urlparse import urlparse

import webapp2


class MainPage(webapp2.RequestHandler):

		def get(self):
			#Check if the user has an active account session
			user = users.get_current_user()
			url = urlparse(self.request.uri)
			mainurl = url.scheme + "://" + url.netloc

			if user:
				newuri = ('%s/guestbook' % mainurl)
				self.redirect(newuri)
			else:
				self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug = True)