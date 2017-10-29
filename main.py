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

#Open config file
with open("variables.yml", "r") as variables_file:
    variables = yaml.load(variables_file)
#The size for opening orders
    buy_size = float(variables['buy_order_size'])
#Minimal size for closing oders
    sell_size = float(variables['min_sell_order_size'])
#The size of profit
    profit = float(variables['multiplier'])
#The main currency
    currency_btc = variables['currency_btc']
#The maximum quantity of open orders at the same time
    max = float(variables['maxorder'])



#Setup tick interval
TICK_INTERVAL = 120  # seconds

#Call pybittrex function for all encrypted connections
market_summ = c.get_market_summaries().json()['result']


#The main function
def main():
    print('Starting trader bot, ticking every ' + str(TICK_INTERVAL) + ' seconds')

#Running clock forever
    while True:
        start = time.time()
        tick()
        end = time.time()
        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))

##################################################################################################################
#what will be done every loop iteration
def tick():
    for summary in market_summ:
        if (summary['MarketName'][0:3]) == currency_btc:
            market = summary['MarketName']
        day_close = summary['PrevDay']
        #Current price
        last = float(summary['Last'])
        bid = float(summary['Bid'])
        ask = float(summary['Ask'])
        #How much market has been changed
        percent_chg = ((last / day_close) - 1) * 100
        #HOW MUCH TO BUY
        buy_quantity = buy_size / last
        #BOUGHT PRICE
        bought_price = get_closed_orders(market, 'PricePerUnit')
        #Bought Quantity need for sell order, to know at which price we bought some currency
        bought_quantity = get_closed_orders(market, 'Quantity')
        sell_quantity = bought_quantity

        #orders =set(get_big_orders('BTC-QTUM','buy'))
        #print get_big_orders('BTC-QTUM', 'BUY')
        #print c.get_market_history('BTC-QTUM', 'Total').json()['result']

#If the price for some currency rapidly increased from 30% till 50%. lets buy something
        if 5 < percent_chg < 50:
            balance_res = get_balance_from_market(market)
            current_balance = balance_res['result']['Available']
            # Check if we have open orders
            if has_open_order(market, 'LIMIT_BUY') or current_balance is not None:
                print('Order already opened to buy  ' + market)
            else:
                #Buy some currency
                print('Purchasing ' + str(format_float(buy_quantity)) +' units of ' + market + ' for ' + str(format_float(ask)))
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                #print c.buy_limit(market, buy_quantity, last).json()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

#Check if we have this currency for sell
        if bought_price != None:

#If  we got our profit, lets sell
            if last >= bought_price*profit:
                balance_res = get_balance_from_market(market)
                current_balance = balance_res['result']['Available']


#check current balance
                if current_balance is None:
                    pass

#If curent balance more then zero
                elif current_balance > 0:
                    # Lets Sell some
                    if has_open_order(market, 'LIMIT_SELL'):
                        print('Order already opened to sell  ' + market)
                    else:
                        print('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(bid)) + '  and getting  +' + str(format_float(bid-bought_price)) + ' BTC')
#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
 #                      print c.sell_limit(market, sell_quantity, last).json()
#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                else:
                    pass
                    #print('Not enough ' + market + ' to open a sell order')
        else:
            pass

###############################################################################################################
#Analize of last buy orders
def get_big_orders(market_type, value):
    bigorders = c.get_market_history(market_type, value).json()
    orders = bigorders['result']
    #return orders
    #items = (itemgetter(0, 1, 2, 3, 4)(orders))
    #if orders['OrderType'] == value:
    #    return orders['Total']
    #return orders
    for i in orders:
        if i['OrderType'] == value:
    #        #time.sleep(15)
            return i['Total']







#Function for checking the history of orders
def get_closed_orders(currency, value):
    orderhistory = c.get_order_history(currency).json()
    orders = orderhistory['result']
    for order in orders:
        if order['Exchange'] == currency:
                return order[value]
        else:
            return False


#Check the market prices
def get_balance_from_market(market_type):
    markets_res = c.get_markets().json()
    markets = markets_res['result']
    #print markets
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])
            # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}

#Getting balance for currency
def get_balance(currency):
    res =c.get_balance(currency).json()
    if res['result'] is not None and len(res['result']) > 0:
        return res
        # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}



#get the orders
def get_open_orders(market):
    return c.get_open_orders(market).json()


#check if order opened or not
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





def format_float(f):
    return "%.8f" % f


if __name__ == "__main__":
    main()