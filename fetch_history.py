import json
import sys, os
import requests
import ast

r =requests.get('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USD-BTC&tickInterval=fiveMin')
responce = r.text
data = json.loads(responce)
result = data['result']
#print (result)
last_date = result[-1]



try:
    file = open("data/hist_data_fivemin.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    last_current_date=dictionary[-1]
    file.close()
except:
    print("Unable to read the fivemin file")


#print (last_date['T'])
#print(last_current_date['T'])


if last_date['T']!=last_current_date['T']:
   try:
      history_file = open('data/hist_data_fivemin.txt', 'a')
      history_file.write(',')
      history_file.write(str(last_date))
      history_file.close()
   except:
      print("Unable to append to file")
else:
   pass 







