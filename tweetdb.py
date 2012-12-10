import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from datetime import datetime

class Tweet(db.Model):
    tweet_id = db.IntegerProperty()
    text = db.StringProperty(multiline=True)
    photo = db.LinkProperty()
    from_user = db.StringProperty()
    from_user_name = db.StringProperty()
    created_at = db.DateProperty()

    def store(self, t):
        self.tweet_id = t["id"]
        self.text = t["text"]
        self.photo = t["profile_image_url"]
        self.from_user = t["from_user"]
        self.from_user_name = t["from_user_name"]
        self.created_at = datetime.strptime(t["created_at"], 
                '%a, %d %b %Y %H:%M:%S +%f').date() 
        self.put()


class Topic(db.Model):
    topic = db.StringProperty()
    user = db.StringProperty()
    photo_url = db.LinkProperty()

    def store(self, t):
        self.topic = self.key().name()
        self.user = t["from_user"]
        self.photo_url = t["profile_image_url"]
        self.put()

