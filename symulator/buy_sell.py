import pandas as pd
import numpy as np
from math import floor
from sqlalchemy import create_engine
import ast
import time
import pymysql
import datetime as dt
import pymysql
import requests
import hashlib
import hmac
import numpy
import datetime
from datetime import date
from datetime import timedelta, date
import io, base64, os, json, re, sys 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import glob
import shutil
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from dateutil import parser
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')
#Read the data for fivemin
dictionary = []
try:
    file = open("../data/hist_data_fivemin.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary.append(i)
    file.close()
except:
    print("Unable to read hist_data_fivemin file")
	
df = pd.DataFrame(dictionary, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])

#print (df)
df['T'] = pd.to_datetime(df['T'])
arr = df["T"].to_numpy()
arr = np.datetime_as_string(arr, unit='D')
dates_list = arr.tolist()
df['day'] = dates_list


#Read the data for summary
dictionary_sum = []
try:
    file = open("../data/summaries.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary_sum.append(i)
    file.close()
except:
    print("Unable to read summaries file")

df_sum = pd.DataFrame(dictionary_sum, columns=['Last', 'Bid', 'Ask', 'PrevDay', 'Volume'])

(df_sum['Volume']) = 150000000 * df_sum['Volume']
#print (df_sum)
df_out = pd.concat([df, df_sum], axis=1)
df = df_out

del df["V"]
df.rename(columns={'Volume':'V'}, inplace=True)
vol = df.pop('V')
df.insert(4, 'V', vol)

#print (df)

#Read the data for day
dictionary_day = []
try:
    file = open("../data/hist_data_day.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary_day.append(i)
    file.close()
except:
    print("Unable to read hist_data_day file")
	
df_day = pd.DataFrame(dictionary_day, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])
df_day['T'] = pd.to_datetime(df_day['T'])
#print (df_day)

#Read the data for hour
dictionary_hour = []
try:
    file = open("../data/hist_data_hour.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary_hour.append(i)
    file.close()
except:
    print("Unable to read hist_data_hour file")
	
df_hour = pd.DataFrame(dictionary_hour, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])
df_hour['T'] = pd.to_datetime(df_hour['T'])
df_hour['T'] = df_hour['T'].dt.strftime('%Y-%m-%d %H')
#print (df_hour)



#Read the data for thirtymin
dictionary_thirty = []
try:
    file = open("../data/hist_data_thirty.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary_thirty.append(i)
    file.close()
except:
    print("Unable to read hist_data_thirty file")
	
df_thirty = pd.DataFrame(dictionary_thirty, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])
df_thirty['T'] = pd.to_datetime(df_thirty['T'])
df_thirty['T'] = df_thirty['T'].dt.strftime('%Y-%m-%d %H:%M')
#print (df_thirty)


#Read the data for twitter
tweetlist = []
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT `date`, `twitter_polarity`, `positive_tweets`, `negative_tweets` FROM `history` WHERE `market`='BTC-USD' and `id` >= '1005' ORDER BY id")
tweets=cursor.fetchall()
for i in tweets:
   tweetlist.append(i)

df_tw = pd.DataFrame.from_records(tweetlist, columns =['Date', 'Polarity', 'Positive', 'Negative'])

#print (df_tw)

#Read the data for AI predictions
ai_list = []
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT `date`, `predicted_price` FROM `history` WHERE `market`='BTC-USD' and `date` >= '2023-01-02' ORDER BY date")
ai_preds=cursor.fetchall()
for i in ai_preds:
   ai_list.append(i)

df_ai = pd.DataFrame.from_records(ai_list, columns =['Date', 'Predicted_price'])

#print (df_ai)


news_score_list = []
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT `date`, `news_score` FROM `history` WHERE `market`='BTC-USD' and `date` >= '2023-01-02' ORDER BY date")
news_score_preds=cursor.fetchall()
for i in news_score_preds:
   news_score_list.append(i)

news_ai = pd.DataFrame.from_records(news_score_list, columns =['Date', 'news_score'])

print (news_ai)



market= "BTC-USD"






#Start the main function  (1 week is about 20 mins of symulation)
def main():
    for i,(index,row) in enumerate(df.iterrows()):
        #if i < 1: continue # skip first 5 rows (normally starts at 2022-01-07 21:35 with interval of 5 min). if we skip 5 rows, then it starts at 22:00 (3700)
        try:         
            fivemin_day = str(df.iloc[index]['day'])	
            print (i, fivemin_day)
            #print (df)
            news_score(market, row)			
            buy(row, market)
            sell(row, market)
            # if index % 2 == 0:	# every 10 mins
               # enable_market(market, row, df_hour, df_day)			   
            if index % 3 == 0: #every 15 mins
               dashboard(market, row)
               heikin_ashi_module(market, df_day, fivemin_day, row)
               obv(market, df_day, fivemin_day, row)
               macd_module(market, df_day, fivemin_day, row)	
               candle_patterns(market, df_day, fivemin_day, row)			   
            if index % 5 == 0: # every 25 mins
               profit_chart()
               aftercount(market, row)
               trend_analizer(market)
            if index % 150 == 0:  # every 12 hours			
               tweeter_charts_img(market, df_tw, row)
               heikin_ashi_module_img(market, df_day, fivemin_day, row)	
               obv_img(market, df_day, fivemin_day, row)
               macd_module_img(market, df_day, fivemin_day, row)	
               candle_patterns_img(market, df_day, fivemin_day, row)
               candle_charts_img(market, df_day, fivemin_day, row)
               ai_prediction(market, row)			   
        except:
            break
        #if i > 20: break




def news_score(market, row):
        print ("Starting news_score module")
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        #print (currtime)		
        currenttime = now[:-3]	
        current_row = news_ai[news_ai.Date == currentdate].iloc[0] 		
        news_score = float(current_row['news_score'])
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set news_score = %s  where market = %s",(news_score, market))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()


def ai_prediction(market, row):
        print ("Starting ai_prediction module")
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        #print (currtime)		
        currenttime = now[:-3]	
        predicted_row = df_ai[(df_ai.Predicted_price > 0) & (df_ai.Date >= currentdate)].iloc[0] 
        #print (predicted_row)		
        predicted_price = float(predicted_row['Predicted_price'])
        predicted_date = (predicted_row['Date'])
        #print (currentdate, predicted_date)	
        curr_ai_dir = current_ai_direction(market)
        #print (curr_ai_dir)
        
	
        if predicted_price > last:
           ai_direction = "UP"
        elif predicted_price < last:
           ai_direction = "DOWN"
        else:
           pass	
		   

#        print (curr_ai_dir)
		
        if currentdate == predicted_date:
            try:
                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                cursor = db.cursor()
                cursor.execute("update markets set ai_direction = 'NEUTRAL'  where market = %s",(market))
                db.commit()
            except pymysql.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)
            finally:
                db.close()            		
        elif curr_ai_dir == "NEUTRAL":
            try:
                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                cursor = db.cursor()
                cursor.execute("update markets set ai_direction = %s  where market = %s",(ai_direction, market))
                db.commit()
            except pymysql.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)
            finally:
                db.close()
        elif curr_ai_dir != "NEUTRAL":
            pass		
	
#        print (ai_direction)



