import time
import config
from pybittrex.client import Client
import MySQLdb
import sys
import requests
import hashlib
import hmac
import numpy
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
c = Client(api_key=config.key, api_secret=config.secret)


def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE  market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False



def status_orders(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


def percent(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM markets order by percent_chg DESC limit 16")
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]
    return 0




def main():
    print('Starting enabling market module')

    ME()



def ME():
    market_summ = c.get_market_summaries().json()['result']

    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                day_close = summary['PrevDay']  # Getting day of closing order
                bought_quantity_sql = float(status_orders(market, 2))
                last = float(summary['Last'])  # last price
                percent_chg = float(((last / day_close) - 1) * 100)

                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set percent_chg= %s  where market = %s",
                        (percent_chg, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()




                #if percent(market, 21) >0:
                #print market, percent(market, 21)#, bought_quantity_sql



                if percent(market, 21) >0:
                    #print market, "We need to enable those currencies"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('update markets set active= 1 where market =("%s")' % market)
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                if percent(market, 21) ==0 and bought_quantity_sql>0:
                    print market, "We have open order, but we need to disable this currency"


                if percent(market, 21)==0 and bought_quantity_sql==0:
                    #print market, "We are disabling this currency"
                    try:
                        printed = ('    We are disabling this currency  ' + market)
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('update markets set active= 0 where market =("%s")' % market)
                        #cursor.execute(
                        #    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


        except:
            continue

def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
