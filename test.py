from yahoo_fin import stock_info as si
import sys, os
import ast

df = si.get_data('BTC-USD')
df = df.iloc[: , :-1]
df = df[-62:]
df = df.reset_index().rename({'index':'date'}, axis = 'columns')

#print (df)
df.rename(columns={ 'date': 'T', 'open': 'O', 'high': 'H', 'low': 'L', 'close': 'C', 'volume': 'V' }, inplace=True)
del df['adjclose']
df['T'] = df['T'].dt.strftime('%Y-%m-%d')
result = df.to_dict('records')
last_date = result[-1]



try:
    file = open("hist_data_day.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    dict_without_last_day= dictionary[:-1]	
    print (dictionary)
    last_current_date=dictionary[-1]
    file.close()
except:
    print("Unable to read the file")




try:
      history_file = open('hist_data_day.txt', 'w')
      history_file.write(str(dict_without_last_day))
      history_file.write(',')
      history_file.write(str(last_date))
      history_file.close()
except:
      print("Unable to append to file")
