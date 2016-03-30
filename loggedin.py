from google.appengine.api import users

import webapp2


class MainPage(webapp2.RequestHandler):

		def get(self):
			#Check if the user has an active account session
			user = users.get_current_user()

			if user:
				self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
				greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
				self.response.out.write('<html><body>%s</body></html>' % greeting)
			else:
				self.redirect(users.create_login_url('/'))
				#greeting = ('Just Sign out! (<a href="%s">sign out</a>)' %
                #        (users.create_logout_url('/')))
				#self.response.out.write('<html><body>%s</body></html>' % greeting)

app = webapp2.WSGIApplication([
	('/loggedin', MainPage),
], debug = True)