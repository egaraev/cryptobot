from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import time 
from datetime import timedelta, date
import os, sys
import pandas as pd
import numpy as np
from math import floor
import pymysql
import matplotlib.pyplot as plt
currtime = int(round(time.time()))
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE  enabled=1")
markets=cursor.fetchall()

def main():
    print('Starting volume module')

    kov_analyze()
	
	


def kov_analyze():
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    currentdate = now.strftime("%Y-%m-%d")
    for market in markets: #Loop through the crypto summary
        try:
           market=(market[0])
           crypto=market[4:]
           market1 = crypto+"-USD"
           btc = yf.Ticker(market1)
           hist = btc.history(period="300d")
           print (hist)


        except:
            pass
    	






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