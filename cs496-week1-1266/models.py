from google.appengine.api import users
from google.appengine.ext import ndb

# Every data store has a primary key called an entity key
# unlike a primary key in relational databases, entity keys
# are permanent and can only be set when the entity is created.  
# it is unique across all entities in the system
# App can set the key name (only one component of the key) to 
# an arbitrary value

class UserPrefs(ndb.Model):
	tz_offset = ndb.FloatProperty(default=0.0)
	user = ndb.UserProperty(auto_current_user_add=True)

# gets the userprefs and determines the user id
# constructs the data store key for an entity of the kind
# UserPrefs with a key name equivalent to the user ID.
# if the entity exists it returns the object otherwise
# it creates the object with default settings and a key
# name corresponding to the user
# put must be invoked to save the new key
def get_userprefs(user_id=None):
	if not user_id:
		user = users.get_current_user()
		if not user:
			return None
		user_id = user.user_id()

	key = ndb.Key('UserPrefs', user_id)
	userprefs = key.get()
	if not userprefs:
		userprefs = UserPrefs(id=user_id)
	return userprefs