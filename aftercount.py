import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
import time
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')
currtime = int(time.time())


def main():
    print('Starting aftercount module')


    ME()



def ME():
    market_summ = c.get_market_summaries().json()['result']
    #print market_count()
    #print c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price
                ask = float(summary['Ask'])  # buy price
                newbid = bid - bid * 0.002
                newask = ask + ask * 0.002
                bought_price_sql = float(status_orders(market, 3))
                aftercount=float(status_orders(market, 25))
                #bought_quantity_sql = float(status_orders(market, 2))
                order_id = closed_orders_id(market)
                procent_serf = float(((newbid / bought_price_sql) - 1) * 100)



                if order_id!=0 and currtime - close_date(market)<172800:

                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()

                        if procent_serf>=percent_serf(market):
                            cursor.execute(
                                "update orders set aftercount=%s where market = %s and active = 0 and order_id = %s",
                                (procent_serf, market, order_id))
                        else:
                            cursor.execute(
                                "update orders set aftercount_min=%s where market = %s and active = 0 and order_id = %s",
                                (procent_serf, market, order_id))

                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                else:
                    pass


                if order_id != 0 and currtime - close_date(market) < 80000 and aftercount-percent_serf(market)>=10:
                 try:
                     print "We have peak situation, lets wait"
                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                     cursor = db.cursor()
                     printed1 = ("We have peak situation, lets wait")
                     cursor.execute(
                         "update markets set strike_date=%s, strike_time2=%s, strike_info=%s  where market = %s",
                         (currenttime, currtime, printed1, market))
                     db.commit()
                 except MySQLdb.Error, e:
                     print "Error %d: %s" % (e.args[0], e.args[1])
                     sys.exit(1)
                 finally:
                     db.close()
                else:
                    pass





                print order_id, market, percent_serf(market), procent_serf, bought_price_sql

        except:
            continue



def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE  enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


def closed_orders_id(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT order_id FROM orders where active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def status_orders(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 0 and market = '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0



def percent_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0


def close_date(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[0])
    return 0


if __name__ == "__main__":
    main()