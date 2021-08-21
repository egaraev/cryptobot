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
# import config
# c1 = Client(api_key=config.key, api_secret=config.secret)
c = Client(api_key='', api_secret='')
currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
days=15
dayid=days-1



def main():
    print('Starting heikin ashi day module')

    HA()



def HA():

    market_summ = c.get_market_summaries().json()['result']
    #print (market_summ)
    

    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                print (market)

                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price
                ask = float(summary['Ask'])  # buy price
                #print (market, last)

				
#######################
                hourlatcandle= get_candles(market, 'hour')['result'][-1:]
                hourcurentopen=float(hourlatcandle[0]['O'])	
                hourcurentclose=float(hourlatcandle[0]['C'])	
                hourcurentlow=float(hourlatcandle[0]['L'])	
                hourcurenthigh=float(hourlatcandle[0]['H'])
                hourpreviouscandle = get_candles(market, 'hour')['result'][-2:]				
                hourprevopen=(hourpreviouscandle[0]['O'])	
                hourprevclose=float(hourpreviouscandle[0]['C'])	
                hourprevlow=float(hourpreviouscandle[0]['L'])	
                hourprevhigh=float(hourpreviouscandle[0]['H'])
                
                #print (market, hourcurentopen)

                daylastcandle = get_candles(market, 'day')['result'][-1:]
                daycurrentdate = (daylastcandle[0]['T'])
                split_string = daycurrentdate.split("T", 1)
                daycurrentdate = split_string[0]
                daycurrentdate = datetime.date(*(int(s) for s in daycurrentdate.split('-')))
                daycurrentlow = float(daylastcandle[0]['L'])
                daycurrenthigh = float(daylastcandle[0]['H'])
                daycurrentopen = float(daylastcandle[0]['O'])
                daycurrentclose = float(daylastcandle[0]['C'])
                daypreviouscandle = get_candles(market, 'day')['result'][-2:]
                dayprevdate = (daypreviouscandle[0]['T'])
                split_string = dayprevdate.split("T", 1)
                dayprevdate = split_string[0]
                dayprevdate = datetime.date(*(int(s) for s in dayprevdate.split('-')))
                dayprevlow = float(daypreviouscandle[0]['L'])
                dayprevhigh = float(daypreviouscandle[0]['H'])
                dayprevopen = float(daypreviouscandle[0]['O'])
                dayprevclose = float(daypreviouscandle[0]['C'])
                daypreviouscandle2 = get_candles(market, 'day')['result'][-3:]
                dayprevdate2 = (daypreviouscandle2[0]['T'])
                split_string = dayprevdate2.split("T", 1)
                dayprevdate2 = split_string[0]
                dayprevdate2 = datetime.date(*(int(s) for s in dayprevdate2.split('-')))
                dayprevlow2 = float(daypreviouscandle2[0]['L'])
                dayprevhigh2 = float(daypreviouscandle2[0]['H'])
                dayprevopen2 = float(daypreviouscandle2[0]['O'])
                dayprevclose2 = float(daypreviouscandle2[0]['C'])
                daypreviouscandle3 = get_candles(market, 'day')['result'][-4:]
                dayprevdate3 = (daypreviouscandle3[0]['T'])
                split_string = dayprevdate3.split("T", 1)
                dayprevdate3 = split_string[0]
                dayprevdate3 = datetime.date(*(int(s) for s in dayprevdate3.split('-')))
                dayprevlow3 = float(daypreviouscandle3[0]['L'])
                dayprevhigh3 = float(daypreviouscandle3[0]['H'])
                dayprevopen3 = float(daypreviouscandle3[0]['O'])
                dayprevclose3 = float(daypreviouscandle3[0]['C'])				
                daypreviouscandle4 = get_candles(market, 'day')['result'][-5:]
                dayprevdate4 = (daypreviouscandle4[0]['T'])
                split_string = dayprevdate4.split("T", 1)
                dayprevdate4 = split_string[0]
                dayprevdate4 = datetime.date(*(int(s) for s in dayprevdate4.split('-')))
                dayprevlow4 = float(daypreviouscandle4[0]['L'])
                dayprevhigh4 = float(daypreviouscandle4[0]['H'])
                dayprevopen4 = float(daypreviouscandle4[0]['O'])
                dayprevclose4 = float(daypreviouscandle4[0]['C'])				
                daypreviouscandle5 = get_candles(market, 'day')['result'][-6:]
                dayprevdate5 = (daypreviouscandle5[0]['T'])
                split_string = dayprevdate5.split("T", 1)
                dayprevdate5 = split_string[0]
                dayprevdate5 = datetime.date(*(int(s) for s in dayprevdate5.split('-')))
                dayprevlow5 = float(daypreviouscandle5[0]['L'])
                dayprevhigh5 = float(daypreviouscandle5[0]['H'])
                dayprevopen5 = float(daypreviouscandle5[0]['O'])
                dayprevclose5 = float(daypreviouscandle5[0]['C'])				
                daypreviouscandle6 = get_candles(market, 'day')['result'][-7:]
                dayprevdate6 = (daypreviouscandle6[0]['T'])
                split_string = dayprevdate6.split("T", 1)
                dayprevdate6 = split_string[0]
                dayprevdate6 = datetime.date(*(int(s) for s in dayprevdate6.split('-')))
                dayprevlow6 = float(daypreviouscandle6[0]['L'])
                dayprevhigh6 = float(daypreviouscandle6[0]['H'])
                dayprevopen6 = float(daypreviouscandle6[0]['O'])
                dayprevclose6 = float(daypreviouscandle6[0]['C'])				
                daypreviouscandle7 = get_candles(market, 'day')['result'][-8:]
                dayprevdate7 = (daypreviouscandle7[0]['T'])
                split_string = dayprevdate7.split("T", 1)
                dayprevdate7 = split_string[0]
                dayprevdate7 = datetime.date(*(int(s) for s in dayprevdate7.split('-')))
                dayprevlow7 = float(daypreviouscandle7[0]['L'])
                dayprevhigh7 = float(daypreviouscandle7[0]['H'])
                dayprevopen7 = float(daypreviouscandle7[0]['O'])
                dayprevclose7 = float(daypreviouscandle7[0]['C'])				
                daypreviouscandle8 = get_candles(market, 'day')['result'][-9:]
                dayprevdate8 = (daypreviouscandle8[0]['T'])
                split_string = dayprevdate8.split("T", 1)
                dayprevdate8 = split_string[0]
                dayprevdate8 = datetime.date(*(int(s) for s in dayprevdate8.split('-')))
                dayprevlow8 = float(daypreviouscandle8[0]['L'])
                dayprevhigh8 = float(daypreviouscandle8[0]['H'])
                dayprevopen8 = float(daypreviouscandle8[0]['O'])
                dayprevclose8 = float(daypreviouscandle8[0]['C'])					
                daypreviouscandle9 = get_candles(market, 'day')['result'][-10:]
                dayprevdate9 = (daypreviouscandle9[0]['T'])
                split_string = dayprevdate9.split("T", 1)
                dayprevdate9 = split_string[0]
                dayprevdate9 = datetime.date(*(int(s) for s in dayprevdate9.split('-')))
                dayprevlow9 = float(daypreviouscandle9[0]['L'])
                dayprevhigh9 = float(daypreviouscandle9[0]['H'])
                dayprevopen9 = float(daypreviouscandle9[0]['O'])
                dayprevclose9 = float(daypreviouscandle9[0]['C'])				
                daypreviouscandle10 = get_candles(market, 'day')['result'][-11:]
                dayprevdate10 = (daypreviouscandle10[0]['T'])
                split_string = dayprevdate10.split("T", 1)
                dayprevdate10 = split_string[0]
                dayprevdate10 = datetime.date(*(int(s) for s in dayprevdate10.split('-')))
                dayprevlow10 = float(daypreviouscandle10[0]['L'])
                dayprevhigh10 = float(daypreviouscandle10[0]['H'])
                dayprevopen10 = float(daypreviouscandle10[0]['O'])
                dayprevclose10 = float(daypreviouscandle10[0]['C'])				
                daypreviouscandle11 = get_candles(market, 'day')['result'][-12:]
                dayprevdate11 = (daypreviouscandle11[0]['T'])
                split_string = dayprevdate11.split("T", 1)
                dayprevdate11 = split_string[0]
                dayprevdate11 = datetime.date(*(int(s) for s in dayprevdate11.split('-')))
                dayprevlow11 = float(daypreviouscandle11[0]['L'])
                dayprevhigh11 = float(daypreviouscandle11[0]['H'])
                dayprevopen11 = float(daypreviouscandle11[0]['O'])
                dayprevclose11 = float(daypreviouscandle11[0]['C'])				
                daypreviouscandle12 = get_candles(market, 'day')['result'][-13:]
                dayprevdate12 = (daypreviouscandle12[0]['T'])
                split_string = dayprevdate12.split("T", 1)
                dayprevdate12 = split_string[0]
                dayprevdate12 = datetime.date(*(int(s) for s in dayprevdate12.split('-')))
                dayprevlow12 = float(daypreviouscandle12[0]['L'])
                dayprevhigh12 = float(daypreviouscandle12[0]['H'])
                dayprevopen12 = float(daypreviouscandle12[0]['O'])
                dayprevclose12 = float(daypreviouscandle12[0]['C'])				
                daypreviouscandle13 = get_candles(market, 'day')['result'][-14:]
                dayprevdate13 = (daypreviouscandle13[0]['T'])
                split_string = dayprevdate13.split("T", 1)
                dayprevdate13 = split_string[0]
                dayprevdate13 = datetime.date(*(int(s) for s in dayprevdate13.split('-')))
                dayprevlow13 = float(daypreviouscandle13[0]['L'])
                dayprevhigh13 = float(daypreviouscandle13[0]['H'])
                dayprevopen13 = float(daypreviouscandle13[0]['O'])
                dayprevclose13 = float(daypreviouscandle13[0]['C'])				
                daypreviouscandle14 = get_candles(market, 'day')['result'][-15:]
                dayprevdate14 = (daypreviouscandle14[0]['T'])
                split_string = dayprevdate14.split("T", 1)
                dayprevdate14 = split_string[0]
                dayprevdate14 = datetime.date(*(int(s) for s in dayprevdate14.split('-')))
                dayprevlow14 = float(daypreviouscandle14[0]['L'])
                dayprevhigh14 = float(daypreviouscandle14[0]['H'])
                dayprevopen14 = float(daypreviouscandle14[0]['O'])
                dayprevclose14 = float(daypreviouscandle14[0]['C'])				

				
				
                data = [[dayprevdate14, dayprevopen14, dayprevhigh14, dayprevlow14, dayprevclose14], [dayprevdate13, dayprevopen13, dayprevhigh13, dayprevlow13, dayprevclose13], [dayprevdate12, dayprevopen12, dayprevhigh12, dayprevlow12, dayprevclose12], [dayprevdate11, dayprevopen11, dayprevhigh11, dayprevlow11, dayprevclose11], [dayprevdate10, dayprevopen10, dayprevhigh10, dayprevlow10, dayprevclose10], [dayprevdate9, dayprevopen9, dayprevhigh9, dayprevlow9, dayprevclose9], [dayprevdate8, dayprevopen8, dayprevhigh8, dayprevlow8, dayprevclose8], [dayprevdate7, dayprevopen7, dayprevhigh7, dayprevlow7, dayprevclose7], [dayprevdate6, dayprevopen6, dayprevhigh6, dayprevlow6, dayprevclose6], [dayprevdate5, dayprevopen5, dayprevhigh5, dayprevlow5, dayprevclose5], [dayprevdate4, dayprevopen4, dayprevhigh4, dayprevlow4, dayprevclose4], [dayprevdate3, dayprevopen3, dayprevhigh3, dayprevlow3, dayprevclose3], [dayprevdate2, dayprevopen2, dayprevhigh2, dayprevlow2, dayprevclose2], [dayprevdate, dayprevopen, dayprevhigh, dayprevlow, dayprevclose], [daycurrentdate, daycurrentopen, daycurrenthigh, daycurrentlow, daycurrentclose]]
                df = pd.DataFrame(list(data), columns=['Date', 'Open', 'High', 'Low', 'Close'])
                
                #print (df)
				

				
                heikin_ashi_df = heikin_ashi_func(df)

                

                day_candle = 'NONE'
                prevday_candle = 'NONE'
                prevday2_candle = 'NONE'

                prevhour_candle='NONE'
                hourcandle_dir='NONE'

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

                if dayprevclose2 > dayprevopen2:
                   prevday2_candle = 'U'
                else:
                   prevday2_candle = 'D'

                if last > daycurrentopen and last > dayprevclose and prevday_candle=='U':
                   candle_dir = 'U'
                else:
                   candle_dir = 'D'
				
				
				