####### BUY START ################
def buy(row, market):
        print ("Starting buying mechanizm")
        buy_size = parameters()[0]
        max_orders = int(parameters()[5])		
        iso_8601= str(row['T'])		
        timestamp = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        now = str(row['T'])
        currentdate = now[:-9]	
        #day_close = summary['PrevDay']   #Getting day of closing order
    #Current prices
        last = float(row['Last'])  #last price
        bid = float(row['Bid'])  # sell price
        ask = float(row['Ask'])  # buy price
        newbid=float("{:.3f}".format(bid - bid*0.002))
        newask=float("{:.3f}".format(ask + ask*0.002))
		
    #HOW MUCH TO BUY
        buy_quantity = buy_size / last
        bought_price_sql = float(status_orders(market, 3))

        bought_quantity_sql = float(status_orders(market, 2))
        active = active_orders(market)
        iteration = int(iteration_orders(market))
        timestamp_old = int(timestamp_orders(market))
        currenttime = now[:-3]
        #print (currenttime, last)
        HAD_trend=heikin_ashi(market, 18)
        candle_direction=heikin_ashi(market, 77)
        hour_candle_direction=heikin_ashi(market, 76)
        today_tweet = df_tw.loc[df_tw['Date'] == currentdate]
        #print (today_tweet)
        tweet_positive=float(today_tweet['Positive'])
        tweet_negative=float(today_tweet['Negative'])
        tweet_ratio = float("{0:.2f}".format(tweet_positive/tweet_negative))
        tweet_polarity=float(today_tweet['Polarity'])

        candle_score=heikin_ashi(market,68)
        news_score=heikin_ashi(market,72)
        ai_direction=str(heikin_ashi(market,9))
        candle_pattern=heikin_ashi(market,69)
        previous_date = str(heikin_ashi(market,46))
        trend = str(heikin_ashi(market,78))					
        macd = str(heikin_ashi(market,79))
        obv = str(heikin_ashi(market,81))
        macd_fluc = macd_fluctuation(market)

        macd_first_day=macd_fluc[0]
        macd_second_day=macd_fluc[1]
        macd_third_day=macd_fluc[2]
		
	
        current_order_count = int(order_count())		
        if (macd_third_day!='none' and macd_second_day!='none' and macd_first_day!='none') or  (macd_third_day!='none' and macd_second_day!='none')  or (macd_third_day!='none'  and macd_first_day!='none') or (macd_third_day!=macd_first_day) or (macd_second_day!=macd_third_day):
            macd_fluct_status = 'fluctuation'
        else:
            macd_fluct_status = 'not-fluctuation'	

        obv_fluc = obv_fluctuation(market)
        obv_first_day=obv_fluc[0]
        obv_second_day=obv_fluc[1]
        obv_third_day=obv_fluc[2]
        if (obv_third_day!='none' and obv_second_day!='none' and obv_first_day!='none') or  (obv_third_day!='none' and obv_second_day!='none')  or (obv_third_day!='none'  and obv_first_day!='none') or (obv_third_day!=obv_first_day) or (obv_second_day!=obv_third_day):
            obv_fluct_status = 'fluctuation'
        else:
            obv_fluct_status = 'not-fluctuation'	
		
                             
        if  candle_direction=='U' and hour_candle_direction=='U':
            candles_status='OK'
        elif candle_direction=='D' and hour_candle_direction=='D':
            candles_status='DOWN'
        else:
            candles_status='STABLE'
                    
        #print (market, candles_status, HAD_trend)		

        print ("Market parameters configured, moving to buy for ", market)
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            serf = float("{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
            if bought_price_sql!=0:
                procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))
                if procent_serf>=percent_serf_max(market):
                    cursor.execute("update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                elif procent_serf<percent_serf_min(market):
                    cursor.execute(
                    "update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",
                    (procent_serf, market))
                else:
                    cursor.execute("update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
            cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
            cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))   ##- for usd trading
            cursor.execute("update markets set current_price = %s  where market = %s and active =1",(newbid,  market))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()
            ########

        max_percent_sql = status_orders(market, 15)
        print ("Updated serf and procent serf stuff for" , market)



        print ("Starting buying mechanizm for " , market)

        # if HAD_trend!="DOWN" and HAD_trend!="Revers-DOWN" and candle_score>=0  and candles_status=='OK' and macd=="Buy" and current_order_count <= max_orders  and obv=="Buy" and macd_fluct_status=='not-fluctuation' and obv_fluct_status=='not-fluctuation' and tweet_polarity>0.14 and tweet_positive>tweet_negative: 
        if current_order_count <= max_orders:		

                            # If we have some currency on the balance
                if bought_quantity_sql !=0.0:
                    print ('    2 - We already have ' + str(
                                        format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                    try:
                        printed = ('    2 - We already have ' + str(
                                        format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                    finally:
                        db.close()
                            # if we have some active orders in sql
                elif active == 1 and iteration != 0:
                    print  ('    3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                    try:
                        printed = ('    3 - We already have ' + str(
                                        float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                    finally:
                        db.close()
                else:
                                # Buy some currency by market analize first time
                    try:
                        print ('    4- Purchasing '  + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(newask)))
                        printed = ('    4- Purchasing '  + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(newask)))
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, last, "1", currenttime, timestamp,  '  HA: ' + str(HAD_trend) + '  Day_candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) +  ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity)  + ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+' MACD: ' +str(macd)  +' OBV: ' +str(obv)))
                        cursor.execute("update orders set serf = %s, one_step_active =1 where market = %s and active =1",(serf, market))
                        db.commit()
                    except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                    finally:
                        db.close()
               


        else:
            pass
####### BUY - END ################


####### SELL START ################
def sell(row, market):
    print('Starting sell module')
    max_sell_timeout = parameters()[2]
    iso_8601= str(row['T'])		
    timestamp = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
    currtime = timestamp
    now = str(row['T'])
    currentdate = now[:-9]
    last = float(row['Last'])
    #day_close = float(row['PrevDay'])	
    macd_fluc = macd_fluctuation(market)
    macd_first_day=macd_fluc[0]
    macd_second_day=macd_fluc[1]
    macd_third_day=macd_fluc[2]
    if (macd_third_day!='none' and macd_second_day!='none' and macd_first_day!='none') or  (macd_third_day!='none' and macd_second_day!='none')  or (macd_third_day!='none'  and macd_first_day!='none')  or (macd_third_day!=macd_first_day) or (macd_second_day!=macd_third_day):
        macd_fluct_status = 'fluctuation'
    else:
        macd_fluct_status = 'not-fluctuation'	

    obv_fluc = obv_fluctuation(market)
    obv_first_day=obv_fluc[0]
    obv_second_day=obv_fluc[1]
    obv_third_day=obv_fluc[2]
    if (obv_third_day!='none' and obv_second_day!='none' and obv_first_day!='none') or  (obv_third_day!='none' and obv_second_day!='none')  or (obv_third_day!='none'  and obv_first_day!='none') or (obv_third_day!=obv_first_day) or (obv_second_day!=obv_third_day):
        obv_fluct_status = 'fluctuation'
    else:
        obv_fluct_status = 'not-fluctuation'
		
    previous_order_sell_time = previous_order(market)
    previous_order_serf = previous_serf(market)
    #Candle analisys
    currentminutes = now[:-4]
    #print (currentminutes)
    currentminutedecade = int(currentminutes[-1])	
    if currentminutedecade < 3:
        currentminutes = now[:-5]+'00'
    else:
        currentminutes = now[:-5]+'30'	
		
    lastcandle = df_thirty.loc[df_thirty['T'] == currentminutes]
    currentopen = lastcandle['O']
    currentopen = list(currentopen)	
    currentopen = currentopen[0]
    currenthigh = (lastcandle['H'])
    currenthigh = list(currenthigh)	
    currenthigh = currenthigh[0]
    currentlow = (lastcandle['L'])
    currentlow = list(currentlow)	
    currentlow = currentlow[0]
    lastcandleindex = lastcandle.index[0]	
    previouscandle = df_thirty.loc[df_thirty.index[lastcandleindex-1]]	
    prevhigh = (previouscandle['H'])
    prevclose = (previouscandle['C'])
    today_tweet = df_tw.loc[df_tw['Date'] == currentdate]
    tweet_positive=float(today_tweet['Positive'])
    tweet_negative=float(today_tweet['Negative'])
    tweet_ratio = float("{0:.2f}".format(tweet_positive/tweet_negative))
    tweet_polarity=float(today_tweet['Polarity'])
    currenttime = now[:-2]	
    #Current prices
    last = float(row['Last'])  #last price 
    #print (type(last), type(currentopen))
    bid = float(row['Bid'])  # sell price
    ask = float(row['Ask'])  # buy price
    newbid=float("{:.3f}".format(bid - bid*0.002))
    newask=float("{:.3f}".format(ask + ask*0.002))
    candles_signal_short = str(heikin_ashi(market, 29))
    candles_signal_long = str(heikin_ashi(market, 30))
    hourcurrentopen = float(heikin_ashi(market, 83))
    daycurrentopen = float(heikin_ashi(market, 84))	
    bought_price_sql = float(status_orders(market, 3))
    bought_quantity_sql = float(status_orders(market, 2))
    danger_order=int(status_orders(market, 29))
    sell_signal=status_orders(market, 23)
    sell_quantity_sql = bought_quantity_sql
    active = active_orders(market)
    iteration = int(iteration_orders(market))
    timestamp_old = int(timestamp_orders(market))
    HAD_trend=heikin_ashi(market, 18)
    candle_direction=heikin_ashi(market, 77)
    hour_candle_direction=heikin_ashi(market, 76)
    news_score=heikin_ashi(market,72)
    candle_pattern=heikin_ashi(market,69)
    previous_date = str(heikin_ashi(market,46))
    trend = str(heikin_ashi(market,78))	
    macd = str(heikin_ashi(market,79))                    
    obv = str(heikin_ashi(market,81))
	
    thirtymin='NONE'
    hour='NONE'
    day='NONE'

    if last>currentopen:
        thirtymin='U'
    else:
        thirtymin='D'

    if last>hourcurrentopen:
        hour='U'
    else:
        hour='D'

    if last>daycurrentopen:
        day='U'
    else:
        day='D'

    if  candle_direction=='U' and hour_candle_direction=='U':
        candles_status='OK'
    elif candle_direction=='D' and hour_candle_direction=='D':
        candles_status='DOWN'
    else:
        candles_status='STABLE'	
	
    print ("Market parameters configured, moving to selling for ", market)
    try:
        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
        cursor = db.cursor()
        serf = float("{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
        if bought_price_sql!=0:
            procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))          
            if procent_serf>=percent_serf_max(market):
                cursor.execute("update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
            elif procent_serf<percent_serf_min(market):
                cursor.execute("update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
            else:
                cursor.execute("update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
        cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))              
        if (percent_serf_min(market)<(-7.5)) or (previous_order_serf>0.0 and currtime-previous_order_sell_time<86400):
            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (1, market))
        if percent_serf_max(market)>5:
            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (0, market))                
        cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))   #- for usd trading
        cursor.execute("update markets set current_price = %s  where market = %s and active =1",(newbid, market))
        #print "5"
        db.commit()
    except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        db.close()
    ########

    max_percent_sql = float("{0:.2f}".format(status_orders(market, 15)))
    min_percent_sql = float("{0:.2f}".format(status_orders(market, 24)))
    print ("Updated sell serf and procent serf stuff for", market)	
	


    print ("Starting selling mechanizm for ", market)
    if bought_price_sql != None:
        if bought_quantity_sql is None or bought_quantity_sql == 0.0:
            # print market, bought_quantity_sql, current_balance
            pass
            # If curent balance of this currency more then zero
        elif bought_quantity_sql > 0:
            ##Check if we have completelly green candle
                            

            print ("Checking reason 2")
            # if ((procent_serf>=2.0 and danger_order==1 and (max_percent_sql - procent_serf > 1)) or  ((max_percent_sql - procent_serf >= 1.5) and 10.0>=procent_serf >= 4.0 and candle_direction=='D' )   or ((max_percent_sql - procent_serf >= 3) and 18.0>=procent_serf >= 10.0 and candles_status=='DOWN')):
            if 	procent_serf>=1.0:		
                                
                                #print "Reason 2 is OK"
                                
                try:
                    netto_value=float(procent_serf-0.5)
                    print ('    2  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + str(netto_value) +'  %')
                    printed = ('    2 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + str(netto_value) +'  %')
                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                    cursor = db.cursor()
                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("2 , Floating_TP   p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								    + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								    + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) + ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                    cursor.execute('update orders set active = 0 where market =("%s")' % market)      
                    cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                    newvalue = summ_serf() + (procent_serf-0.5)
                    cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                    db.commit()
                except pymysql.Error as e:
                    print ("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit(1)
                finally:
                    db.close()



            if procent_serf > 0  and (((currentopen == currentlow and prevhigh <= currentopen and currentopen < currenthigh and last > prevhigh and thirtymin=='U') or (currentopen == currentlow and currentopen < currenthigh and last > prevhigh and thirtymin=='U') )):  

                    print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                    try:
                        printed = ("    2.1 - We have GREEN candle for " + market + " and let`s wait it to be up")
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                    finally:
                        db.close()
                    pass



            else:
                print ("Checking reason 3")
                #if  procent_serf>=18: 
                if  procent_serf>=18 and (max_percent_sql - procent_serf > 1):

                    try:
                        netto_value=float(procent_serf-0.5)
                        print ('    3  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + str(netto_value) +'  %')
                        printed = ('    3 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + str(netto_value) +'  %')
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("3 , Fixed_TP p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        cursor.execute(
                            'update orders set active = 0 where market =("%s")' % market)
                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        newvalue = summ_serf() + (procent_serf-0.5)
                        cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                            currenttime, newvalue, market))
                        db.commit()
                    except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                    finally:
                        db.close()


            print ("Checking reason 4")
            if procent_serf <= -15  and  percent_serf_max(market) < 0.1  and candle_direction=='D' and HAD_trend!="UP" and HAD_trend!="Revers-UP" and candle_score<=0:
                try:
                        netto_value=float(procent_serf-0.5)
                        print ('    4  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + str(netto_value) +'  %')
                        printed = ('    4 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + str(netto_value) +'  %')

                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("4 , Floating_SL  p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend)  + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        cursor.execute(
                            'update orders set active = 0 where market =("%s")' % market)
                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        newvalue = summ_serf() + (procent_serf-0.5)
                        cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                        db.commit()
                except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                finally:
                        db.close()






            print ("Checking reason 5") 
            if procent_serf <= -20  and  macd=="Sell"  and candle_direction=='D' and HAD_trend!="UP" and HAD_trend!="Revers-UP" and HAD_trend!="STABLE" and candle_score<=0:
                try:
                        netto_value=float(procent_serf-0.5)
                        print ('    5  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + str(netto_value) +'  %')
                        printed = ('    5 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + str(netto_value) +'  %')

                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("5 , MACD_SL  p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend)  + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        cursor.execute(
                            'update orders set active = 0 where market =("%s")' % market)
                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        newvalue = summ_serf() + (procent_serf-0.5)
                        cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                        db.commit()
                except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                finally:
                        db.close()







            print ("Checking reason 6")
            if procent_serf <= -30:
                try:
                        netto_value=float(procent_serf-0.5)
                        print ('    6  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + str(netto_value) +'  %')
                        printed = ('    6 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + str(netto_value) +'  %')
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("6 , Fixed_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        cursor.execute(
                            'update orders set active = 0 where market =("%s")' % market)
                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        newvalue = summ_serf() + (procent_serf-0.5)
                        cursor.execute(
                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                        currenttime, newvalue, market))
                        db.commit()
                except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                finally:
                        db.close()

									
									
									

            print ("Checking reason 7")
            if (1.0>procent_serf>=-10 and danger_order==1 and candle_direction=='D' and percent_serf_min(market) <= -20 and timestamp-timestamp_old >=2500000) or (1.0>procent_serf>=-15 and danger_order==1 and candle_direction=='D' and hour_candle_direction=='D' and percent_serf_min(market) <= -20 and timestamp-timestamp_old >=3500000 and candle_score<0) : # and (candle_score<0 or news_score<0)):
                try:
                        netto_value=float(procent_serf-0.5)
                        print ('    7  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and losing  '   + str(netto_value) +'  %')
                        printed = ('    7 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and losing   '     + str(netto_value) +'  %')
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("7 , Long_lasting_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        cursor.execute(
                            'update orders set active = 0 where market =("%s")' % market)
                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        newvalue = summ_serf() + (procent_serf-0.5)
                        cursor.execute(
                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                            currenttime, newvalue, market))
                        db.commit()
                except pymysql.Error as e:
                        print ("Error %d: %s" % (e.args[0], e.args[1]))
                        sys.exit(1)
                finally:
                        db.close()





            # print ("Checking reason 8")
            # if (macd=="Sell" and macd_fluct_status == 'not-fluctuation'):
                # try:
                        # netto_value=float(procent_serf-0.5)
                        # print ('    8  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting or losing  '   + str(netto_value) +'  %')
                        # printed = ('    8 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or losing   '     + str(netto_value) +'  %')
                        # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                        # cursor = db.cursor()
                        # cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        # cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("8 , MACD_SELL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        # + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score)   + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        # + ' Tweet_polarity: ' + str(tweet_polarity)   + ' Candle_pattern: ' + str(candle_pattern) +   ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                        # cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                        # cursor.execute(
                            # 'update orders set active = 0 where market =("%s")' % market)
                        # cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                        # newvalue = summ_serf() + (procent_serf-0.5)
                        # cursor.execute(
                            # 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                            # currenttime, newvalue, market))
                        # db.commit()
                # except pymysql.Error as e:
                        # print ("Error %d: %s" % (e.args[0], e.args[1]))
                        # sys.exit(1)
                # finally:
                        # db.close()





            else:
                pass


        else:
             pass					

    else:
        pass
####### SELL - END ################




		










def heikin_ashi_module(market, df_day, fivemin_day, row):
        print ("Starting heikin ashi module")
        days=15
        dayid=days-1	
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)	
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-14:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date 		
        df = df_day
        #print (fivemin_day)

        daycurrentdate = (df['Date'][14])		
        dayprevdate = (df['Date'][13])
        dayprevdate2 = (df['Date'][12])
        dayprevdate3 = (df['Date'][11])
        dayprevdate4 = (df['Date'][10])
        dayprevdate5 = (df['Date'][9])
        dayprevdate6 = (df['Date'][8])
        dayprevdate7 = (df['Date'][7])          
        dayprevdate8 = (df['Date'][6])
        dayprevdate9 = (df['Date'][5])
        dayprevdate10 = (df['Date'][4])
        dayprevdate11 = (df['Date'][3])
        dayprevdate12 = (df['Date'][2])          
        dayprevdate13 = (df['Date'][1])
        dayprevdate14 = (df['Date'][0])
        heikin_ashi_df = heikin_ashi_func(df)
        ohlc_df = heikin_ashi_df.copy()
        date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]
        ohlc_df['Date']=date
        ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
	
					
        HAD_PREV_Close4 = ohlc_df['Close'][dayid-4]
        HAD_PREV_Open4 = ohlc_df['Open'][dayid-4]
        HAD_PREV_Low4 = ohlc_df['High'][dayid-4]
        HAD_PREV_High4 = ohlc_df['Low'][dayid-4]
        HAD_PREV_Close3 = ohlc_df['Close'][dayid-3]
        HAD_PREV_Open3 = ohlc_df['Open'][dayid-3]
        HAD_PREV_High3 = ohlc_df['High'][dayid-3]
        HAD_PREV_Low3 = ohlc_df['Low'][dayid-3]
        HAD_PREV_Close2 = ohlc_df['Close'][dayid-2]
        HAD_PREV_Open2 = ohlc_df['Open'][dayid-2]
        HAD_PREV_High2 = ohlc_df['High'][dayid-2]
        HAD_PREV_Low2 = ohlc_df['Low'][dayid-2]
        HAD_PREV_Close = ohlc_df['Close'][dayid-1]
        HAD_PREV_Open = ohlc_df['Open'][dayid-1]
        HAD_PREV_High = ohlc_df['High'][dayid-1]
        HAD_PREV_Low = ohlc_df['Low'][dayid-1]
        HAD_Close = ohlc_df['Close'][dayid]
        HAD_Open = ohlc_df['Open'][dayid]
        HAD_High = ohlc_df['High'][dayid]
        HAD_Low = ohlc_df['Low'][dayid]				
        HAD_trend = "NONE"
        had_direction_down_short0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 2)  and (HAD_Open - HAD_Close !=0)
        had_direction_down_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 2) and (HAD_PREV_Open - HAD_PREV_Close !=0)
        had_direction_down_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 2) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
        had_direction_down_shorter0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 4)  and (HAD_Open - HAD_Close !=0)
        had_direction_down_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 4) and (HAD_PREV_Open - HAD_PREV_Close !=0)
        had_direction_down_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 4) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
        had_direction_down0 = (HAD_Close < HAD_Open)
        had_direction_down1 = (HAD_PREV_Close < HAD_PREV_Open)
        had_direction_down2 = (HAD_PREV_Close2 < HAD_PREV_Open2)
        had_direction_down_long_0 = (HAD_Open == HAD_High and HAD_Close < HAD_Open)
        had_direction_down_long_1 = (HAD_PREV_Open == HAD_PREV_High and HAD_PREV_Close < HAD_PREV_Open)
        had_direction_down_long_2 = (HAD_PREV_Open2 == HAD_PREV_High2 and HAD_PREV_Close2 < HAD_PREV_Open2)
        had_direction_down_longer = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
        had_direction_down_longermax = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) > numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2 ) and had_direction_down0 and had_direction_down1 and had_direction_down2)
        had_direction_down_smaller = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
        had_direction_down_smaller1 = (numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down1 and had_direction_down2)
        had_direction_down_smallermax = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down0 and had_direction_down1 and had_direction_down2)
        had_direction_spin0 = (HAD_Open == HAD_Close)
        had_direction_spin1 = (HAD_PREV_Open == HAD_PREV_Close)
        had_direction_spin2 = (HAD_PREV_Open2 == HAD_PREV_Close2)
        had_direction_up_short0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 2) and (HAD_Close - HAD_Open !=0)
        had_direction_up_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 2) and (HAD_PREV_Close - HAD_PREV_Open !=0)
        had_direction_up_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 2) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
        had_direction_up_shorter0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 4) and (HAD_Close - HAD_Open !=0)
        had_direction_up_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 4) and (HAD_PREV_Close - HAD_PREV_Open !=0)
        had_direction_up_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 4) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
        had_direction_up0 = (HAD_Close > HAD_Open)
        had_direction_up1 = (HAD_PREV_Close > HAD_PREV_Open)
        had_direction_up2 = (HAD_PREV_Close2 > HAD_PREV_Open2)
        had_direction_up_long_0 = (HAD_Open == HAD_Low and HAD_Close > HAD_Open)
        had_direction_up_long_1 = (HAD_PREV_Open == HAD_PREV_Low and HAD_PREV_Close > HAD_PREV_Open)
        had_direction_up_long_2 = (HAD_PREV_Open2 == HAD_PREV_Low2 and HAD_PREV_Close2 > HAD_PREV_Open2)
        had_direction_up_longer = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
        had_direction_up_longermax = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) > numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
        had_direction_up_smaller = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
        had_direction_up_smaller1 = (numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up1 and had_direction_up2)
        had_direction_up_smallermax = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)

        if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
                    HAD_trend = "DOWN"
        elif (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
                    HAD_trend = "UP"
        elif ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
                    HAD_trend = "Revers-UP"
        elif ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
                    HAD_trend = "Revers-DOWN"
        else:
                    HAD_trend = "STABLE"  

        if (had_direction_spin0):
                    HaD_current_candle = "had_direction_spin0"
        if (had_direction_down_short0):
                    HaD_current_candle = "had_direction_down_short0"                    
        if (had_direction_down_long_0):
                    HaD_current_candle = "had_direction_down_long_0"                    
        if (had_direction_down0):
                    HaD_current_candle = "had_direction_down0"
        if (had_direction_up_short0):
                    HaD_current_candle = "had_direction_up_short0"                    
        if (had_direction_up_long_0):
                    HaD_current_candle = "had_direction_up_long_0"
        if (had_direction_up0):
                    HaD_current_candle = "had_direction_up0"
        if (had_direction_spin1):
                    HaD_previous_candle = "had_direction_spin1" 
        if (had_direction_down_short1):
                    HaD_previous_candle = "had_direction_down_short1"                    
        if (had_direction_down_long_1):
                    HaD_previous_candle = "had_direction_down_long_1" 
        if (had_direction_down1):
                    HaD_previous_candle = "had_direction_down1"
        if (had_direction_up_short1):
                    HaD_previous_candle = "had_direction_up_short1"                     
        if (had_direction_up_long_1):
                    HaD_previous_candle = "had_direction_up_long_1"
        if (had_direction_up1):
                    HaD_previous_candle = "had_direction_up1"				
				
        print (market, HAD_trend)
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set current_price = %s, ha_direction_daily=%s, had_candle_previous=%s, had_candle_current=%s  where market = %s",(last,  HAD_trend, HaD_previous_candle, HaD_current_candle,  market))                   
            cursor.execute("update markets set ha_day=%s  where market = %s",(HAD_trend,  market))
            cursor.execute("update history set price='%s' where market='%s' and date='%s'" % (last, market, currentdate))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()

        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set ha_day=%s, ha_time_second=%s  where market = %s",(HAD_trend, currtime, market))
            cursor.execute("update history set ha_day='%s'  where market='%s' and date='%s'" % (HAD_trend, market, currentdate))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()					
	

def heikin_ashi_module_img(market, df_day, fivemin_day, row):
        print ("Starting heikin ashi module")
        days=15
        dayid=days-1	
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-14:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date 		
        df = df_day
        daycurrentdate = (df['Date'][14])		
        dayprevdate = (df['Date'][13])
        dayprevdate2 = (df['Date'][12])
        dayprevdate3 = (df['Date'][11])
        dayprevdate4 = (df['Date'][10])
        dayprevdate5 = (df['Date'][9])
        dayprevdate6 = (df['Date'][8])
        dayprevdate7 = (df['Date'][7])          
        dayprevdate8 = (df['Date'][6])
        dayprevdate9 = (df['Date'][5])
        dayprevdate10 = (df['Date'][4])
        dayprevdate11 = (df['Date'][3])
        dayprevdate12 = (df['Date'][2])          
        dayprevdate13 = (df['Date'][1])
        dayprevdate14 = (df['Date'][0])
        heikin_ashi_df = heikin_ashi_func(df)
        ohlc_df = heikin_ashi_df.copy()
        date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]
        ohlc_df['Date']=date
        ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.xaxis_date()
        candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
        plt.title(market)
        plt.gcf().autofmt_xdate()
        plt.autoscale(tight=True)  				
        plt.grid()
        ax.grid(True)
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/hachart.png')
        plt.clf()
        plt.cla()
        plt.close() 		
        newfilename=("{}_hachart.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/hachart.png"		
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)
        print (new_name)
        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator"
        for pngfile in glob.iglob(os.path.join(src_dir, "*_hachart.png")):
            shutil.copy(pngfile, dst_dir)	
					
        HAD_PREV_Close4 = ohlc_df['Close'][dayid-4]
        HAD_PREV_Open4 = ohlc_df['Open'][dayid-4]
        HAD_PREV_Low4 = ohlc_df['High'][dayid-4]
        HAD_PREV_High4 = ohlc_df['Low'][dayid-4]
        HAD_PREV_Close3 = ohlc_df['Close'][dayid-3]
        HAD_PREV_Open3 = ohlc_df['Open'][dayid-3]
        HAD_PREV_High3 = ohlc_df['High'][dayid-3]
        HAD_PREV_Low3 = ohlc_df['Low'][dayid-3]
        HAD_PREV_Close2 = ohlc_df['Close'][dayid-2]
        HAD_PREV_Open2 = ohlc_df['Open'][dayid-2]
        HAD_PREV_High2 = ohlc_df['High'][dayid-2]
        HAD_PREV_Low2 = ohlc_df['Low'][dayid-2]
        HAD_PREV_Close = ohlc_df['Close'][dayid-1]
        HAD_PREV_Open = ohlc_df['Open'][dayid-1]
        HAD_PREV_High = ohlc_df['High'][dayid-1]
        HAD_PREV_Low = ohlc_df['Low'][dayid-1]
        HAD_Close = ohlc_df['Close'][dayid]
        HAD_Open = ohlc_df['Open'][dayid]
        HAD_High = ohlc_df['High'][dayid]
        HAD_Low = ohlc_df['Low'][dayid]				
        HAD_trend = "NONE"
        had_direction_down_short0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 2)  and (HAD_Open - HAD_Close !=0)
        had_direction_down_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 2) and (HAD_PREV_Open - HAD_PREV_Close !=0)
        had_direction_down_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 2) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
        had_direction_down_shorter0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 4)  and (HAD_Open - HAD_Close !=0)
        had_direction_down_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 4) and (HAD_PREV_Open - HAD_PREV_Close !=0)
        had_direction_down_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 4) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
        had_direction_down0 = (HAD_Close < HAD_Open)
        had_direction_down1 = (HAD_PREV_Close < HAD_PREV_Open)
        had_direction_down2 = (HAD_PREV_Close2 < HAD_PREV_Open2)
        had_direction_down_long_0 = (HAD_Open == HAD_High and HAD_Close < HAD_Open)
        had_direction_down_long_1 = (HAD_PREV_Open == HAD_PREV_High and HAD_PREV_Close < HAD_PREV_Open)
        had_direction_down_long_2 = (HAD_PREV_Open2 == HAD_PREV_High2 and HAD_PREV_Close2 < HAD_PREV_Open2)
        had_direction_down_longer = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
        had_direction_down_longermax = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) > numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2 ) and had_direction_down0 and had_direction_down1 and had_direction_down2)
        had_direction_down_smaller = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
        had_direction_down_smaller1 = (numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down1 and had_direction_down2)
        had_direction_down_smallermax = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down0 and had_direction_down1 and had_direction_down2)
        had_direction_spin0 = (HAD_Open == HAD_Close)
        had_direction_spin1 = (HAD_PREV_Open == HAD_PREV_Close)
        had_direction_spin2 = (HAD_PREV_Open2 == HAD_PREV_Close2)
        had_direction_up_short0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 2) and (HAD_Close - HAD_Open !=0)
        had_direction_up_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 2) and (HAD_PREV_Close - HAD_PREV_Open !=0)
        had_direction_up_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 2) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
        had_direction_up_shorter0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 4) and (HAD_Close - HAD_Open !=0)
        had_direction_up_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 4) and (HAD_PREV_Close - HAD_PREV_Open !=0)
        had_direction_up_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 4) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
        had_direction_up0 = (HAD_Close > HAD_Open)
        had_direction_up1 = (HAD_PREV_Close > HAD_PREV_Open)
        had_direction_up2 = (HAD_PREV_Close2 > HAD_PREV_Open2)
        had_direction_up_long_0 = (HAD_Open == HAD_Low and HAD_Close > HAD_Open)
        had_direction_up_long_1 = (HAD_PREV_Open == HAD_PREV_Low and HAD_PREV_Close > HAD_PREV_Open)
        had_direction_up_long_2 = (HAD_PREV_Open2 == HAD_PREV_Low2 and HAD_PREV_Close2 > HAD_PREV_Open2)
        had_direction_up_longer = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
        had_direction_up_longermax = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) > numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
        had_direction_up_smaller = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
        had_direction_up_smaller1 = (numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up1 and had_direction_up2)
        had_direction_up_smallermax = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)

        if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
                    HAD_trend = "DOWN"
        elif (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
                    HAD_trend = "UP"
        elif ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
                    HAD_trend = "Revers-UP"
        elif ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
                    HAD_trend = "Revers-DOWN"
        else:
                    HAD_trend = "STABLE"  

        if (had_direction_spin0):
                    HaD_current_candle = "had_direction_spin0"
        if (had_direction_down_short0):
                    HaD_current_candle = "had_direction_down_short0"                    
        if (had_direction_down_long_0):
                    HaD_current_candle = "had_direction_down_long_0"                    
        if (had_direction_down0):
                    HaD_current_candle = "had_direction_down0"
        if (had_direction_up_short0):
                    HaD_current_candle = "had_direction_up_short0"                    
        if (had_direction_up_long_0):
                    HaD_current_candle = "had_direction_up_long_0"
        if (had_direction_up0):
                    HaD_current_candle = "had_direction_up0"
        if (had_direction_spin1):
                    HaD_previous_candle = "had_direction_spin1" 
        if (had_direction_down_short1):
                    HaD_previous_candle = "had_direction_down_short1"                    
        if (had_direction_down_long_1):
                    HaD_previous_candle = "had_direction_down_long_1" 
        if (had_direction_down1):
                    HaD_previous_candle = "had_direction_down1"
        if (had_direction_up_short1):
                    HaD_previous_candle = "had_direction_up_short1"                     
        if (had_direction_up_long_1):
                    HaD_previous_candle = "had_direction_up_long_1"
        if (had_direction_up1):
                    HaD_previous_candle = "had_direction_up1"				
				
        print (market, HAD_trend)
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set current_price = %s, ha_direction_daily=%s, had_candle_previous=%s, had_candle_current=%s  where market = %s",(last,  HAD_trend, HaD_previous_candle, HaD_current_candle,  market))                   
            cursor.execute("update markets set ha_day=%s  where market = %s",(HAD_trend,  market))
            cursor.execute("update history set price='%s' where market='%s' and date='%s'" % (last, market, currentdate))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()

        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set ha_day=%s, ha_time_second=%s  where market = %s",(HAD_trend, currtime, market))
            cursor.execute("update history set ha_day='%s'  where market='%s' and date='%s'" % (HAD_trend, market, currentdate))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()		


def obv(market, df_day, fivemin_day, row):
        print ("Starting obv module")
        increased_volume = []		
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        #print (row)

        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-59:df_day_index]
        #print (df_day)		
        df_day = df_day.append(row, ignore_index=True)
        #print (df_day)
        del df_day["day"]
        del df_day["BV"]

        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        #print (fivemin_day)
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name		
        df = df_day 
        df = df.reset_index().rename({'index':'date'}, axis = 'columns')
        #print (df)		
        market_df = df[['date', 'adjclose', 'volume']]
        market_df.columns = ['date', 'close', 'volume']
        market_df = market_df.sort_values('date')
        #print (market_df)
        df = on_balance_volume(market_df)
        new_df = df.copy()
        new_df = new_df.drop(['close', 'volume'], axis = 1)
        new_obv = get_obv(new_df)
        buy_price, sell_price, obv_signal = implement_obv_strategy(df['close'], new_obv)

        position = []
        for i in range(len(obv_signal)):
          if obv_signal[i] > 1:
              position.append(0)
          else:
              position.append(1)
        
        for i in range(len(df['close'])):
          if obv_signal[i] == 1:
             position[i] = 1
          elif obv_signal[i] == -1:
             position[i] = 0
          else:
             position[i] = position[i-1]

        obv = new_obv['obv']
        signal = new_obv['obv_ema21']
        close_price = df['close']
        obv_signal = pd.DataFrame(obv_signal).rename(columns = {0:'obv_signal'}).set_index(df.index)
        position = pd.DataFrame(position).rename(columns = {0:'obv_position'}).set_index(df.index)
        frames = [close_price, obv, signal, obv_signal, position]
        strategy = pd.concat(frames, join = 'inner', axis = 1)
        row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
        first_max = strategy.values[row_ix, range(strategy.shape[1])]
        out = pd.DataFrame([first_max], columns=strategy.columns)
        last_obv_signal = int(out['obv_signal'])
        #print (last_obv_signal)

        obv_signal= strategy.iloc[-1]
        obv_signal = int(obv_signal['obv_signal'])
        if obv_signal == 0:
           print ("OBV is 0, nothing to do")
        else:
           if obv_signal == 1:
              signal = "Buy"
              print ("OBV is Buy")			  
           else:
              signal = "Sell"
              print ("OBV is Sell")
           try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set obv_signal='%s'  where market='%s'" % (signal, market))
               cursor.execute("update history set obv_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
               db.commit()
           except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
           finally:
               db.close()



        if last_obv_signal == 1:
              signal = "Buy"
        else:
              signal = "Sell"
        try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set obv_signal='%s'  where market='%s'" % (signal, market))
               db.commit()
        except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
        finally:
               db.close()


def obv_img(market, df_day, fivemin_day, row):
        print ("Starting obv module")
        increased_volume = []		
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        #print (df_day_today)

        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-59:df_day_index]
        #print (df_day)		
        df_day = df_day.append(row, ignore_index=True)
        #print (df_day)
        del df_day["day"]
        del df_day["BV"]

        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        #print (fivemin_day)
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name		
        df = df_day 
        df = df.reset_index().rename({'index':'date'}, axis = 'columns')
        #print (df)		
        market_df = df[['date', 'adjclose', 'volume']]
        market_df.columns = ['date', 'close', 'volume']
        market_df = market_df.sort_values('date')
        #print (market_df)
        df = on_balance_volume(market_df)
        new_df = df.copy()
        new_df = new_df.drop(['close', 'volume'], axis = 1)
        new_obv = get_obv(new_df)
        buy_price, sell_price, obv_signal = implement_obv_strategy(df['close'], new_obv)
        fig, ax = plt.subplots(figsize=(16, 8))
        plt.title(market)
        plt.plot(df['date'], df['close'], label='Close', color='black')
        plt.plot(df['date'], buy_price, marker = '^', color = 'green', markersize = 8, label = 'BUY SIGNAL', linewidth = 0)
        plt.plot(df['date'], sell_price, marker = 'v', color = 'r', markersize = 8, label = 'SELL SIGNAL', linewidth = 0)
        plt.legend(loc='upper left')
        plt.grid()
        # Get second axis
        ax2 = ax.twinx()
        plt.plot(df['date'],  df['obv'], label='obv',color='blue')
        plt.plot(df['date'],  df['obv_ema21'], label='obv_ema21',color='red')
        ax.plot(df['date'], buy_price, marker = '^', color = 'green', markersize = 8, label = 'BUY SIGNAL', linewidth = 0)
        ax.plot(df['date'], sell_price, marker = 'v', color = 'r', markersize = 8, label = 'SELL SIGNAL', linewidth = 0)
        for i in range(len(new_obv)):
            if str(new_obv['hist'][i])[0] == '-':
                 ax2.bar(new_obv['date'][i], new_obv['hist'][i], color = '#ef5350')
            else:
                ax2.bar(new_obv['date'][i], new_obv['hist'][i], color = '#26a69a') 
        plt.legend(loc='upper right')
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/obv_results.png')
        plt.clf()
        plt.cla()
        plt.close() 
        newfilename=("{}_obv_results.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/obv_results.png"
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)
        print (new_name)
        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator/"
        for pngfile in glob.iglob(os.path.join(src_dir, "*obv_results.png")):
            shutil.copy(pngfile, dst_dir)

        position = []
        for i in range(len(obv_signal)):
          if obv_signal[i] > 1:
              position.append(0)
          else:
              position.append(1)
        
        for i in range(len(df['close'])):
          if obv_signal[i] == 1:
             position[i] = 1
          elif obv_signal[i] == -1:
             position[i] = 0
          else:
             position[i] = position[i-1]

        obv = new_obv['obv']
        signal = new_obv['obv_ema21']
        close_price = df['close']
        obv_signal = pd.DataFrame(obv_signal).rename(columns = {0:'obv_signal'}).set_index(df.index)
        position = pd.DataFrame(position).rename(columns = {0:'obv_position'}).set_index(df.index)
        frames = [close_price, obv, signal, obv_signal, position]
        strategy = pd.concat(frames, join = 'inner', axis = 1)
        row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
        first_max = strategy.values[row_ix, range(strategy.shape[1])]
        out = pd.DataFrame([first_max], columns=strategy.columns)
        last_obv_signal = int(out['obv_signal'])
        print (last_obv_signal)

        obv_signal= strategy.iloc[-1]
        obv_signal = int(obv_signal['obv_signal'])
        if obv_signal == 0:
           print ("OBV is 0, nothing to do")
        else:
           if obv_signal == 1:
              signal = "Buy"
           else:
              signal = "Sell"
           try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set obv_signal='%s'  where market='%s'" % (signal, market))
               cursor.execute("update history set obv_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
               db.commit()
           except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
           finally:
               db.close()



        if last_obv_signal == 1:
              signal = "Buy"
        else:
              signal = "Sell"
        try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set obv_signal='%s'  where market='%s'" % (signal, market))
               db.commit()
        except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
        finally:
               db.close()


def macd_module(market, df_day, fivemin_day, row):
        print ("Starting macd module")		
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-59:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name
        df = df_day
        new_macd = get_macd(df['close'], 26, 12, 6)
        #print (new_macd)		
        buy_price, sell_price, macd_signal = implement_macd_strategy(df['close'], new_macd)

		  
        position = []
        for i in range(len(macd_signal)):
          if macd_signal[i] > 1:
             position.append(0)
          else:
             position.append(1)
        
        for i in range(len(df['close'])):
          if macd_signal[i] == 1:
             position[i] = 1
          elif macd_signal[i] == -1:
             position[i] = 0
          else:
             position[i] = position[i-1]
        
        macd = new_macd['macd']
        signal = new_macd['signal']
        close_price = df['close']
        macd_signal = pd.DataFrame(macd_signal).rename(columns = {0:'macd_signal'}).set_index(df.index)
        position = pd.DataFrame(position).rename(columns = {0:'macd_position'}).set_index(df.index)

        frames = [close_price, macd, signal, macd_signal, position]
        strategy = pd.concat(frames, join = 'inner', axis = 1)

          #print (strategy)
        row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
        first_max = strategy.values[row_ix, range(strategy.shape[1])]
        out = pd.DataFrame([first_max], columns=strategy.columns)
          #print (out)
        last_macd_signal = int(out['macd_signal'])
        #print (last_macd_signal)
		  
        macd_signal= strategy.iloc[-1]
        macd_signal = int(macd_signal['macd_signal'])
        if macd_signal == 0:
           print ("MACD is 0, nothing to do")
        else:
           if macd_signal == 1:
              signal = "Buy"
              print ("MACD is Buy")
           else:
              signal = "Sell"
              print ("MACD is Sell")
           try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
               cursor.execute("update history set macd_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
               db.commit()
           except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
           finally:
               db.close()

        if last_macd_signal == 1:
              signal = "Buy"
        else:
              signal = "Sell"
        try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
               db.commit()
        except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
        finally:
               db.close()				 


def macd_module_img(market, df_day, fivemin_day, row):
        print ("Starting macd module")		
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-59:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name
        df = df_day
        new_macd = get_macd(df['close'], 26, 12, 6)
        #print (new_macd)		
        buy_price, sell_price, macd_signal = implement_macd_strategy(df['close'], new_macd)
        plt.rcParams['figure.figsize'] = (20, 15)
        plt.style.use('fivethirtyeight')
        ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
        ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
        ax1.plot(df['close'], color = 'skyblue', linewidth = 2, label = market)
        ax1.plot(df.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
        ax1.plot(df.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
        ax1.legend()
        ax1.set_title('MACD SIGNALS')
        ax2.plot(new_macd['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
        ax2.plot(new_macd['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')
        for i in range(len(new_macd)):
            if str(new_macd['hist'][i])[0] == '-':
               ax2.bar(new_macd.index[i], new_macd['hist'][i], color = '#ef5350')
            else:
               ax2.bar(new_macd.index[i], new_macd['hist'][i], color = '#26a69a')
        plt.legend(loc = 'lower right')
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/macd_results.png', bbox_inches='tight')  
        plt.clf()
        plt.cla()
        plt.close() 		
        newfilename=("{}_macd_results.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/macd_results.png"
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)

        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator/"
        for pngfile in glob.iglob(os.path.join(src_dir, "*macd_results.png")):
           shutil.copy(pngfile, dst_dir)				 
        print (new_name)

        #print (macd_signal)
		  
        position = []
        for i in range(len(macd_signal)):
          if macd_signal[i] > 1:
             position.append(0)
          else:
             position.append(1)
        
        for i in range(len(df['close'])):
          if macd_signal[i] == 1:
             position[i] = 1
          elif macd_signal[i] == -1:
             position[i] = 0
          else:
             position[i] = position[i-1]
        
        macd = new_macd['macd']
        signal = new_macd['signal']
        close_price = df['close']
        macd_signal = pd.DataFrame(macd_signal).rename(columns = {0:'macd_signal'}).set_index(df.index)
        position = pd.DataFrame(position).rename(columns = {0:'macd_position'}).set_index(df.index)

        frames = [close_price, macd, signal, macd_signal, position]
        strategy = pd.concat(frames, join = 'inner', axis = 1)

          #print (strategy)
        row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
        first_max = strategy.values[row_ix, range(strategy.shape[1])]
        out = pd.DataFrame([first_max], columns=strategy.columns)
          #print (out)
        last_macd_signal = int(out['macd_signal'])
        #print (last_macd_signal)
		  
        macd_signal= strategy.iloc[-1]
        macd_signal = int(macd_signal['macd_signal'])
        if macd_signal == 0:
           print ("MACD is 0, nothing to do")
        else:
           if macd_signal == 1:
              signal = "Buy"
           else:
              signal = "Sell"
           try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
               cursor.execute("update history set macd_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
               db.commit()
           except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
           finally:
               db.close()

        if last_macd_signal == 1:
              signal = "Buy"
        else:
              signal = "Sell"
        try:
               db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
               cursor = db.cursor()
               cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
               db.commit()
        except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
        finally:
               db.close()		
	
	
def candle_patterns(market, df_day, fivemin_day, row):
        print ("Starting candle patterns module")
        days=30
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-30:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date  		

        df = df_day
        ohlc_df = df.copy()
        ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]	  
        df=candle_df(df)
        #print (df)
        candle_score=market_values(market,68)
        candle_pattern=market_values(market,69)
        candletime=int(market_values(market,70))
        buy_df = df.copy()
        candle_scored_buy= buy_df[(buy_df['candle_score'] > 0)]
        candle_scored_sell= df[(df['candle_score'] < 0)]		  
        labels_buy=(candle_scored_buy['candle_pattern'].tolist())
        labels_sell=(candle_scored_sell['candle_pattern'].tolist())	
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
        legend_elements = [Line2D([0], [0], marker="^", color='w', label='B_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_w_s -> Three_white_soldiers', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_b -> Tweezer_Bottom', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='M_S -> Morning_Star', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_HR -> Bullish_Harami', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='Bu_E -> Bullish_Engulfing', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='H_M_Bu -> Hanging_Man_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_c -> Three_black_crows', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_g -> Two_black_gapping', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_t -> Tweezer_Top', markersize=15), Line2D([0], [0], marker="v", color='r', label='E_S -> Evening_Star', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_HR -> Bearish_Harami', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_R -> Bearish_Reversal', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BE -> Shooting_Star_Bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='Be_E -> Bearish_Engulfing', markersize=15), Line2D([0], [0], marker="v", color='r', label='H_M_Be -> Hanging_Man_bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BU -> Shooting_Star_Bullish', markersize=15)]


        new_df= (buy_df.iloc[-2:])
        #print (new_df)
        sum_score = new_df['candle_score'].sum()
        last_df= buy_df.iloc[-1]
        last_pattern = last_df['candle_pattern']
        new_df_check_patten=(buy_df.iloc[-2:])
        previous_day_pattern=(new_df_check_patten.iloc[:1])
        previous_day_pattern=previous_day_pattern.iloc[-1]
        previous_day_pattern=previous_day_pattern['candle_pattern']
        #print (sum_score)


        if (last_pattern =="" and previous_day_pattern!=candle_pattern):
            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()				  



        if (last_pattern =="" and currtime-candletime>400000):
            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()	


				 
        if last_pattern !="":
            print (last_pattern, previous_day_pattern)

            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s', candle_time='%s'  where market='%s'" % (last_pattern, currtime, market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (sum_score, market))
                     cursor.execute("update history set candle_score='%s', candle_pattern='%s'  where market='%s' and date='%s'" % (sum_score, last_pattern, market, currentdate))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()

        else:
            pass 


def candle_patterns_img(market, df_day, fivemin_day, row):
        print ("Starting candle patterns module")
        days=30
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-30:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date  		

        df = df_day
        ohlc_df = df.copy()
        ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]	  
        df=candle_df(df)
        #print (df)
        candle_score=market_values(market,68)
        candle_pattern=market_values(market,69)
        candletime=int(market_values(market,70))
        buy_df = df.copy()
        candle_scored_buy= buy_df[(buy_df['candle_score'] > 0)]
        candle_scored_sell= df[(df['candle_score'] < 0)]		  
        labels_buy=(candle_scored_buy['candle_pattern'].tolist())
        labels_sell=(candle_scored_sell['candle_pattern'].tolist())	
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
        legend_elements = [Line2D([0], [0], marker="^", color='w', label='B_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_w_s -> Three_white_soldiers', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_b -> Tweezer_Bottom', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='M_S -> Morning_Star', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_HR -> Bullish_Harami', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='Bu_E -> Bullish_Engulfing', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='H_M_Bu -> Hanging_Man_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_c -> Three_black_crows', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_g -> Two_black_gapping', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_t -> Tweezer_Top', markersize=15), Line2D([0], [0], marker="v", color='r', label='E_S -> Evening_Star', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_HR -> Bearish_Harami', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_R -> Bearish_Reversal', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BE -> Shooting_Star_Bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='Be_E -> Bearish_Engulfing', markersize=15), Line2D([0], [0], marker="v", color='r', label='H_M_Be -> Hanging_Man_bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BU -> Shooting_Star_Bullish', markersize=15)]

        fig, ax = plt.subplots(figsize=(20, 15))
        ax.legend(handles=legend_elements, loc='upper left')
        # Converts raw mdate numbers to dates
        ax.xaxis_date()
        plt.xlabel("Date")	  
        # Making candlestick plot
        candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
        plt.ylabel("Price")
        plt.title(market) 	  
        ax2 = ax.twinx()
        candle_scored_buy['Date'] = ohlc_df['Date']
        x=candle_scored_buy['Date'].tolist()
        y=candle_scored_buy['candle_score'].tolist()
        n = labels_buy
        ax2.axhline(y=2)
        ax2.plot([x], [2], marker='o', markersize=1)
        ax2.scatter(x, y, c='g', marker="^", s=120)
        for i, txt in enumerate(n):
            ax2.annotate(txt, (x[i], y[i]))
        x1=candle_scored_sell['Date'].tolist()
        y1=candle_scored_sell['candle_score'].tolist()
        n1 = labels_sell
        ax2.scatter(x1, y1, c='r', marker="v", s=120)
        for a, txt1 in enumerate(n1):
            ax2.annotate(txt1, (x1[a], y1[a]))	
        ax2.axhline(y=-2)
		
        plt.gcf().autofmt_xdate()   # Beautify the x-labels
        plt.autoscale(tight=True)
        plt.grid()
        ax.grid(True)
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/candlesticks.png')
        plt.clf()
        plt.cla()
        plt.close()  
        newfilename=("{}_candlesticks.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/candlesticks.png"
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)
        print (new_name)
        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator/"
        for pngfile in glob.iglob(os.path.join(src_dir, "*_candlesticks.png")):
            shutil.copy(pngfile, dst_dir)

        new_df= (buy_df.iloc[-2:])
        #print (new_df)
        sum_score = new_df['candle_score'].sum()
        last_df= buy_df.iloc[-1]
        last_pattern = last_df['candle_pattern']
        new_df_check_patten=(buy_df.iloc[-2:])
        previous_day_pattern=(new_df_check_patten.iloc[:1])
        previous_day_pattern=previous_day_pattern.iloc[-1]
        previous_day_pattern=previous_day_pattern['candle_pattern']
        #print (sum_score)


        if (last_pattern =="" and previous_day_pattern!=candle_pattern):
            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()				  



        if (last_pattern =="" and currtime-candletime>400000):
            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()	


				 
        if last_pattern !="":
            print (last_pattern, previous_day_pattern)

            try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s', candle_time='%s'  where market='%s'" % (last_pattern, currtime, market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (sum_score, market))
                     cursor.execute("update history set candle_score='%s', candle_pattern='%s'  where market='%s' and date='%s'" % (sum_score, last_pattern, market, currentdate))					 
                     db.commit()
            except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
            finally:
                     db.close()

        else:
            pass 


def candle_charts_img(market, df_day, fivemin_day, row):
        print ("Starting candle chart module")
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]		
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-15:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date  		
        #print (df_day)
        df = df_day
        #print (df)
         # Converting dates column to float values
        ohlc_df = df.copy()
        ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
        fig, ax = plt.subplots(figsize=(8, 4))
        # Converts raw mdate numbers to dates
        ax.xaxis_date()
        plt.xlabel("Date")
        # Making candlestick plot
        candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
        plt.title(market)
        plt.plot(ohlc_df['Date'], ohlc_df['Close'], linestyle = '--', linewidth = 1, c='black')
        plt.gcf().autofmt_xdate()   # Beautify the x-labels
        plt.autoscale(tight=True)
        plt.grid()
        ax.grid(True)
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/chart.png')
        plt.clf()
        plt.cla()
        plt.close()
        newfilename=("{}_chart.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/chart.png"
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)
        print (new_name)
        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator/"
        for pngfile in glob.iglob(os.path.join(src_dir, "*_chart.png")):
          shutil.copy(pngfile, dst_dir)


def profit_chart():
    print ("Starting profit chart module")
    engine = create_engine('mysql+pymysql://cryptouser:123456@database-service:3306/cryptodb_simulator')
    df = pd.read_sql_query('SELECT serf FROM statistics', engine)
    df.to_csv('data/out.csv', header=None, sep=' ')
    #print (df)
    days, summ = np.loadtxt("data/out.csv", unpack=True)
    x=days
    y=summ
    plt.plot(x, y, c='r')
    plt.title("Cryptobot chart")
    plt.ylabel("%")
    plt.xlabel("Trades")
    plt.grid(True)
    plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/symulator_crypto_results.png', bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()


def dashboard(market, row):
    print ("Starting dashboard module")
    now = str(row['T'])
    currenttime = now[:-9]
    #print (currenttime)
    #print (date_exist(market, currenttime))
    #print (market, currenttime)
    if date_exist(market, currenttime) != 1:
        try:
                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                cursor = db.cursor()
                cursor.execute('insert into history(date, market) values(%s, %s)', (currenttime, market))
                db.commit()
        except pymysql.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)
        finally:
                db.close()
    else:
        pass


def aftercount(market, row):
        print ("Starting aftercount module")
        last = float(row['Last'])
        now = str(row['T'])
        currentdate = now[:-9] 	
        iso_8601= now	
        currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
        currenttime = now[:-3]
        #Current prices
        last = float(row['C'])  #last price
        bid = last  # sell price
        ask = last  # buy price
        newbid=float("{:.3f}".format(bid - bid*0.002))
        newask=float("{:.3f}".format(ask + ask*0.002))
        bought_price_sql = float(status_orders(market, 3))
        aftercount=float(status_orders(market, 25))
        min_percent=float(status_orders(market, 24))
        aftercount_min=float(status_orders(market, 26))
        order_id = closed_orders_id(market)
        if bought_price_sql>0:
           procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))
           if order_id!=0 and currtime - close_date(market)<432000:
               try:
                  db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                  cursor = db.cursor()

                  if procent_serf>=percent_serf(market) and procent_serf>=aftercount:
                      cursor.execute(
                                "update orders set aftercount=%s where market = %s and active = 0 and order_id = %s",
                                (procent_serf, market, order_id))
                  elif procent_serf<percent_serf(market) and procent_serf<aftercount_min:
                      cursor.execute(
                                "update orders set aftercount_min=%s where market = %s and active = 0 and order_id = %s",
                                (procent_serf, market, order_id))

                  db.commit()
               except pymysql.Error as e:
                  print ("Error %d: %s" % (e.args[0], e.args[1]))
                  sys.exit(1)
               finally:
                  db.close()
           else:
               pass
        else:
            pass 		


def trend_analizer(market):
        print ("Starting trend_analizer module")
        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
        cursor = db.cursor()
        cursor.execute("SELECT price FROM history WHERE market = '%s' and price !='None' order by id desc limit 6" % market)
        price=cursor.fetchall()
        currentprice = (price[0][0])
        daybeforeprice = (price[1][0])
        twodaysbeforeprice = (price[2][0])
        threedaysbeforeprice = (price[3][0])
        fourdaysbeforeprice = (price[4][0])
        fivedaysbeforeprice = (price[5][0])
        prices= [currentprice, daybeforeprice, twodaysbeforeprice, threedaysbeforeprice, fourdaysbeforeprice, fivedaysbeforeprice]
        percent_change = float("{0:.2f}".format(currentprice/min(prices)*100-100))
        if (currentprice==max(prices) and percent_change>=4.0):
           print ("Peak " + str(percent_change))
           trend = "Peak " + str(percent_change)+" %"
        elif (currentprice>fivedaysbeforeprice and daybeforeprice==max(prices)) or (currentprice>fivedaysbeforeprice and twodaysbeforeprice==max(prices)):
           print ("Afterpeak " + str(percent_change))
           trend = "Afterpeak " + str(percent_change)+" %"
        else:
           print ("Fluctuating " + str(percent_change))
           trend = "Fluctuating " + str(percent_change)+" %"

        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute("update markets set trend='%s'  where market='%s'" % (trend, market))		  
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()


def enable_market(market, row, df_hour, df_day):
    print ("Starting enable market module")
    max_markets = parameters()[6]
    last = float(row['Last'])
    #day_close = float(row['PrevDay'])	
    percent_chg = float(row['PrevDay'])
    now = str(row['T'])
    currentdate = now[:-9] 	
    iso_8601= now	
    currtime = epoch_seconds_from_iso_8601_with_tz_offset(iso_8601)
    currenttime = now[:-3]
    bid = float(row['Bid'])  # sell price
    ask = float(row['Ask'])  # buy price
    newbid=float("{:.3f}".format(bid - bid*0.002))
    newask=float("{:.3f}".format(ask + ask*0.002))	
    bought_quantity_sql = float(status_orders(market, 2))
    #percent_chg = float(((last / day_close) - 1) * 100)
    percent_sql = float(heikin_ashi(market, 21))
    HAD_trend = heikin_ashi(market, 18)
    ha_time_second = heikin_ashi(market, 23)
    spread = float(((ask / bid) - 1) * 100)	
    volume = (row['V'])	

	
    try:
        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
        cursor = db.cursor()
        cursor.execute("update markets set spread= %s where market =%s", (spread, market))
        db.commit()
    except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        db.close()                

    if percent_chg>percent_sql:
        percent_grow=1
    elif percent_chg<percent_sql:
        percent_grow=-1
    else:
        percent_grow=0
    #print (market, percent_grow)

    if spread>0.5 and bought_quantity_sql>0.0 and percent_grow==-1:
        print (market, "We have open order, but we need to disable this currency")


    if spread>0.5 and percent_grow==-1 and bought_quantity_sql==0.0:
            print (market, "We are disabling this currency")
            try:
                printed = ('    We are disabling this currency  ' + market)
                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                cursor = db.cursor()
                cursor.execute('update markets set active= 0 where enabled=1 and market =("%s")' % market)
                db.commit()
            except pymysql.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)
            finally:
                db.close()
    if ((HAD_trend=="DOWN" or HAD_trend=="Revers-DOWN") and currtime - ha_time_second < 3000) and bought_quantity_sql==0.0:
            print (market, "We are disabling this currency")
            try:
                printed = ('    We are disabling this currency because of HA  ' + market)
                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
                cursor = db.cursor()
                cursor.execute('update markets set active= 0 where enabled=1 and market =("%s")' % market)
                db.commit()
            except pymysql.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                sys.exit(1)
            finally:
                db.close()

    if spread<0.5 and (percent_grow==1 or percent_grow==0) and (market_count() <=max_markets) and (HAD_trend!="DOWN" and HAD_trend!="Revers-DOWN"):
        print (market, "We need to enable those currencies")
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute('update markets set active= 1 where enabled=1 and market =("%s")' % market)
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()
    #Candle analisys
    currenthour = now[:-6]
    hourlastcandle = df_hour.loc[df_hour['T'] == currenthour]
    print (hourlastcandle, currenthour)
    hourcurentopen = float(hourlastcandle['O'])	
    hourlastcandleindex = hourlastcandle.index[0]	
    hourpreviouscandle = df_hour.loc[df_hour.index[hourlastcandleindex-1]]	
    hourprevopen=float(hourpreviouscandle['O'])				
    hourprevclose=float(hourpreviouscandle['C'])	
    hourprevlow=float(hourpreviouscandle['L'])	
    hourprevhigh=float(hourpreviouscandle['H'])
    daylastcandle = df_day.loc[df_day['T'] == currentdate]
    daycurrentlow = float(daylastcandle['L'])
    daycurrenthigh = float(daylastcandle['H'])
    daycurrentopen = float(daylastcandle['O'])
    daycurrentclose = float(daylastcandle['C'])
    daylastcandleindex = daylastcandle.index[0]	
    daypreviouscandle = df_day.loc[df_day.index[daylastcandleindex-1]]	
    dayprevlow = float(daypreviouscandle['L'])
    dayprevhigh = float(daypreviouscandle['H'])
    dayprevopen = float(daypreviouscandle['O'])
    dayprevclose = float(daypreviouscandle['C'])
    day_candle = 'NONE'
    prevhour_candle='NONE'
    hourcandle_dir='NONE'
    candle_dir='NONE'
    if hourprevclose > hourprevopen:
        prevhour_candle = 'U'
    else:
        prevhour_candle = 'D'		  
		  
    if last > hourcurentopen and last > hourprevclose and prevhour_candle=='U':
        hourcandle_dir = 'U'
    else:
        hourcandle_dir = 'D'

    if last > daycurrentopen:
         day_candle = 'U'
    else:
        day_candle = 'D'
    if dayprevclose > dayprevopen:
        prevday_candle = 'U'
    else:
        prevday_candle = 'D'

    if last > daycurrentopen and last > dayprevclose: # and prevday_candle=='U':
        candle_dir = 'U'
    else:
        candle_dir = 'D'
    #print (market, hourcandle_dir, candle_dir)
    try:
        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
        cursor = db.cursor()
        cursor.execute(
                        "update markets set percent_chg= %s, volume=%s, candle_direction=%s, hour_candle_direction=%s, daycurrentopen=%s, hourcurrentopen=%s where enabled=1 and market = %s",
                        (percent_chg, volume, candle_dir, hourcandle_dir, daycurrentopen, hourcurentopen, market))
        cursor.execute("update history set day_direction= %s where market=%s and date=%s", (candle_dir, market, currentdate))
        db.commit()
    except pymysql.Error as e:
        print ("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        db.close()


def tweeter_charts_img(market, df_tw, row):
        print ("Starting tweeter chart module")
        now = str(row['T'])
        currentdate = now[:-9] 
        currenttime = now[:-3]		
        today_tweet = df_tw.loc[df_tw['Date'] == currentdate]
        positive=float(today_tweet['Positive'])
        negative=float(today_tweet['Negative'])
        neutral= (100 - negative - positive)
        labels = 'Neutral', 'Negative', 'Positive' 
        printed = (market, "Positive tweets percentage: {} %".format(positive), "Negative tweets percentage: {} %".format(negative))
        #print (neutral, negative, positive)
        try:
            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
            cursor = db.cursor()
            cursor.execute('update markets set positive_sentiments = %s, negative_sentiments =%s where market=%s',(positive, negative,  market))
            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
            cursor.execute("update history set positive_tweets = %s, negative_tweets =%s  where market='%s' and date='%s'" % (positive, negative, market, currentdate))
            db.commit()
        except pymysql.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            db.close()
        sizes = (neutral, negative, positive)
        colors = ["#1f77b4",  "#fe2d00", "#2ca02c"]				
        explode = (0, 0.1, 0)  
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.grid()
        plt.title(market, bbox={'facecolor':'0.8', 'pad':5}, fontsize=18)
        #plt.show()
        plt.savefig('/root/PycharmProjects/cryptobot/images/symulator/temp/tweets.png', bbox_inches = 'tight', pad_inches = 0)
        plt.clf()
        plt.cla()
        plt.close()
        newfilename=("{}_tweets.png".format(market))
        my_path = "/root/PycharmProjects/cryptobot/images/symulator/temp/tweets.png"
        new_name = os.path.join(os.path.dirname(my_path), newfilename)
        os.rename(my_path, new_name)
        print (new_name)
        src_dir = "/root/PycharmProjects/cryptobot/images/symulator/temp/"
        dst_dir = "/root/PycharmProjects/cryptobot/images/symulator/"
        for pngfile in glob.iglob(os.path.join(src_dir, "*_tweets.png")):
            shutil.copy(pngfile, dst_dir)









def current_ai_direction(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT ai_direction FROM markets where market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0


def current_ai_time(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT ai_time FROM markets where market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0
	

def market_count():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM markets where enabled=1 and active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0

def previous_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT percent_serf FROM `orders` WHERE  market = '%s' and active=0 ORDER BY order_id DESC LIMIT 1" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0

def previous_order(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT sell_time FROM `orders` WHERE  market = '%s' and active=0 ORDER BY order_id DESC LIMIT 1" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0

def hist_price(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT price FROM history WHERE market = '%s' order by date desc limit 5" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

def close_date(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[0])
    return 0

def closed_orders_id(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT order_id FROM orders where active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0

def date_exist(marketname, currenttime):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM history WHERE market = '%s' and date='%s'" % (market, currenttime))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return 1

        else:
            return 0

def candle_score(lst_0,lst_1,lst_2,lst_3):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]  #current
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]  #previous
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]  #previous2
    O_3,H_3,L_3,C_3=lst_3[0],lst_3[1],lst_3[2],lst_3[3]  #previous3
    
    DojiSize = 0.1

# UP trend: (C_2>C_3)
# Green candles before: (C_3 > O_3) & (C_2 > O_2)
#DOWN trend: (C_2<C_3)
# Red candles before: (C_3 < O_3) & (C_2 < O_2)
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)	
    Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
	
    Inverted_Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    Inverted_Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6))    
    
    Bullish_Reversal = (O_2 > C_2)&(O_1 > C_1)&doji
    Bearish_Reversal = (O_2 < C_2)&(O_1 < C_1)&doji
    
    Evening_Star= (C_3 > O_3) & (C_2 > O_2) & (C_1 < O_1) & (O_1 > C_2) & (O_0 <O_1) & (C_0 < O_0 ) & ((C_2-O_2)>(O_1-C_1)) & ((O_0-C_0)>(O_1-C_1))

    Morning_Star= (C_3 < O_3) & (C_2 < O_2) & (C_1 > O_1) & (O_1 < C_2) & (O_0 > O_1) & (C_0 > O_0 )	 & ((O_2- C_2)>(C_1 - O_1)) & ((C_0-O_0)>(C_1-O_1))
	

    Shooting_Star_Bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer
    
    Shooting_Star_Bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer	
    
    Bearish_Harami =  (O_2 < C_2)&  (C_2<C_1)&  (C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 < C_0) & ((O_0 - C_0) < (C_1 - O_1)) & ((C_1 - O_1)/(O_0 - C_0)>=2)
	
    Bullish_Harami =  (C_2 < O_2)&  (C_1<C_2)&  (O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 < O_0) & ((C_0 - O_0) < (O_1 - C_1)) & ((O_1 - C_1)/(C_0 - O_0)>=2)	
	
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 > C_1) & (O_1 > C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))  & (C_2 > O_2)
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 > O_1) & (C_1 > O_0) & ((C_0 - O_0) > (O_1 - C_1 ))  & (C_2 < O_2)	
	
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)
	
    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer
	
    Tweezer_Top = (C_3 > O_3) & (C_2 > O_2) & (C_1>O_1) & (C_0<O_0) & (C_1==O_0)
	
    Tweezer_Bottom=(C_3 < O_3) & (C_2 < O_2) & (C_1<O_1) & (C_0>O_0) & (O_1==C_0)

    Two_black_gapping = (C_3 > O_3) & (C_2 > O_2) & (C_1<O_1) & (C_0<O_0) & (L_1>H_0)	

    Three_white_soldiers=(C_3 < O_3) & (C_2 > O_2) & (C_1 > O_1) & (C_0 > O_0)  & (O_0>O_1) &(O_1>O_2) & (L_3<L_2)

    Three_black_crows=(C_3 > O_3) & (C_2 < O_2) & (C_1 < O_1) & (C_0 < O_0)	& (O_0<O_1) &(O_1<O_2) & (L_3>L_2)

    strCandle=''
    candle_score=0
    
