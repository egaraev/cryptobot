from bittrex import Bittrex
import config
api = Bittrex(config.key, config.secret)

currency = 'XCP'
currency2 = 'BTC'
currency3 = 'ETH'

# Gets the current balance
xcpbalance = api.get_balance(currency)[u'result']
print "Your balance is {0} {1}.".format(xcpbalance['Available'], currency)
btcbalance = api.get_balance(currency2)[u'result']
print "Your balance is {0} {1}.".format(btcbalance['Available'], currency2)
ethbalance = api.get_balance(currency3)[u'result']
print "Your balance is {0} {1}.".format(ethbalance['Available'], currency3)
print " "
print " "

#Gets the deposit history
market = api.get_deposit_history(currency2)['result']
market3 = api.get_deposit_history(currency3)['result']
print "We have following transaction history for {0}".format(currency2)
print " "
for index in enumerate(api.get_deposit_history(currency2)['result']):
        i = index[0]
        items = market[i].items()
        for item in items:
            print "     ".join(repr(x).lstrip('u')[1:-1] for x in item)
        print " "
