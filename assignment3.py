import cgi
import webapp2

from google.appengine.ext import db
from google.appengine.api import memcache

from search import searchTweets, getBuzz
from tweetdb import Tweet, Topic

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
          <html>
          <body>
			<h2>Welcome!</h2>
			 This is assignment3 for Columbia Univ 6998 Cloud Computing. By Kina Winoto (ksw2123) and Yongxu Zhang (yz2419).</br>
			 It is built using Google App Engine, Python SDK. 
			 Note that the assignment specification was a little vague and where there was ambiguity, we made our own decisions.</br>
			 Thus, here's a little about it to clear up some confusion: </br>
				Enter a topic below. </br>
				Returned, is the "buzz" (the most significant tweet) about that topic. We calculate that by: </br>
					<ol><li>Counting the frequency of each word in all of the tweets associated with 
							your topic, excluding words such as "a", "the", etc..</li>
						<li>Using that frequency, we give each tweet a score. The more words with non-zero frequencies
							that a tweet has, the higher the score.</li>
						<li>The buzz-tweet is the tweet with the highest score.</li>
					</ol>
				We use DataStore to store all of the tweets and buzz-tweets associated with a topic.</br>
				We use memcache to store each topic's buzz-tweet. (It is kept for only 1 minute within memcache so
				that buzzes are always up to date) </br>
				You can click on Tweet Contents to see all of the tweets about that topic (non-formatted). </br>
            <h3>Please enter the topic:</h3>
            <form action="/findtweets" method="post">
              <div><textarea name="content" rows="3" cols="60"></textarea></div>
              <div><input type="submit" value="Search"></div>
            </form>
            <table border="1">
              <th>Topic</th>
              <th>User</th>
              <th>Buzz</th>""")

		topics = Topic.all()
		for buzz in topics:
			self.response.out.write("""
              <tr>
                <td>%s</td>
                <td>%s<br><img src="%s" /></td>
                <td>%s</td>
              </tr>""" % (cgi.escape(buzz.topic),
                          cgi.escape(buzz.user),
                          cgi.escape(buzz.photo_url),
                          cgi.escape(buzz.text)))
              
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
			# We are using memcache to remember the buzz associated
			# with each topic. (Assignment spec was ambiguous) 
			tbuzz = memcache.get('%s:buzz' % keyword)
			if tbuzz is None:
				tbuzz = getBuzz(tweetlist)
				# Buzz-ed tweet expires in one minute (60 sec)
				memcache.add('%s:buzz' % keyword, tbuzz, 60)
			par.store(tbuzz)
			for t in tweetlist:
				tweet = Tweet(parent=par)
				tweet.store(t)
			 

		self.redirect('/')



app = webapp2.WSGIApplication([('/', MainPage),
                               ('/findtweets', FindTweets)],
                              debug=True)

