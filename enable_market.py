import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
c = Client(api_key=config.key, api_secret=config.secret)




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



def status_orders(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


def has_open_order(market, order_type):
    orders_res = c.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
# Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True
    return False



def percent(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM markets where percent_chg>(SELECT AVG(percent_chg)/1.5 FROM markets where percent_chg>1) and ha_direction_daily!='DOWN' and ha_direction_daily!='Revers-DOWN' and enabled=1 ORDER BY volume DESC  limit 10")
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
                volume = int(summary['BaseVolume'])
                bought_quantity_sql = float(status_orders(market, 2))
                last = float(summary['Last'])  # last price
                percent_chg = int(((last / day_close) - 1) * 100)

                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set percent_chg= %s, volume=%s  where enabled=1 and market = %s",
                        (percent_chg, volume, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()



                if percent(market, 21) >0:
                    print market, "We need to enable those currencies"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('update markets set active= 1 where enabled=1 and market =("%s")' % market)
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                if percent(market, 21) ==0 and bought_quantity_sql>0:
                    print market, "We have open order, but we need to disable this currency"


                if percent(market, 21)==0 and bought_quantity_sql==0 :
                    if has_open_order(market, 'LIMIT_SELL') or has_open_order(market, 'LIMIT_BUY'):
                        pass
                    else:
                    #print market, "We are disabling this currency"
                        try:
                            printed = ('    We are disabling this currency  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('update markets set active= 0 where enabled=1 and market =("%s")' % market)
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


        except:
            continue



if __name__ == "__main__":
    main()