#    if doji:
#        strCandle='doji'
    if    Three_black_crows:
        strCandle=strCandle+'/ '+'T_b_c-v'
        candle_score=candle_score-1	
    if    Three_white_soldiers:
        strCandle=strCandle+'/ '+'T_w_s-^'
        candle_score=candle_score+1			
    if    Two_black_gapping:
        strCandle=strCandle+'/ '+'T_b_g-v'
        candle_score=candle_score-1		
    if    Tweezer_Top:
        strCandle=strCandle+'/ '+'T_t-v'
        candle_score=candle_score-1
    if    Tweezer_Bottom:
        strCandle=strCandle+'/ '+'T_b-^'
        candle_score=candle_score+1		
    if    Evening_Star:
        strCandle=strCandle+'/ '+'E_S-v'
        candle_score=candle_score-1	
    if    Morning_Star:
        strCandle=strCandle+'/ '+'M_S-^'
        candle_score=candle_score+1		
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'BU_HR-^'
        candle_score=candle_score+1
    if    Bearish_Harami:
        strCandle=strCandle+'/ '+'BE_HR-v'
        candle_score=candle_score-1	
    if    Bullish_Reversal:
        strCandle=strCandle+'/ '+'BU_R-^'
        candle_score=candle_score+1
    if    Bearish_Reversal:
        strCandle=strCandle+'/ '+'BE_R-v'
        candle_score=candle_score-1		
