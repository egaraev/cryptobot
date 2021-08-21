from bittrex.bittrex import *
import config
import json
api_key=config.key
api_secret=config.secret
from yahoo_fin import stock_info as si
my_bittrex = Bittrex(api_key, api_secret, api_version=API_V1_1)



#print (my_bittrex.get_open_orders('USD-ETH')['result'][0]['OrderUuid'])

#print (my_bittrex.get_balance('ETH'))
#print (my_bittrex.buy_limit('USD-ETH', '0.00160951', '3083.394') )

market="USD-LTC"
crypto=market[4:]
market = crypto+"-USD"
print (market)
df = si.get_data(market)
print (df)

