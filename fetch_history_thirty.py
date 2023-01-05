import json
import sys, os
import requests
import ast

r =requests.get('https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=900')
responce = r.text
data = json.loads(responce)
last_date = data[0]

#print (last_date)
timestamp = last_date[0]
output_stream = os.popen(f'date -d @{timestamp} +%FT%T.%2NZ')
datestamp = (output_stream.read())


openprice = last_date[3]
highprice = last_date[2]
lowprice  = last_date[1]
closeprice = last_date[4]
volume = last_date[5]

datestamp = datestamp.strip('\n')


record = {"O":openprice,"H":highprice,"L":lowprice,"C":closeprice,"V":volume,"T":datestamp[:-1],"BV":volume}

#print(record)


try:
    file = open("data/hist_data_thirty.txt", "r")
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
      history_file = open('data/hist_data_thirty.txt', 'a')
      history_file.write(',')
      history_file.write(str(record))
      history_file.close()
   except:
      print("Unable to append to file")
else:
   pass 
