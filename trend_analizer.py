# Import libraries
import time
import re
import pymysql
import pandas as pd
import sys
import os
import time
import datetime


db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE active=1 and enabled=1")
markets=cursor.fetchall()

def main():
    print('Starting trend analize  module')


    TA()

	
	
def TA():
    for market in markets: #Loop trough the stock summary
        try:
          market=(market[0])
          db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
          cursor = db.cursor()
          cursor.execute("SELECT price FROM history WHERE market = '%s' and price !='None' order by id desc limit 6" % market)
          price=cursor.fetchall()
          print (market)
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
              db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
              cursor = db.cursor()
              cursor.execute("update markets set trend='%s'  where market='%s'" % (trend, market))		  
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()



        except:
            continue


def hist_price(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT price FROM history WHERE market = '%s' order by date desc limit 5" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

if __name__ == "__main__":
    main()
