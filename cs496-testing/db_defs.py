from google.appengine.ext import ndb

# converts model to proper format for json reading
class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Pages(ndb.Model):
	pageName = ndb.StringProperty(required=True)
	pageTitle = ndb.StringProperty(required=True)
	pageContent = ndb.StringProperty(required=True)

class SiteData(ndb.Model):
	siteName = ndb.StringProperty(required=True)

# customer needs to be able to be created
class Customer(ndb.Model):
	firstName = ndb.StringProperty(required=True)
	lastName = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	phone = ndb.StringProperty(required=True)
	sms_on = ndb.BooleanProperty(default=True)
	email_on = ndb.BooleanProperty(default=True)
	pointLog = ndb.KeyProperty()
	created = ndb.DateTimeProperty(auto_now_add=True)
	modified = ndb.DateTimeProperty(auto_now_add=True)
	points = ndb.IntegerProperty(required=0, default=0)

class PointsLog(ndb.Model):
	pointValue = ndb.IntegerProperty(required=true)
	pointLevel = ndb.KeyProperty()

class PointLevels(ndb.Model):
	pointValue = ndb.IntegerProperty(required=true)
	pointDesc = ndb.StringProperty(required=true)

