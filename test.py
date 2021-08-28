from bittrex.bittrex import *
import config
import json
api_key=config.key
api_secret=config.secret
from yahoo_fin import stock_info as si
my_bittrex = Bittrex(api_key, api_secret, api_version=API_V1_1)
import requests
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import matplotlib.pyplot as plt
# plt.rcParams['figure.figsize'] = (20, 10)
# plt.style.use('fivethirtyeight')
import pandas as pd
from tti.indicators import KlingerOscillator

#print (my_bittrex.get_open_orders('USD-ETH')['result'][0]['OrderUuid'])

#print (my_bittrex.get_balance('ETH'))
#print (my_bittrex.buy_limit('USD-ETH', '0.00160951', '3083.394') )

symbol="USD-BTC"
crypto=symbol[4:]
market = crypto+"-USD"
print (market)
df = si.get_data(market)
df = df.iloc[: , :-1]
df = df[-100:]
print (df)


kov = KlingerOscillator(input_data=df)


print('\nMost recent Technical Indicator value:', kov.getTiValue())
print('\nTechnical Indicator signal:', kov.getTiSignal())
kov.getTiGraph().savefig("images/kov.png")