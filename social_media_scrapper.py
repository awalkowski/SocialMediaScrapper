from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import twitter_credentials
from numpy import numpy as np
from pandas import pandas as pd
# # # Twitter Client # # #


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticater().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        print("hey")
        print(Cursor(self.twitter_client.user_timeline).items(num_tweets))
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            # print("hey")
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline). items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

# # # Twitter Authenticater # # #


class TwitterAuthenticater():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCES_TOKEN_SECRET)
        return auth


class TwttierStreamer():
    """
        Class for streaming and processing live tweets
    """

    def _init__(self):
        self.twitter_authenticator = TwitterAuthenticater()

    def stream_tweets(self, fetched_tweet_filename, key_word_list):
        """
            functionSummary stream_tweets
            - this handles twitter authentication and the connection to the twitter Streaming API
        """
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=key_word_list, languages=["en"], )


class TwitterListener(StreamListener):
    """
        This is a basic listener class that just prints recieved tweets to stdout
    """

    def init(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, "a") as fetched_file:
                fetched_file.write(data)
            return True
        except BaseException as exception:
            print("Error on_data:" + str(exception))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning false on data method incase rate limit occurs
            return False
        print(status)


if __name__ == "__main__":

    list_of_keywords = ["Donald Trump", "Trump",
                        "Joe Biden", "Biden",
                        "President", "2020 election"]
    fetched = "tweets.json"
    twitter_client = TwitterClient("realDonaldTrump")
    print(twitter_client.get_user_timeline_tweets(1))
#    twitter_streamer = TwttierStreamer()
#    twitter_streamer.stream_tweets(fetched, list_of_keywords)
