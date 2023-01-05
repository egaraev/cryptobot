from yahoo_fin import stock_info as si
import sys, os
import ast
import json

df = si.get_data('BTC-USD')
df = df.iloc[: , :-1]
df = df[-32:]
df = df.reset_index().rename({'index':'date'}, axis = 'columns')

#print (df)
df.rename(columns={ 'date': 'T', 'open': 'O', 'high': 'H', 'low': 'L', 'close': 'C', 'volume': 'V' }, inplace=True)
del df['adjclose']
print (df)