#    if    Hammer:
#        strCandle=strCandle+'/ '+'H'
#    if    Inverted_Hammer:
#        strCandle=strCandle+'/ '+'I_H'
    if Shooting_Star_Bearish:
        strCandle=strCandle+'/ '+'SS_BE-v'
        candle_score=candle_score-1
    if Shooting_Star_Bullish:
        strCandle=strCandle+'/ '+'SS_BU-v'
        candle_score=candle_score-1		
    if    Bearish_Engulfing:
        strCandle=strCandle+'/ '+'Be_E-v'
        candle_score=candle_score-1
    if    Bullish_Engulfing:
        strCandle=strCandle+'/ '+'Bu_E-^'
        candle_score=candle_score+1
    if    Piercing_Line_bullish:
        strCandle=strCandle+'/ '+'P_L-^'
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle=strCandle+'/ '+'H_M_Be-v'
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle=strCandle+'/ '+'H_M_Bu-^'
        candle_score=candle_score+1



		
        
    #return candle_score
    return candle_score,strCandle

def candle_df(df):

    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=''


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_3=[df_candle['Open'].iloc[c-3],df_candle['High'].iloc[c-3],df_candle['Low'].iloc[c-3],df_candle['Close'].iloc[c-3]]
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2,lst_3)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    #df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
    return df_candle			

