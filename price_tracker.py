import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
import time
import math

c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')

now = datetime.datetime.now()

TICK_INTERVAL = 60  # seconds

def main():
    print('Starting price_tracking module')

    # Running clock forever
    while True:
        start = time.time()
        tick()
        end = time.time()
        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))



def tick():
    market_summ = c.get_market_summaries().json()['result']
    currtime = int(time.time())
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    #print currenttime
    #print c.get_market_summaries().json()['result']                      
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price 
                print "First 10 seconds of the minute: ", last
                time.sleep(10)
                #print currtime
		summa=float(summ_percent(market))
		#print summa
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set tenseconds= %s, twentyseconds= %s, thirtyseconds= %s, fourtyseconds= %s, fiftyseconds= %s, sixtyseconds= %s, grow_fivemins= %s   where market = %s",
                        (0,0,0,0,0,0,summa, market))
                    cursor.execute(
                        "update markets set tenseconds= %s  where market = %s",
                        (last, market))
                    cursor.execute('insert into prices(market, start_price, time, date) values("%s", "%s", "%s", "%s")' % (market, last, currtime, currenttime))
                                    
                    
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                
        except:
            continue   
    
    for summary in market_summ: #Loop trough the market summary
        try:    
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price
                print "First 20 seconds of the minute: ", last
                time.sleep(10)
                #print currtime
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set twentyseconds= %s  where market = %s",
                        (last, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                    
        except:
            continue
            
            
            
    for summary in market_summ: #Loop trough the market summary
        try:                   
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price  
                print "First 30 seconds of the minute: ", last
                time.sleep(10)
                #print currtime
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set thirtyseconds= %s  where market = %s",
                        (last, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                
        except:
            continue               
                
                
    for summary in market_summ: #Loop trough the market summary
        try:                  
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price  
                print "First 40 seconds of the minute: ", last
                time.sleep(10)
                #print currtime
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set fourtyseconds= %s  where market = %s",
                        (last, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
        except:
            continue 
            
    for summary in market_summ: #Loop trough the market summary
        try:                
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price  
                print "First 50 seconds of the minute: ", last
                time.sleep(10)
                #print currtime
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set fiftyseconds= %s  where market = %s",
                        (last, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

        except:
            continue
            

    for summary in market_summ: #Loop trough the market summary
        try:    
            if available_market_list(summary['MarketName']):
                market_summ = c.get_market_summaries().json()['result']
                market = summary['MarketName']
                last = float(summary['Last'])  # last price                
                print "End of the minute: ", last
                time.sleep(10)
                
               # print currtime
                
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set sixtyseconds= %s  where market = %s",
                        (last, market))
                    cursor.execute(
                        "update prices set end_price= %s  where market = %s and time =%s",
                        (last, market, currtime))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                    
                beginning_minute= get_prices(currtime, 2)    
                end_minute= get_prices(currtime, 3)
                
                if end_minute>=beginning_minute:
			percent_change= math.fabs(beginning_minute/end_minute*100-100)
		else:
			percent_change= -1*(beginning_minute/end_minute*100-100)
			
		print "Percent change is : ", percent_change
                    
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update prices set percent_change= %s  where market = %s and time =%s",
                        (percent_change, market, currtime))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                    
        except:
            continue



def status_orders(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0






def heikin_ashi(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False






def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE  enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False



def get_prices(timestamp, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    time = timestamp
    cursor.execute("SELECT * FROM prices WHERE time = '%s'" % time)
    r = cursor.fetchall()
    for row in r:
        if row[5] == timestamp:
            return row[value]

    return False


def summ_percent(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_change) FROM prices WHERE market = '%s' order by id desc limit 5" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
	#if row[1] == marketname:
            return float("{0:.5f}".format(row[0]))
            # return 0
        else:
            return 0





if __name__ == "__main__":
    main()
