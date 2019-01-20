import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
import time
import hmac
import requests
import hashlib
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')
currtime = int(time.time())


def main():
    print('Starting enabling market module')


    ME()



def ME():
    market_summ = c.get_market_summaries().json()['result']
    #print market_count()
    max_markets = parameters()[6]
#    print c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                day_close = summary['PrevDay']  # Getting day of closing order
                volume = int(summary['BaseVolume'])
                bought_quantity_sql = float(status_orders(market, 2))
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])    #sell price
                ask = float(summary['Ask'])    #buy price
                percent_chg = float(((last / day_close) - 1) * 100)
                percent_sql = float(heikin_ashi(market, 21))
                spread = float(((ask / bid) - 1) * 100)
                HAD_trend = heikin_ashi(market, 18)
                ha_time_second = heikin_ashi(market, 23)

                if percent_chg>percent_sql:
                    percent_grow=1
                elif percent_chg<percent_sql:
                    percent_grow=-1
                else:
                    percent_grow=0
                #Candle analisys
                lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                currentopen = float(lastcandle[0]['O'])

                lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                currentopen5 = float(lastcandle5[0]['O'])
                hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                hourcurrentopen = float(hourlastcandle[0]['O'])

                fivemin='NONE'
                thirtymin='NONE'
                hour='NONE'

                if last>currentopen5:
                    fivemin='U'
                else:
                    fivemin='D'

                if last>currentopen:
                    thirtymin='U'
                else:
                    thirtymin='D'

                if last>hourcurrentopen:
                    hour='U'
                else:
                    hour='D'


                #print market, last, hour, thirtymin, fivemin

                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute(
                        "update markets set percent_chg= %s, volume=%s, candles=%s where enabled=1 and market = %s",
                        (percent_chg, volume, ' HC: ' + str(hour) + ' 30mC: ' + str(thirtymin) + ' 5mC: ' + str(fivemin), market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()


                #print market, percent(market, 21)

                if (spread>0.5 and bought_quantity_sql>0 and percent_grow==-1 and open_buy(market)==2  and ((get_balance_from_market(market)['result']['Available'] >0.0 or get_balance_from_market(market)['result']['Balance'] >0.0))):
                    print market, "We have open order, but we need to disable this currency"


                if (spread>0.5 and bought_quantity_sql==0 and percent_grow==-1) or ((HAD_trend=="DOWN" or HAD_trend=="Revers-DOWN") and currtime - ha_time_second < 3000):
                    if has_open_order(market, 'LIMIT_SELL') or has_open_order(market, 'LIMIT_BUY') or open_buy(market)==2:
                        pass
                    else:
                        print market, "We are disabling this currency"
                        try:
                            printed = ('    We are disabling this currency  ' + market)
                            db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('update markets set active= 0 where enabled=1 and market =("%s")' % market)
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


                if spread<0.5 and (percent_grow==1 or percent_grow==0)  and market_count() <=max_markets:
                    print market, "We need to enable those currencies"
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('update markets set active= 1 where enabled=1 and market =("%s")' % market)
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()



        except:
            continue

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


def open_buy(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT active FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0




def get_balance_from_market(market_type):
    markets_res = c1.get_markets().json()
    markets = markets_res['result']
    #print markets
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])
            # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}

def get_balance(currency):
    res =c1.get_balance(currency).json()
    if res['result'] is not None and len(res['result']) > 0:
        return res
        # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}


def parameters():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24])

    return 0




def market_count():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM markets where enabled=1 and active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0




def status_orders(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


def has_open_order(market, order_type):
    orders_res = c1.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
# Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True
    return False



def percent(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    min_percent_chg = float(parameters()[7])
    order_devider = parameters()[6]
    #cursor.execute("SELECT * FROM markets where percent_chg>(SELECT AVG(percent_chg)/1.5 FROM markets where percent_chg>'%s') and ha_direction_daily!='DOWN' and ha_direction_daily!='Revers-DOWN' and enabled=1 ORDER BY volume DESC  limit 10" % min_percent_chg)
#    cursor.execute(
#        "SELECT * FROM markets where percent_chg>'%s' and ha_direction_daily!='DOWN' and ha_direction_daily!='Revers-DOWN' and enabled=1 ORDER BY volume DESC" % min_percent_chg)
    cursor.execute(
        "SELECT * FROM markets where percent_chg>'%s' and ha_direction_daily!='DOWN' and ha_direction_daily!='Revers-DOWN'  and enabled=1 ORDER BY volume DESC" % min_percent_chg)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]
    return 0


def heikin_ashi(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False



def get_candles(market, tick_interval):
    url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market +'&tickInterval=' + str(tick_interval)
    return signed_request(url)


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()









if __name__ == "__main__":
    main()
