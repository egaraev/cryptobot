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

