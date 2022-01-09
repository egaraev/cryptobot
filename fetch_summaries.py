import json
import sys, os
import requests
import ast

r =requests.get('https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=usd-btc')
responce = r.text
data = json.loads(responce)
result = data['result']
last_date = result[-1]
print (last_date)


try:
    file = open('data/summaries.txt', 'r')
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    last_current_date=dictionary[-1]
    file.close()
except:
    print("Unable to read the file")


try:
    summary_file = open('data/summaries.txt', 'a')
    summary_file.write(',')
    summary_file.write(str(last_date))
    summary_file.close()
except:
    print("Unable to append to file")



