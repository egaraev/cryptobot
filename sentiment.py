import time
import config
from pybittrex.client import Client
import sys
import datetime
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os
import pymysql
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import shutil
import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
c=Client(api_key='', api_secret='')






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

    def get_tweet_score(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity != 0:
            return analysis.sentiment.polarity			
        else:
            return 'neutral'


    def get_tweets(self, query):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:


#            marketcount=market_count()
#            print (marketcount)

#            max_tweets=1200/marketcount
            max_tweets=1200

            fetched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(max_tweets)]

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['score'] = self.get_tweet_score(tweet.text)
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

                print (market, (" Number of tweets extracted: {}.\n".format(len(tweets))))
                #print tweets

                # picking positive tweets from tweets
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                # percentage of positive tweets
                print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
                positive=round(100 * len(ptweets) / len(tweets), 2)
                # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                negative=round(100 * len(ntweets) / len(tweets), 2)
                # percentage of negative tweets
                print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
                #printed=(market, "Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)), "Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
			
                tweets_score = [tweet for tweet in tweets if tweet['score'] != 'neutral']
                	
                tweet_score= [ sub['score'] for sub in tweets_score ]
                tweet_texts= [ sub['text'] for sub in tweets_score ]
                passage = str(tweet_texts)

                nltk_score= round(sia.polarity_scores(passage)['compound'], 2)
                print ("Sentiment Score: ", round(sia.polarity_scores(passage)['compound'], 2))
                average = sum(tweet_score) / len(tweet_score)
                average= round(average, 2)

                printed = market, "Positive tweets percentage: {} %".format(positive), "Negative tweets percentage: {} %".format(negative), "Average NLTK Score is: {} ".format(average)
                #print (printed)
                news_score=nltk_score


					
					

					
                try:
                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute('update markets set positive_sentiments = %s, negative_sentiments =%s, tweeter_polarity =%s, tweeter_score=%s where market=%s',(positive, negative, average, nltk_score, market))
                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    cursor.execute("update history set positive_tweets = %s, negative_tweets =%s, twitter_polarity ='%s', twitter_score='%s', news_score='%s'  where market='%s' and date='%s'" % (positive, negative, average, nltk_score, news_score, market, currentdate))
                    db.commit()
                except pymysql.Error as e:
                    print ("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit(1)
                finally:
                    db.close()
					


                neutral= (100 - negative - positive)
                labels = 'Neutral', 'Negative', 'Positive' 
                print (neutral, negative, positive)
                sizes = (neutral, negative, positive)
                colors = ["#1f77b4",  "#fe2d00", "#2ca02c"]				
                explode = (0, 0.1, 0)  
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.grid()
                plt.title(market, bbox={'facecolor':'0.8', 'pad':5}, fontsize=18)
                plt.xlabel("Polarity is: {} ".format(average)+" NLTK Score is: {} ".format(nltk_score), fontsize=18)
                # plt.ylabel("Unit")
                plt.show()
                plt.savefig('/root/PycharmProjects/cryptobot/images/tweets.png', bbox_inches = 'tight', pad_inches = 0)
                newfilename=("{}_tweets.png".format(market))
                my_path = "/root/PycharmProjects/cryptobot/images/tweets.png"
                new_name = os.path.join(os.path.dirname(my_path), newfilename)
                print (new_name)
                os.rename(my_path, new_name)
                src_dir = "/root/PycharmProjects/cryptobot/images/"
                dst_dir = "/var/www/html/images/"
                for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
                    shutil.copy(pngfile, dst_dir)
                time.sleep(5)
				
				
        except:
            continue



def available_market_list(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False




def heikin_ashi(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False




def market_count():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM markets where enabled=1 and active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0

if __name__ == "__main__":
    main()