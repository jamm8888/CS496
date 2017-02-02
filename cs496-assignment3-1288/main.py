import webapp2
from urlparse import urlparse
import json

from google.appengine.api import oauth

config = {'default-group':'api-base-data'}

class MainHandler(webapp2.RequestHandler):

	def get(self):
		#http://stackoverflow.com/questions/3697033/how-can-i-get-the-base-uri-in-appengine
		url = urlparse(self.request.url)
		url1 = url.scheme + "://" + url.netloc
		base_url1 = str(url1)
		info = {
			"customers_url": base_url1 + "/customers",
			"orders_url": base_url1 + "/orders",
			"products_url": base_url1 + "/products",
			"customers_path":"/customers",
			"orders_path":"/orders",
			"products_path":"/products"
		}
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("{\n")
		for x in info:
			self.response.write("\t\"" + x + "\"=\"" + info[x] + "\",\n")
		self.response.write("\t\"main_url\"=\"" + base_url1 + "\"\n")
		self.response.write("}")

app = webapp2.WSGIApplication([
	('/', 'main.MainHandler'),
], debug = True, config=config)

app.router.add(webapp2.Route(r'/customers<:/?>', 'customer.Customers'))
app.router.add(webapp2.Route(r'/customers/<cid:[0-9]+><:/?>', 'customer.Customers'))
app.router.add(webapp2.Route(r'/customers/search<:/?>', 'customer.CustomerSearch'))
app.router.add(webapp2.Route(r'/customers/<cid:[0-9]+>/orders/<oid:[0-9]+><:/?>', 'order.Orders'))
app.router.add(webapp2.Route(r'/customers/<cid:[0-9]+>/orders<:/?>', 'order.Orders'))
app.router.add(webapp2.Route(r'/orders/<oid:[0-9]+><:/?>', 'order.Orders'))
app.router.add(webapp2.Route(r'/orders<:/?>', 'order.Orders'))
#app.router.add(webapp2.Route(r'/orders/search<:/?>', 'order.OrderSearch'))
app.router.add(webapp2.Route(r'/orders/<oid:[0-9]+>/products<:/?>', 'product.Products'))
app.router.add(webapp2.Route(r'/orders/<oid:[0-9]+>/products/<pid:[0-9]+><:/?>', 'product.Products')) # add an existing product to an order
app.router.add(webapp2.Route(r'/products<:/?>', 'product.Products'))
app.router.add(webapp2.Route(r'/products/<pid:[0-9]+><:/?>', 'product.Products'))
app.router.add(webapp2.Route(r'/products/search<:/?>', 'product.ProductSearch'))
app.router.add(webapp2.Route(r'/load', 'load_data.LoadData'))
app.router.add(webapp2.Route(r'/testing', 'testing.TestCustomer'))
