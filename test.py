import requests
import json
market = "BTC-USD"
tick_interval = 900

def get_coinbase_candles(market, tick_interval):
    url = ('https://api.exchange.coinbase.com/products/' + market +'/candles?granularity=' + str(tick_interval))
	#[ time, low, high, open, close, volume ]
    r = requests.get(url)
    requests.session().close()
    return r.json()


lastcandle = get_coinbase_candles(market, tick_interval)[-1:]
currentlow = float(lastcandle[0][1])
currentopen = float(lastcandle[0][3])
currenthigh = float(lastcandle[0][2])
previouscandle = get_coinbase_candles(market, tick_interval)[-2:]
prevhigh = float(previouscandle[0][2])
prevclose = float(previouscandle[0][4])

print (lastcandle, currentlow)	
