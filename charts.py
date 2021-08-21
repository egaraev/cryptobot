import time
import config
from pybittrex.client import Client
import pymysql
import requests
import hashlib
import hmac
import matplotlib as mpl
import matplotlib.pyplot as plt
import io, base64, os, json, re, sys 
import glob
import shutil
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from datetime import timedelta, date
currtime = int(round(time.time()))
c=Client(api_key='', api_secret='')




###
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE active=1 and enabled=1")
markets=cursor.fetchall()
days=15

def main():
    print('Starting cryto-charts module')

    prices()




def prices():
    for market in markets: #Loop trough the crypto summary
        try:
          market=(market[0])
          name=market_full_name(market, 73)
          print (market)

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
  
          ohlc_df = df.copy()
          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
          print (ohlc_df)


         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)

          fig, ax = plt.subplots(figsize=(8, 4))
          # Converts raw mdate numbers to dates
          ax.xaxis_date()
          plt.xlabel("Date")

		  
		  
          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          plt.ylabel("Price")
          plt.title(market)
          plt.plot(ohlc_df['Date'], ohlc_df['Close'], linestyle = '--', linewidth = 1, c='black')
          plt.gcf().autofmt_xdate()   # Beautify the x-labels
          plt.autoscale(tight=True)
          ax.grid(True)
          plt.grid()
          plt.savefig('/root/PycharmProjects/cryptobot/images/charts.png')
		  
          newfilename=("{}_chart.png".format(market))
          my_path = "/root/PycharmProjects/cryptobot/images/charts.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/cryptobot/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)



        except:
            continue



def get_candles(market, tick_interval):
    url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    r = requests.get(url)
    requests.session().close()
    return r.json()

def market_full_name(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False



if __name__ == "__main__":
    main()
