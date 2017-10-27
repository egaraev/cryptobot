#Imports from modules, libraries and config files
from bittrex import Bittrex
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
import yaml
from pybittrex.auth import BittrexAuth
#Configuring bytrex client
c = Client(api_key=config.key, api_secret=config.secret)

#Opening config file with variables
with open("variables.yml", "r") as variables_file:
    variables = yaml.load(variables_file)

#Setup tick interval
TICK_INTERVAL = 60  # seconds
market_summ = c.get_market_summaries().json()['result']



def main():
    print('Starting trader bot, ticking every ' + str(TICK_INTERVAL) + ' seconds')

    while True:
        start = time.time()
        tick()
        end = time.time()
        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))

def tick():
    for summary in market_summ:
        market = summary['MarketName']
        day_close = summary['PrevDay']
        last = summary['Last']
        percent_chg = ((last / day_close) - 1) * 100
        print(market + ' changed ' + str(percent_chg))




        if 40 < percent_chg < 60:
            # Fomo strikes! Let's buy some
            if has_open_order(market, 'LIMIT_BUY'):
                print('Order already opened to buy 5 ' + market)
            else:
                print('Purchasing 5 units of ' + market + ' for ' + str(format_float(last)))
                #res = buy_limit(market, 5, last)
                #print(res)

        if percent_chg < -20:
            # Do we have any to sell?
            balance_res = get_balance_from_market(market)
            current_balance = balance_res['result']['Available']

            if current_balance > 5:
                # Ship is sinking, get out!
                if has_open_order(market, 'LIMIT_SELL'):
                    print('Order already opened to sell 5 ' + market)
                else:
                    print('Selling 5 units of ' + market + ' for ' + str(format_float(last)))
 #                   res = sell_limit(market, 5, last)
 #                   print(res)
            else:
                print('Not enough ' + market + ' to open a sell order')



def has_open_order(market, order_type):
    orders_res = c.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
# Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True
    return False


def get_open_orders(market):
    return c.get_open_orders(market).json()


def get_balance_from_market(market_type):
    markets_res = c.get_markets().json()
    markets = markets_res['result']
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])
            # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}


def get_balance(currency):
    res =c.get_balance(currency).json()
    if res['result'] is not None and len(res['result']) > 0:
        return res
        # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}

def format_float(f):
    return "%.8f" % f


if __name__ == "__main__":
    main()