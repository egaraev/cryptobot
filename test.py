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
import json
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')
currtime = int(time.time())


def main():
    print('Starting test module')


    ME()



def ME():
    market_summ = c.get_market_summaries().json()['result']
    print c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price
                ask = float(summary['Ask'])  # buy price
		print market, ask, bid
			

		hourcandles=0
                hourcurrentlow = 0
                hourcurrenthigh = 0
                hourcurrentopen = 0
                hourcurrentclose = 0
                hourprevlow = 0
                hourprevhigh = 0
                hourprevopen = 0
                hourprevclose = 0
                hourprevlow2 = 0
                hourprevhigh2 = 0
                hourprevopen2 = 0
                hourprevclose2 = 0
		lastcandle5=''

                hourcandles = get_candles(market, 'hour')['result'][-25:]
                hourcurrentlow = float(hourcandles[24]['L'])*100000
                hourcurrenthigh = float(hourcandles[24]['H'])*100000
                hourcurrentopen = float(hourcandles[24]['O'])*100000
                hourcurrentclose = float(hourcandles[24]['C'])*100000

                hourprevlow = float(hourcandles[23]['L'])*100000
                hourprevhigh = float(hourcandles[23]['H'])*100000
                hourprevopen = float(hourcandles[23]['O'])*100000
                hourprevclose = float(hourcandles[23]['C'])*100000

                hourprevlow2 = float(hourcandles[22]['L'])*100000
                hourprevhigh2 = float(hourcandles[22]['H'])*100000
                hourprevopen2 = float(hourcandles[22]['O'])*100000
                hourprevclose2 = float(hourcandles[22]['C'])*100000

                hourprevlow24 = float(hourcandles[0]['L'])*100000
                hourprevhigh24 = float(hourcandles[0]['H'])*100000
                hourprevopen24 = float(hourcandles[0]['O'])*100000
                hourprevclose24 = float(hourcandles[0]['C'])*100000
                
                lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                currentopen = float(lastcandle[0]['O'])
                currenthigh = float(lastcandle[0]['H'])
                hourpreviouscandle4 = get_candles(market, 'hour')['result'][-5:]
                hourprevopen4 = float(hourpreviouscandle4[0]['O'])
                fivehourcurrentopen = hourprevopen4
                hourpreviouscandle9 = get_candles(market, 'hour')['result'][-10:]
                hourprevopen9 = float(hourpreviouscandle9[0]['O'])
                hourpreviouscandle5 = get_candles(market, 'hour')['result'][-6:]
                hourprevclose5 = float(hourpreviouscandle5[0]['C'])
                fivehourprevopen = hourprevopen9
                fivehourprevclose = hourprevclose5
                try:
			lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
		except:
		    continue
                currentlow5 = float(lastcandle5[0]['L'])
                currentopen5 = float(lastcandle5[0]['O'])
                currenthigh5 = float(lastcandle5[0]['H'])
                hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                hourcurrentopen = float(hourlastcandle[0]['O'])
                hourcurrenthigh = float(hourlastcandle[0]['H'])
                daylastcandle = get_candles(market, 'day')['result'][-1:]
                daycurrentopen = float(daylastcandle[0]['O'])
                daycurrenthigh = float(daylastcandle[0]['H'])

# 	 	print hourcandles, lastcandle, hourpreviouscandle4, hourpreviouscandle9, hourpreviouscandle5, lastcandle5, hourlastcandle, daylastcandle
		print len(lastcandle5)
		if len(lastcandle5)==0:
			print "Connection failed"
		else:
			print "Connection OK"
		


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

def format_float(f):
    return "%.7f" % f

if __name__ == "__main__":
    main()
