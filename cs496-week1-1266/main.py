import datetime
import jinja2
import os
import webapp2
import models

from google.appengine.api import users

# Configuring Jinja2 with and Environment object
# Declare they are loaded from the FileSystem
# Store the object in global variable template_env
# os.getcwd() finds templates in the working directory
template_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.getcwd()))

class MainPage(webapp2.RequestHandler):

	def get(self):
		current_time = datetime.datetime.now()
		# returns an object of class users or none if not signed in
		user = users.get_current_user()
		# create_login_url and create_logout_url take a url path as an argument
		login_url = users.create_login_url(self.request.path)
		logout_url = users.create_logout_url(self.request.path)

		userprefs = models.get_userprefs()

		if userprefs:
			current_time += datetime.timedelta(
				0, 0, 0, 0, 0, userprefs.tz_offset)

		template = template_env.get_template('home.html')
		# map the template variables to python variables
		context = {
			'current_time': current_time,
			'user': user,
			'login_url': login_url,
			'logout_url': logout_url,
			'userprefs': userprefs
		}
		self.response.out.write(template.render(context))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)


