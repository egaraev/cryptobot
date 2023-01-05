import json
import sys, os
import requests
import ast
market="BTC-USD"
import pymysql

def available_market_list(symbol):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = symbol
    cursor.execute("SELECT * FROM markets WHERE  enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbol:
            return True

    return False





r =requests.get('https://api.bittrex.com/v3/markets/BTC-USD/summary')
responce = r.text
data = json.loads(responce)

r_ticker =requests.get('https://api.bittrex.com/v3/markets/tickers')
responce_ticker = r_ticker.text
data_ticker = json.loads(responce_ticker)

r_summ =requests.get('https://api.bittrex.com/v3/markets/summaries')
responce_summaries = r_summ.text
data_summ = json.loads(responce_summaries)

percent_chg = 0

for summary in data_summ: #Loop trough the market summary
    if available_market_list(summary['symbol']):
        market = summary['symbol']
        percent_chg = float(summary['percentChange'])


last = float([tick['lastTradeRate'] for tick in data_ticker if tick['symbol']==market][0]) 
bid = float([tick['bidRate'] for tick in data_ticker if tick['symbol']==market][0])   
ask = float([tick['askRate'] for tick in data_ticker if tick['symbol']==market][0])	
#print (last,bid,ask)


marketname = data['symbol']
highprice = float(data['high'])
lowprice  = float(data['low'])
volume = float(data['volume'])
basevolume = float(data['quoteVolume'])
percentChange = data['percentChange']
datestamp = data['updatedAt']


created = ([tick['updatedAt'] for tick in data_ticker if tick['symbol']==market][0])	

#{'MarketName': 'USD-BTC', 'High': 43234.686, 'Low': 40601.15, 'Volume': 265.67021027, 'Last': 41927.912, 'BaseVolume': 11105532.24025511, 'TimeStamp': '2022-01-07T21:45:54.39', 'Bid': 41894.601, 'Ask': 41912.377, 'OpenBuyOrders': 5541, 'OpenSellOrders': 5259, 'PrevDay': 43077.091, 'Created': '2018-05-31T13:24:40.77'}


record = {'MarketName': marketname, 'High': highprice, 'Low': lowprice, 'Volume': volume, 'Last': last, 'BaseVolume': basevolume, 'TimeStamp': datestamp[:-2], 'Bid': bid, 'Ask': ask, 'PrevDay': percent_chg, 'Created': created[:-6]}


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
    summary_file.write(str(record))
    summary_file.close()
except:
    print("Unable to append to file")

print (record)

