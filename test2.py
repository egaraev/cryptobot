from bittrex import Bittrex
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
from pybittrex.auth import BittrexAuth
c = Client(api_key=config.key, api_secret=config.secret)
api = Bittrex(config.key, config.secret)
market = "BTC-VTC"
vtc = 3
currency = "VTC"

#Used to get the open and available trading markets at Bittrex along with other metadata.
markets = c.get_markets().json()['result']
#For specific currency  markets[0] index means the number of currency pair
market = (markets[2])['MarketName']
print "We are working on following market: {0} ".format(market)
    #market = (markets[2])['MarketName']
#For all markets
#for i in markets:
#    print(i['MarketName'])

#Used to get all supported currencies at Bittrex along with other metadata
currencies = c.get_currencies().json()['result']
print "We selected this currency: {0}".format((currencies[vtc])['Currency'])

#Used to get the current tick values for a market.
ticker = c.get_ticker(market).json()['result']
print "The current Ask is: {0}".format((ticker)['Ask'])
print "The current Bid is: {0}".format((ticker)['Bid'])

#Used to get the last 24 hour summary of all active exchanges.
market_summ = c.get_market_summaries().json()['result']
market_summ_vtc = market_summ[175]
print "The current bought volume is {0}".format(market_summ_vtc['Volume'])
# The BID for volume
# print market_summ_vtc['Bid']


#Used to get retrieve the orderbook for a given market.
sellorderbook = c.get_orderbook(market, 'sell').json()['result']
buyorderbook = c.get_orderbook(market, 'buy').json()['result']

# show 2 last  sell orders
items = (itemgetter(0, 1)(sellorderbook))
for i in items:
    print "One of the last SELL orders {0}".format(i['Quantity'])

# show 2 last buy orders
items = (itemgetter(0, 1)(buyorderbook))
for b in items:
    print "One of the last BUY orders {0}".format(b['Quantity'])



markethistory = c.get_market_history(market).json()['result']
#print markethistory
# show 2 last  sell orders from history
items = (itemgetter(2, 3)(markethistory))
for i in items:
  print "The last 2 SELL orders from history {0}".format(i['Total'])


# Account API
#Used to retrieve balances from your account.
balances = c.get_balances().json()['result']
items = (itemgetter(0, 1)(balances))
for i in balances:
    print "Balance for {0} is:".format(i['Currency'])
    print (i['Balance'])












