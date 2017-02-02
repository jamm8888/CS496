import webapp2

config = {'default-group':'pos-base-data'}

app = webapp2.WSGIApplication([
	('/admin', 'admin.AdminHandler'),
	('/admin.*', 'admin.AdminHandler'),
	('/', 'content.contentHandler')
], debug=True, config=config)