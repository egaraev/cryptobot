from bittrex import Bittrex
import config
from operator import itemgetter

api = Bittrex(config.key, config.secret)

xcp = 'XCP'
btc = 'BTC'
eth = 'ETH'



# Get the current balance
allbalance = api.get_balances()[u'result']
#print allbalance
print "Your current balance is:"
for i in enumerate(allbalance):
    i = i[0]
    items = allbalance[i].items()
    items = (itemgetter(1, 0)(items))
    for item in items:
        p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
        print p
    print " "

#xcpbalance = api.get_balance(currency)[u'result']
#print "Your balance is {0} {1}.".format(xcpbalance['Available'], currency)
#btcbalance = api.get_balance(currency2)[u'result']
#print "Your balance is {0} {1}.".format(btcbalance['Available'], currency2)
#ethbalance = api.get_balance(currency3)[u'result']
#print "Your balance is {0} {1}.".format(ethbalance['Available'], currency3)
#print " "
#print " "


#Get the deposit history
market = api.get_deposit_history(btc)['result']
market3 = api.get_deposit_history(eth)['result']
print "We have following transaction history for {0}".format(btc)
print " "
for index in enumerate(api.get_deposit_history(btc)['result']):
        i = index[0]
        items = market[i].items()
        items = (itemgetter(0,2,3)(items))
        for item in items:
            p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
            print p
        print " "

#Get the open orders
markets = 'BTC-VTC'
orders = api.get_open_orders(markets)['result']
print "We have these open orders {0} ".format(orders)
for i in enumerate(orders):
    i = i[0]
    items = orders[i].items()
    #items = (itemgetter(0, 2, 3, 4, 5, 6, 7, 8, 9, 10)(items))
    for item in items:
        p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
        print p
    print " "


#Get the closed orders
clorders = api.get_order_history(market)['result']
print "We have this order history {0} ".format(clorders)

#Get the withdrawal history
withdraw = api.get_withdrawal_history()['result']
print "We have this withdrawal history {0} ".format(withdraw)

#Get the balance
balance = api.get_balances()['result']
print "We have this current balance"
for i in enumerate(balance):
    i = i[0]
    items = balance[i].items()
    items = (itemgetter(1, 2)(items))
    for item in items:
        p = "       ".join(repr(x).lstrip('u')[1:-1] for x in item)
        print p
    print " "

#Public commands
#Get the price
price = api.get_ticker('BTC-VTC')['result']
print price




print c.get_market_summaries().json()['result']

{u'PrevDay': 5.114e-05, u'Volume': 764229.87748726, u'Last': 4.899e-05, u'OpenSellOrders': 5715, u'TimeStamp': u'2017-10-31T18:38:45.76', u'Bid': 4.899e-05, u'Created': u'2017-06-06T01:22:35.727', u'OpenBuyOrders': 182, u'High': 5.367e-05, u'MarketName': u'BTC-1ST', u'Low': 4.7e-05, u'Ask': 4.9e-05, u'BaseVolume': 38.96921826}, {u'PrevDay': 8.2e-07, u'Volume': 3423432.74044269, u'Last': 8.3e-07, u'OpenSellOrders': 2376, u'TimeStamp': u'2017-10-31T18:46:11.77', u'Bid': 8e-07, u'Created': u'2016-05-16T06:44:15.287', u'OpenBuyOrders': 133, u'High': 8.7e-07, u'MarketName': u'BTC-2GIVE', u'Low': 7.7e-07, u'Ask': 8.3e-07, u'BaseVolume': 2.84692667}

for summary in market_summ:
    market = summary['MarketName']
    day_close = summary['PrevDay']
    last = float(summary['Last'])

allowed_markets = ('BTC-QTUM', 'BTC-ETH', 'BTC-VTC', 'BTC-LTC', 'BTC-XCP')






for summary in market_summ:
    if (summary['MarketName']) == market_list():
        market = summary['MarketName']
    day_close = summary['PrevDay']
    last = float(summary['Last'])



def market_list():
    allowed_markets = ('BTC-QTUM', 'BTC-ETH', 'BTC-VTC', 'BTC-LTC', 'BTC-XCP')
    for markets in allowed_markets:
        return markets


print c.get_orderbook(market, 'sell').json()['result']

{u'Rate': 4.96e-05, u'Quantity': 107.96278}, {u'Rate': 4.961e-05, u'Quantity': 18.97173211}, {u'Rate': 4.968e-05, u'Quantity': 204.29009193}, {u'Rate': 5e-05, u'Quantity': 130.91176861}, {u'Rate': 5.092e-05, u'Quantity': 16.60063353},