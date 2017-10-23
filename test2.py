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


#                                       Public API
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


#                                           Account API
#Used to retrieve balances from your account.
balances = c.get_balances().json()['result']
items = (itemgetter(0, 1)(balances))
for i in balances:
    print "Balance for {0} is:".format(i['Currency'])
    print (i['Balance'])



#used to retrieve balance for specific currency
balance = c.get_balance(currency).json()['result']
print "The current balance for {1} is {0}".format(balance['Available'],balance['Currency'])


#Used to retrieve or generate an address for a specific currency. If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available
balance = c.get_deposit_address(currency).json()['result']
print "The deposit address for {1} is {0}".format(balance['Address'],balance['Currency'])


#Used to retrieve your order history
orderhistory = c.get_order_history().json()['result']
for i in orderhistory:
  print "The  orders from history for currency: {0} cost is: {1} uuid is: {2}".format(i['Exchange'], i['Price'], i['OrderUuid'])
vtcorderuuid =  orderhistory[0]['OrderUuid']
#print vtcorderuuid


#Used to retrieve a single order by uuid
order = c.get_order(vtcorderuuid).json()['result']
print "The UUID for this currency: {1} is: {0}".format(order['OrderUuid'], order['Exchange'])


#Used to retrieve your withdrawal history
withdrawhistory = c.get_withdrawal_history().json()['result']
for i in withdrawhistory:
  print "Withdrawal is:".format(i)
#print withdrawhistory


#Used to retrieve your deposit history
deposithistory = c.get_deposit_history().json()['result']
print "This is my deposit history"
for index in enumerate(deposithistory):
        i = index[0]
        items = deposithistory[i].items()
        items = (itemgetter(0,2,3)(items))
        #print items
        for item in items:
            p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
            print p


#Used to withdraw funds from your account. Will be tested in future
#withdraw = c.withdraw().json()
#{'currency': currency, 'quantity': qty, 'address': address, 'paymentid': memo}



#                                   Market API

#Get all orders that you currently have opened. A specific market can be requested
openorders = c.get_open_orders().json()['result']
print "We have these open orders:"
for i in enumerate(openorders):
    i = i[0]
    items = openorders[i].items()
    for item in items:
        p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
        print p


#Those will be checked later
#Used to place a buy order in a specific market. Use buylimit to place limit orders
#buy = c.buy_limit()

#Used to place an sell order in a specific market. Use selllimit to place limit orders.
#sell = c.sell_limit()

#Used to cancel a buy or sell order.
#cancel = c.market_cancel()
