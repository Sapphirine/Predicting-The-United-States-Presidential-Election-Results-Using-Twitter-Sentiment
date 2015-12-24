from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pymongo import MongoClient
from auth import TwitterOAuth

class StdOutListener(StreamListener):
    
    def on_connect(self):
        #Called when the connection is made
        print("You're connected to the streaming server.")
	
	#This function gets called every time a new tweet is received on the stream
    #Store tweets in 'trumpTweets' collection in 'elections' database
    def on_data(self, data):
        #print(data)
        
        client = MongoClient('localhost', 27017)
        
        # Use 'elections' database
        db = client.elections
        
        # Decode JSON
        datajson = json.loads(data)
        
        # We only want to store tweets in English
        if "lang" in datajson and datajson["lang"] == "en":
            # Store tweet info into the 'clintonTweets' collection.
            db.trumpTweets.insert(datajson)
            #print('Tweet is loaded')
            
    def on_error(self, status):
		print("ERROR")
		print(status)
		
if __name__ == '__main__':
	try:
        #Create the listener
		l = StdOutListener()
		auth = OAuthHandler(TwitterOAuth.consumer_key, TwitterOAuth.consumer_secret)
		auth.set_access_token(TwitterOAuth.access_token, TwitterOAuth.access_token_secret)

		#Connect to the Twitter stream
		stream = Stream(auth, l)	
      
		#Terms to track
		stream.filter(track=["@realDonaldTrump","Trump","Donald Trump"])
		
	except KeyboardInterrupt:
		#ctrl+c ->to exit the program
		pass
