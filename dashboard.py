import pymysql
import pandas as pd
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d")
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE enabled=1")
markets=cursor.fetchall()


def main():
    print('Starting dashboard  module')


    SL()


def SL():
    for market in markets: #Loop trough the stock summary
        try:
          market=(market[0])
          print (date_exist(market, currenttime))
#          print (market, currenttime)
          if date_exist(market, currenttime) != 1:
             try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
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

          	  
			  

        except:
            continue


			
			
			
			
			
def date_exist(marketname, currenttime):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM history WHERE market = '%s' and date='%s'" % (market, currenttime))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return 1

        else:
            return 0


if __name__ == "__main__":
    main()
