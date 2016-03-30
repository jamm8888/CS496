from google.appengine.api import users

import webapp2


class MainPage(webapp2.RequestHandler):

		def get(self):
			#Check if the user has an active account session
			user = users.get_current_user()

			if user:
				newuri = ('%s' % self.request.uri)
				self.redirect(newuri)
			else:
				self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug = True)