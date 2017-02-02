from google.appengine.ext import ndb

class Product(ndb.Model):
	sku = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	description = ndb.StringProperty(required=True)
	cost = ndb.FloatProperty(required=True)
	active = ndb.BooleanProperty(required=True)
	categories = ndb.KeyProperty(repeated=True)
	added = ndb.DateTimeProperty(required=True)
	lastmodified = ndb.DateTimeProperty(required=True)

	# from https://cloud.google.com/appengine/docs/python/ndb/queries
	# definition from https://docs.python.org/2/library/functions.html
	@classmethod
 	def query_product(cls, ancestor_key):
 		return cls.query(ancestor=ancestor_key).order(-cls.date)

class Category(ndb.Model):
	name = ndb.StringProperty(required=True)
	active = ndb.BooleanProperty(required=True)
	added = ndb.DateTimeProperty(required=True)
	lastmodified=ndb.DateTimeProperty(required=True)

	# from https://cloud.google.com/appengine/docs/python/ndb/queries
	# definition from https://docs.python.org/2/library/functions.html
	@classmethod
	def query_category(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.date)
