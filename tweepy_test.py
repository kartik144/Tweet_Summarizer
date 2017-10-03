import tweepy
import twitter_tokens
import json
import preprocess
from time import time

t0=time()
print("Logging in...")
auth = tweepy.OAuthHandler(twitter_tokens.consumer_key,twitter_tokens. consumer_secret)
auth.set_access_token(twitter_tokens.access_token, twitter_tokens.access_token_secret)
api=tweepy.API(auth)
print("Logged in in %f seconds..." % (time()-t0))
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print (tweet.text+"\n")

def streamTweets(hashtag,api):
	while True:
		try:
			print("Opening Stream...")
			myStreamListener = MyStreamListener()
			myStream = tweepy.Stream(auth=api.auth,listener=myStreamListener)
			myStream.filter(languages=["en"],track=hashtag)
		except:
			print("Error!! Retrying....")
			continue
			
class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		if not status.retweeted and "RT @" not in status.text:
			print (status.text)
			with open(hashtag[0]+'_eng_processed_tweets_2.txt','a') as tf:
				tf.write(preprocess.strip_links(status.text)+"\n")
			return

	def on_error(self, status_code):
		if status_code == 420:
            		print("Error Occured! max tries reached!")#returning False in on_data disconnects the stream
		return False

#hashtag=['#mayweathervmcgregor','#mcgregor','#Mayweather']
hashtag=['#BarcelonaAttack','#BarcelonaTerrorAttack']
streamTweets(hashtag,api)
