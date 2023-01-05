import time
from pybittrex.client import Client
import pymysql
import requests
import hashlib
import hmac
import numpy
import datetime
from datetime import date
import pandas as pd
import sys
import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import shutil
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import json
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
import config
from bittrex_api import Bittrex
bittrex = Bittrex(
    api_key=config.key,              # YOUR API KEY
    secret_key=config.secret,           # YOUR API SECRET
    max_request_try_count=3, # Max tries for a request to succeed
    sleep_time=2,            # sleep seconds between failed requests
    debug_level=3
)
c = bittrex.v3
currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
days=15
dayid=days-1
import yfinance as yf
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
import pandas as pd


def main():
    print('Starting heikin ashi day module')

    HA()



def HA():

    market_summ = c.get_market_summaries()
    #print (market_summ)
    tickers = c.get_tickers()

    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['symbol']):
                market = summary['symbol']
                stock = yf.Ticker(market)
                hist = stock.history(period="{}d".format(days))
                df = pd.DataFrame(hist)
                df = df.reset_index(level=['Date'])
                #print (df)
                #pd.set_option('display.float_format', lambda x: '%0.2f' % x)
                #print (df)
                # Current prices
                last = float([tick['lastTradeRate'] for tick in tickers if tick['symbol']==market][0]) #last price
                bid = float([tick['bidRate'] for tick in tickers if tick['symbol']==market][0])   #sell price
                ask = float([tick['askRate'] for tick in tickers if tick['symbol']==market][0])	#buy price	
                #print (market, last)

				

				
                daycurrentdate = (df['Date'][14]).date()
                dayprevdate = (df['Date'][13]).date()
                dayprevdate2 = (df['Date'][12]).date()
                dayprevdate3 = (df['Date'][11]).date()
                dayprevdate4 = (df['Date'][10]).date()
                dayprevdate5 = (df['Date'][9]).date()
                dayprevdate6 = (df['Date'][8]).date()
                dayprevdate7 = (df['Date'][7]).date()          
                dayprevdate8 = (df['Date'][6]).date()
                dayprevdate9 = (df['Date'][5]).date()
                dayprevdate10 = (df['Date'][4]).date()
                dayprevdate11 = (df['Date'][3]).date()
                dayprevdate12 = (df['Date'][2]).date()          
                dayprevdate13 = (df['Date'][1]).date()
                dayprevdate14 = (df['Date'][0]).date()

                heikin_ashi_df = heikin_ashi_func(df)
      
                

				
				
				
####
                ohlc_df = heikin_ashi_df.copy()
                date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]
                ohlc_df['Date']=date
                ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
                
                #print(ohlc_df)                 

                ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
                #print (ohlc_df.info())
  
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.xaxis_date()

                candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)

                plt.title(market)

                plt.gcf().autofmt_xdate()
                plt.autoscale(tight=True)  				
                plt.grid()
                ax.grid(True)
                plt.savefig('/root/PycharmProjects/cryptobot/images/temp/hachart.png')				
                newfilename=("{}_hachart.png".format(market))
                my_path = "/root/PycharmProjects/cryptobot/images/temp/hachart.png"		
                new_name = os.path.join(os.path.dirname(my_path), newfilename)
                os.rename(my_path, new_name)
                print (new_name)

                src_dir = "/root/PycharmProjects/cryptobot/images/temp/"
                dst_dir = "/root/PycharmProjects/cryptobot/images/"
                for pngfile in glob.iglob(os.path.join(src_dir, "*_hachart.png")):
                    shutil.copy(pngfile, dst_dir)

				
				
###############
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

#############
                HAD_trend = "NONE"
               # had_trend = "NONE"
#############
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

                    
                    
                    
                # if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
                    # had_trend = "DOWN"
                # if (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
                    # had_trend = "UP"
                # if ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
                    # had_trend = "Revers-UP"
                # if ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
                    # had_trend = "Revers-DOWN"
                # if  had_trend != "Revers-DOWN" and   had_trend != "Revers-UP" and  had_trend != "DOWN" and had_trend != "UP":
                    # had_trend = "STABLE"    
                    
                    
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



                #print (HaD_current_candle, HaD_previous_candle)

                    
                    

                print (market, HAD_trend)
                try:
                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set current_price = %s, ha_direction_daily=%s, had_candle_previous=%s, had_candle_current=%s  where market = %s",(last,  HAD_trend, HaD_previous_candle, HaD_current_candle,  market))
                    #cursor.execute("update markets set current_price = %s, ha_direction_daily=%s, had_candle_previous=%s, had_candle_current=%s  where market = %s",(last,  HAD_trend, HaD_previous_candle, HaD_current_candle,  market))                   
                    cursor.execute("update markets set ha_day=%s  where market = %s",(HAD_trend,  market))
                    cursor.execute("update history set price='%s' where market='%s' and date='%s'" % (last, market, currentdate))
                    db.commit()
                except pymysql.Error as e:
                    print ("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit(1)
                finally:
                    db.close()




                try:
                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set ha_day=%s, ha_time_second=%s  where market = %s",(HAD_trend, currtime, market))
                    cursor.execute("update history set ha_day='%s'  where market='%s' and date='%s'" % (HAD_trend, market, currentdate))
                    db.commit()
                except pymysql.Error as e:
                    print ("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit(1)
                finally:
                    db.close()					
					


					
            # else:
                # pass 

        except:
            continue


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


def available_market_list(symbol):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = symbol
    cursor.execute("SELECT * FROM `markets` where  enabled=1 and market = '%s'" % market)

    r = cursor.fetchall()
    for row in r:
        if row[1] == symbol:
            return True

    return False


def get_candles(market, tick_interval):
    url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    r = requests.get(url)
    requests.session().close()
    return r.json()







if __name__ == "__main__":
    main()
