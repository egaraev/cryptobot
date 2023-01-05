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
import yfinance as yf
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *



###
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE  enabled=1")
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
          crypto=market[4:]
          stock = yf.Ticker(crypto)
          hist = stock.history(period="{}d".format(days))
          df = pd.DataFrame(hist)
          df = df.reset_index(level=['Date'])    
          print (df)		  

          ohlc_df = df.copy()
          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
          #print (ohlc_df)


         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)

          fig, ax = plt.subplots(figsize=(8, 4))
          # Converts raw mdate numbers to dates
          ax.xaxis_date()
          plt.xlabel("Date")

		  
		  
          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          #plt.ylabel("Price")
          plt.title(market)
          plt.plot(ohlc_df['Date'], ohlc_df['Close'], linestyle = '--', linewidth = 1, c='black')
          plt.gcf().autofmt_xdate()   # Beautify the x-labels
          plt.autoscale(tight=True)
          plt.grid()
          ax.grid(True)
          plt.savefig('/root/PycharmProjects/cryptobot/images/temp/chart.png')
          plt.clf()
          plt.cla()
          plt.close()
          newfilename=("{}_chart.png".format(market))
          my_path = "/root/PycharmProjects/cryptobot/images/temp/chart.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/cryptobot/images/temp/"
          dst_dir = "/root/PycharmProjects/cryptobot/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*_chart.png")):
            shutil.copy(pngfile, dst_dir)

        except:
            continue



# def get_candles(market, tick_interval):
    # url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    # r = requests.get(url)
    # requests.session().close()
    # return r.json()

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
