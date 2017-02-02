import webapp2
import base_page

class contentHandler(base_page.BaseHandler):

	def render(self, page):
		base_page.BaseHandler.render(self, page)

	def get(self):
		self.render('content.html')