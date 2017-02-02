from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Customer(ndb.Model):
	firstName = ndb.StringProperty(required=True)
	lastName = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	created = ndb.DateTimeProperty(required=True)
	lastModified = ndb.DateTimeProperty(required=True)
	lastOID = ndb.IntegerProperty(required=True, default=0)

	@staticmethod
	def nameRegex():
		return "^[a-zA-Z0-9 \\'\\-]+$"

	@staticmethod
	def emailRegex():
		return "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class Order(ndb.Model):
	orderId = ndb.StringProperty(required=True)
	created = ndb.DateTimeProperty(required=True)
	lastModified = ndb.DateTimeProperty(required=True)
	indexID = ndb.StringProperty(required=True, default='')

	@staticmethod
	def orderIdRegex():
		return "^[a-zA-Z0-9]+$"

class Product(ndb.Expando):
	sku = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty(required=True)
	cost = ndb.FloatProperty(required=True)
	created = ndb.DateTimeProperty(required=True)
	lastModified = ndb.DateTimeProperty(required=True)
	indexID = ndb.StringProperty(required=True, default='')
	#http://stackoverflow.com/questions/12954899/ndb-retrieving-entity-key-by-id-without-parent

	@staticmethod
	def skuRegex():
		return "^[a-zA-Z0-9-]+$"

	@staticmethod
	def nameRegex():
		return "^[a-zA-Z0-9 \\'\\-']+$"

	@staticmethod
	def descRegex():
		return "^[a-zA-Z0-9 \\.\\?\\-\\!\\#\\$\\(\\)\\+\\~\\`\\,\\:\\;\\']+$"

	@staticmethod
	def costRegex():
		return "^-?[\d]+(\.[\d]+)?$"

	@staticmethod
	def quantityRegex():
		return "^[0-9]+$"