def implement_macd_strategy(prices, data):    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal

def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df

def on_balance_volume(data, close_col='close', vol_col='volume', trend_periods=21):
    
    data_tmp = data.copy()
    counter = 0
  
    for index, row in data_tmp.iterrows():
        if counter > 0:
            last_obv = data_tmp.at[index - 1, 'obv']
            if row[close_col] > data_tmp.at[index - 1, close_col]:
                current_obv = last_obv + row[vol_col]
            elif row[close_col] < data_tmp.at[index - 1, close_col]:
                current_obv = last_obv - row[vol_col]
            else:
                current_obv = last_obv
        else:
            last_obv = 0
            current_obv = row[vol_col]
        counter += 1
       
        data_tmp.set_value(index, 'obv', current_obv)
    data_tmp['obv_ema' + str(trend_periods)] = data_tmp['obv'].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()
    
    return data_tmp

def implement_obv_strategy(prices, data):    
    buy_price = []
    sell_price = []
    obv_signal = []
    signal = 0

    for i in range(len(data)):
        if data['obv'][i] > data['obv_ema21'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                obv_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                obv_signal.append(0)
        elif data['obv'][i] < data['obv_ema21'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                obv_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                obv_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            obv_signal.append(0)
            
    return buy_price, sell_price, obv_signal

def get_obv(data):    
    data_tmp = data.copy()
    data_tmp['hist'] = data_tmp['obv'] - data_tmp['obv_ema21'] 
    return data_tmp

def heikin_ashi_func(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close'])
    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2      
    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)
    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
    
    return heikin_ashi_df

def order_count():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0

def percent_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

def percent_serf_max(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_max FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

def percent_serf_min(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_min FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

def timestamp_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[6])

    return 0

def active_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[4])

    return 0

def status_orders(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0

def iteration_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[7])

    return 0
	
def epoch_seconds_from_iso_8601_with_tz_offset(iso_8601):
    """ Convert ISO 8601 with a timezone offset to unix timestamp """
    iso_8601_dt = dt.datetime.strptime(iso_8601, '%Y-%m-%d %H:%M:%S')
    utc_at_epoch = dt.datetime(1970, 1, 1)
    epoch_without_tz_offset = int((iso_8601_dt - utc_at_epoch).total_seconds())
    return epoch_without_tz_offset

def parameters():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24]), (row[25]), (row[26]), (row[27]), (row[28]), (row[29]), (row[30]), (row[31]), (row[32])

    return 0

def macd_fluctuation(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT GROUP_CONCAT(macd_signal) FROM `history` WHERE market='%s' order by id desc" % market)
    res = cursor.fetchall()
    for row in res:
       r = list(row[0].split(","))
       r = r[-3:]
       return (r)
    return 0

def obv_fluctuation(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT GROUP_CONCAT(obv_signal) FROM `history` WHERE market='%s' order by id desc" % market)
    res = cursor.fetchall()
    for row in res:
       r = list(row[0].split(","))
       r = r[-3:]
       return (r)
    return 0

def market_values(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False

def heikin_ashi(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False

def summ_serf():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    # market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0")
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float("{0:.2f}".format(row[0]))
            # return 0
        else:
            return 0


	
def format_float(f):
    return "%.4f" % f

if __name__ == "__main__":
    main()
