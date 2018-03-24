#Imports from modules, libraries and config files
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
import yaml
import hmac
import hashlib
import MySQLdb
import sys
import subprocess
c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file

currtime = int(round(time.time()))

def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE active =1  and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()


def get_candles(market, tick_interval):
    url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market +'&tickInterval=' + str(tick_interval)
    return signed_request(url)

def main():
    print('Starting weekly analisys module')

    analize()


def analize():

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ:  # Loop trough the market summary
        if available_market_list(summary['MarketName']):
            market = summary['MarketName']
            #print market
            #Candle analisys
            lastcandle = get_candles(market, 'day')['result'][-1:]
            currentlow = float(lastcandle[0]['L'])
            currenthigh = float(lastcandle[0]['H'])
            currentopen = float(lastcandle[0]['O'])
            currentclose = float(lastcandle[0]['C'])
            previouscandle = get_candles(market, 'day')['result'][-2:]
            prevlow = float(previouscandle[0]['L'])
            prevhigh = float(previouscandle[0]['H'])
            prevopen = float(previouscandle[0]['O'])
            prevclose = float(previouscandle[0]['C'])
            oldcandle = get_candles(market, 'day')['result'][-3:]
            oldlow = float(previouscandle[0]['L'])
            oldhigh = float(previouscandle[0]['H'])
            oldopen = float(previouscandle[0]['O'])
            oldclose = float(previouscandle[0]['C'])
            #print market, currentopen, currenthigh
            #if (prevclose>=currentopen or currentopen==currenthigh):
            #    print market
            if (prevclose>=currentopen or currentopen==currenthigh) is not True:
                print market














if __name__ == "__main__":
    main()