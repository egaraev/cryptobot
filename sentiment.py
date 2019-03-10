import time
import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob







def main():
    print('Starting twitter module')


    tw()


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        access_token = config.access_token
        access_token_secret = config.access_token_secret



        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0.1:
            return 'positive'
        elif analysis.sentiment.polarity == 0 or analysis.sentiment.polarity == 0.1:
            return 'neutral'
        else:
            return 'negative'




    def get_tweets(self, query):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:


            marketcount=market_count()


            max_tweets=1200/marketcount

            fetched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(max_tweets)]

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
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




def tw():

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                # creating object of TwitterClient Class
                api = TwitterClient()


                query = heikin_ashi(market, 35)
                # calling function to get tweets
                tweets = api.get_tweets(query=query)

                print market, (" Number of tweets extracted: {}.\n".format(len(tweets)))
                #print tweets

                # picking positive tweets from tweets
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                # percentage of positive tweets
                print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
                positive=(100 * len(ptweets) / len(tweets))
                # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                negative=(100 * len(ntweets) / len(tweets))
                # percentage of negative tweets
                print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set positive_sentiments = %s, negative_sentiments =%s  where market = %s",(positive, negative, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                # percentage of neutral tweets
                print ("Neutral tweets percentage: {} %".format(
                    100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

                # printing first 5 positive tweets
                print("\n\nPositive tweets:")
                for tweet in ptweets[:10]:
                    print(tweet['text'])

                # printing first 5 negative tweets
                print("\n\nNegative tweets:")
                for tweet in ntweets[:10]:
                    print(tweet['text'])

                time.sleep(5)



        except:
            continue



def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False




def heikin_ashi(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False




def market_count():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM markets where enabled=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0

if __name__ == "__main__":
    main()