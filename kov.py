from yahoo_fin import stock_info as si
import datetime
import time 
from datetime import timedelta, date
import os, sys
import pandas as pd
import numpy as np
from math import floor
import pymysql
import matplotlib.pyplot as plt
from tti.indicators import KlingerOscillator
currtime = int(round(time.time()))
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE  enabled=1")
markets=cursor.fetchall()

def main():
    print('Starting cryto-charts module')

    kov_analyze()
	
	


def kov_analyze():
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    currentdate = now.strftime("%Y-%m-%d")
    for market in markets: #Loop trough the crypto summary
        try:
          market=(market[0])
          crypto=market[4:]
          market1 = crypto+"-USD"
          print (market)
          df = si.get_data(market1)
          df = df.iloc[: , :-1]
          df = df[-100:]
          #print (df)
          kov = KlingerOscillator(input_data=df)
          kov_signal = kov.getTiSignal()
          print (kov_signal)
          kov.getTiGraph().savefig('/root/PycharmProjects/cryptobot/images/kov_results.png')
          newfilename=("{}_kov_results.png".format(market))
          my_path = "/root/PycharmProjects/cryptobot/images/kov_results.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)
          print (new_name)
          if kov_signal == ('hold', 0):
             print ("KOV is 0, nothing to do")
          else:
             if macd_signal == ('buy', -1):
                signal = "Buy"
             else:
                signal = "Sell"
             try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute("update markets set kov_signal='%s'  where market='%s'" % (signal, market))
                 cursor.execute("update history set kov_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()
		  


        except:
            continue






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