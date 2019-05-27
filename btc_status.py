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


c1 = Client(api_key=config.key, api_secret=config.secret)
c = Client(api_key='', api_secret='')

currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
btc_status = "OK"


def main():
    print('Starting btc status module')

    HA()


def HA():
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    btclastcandle = get_candles('USDT-BTC', 'thirtyMin')['result'][-1:]
    btccurrentlow = float(btclastcandle[0]['L'])
    btccurrentopen = float(btclastcandle[0]['O'])
    btccurrentclose = float(btclastcandle[0]['C'])
    btccurrenthigh = float(btclastcandle[0]['H'])
    btcprevcandle = get_candles('USDT-BTC', 'thirtyMin')['result'][-2:]
    btcprevlow = float(btcprevcandle[0]['L'])
    btcprevopen = float(btcprevcandle[0]['O'])
    btcprevclose = float(btcprevcandle[0]['C'])
    btcprevhigh = float(btcprevcandle[0]['H'])
    btcprevcandle2 = get_candles('USDT-BTC', 'thirtyMin')['result'][-3:]
    btcprevlow = float(btcprevcandle2[0]['L'])
    btcprevopen = float(btcprevcandle2[0]['O'])
    btcprevclose = float(btcprevcandle2[0]['C'])
    btcprevhigh = float(btcprevcandle2[0]['H'])

    if (btccurrentopen - BTC_price >= 150 or (btcprevopen - BTC_price >= 200 and btccurrentopen > BTC_price)):
        btc_status = "STOP"
        print ('   Received BTC STOP sell signal ')
        try:
            db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
            cursor = db.cursor()
            printed = ('   Received BTC STOP sell signal ')
            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
            db.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            db.close()
        print printed
    else:
        btc_status = "OK"

    print btc_status, btccurrentopen, BTC_price


    market_summ = c.get_market_summaries().json()['result']

#    for summary in market_summ:  # Loop trough the market summary
#        try:
#            if available_market_list(summary['MarketName']):
#                market = summary['MarketName']

#                if (btc_status == "STOP"):

#                    try:
#                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
#                        cursor = db.cursor()
#                        cursor.execute('update orders set sell = 7 where active=1 and market =("%s")' % market)
#                        db.commit()
#                    except MySQLdb.Error, e:
#                        print "Error %d: %s" % (e.args[0], e.args[1])
#                        sys.exit(1)
#                    finally:
#                        db.close()
#                else:
#                    pass
    

#        except:
#            continue


def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


def get_candles(market, tick_interval):
    url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market + '&tickInterval=' + str(
        tick_interval)
    return signed_request(url)


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()


def status_markets(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False


def status_orders(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
