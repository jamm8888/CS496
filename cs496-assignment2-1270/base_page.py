import webapp2
import os
import jinja2

class BaseHandler(webapp2.RequestHandler):
	# https://webapp-improved.appspot.com/api/webapp2.html
	# The function wrapped is called the first time to retrieve the result and then that calculated result is used the next time you access the value:
	# The class has to have a __dict__ in order for it to properly work
	@webapp2.cached_property
	def jinja2(self):
		# This basically loads the environment to look in the templates directory
		return jinja2.Environment(
			loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
			extensions=['jinja2.ext.autoescape'],
			autoescape=True
			)

	def render(self, page, template_variables={}):
		htmltemplate = self.jinja2.get_template(page)
		self.response.write(htmltemplate.render(template_variables))




