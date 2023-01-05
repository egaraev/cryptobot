import config
from pybittrex.client import Client
import pymysql
import sys
import datetime
import time
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
from bittrex_api import Bittrex
bittrex = Bittrex(
    api_key=config.key,              # YOUR API KEY
    secret_key=config.secret,           # YOUR API SECRET
    max_request_try_count=3, # Max tries for a request to succeed
    sleep_time=2,            # sleep seconds between failed requests
    debug_level=3
)
c = bittrex.v3


currtime = int(time.time())
tickers = c.get_tickers()

def main():
    print('Starting aftercount module')


    ME()



def ME():
    market_summ = c.get_market_summaries()
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['symbol']):
                market = summary['symbol']
                # Current prices

                last = float([tick['lastTradeRate'] for tick in tickers if tick['symbol']==market][0]) #last price
                bid = float([tick['bidRate'] for tick in tickers if tick['symbol']==market][0])   #sell price
                ask = float([tick['askRate'] for tick in tickers if tick['symbol']==market][0])	#buy price
			
                newbid=float("{:.5f}".format(bid - bid*0.002))
                newask=float("{:.5f}".format(ask + ask*0.002))

                bought_price_sql = float(status_orders(market, 3))
                aftercount=float(status_orders(market, 25))
                min_percent=float(status_orders(market, 24))
                aftercount_min=float(status_orders(market, 26))
                #bought_quantity_sql = float(status_orders(market, 2))
                order_id = closed_orders_id(market)
                procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))
                #print market, procent_serf, percent_serf(market)


                if order_id!=0 and currtime - close_date(market)<432000:

                    try:
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
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


                # if order_id != 0 and currtime - close_date(market) < 80000 and aftercount-percent_serf(market)>=10:
                 # try:
                     # print "We have peak situation, lets wait"
                     # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                     # cursor = db.cursor()
                     # printed1 = ("We have peak situation, lets wait")
                     # cursor.execute(
                         # "update markets set strike_date=%s, strike_time2=%s, strike_info=%s  where market = %s",
                         # (currenttime, currtime, printed1, market))
                     # db.commit()
                 # except pymysql.Error as e:
                     # print ("Error %d: %s" % (e.args[0], e.args[1]))
                     # sys.exit(1)
                 # finally:
                     # db.close()
                # else:
                    # pass





                print (market, percent_serf(market), procent_serf, aftercount, min_percent)

        except:
            continue



def available_market_list(symbol):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = symbol
    cursor.execute("SELECT * FROM markets WHERE  enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbol:
            return True

    return False


def closed_orders_id(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT order_id FROM orders where active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def status_orders(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 0 and market = '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0



def percent_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0


def close_date(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[0])
    return 0


if __name__ == "__main__":
    main()