####
                ohlc_df = heikin_ashi_df.copy()
                date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]
                ohlc_df['Date']=date
                ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
                

                ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
                #print (ohlc_df.info())
                #print(ohlc_df)   
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.xaxis_date()

                candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)

                plt.title(market)

                plt.gcf().autofmt_xdate()
                plt.autoscale(tight=True)  				
                plt.grid()
                ax.grid(True)
                plt.savefig('/root/PycharmProjects/cryptobot/images/hacharts.png')				
                newfilename=("{}_hachart.png".format(market))
                my_path = "/root/PycharmProjects/cryptobot/images/hacharts.png"		
                new_name = os.path.join(os.path.dirname(my_path), newfilename)
                os.rename(my_path, new_name)
                print (new_name)



				
				
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
                    cursor.execute("update markets set current_price = %s, ha_direction_daily=%s, had_candle_previous=%s, had_candle_current=%s, candle_direction=%s, hour_candle_direction=%s  where market = %s",(last,  HAD_trend, HaD_previous_candle, HaD_current_candle, candle_dir, hourcandle_dir,  market))
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


def available_market_list(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM `markets` where  enabled=1 and market = '%s'" % market)

    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


def get_candles(market, tick_interval):
    url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    r = requests.get(url)
    requests.session().close()
    return r.json()







if __name__ == "__main__":
    main()
