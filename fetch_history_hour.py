import json
import sys, os
import requests
import ast

r =requests.get("https://api.bittrex.com/v3/markets/BTC-USD/candles/HOUR_1/recent")
responce = r.text
data = json.loads(responce)
result = data
last_date = result[-1]

#print(last_date)

openprice = float(last_date['open'])
highprice = float(last_date['high'])
lowprice  = float(last_date['low'])
closeprice = float(last_date['close'])
volume = float(last_date['volume'])
qvolume = float(last_date['quoteVolume'])
datestamp = last_date['startsAt']

record = {"O":openprice,"H":highprice,"L":lowprice,"C":closeprice,"V":volume,"T":datestamp[:-1],"BV":qvolume}

#print (record)


try:
    file = open("data/hist_data_hour.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    last_current_date=dictionary[-1]
    file.close()
except:
    print("Unable to read the file")


print (datestamp)
print(last_current_date['T'])


if datestamp!=last_current_date['T']:
   try:
      history_file = open('data/hist_data_hour.txt', 'a')
      history_file.write(',')
      history_file.write(str(record))
      history_file.close()
   except:
      print("Unable to append to file")
else:
   pass 
