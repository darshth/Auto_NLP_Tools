"""This Tweet Parser uses Tweepy API to Parse Tweets.
Textblob is used to label the sentiment of the tweet.
"""

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


consumerkey = input("Enter Consumer Key: ")
consumersecret = input("Enter Consumer Secret Key: ")
accesskey = input("Enter Access Token: ")
accesssecret = input("Enter Secret Access Token: ")
keyword = input("Enter The Search Keyword or Hashtag: ")


"""The modular code design takes inputs from the input variables described below.
-Download this code on your computer.
-Open the terminal window.
-Navigate to the directory containing the code using your CLI.
-Run the code using "python tweetanalyzer.py".
"""


class TwitterClient(object):
    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        consumer_key = consumerkey
        consumer_secret = consumersecret
        access_token = accesskey
        access_token_secret = accesssecret

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")


    def clean_tweet(self, tweet):
        """
        Uses regex to remove special characters, links and clean the text.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


    def get_tweet_sentiment(self, tweet):
        """
        Textblob is a sentiment analysis tool.
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity >= 0:
            return 'positive'
        else:
            return 'negative'


    def get_tweets(self, query, count=10000, tweet_mode="extended"):
        """
        Main function to fetch tweets and parse them.
        """
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['time'] = tweet.created_at
                parsed_tweet['location'] = tweet.user.location
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))



def main():
    api = TwitterClient()
    tweets = api.get_tweets(query=keyword, count=10000, tweet_mode="extended")
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    print("\n\nPositive tweets:")
    for tweet in ptweets:
        print(tweet['text'], tweet['time'])
    print("\n\nNegative tweets:")
    for tweet in ntweets:
        print(tweet['text'], tweet['time'])


if __name__ == "__main__":
    # calling main function
    main()