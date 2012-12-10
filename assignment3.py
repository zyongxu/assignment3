import cgi
import webapp2

from google.appengine.ext import db

from search import searchTweets
from tweetdb import Tweet, Topic

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
          <body>
            <h3>Please enter the topic:</h3>
            <form action="/findtweets" method="post">
              <div><textarea name="content" rows="3" cols="60"></textarea></div>
              <div><input type="submit" value="Search"></div>
            </form>
            <table border="1">
              <th>Topic</th>
              <th># of Tweets</th>
              <th>User</th>""")

        topics = Topic.all()
        for buzz in topics:
            self.response.out.write("""
              <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s<br><img src="%s" /></td>
              </tr>""" % (cgi.escape(buzz.topic),
                          cgi.escape("111"),
                          cgi.escape(buzz.user),
                          cgi.escape(buzz.photo_url)))
              
        self.response.out.write("""
            </table>
            <form action="/findtweets" method="get">
              <div><input type="submit" value="Tweet Contents"></div>
            </form>
          </body>
          </html>""")


class FindTweets(webapp2.RequestHandler):
    def get(self):
        """display the text of all tweets in db"""
        tweets = db.GqlQuery("SELECT * "
                             "FROM Tweet")

        for tweet in tweets:
            self.response.out.write('topic="%s": ' %
                                    cgi.escape(tweet.parent_key().name()))
            self.response.out.write('<blockquote>%s</blockquote>' %
                                    cgi.escape(tweet.text))


    def post(self):
        """search tweets and populate db"""
        keywords = cgi.escape(self.request.get('content'))
        klist = [kw for kw in keywords.split('\n') if kw.strip()]

        for keyword in klist:
            tweetlist = searchTweets(keyword)

            # the parent key (topic) of the tweet
            par = Topic(key_name=keyword)
            par.store(tweetlist[0])
            for t in tweetlist:
                tweet = Tweet(parent=par)
                tweet.store(t)
            
        self.redirect('/')



app = webapp2.WSGIApplication([('/', MainPage),
                               ('/findtweets', FindTweets)],
                              debug=True)

