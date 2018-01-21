#Imports from modules, libraries and config files
from bittrex import Bittrex
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
import yaml
import hmac
import hashlib
from pybittrex.auth import BittrexAuth
import MySQLdb
import sys




c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file

#Opening config file with variables

with open("variables.yml", "r") as variables_file:   #Open config file
    variables = yaml.load(variables_file)
    buy_size = float(variables['buy_order_size']) #The size for opening orders for STOP_LOSS mode
    buy_size2 = float(variables['buy_order_size2'])  # The size for opening orders for FIBONACI Mode
    sell_size = float(variables['min_sell_order_size'])  #Minimal size for closing oders
    profit = float(variables['multiplier'])  #The size of profit we want to take
    stop_loss = float(variables['stop_loss'])  #If stop_loss==1 we use stop loss mechanism, of not - we use fibonachi mechanism
    sql = float(variables['sql'])

#The list of available markets for trading with max order sizes (order sizes from history, which we can count as BIG)
available_markets = [{"MarketName": 'BTC-QTUM', "BuyOrders": 1000, "SellOrders": 1000}, {"MarketName": 'BTC-ETH', "BuyOrders": 30, "SellOrders": 30},
                     {"MarketName": 'BTC-LTC', "BuyOrders": 100, "SellOrders": 100}, {"MarketName": 'BTC-VTC', "BuyOrders": 1000, "SellOrders": 1000},
                     {"MarketName": 'BTC-XMR', "BuyOrders": 100, "SellOrders": 100}, {"MarketName": 'BTC-XRP', "BuyOrders": 3000, "SellOrders": 3000},
                     {"MarketName": 'BTC-ZEC', "BuyOrders": 50, "SellOrders": 50}, {"MarketName": 'BTC-ETC', "BuyOrders": 600, "SellOrders": 600},
                     {"MarketName": 'BTC-DASH', "BuyOrders": 20, "SellOrders": 20}, {"MarketName": 'BTC-NEO', "BuyOrders": 400, "SellOrders": 400},
                     {"MarketName": 'BTC-XLM', "BuyOrders": 1000000, "SellOrders": 1000000}, {"MarketName": 'BTC-OMG', "BuyOrders": 1000, "SellOrders": 1000},
                     {"MarketName": 'BTC-BCC', "BuyOrders": 15, "SellOrders": 15}, {"MarketName": 'BTC-LSK', "BuyOrders": 1000, "SellOrders": 1000}]

#Setup tick interval
TICK_INTERVAL = 60  # seconds

#Get the market summaries
market_summ = c.get_market_summaries().json()['result']

BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']


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



    #global active
    for summary in market_summ: #Loop trough the market summary
        if market_list(summary['MarketName']):  #Check if currency is from my allowed list
            market = summary['MarketName']
            buyorders = buysellorders(market,'BuyOrders') #Get the size of big buy orders from history
            sellorders = buysellorders(market,'SellOrders')  #Get the size of big sell orders from history
            buyorderbook = c.get_orderbook(market, 'buy').json()['result'][:50]  #getting buy orders history last 50 orders
            buycount = 0
            buysum = 0
            for buyorder in buyorderbook:  #Counting how much big buy orders we have in history
                buyamount = buyorder['Quantity']
                if buyamount >= buyorders:
                    buycount += 1
                    buysum = buyamount + buysum
            buytotalsumm = buysum  #total summ of BUY orders on the market
            buycountresult = buycount

            sellorderbook = c.get_orderbook(market, 'sell').json()['result'][:50]  #getting sell orders history last 50 orders
            sellcount = 0
            sellsum = 0
            for sellorder in sellorderbook:   #Counting how much big buy orders we have in history
                sellamount = sellorder['Quantity']
                if sellamount >= sellorders:
                    sellcount += 1
                    sellsum = sellamount + sellsum
            selltotalsumm = sellsum  #total summ of SELL orders on the market
            sellcountresult = sellcount
            #Candle analisys
            lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
            currentlow = float(lastcandle[0]['L'])
            currentopen = float(lastcandle[0]['O'])
            currentclose = float(lastcandle[0]['C'])
            previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
            prevlow = float(previouscandle[0]['L'])
            prevopen = float(previouscandle[0]['O'])
            prevclose = float(previouscandle[0]['C'])
            currtime = time.ctime()
            timestamp = int(time.time())
            #print timestamp


            """                 ####Insert operation
            try:
                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                cursor = db.cursor()
                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, market))
                db.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            finally:
                db.close()"""


            """                ##### Read operation
                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM orders WHERE market = '%s'" % market)
                    r = cursor.fetchall()
                    for row in r:
                        market = row[1]
                        date = row[5]
                        active = row[4]
                        #print "market=%s, date=%s, active=%d" % (market, date, active)
                        print market, date, active
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                    #####"""


###################

####################
            day_close = summary['PrevDay']   #Getting day of closing order
        #Current prices
            last = float(summary['Last'])  #last price
            bid = float(summary['Bid'])    #sell price
            ask = float(summary['Ask'])    #buy price
        #How much market has been changed
            percent_chg = ((last / day_close) - 1) * 100
        #HOW MUCH TO BUY
            buy_quantity = buy_size / last
            buy_quantity2 = buy_size2 / last
        #BOUGHT PRICE
            bought_price = get_closed_orders(market, 'PricePerUnit')
        #Bought Quantity need for sell order, to know at which price we bought some currency
            bought_quantity = get_closed_orders(market, 'Quantity')
            sell_quantity = bought_quantity

            ##FOR SQL MODE
            bought_price_sql = float(status_orders(market, 3))
            #bought_price_sql = float(bought_price_sql_1)
            #print market, (type(bought_price_sql), bought_price_sql)
            bought_quantity_sql = float(status_orders(market, 2))
            sell_quantity_sql = bought_quantity_sql
            active = active_orders(market)



            #print time.ctime(), market, buycountresult, sellcountresult


#####---------------------##################################
##
##STOP LOSS MODE     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###
####----------------------################################
            # Bot works in STOP_LOSS mode. It means that sell orders will be opened by 0.001 BTC and closed after losing 50%.
            if stop_loss == 1:

                        #################################BUYING ALGORITHM#####################
            ###################################################################################################
#If the price for some currency rapidly increased from 25% till 50%  let`s buy something too
                if 25 < percent_chg < 50:  #should start from 25
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']

                #print active
                #print float(status_orders(market, 2))
                #print market, current_balance
            # Check if we have open orders or some unsold currency
                    if has_open_order(market, 'LIMIT_BUY'):
                        print('Order already opened to buy  ' + market)
                        try:
                            printed = ('Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    elif current_balance is not None and current_balance != 0.0:
                        print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(format_float(current_balance)) + '  ' + market +  ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                # For stop loss ==1

                    elif active == 1 and sql == 1:
                        print ('We already have ' + str(float(status_orders(market, 2))) +' units of ' + market +  ' on our balance')
                        try:
                            printed = ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    else:
                #Buy some currency
                    #print active
                        print('Purchasing ' + str(format_float(buy_quantity)) +' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing ' + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            if sql == 1:
                                cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1"))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                #print c.buy_limit(market, buy_quantity, last).json()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################



#If we have twice more BIG buy orders then BIG sell Orders, and volume of BUY order is twice bigger then volume of sell orders, it means that price is growing, Let` buy something

                elif buytotalsumm > selltotalsumm*2 and buycountresult > sellcountresult*2:  #should be *2 on both
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    active = active_orders(market)
                #print active
                #print float(status_orders(market, 2))
                # Check if we have open orders or some unsold currency
                    if has_open_order(market, 'LIMIT_BUY'):
                        print('Order already opened to buy  ' + market)
                        try:
                            printed = ('Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    elif current_balance is not None and current_balance != 0.0:
                        print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market +  ' on our balance')
                        try:
                            printed = ('We already have ' + str(format_float(current_balance)) + '  ' + market +  ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                #For SQL storing (TESTING)
                    elif active == 1 and sql == 1:
                        print ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


                    else:
                    # Buy some currency
                    #print active
                        print('Purchasing ' + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing ' + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed ))
                            if sql == 1:
                                cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1"))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                    # print c.buy_limit(market, buy_quantity, last).json()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################


                        #################################SELLING ALGORITHM#####################
                    ################################################################################
#Check if we have this currency for sell
                if sql == 0:
                    if bought_price != None:
                        balance_res = get_balance_from_market(market)
                        current_balance = balance_res['result']['Available']
                        #print market, bought_price, bought_price_sql

                # check current balance
                #print market,  current_balance, sell_quantity

                        if current_balance is None or current_balance == 0.0:  #active for SQL testing
                            #print market, bought_quantity_sql, current_balance
                            pass
                    # If curent balance of this currency more then zero
                        elif current_balance > 0:  #active for SQL testing
                            #print market, current_balance, bought_quantity_sql
                ##Check if we have completelly green candle
                            if currentopen == currentlow and prevclose <= currentopen:
                                print (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                                try:
                                    printed = (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            elif currentopen == prevclose and last > bought_price*profit:
                                print ("We have good trend for " + market)
                                try:
                                    printed = ("We have good trend for " + market)
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            else:
#If  we got our profit, lets sell this shitcoins
#!!!!!!!!!!!
## "TAKE PROFIT" MECHANIZM - we can take our percent from profit variable and sell currency
                                if last >= bought_price*profit:  #should be >=  + added status orders for SQL testing

                    # Lets Sell some
                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                    else:
                                        print('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask*bought_quantity - bought_price*bought_quantity)) + ' BTC' + ' or ' + str(format_float((ask*bought_quantity - bought_price*bought_quantity)*BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask-bought_price)) + ' BTC')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
 #                      print c.sell_limit(market, sell_quantity, last).json()
#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


#"STOP LOSS" MECHANIZM. WE should sell failed currency before price goes down and reach min selling limit. If sell now we are losing 50%. If not - we will lose 100% of order`s cost
                                elif last < bought_price and sell_size <= sell_quantity*last:

                        # Lets Sell some
                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                    else:
                                        print ('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask*bought_quantity - bought_price*bought_quantity)) + ' BTC' ' or ' + str(format_float((ask*bought_quantity - bought_price*bought_quantity)*BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask-bought_price)) + ' BTC')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()

#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                #   print c.sell_limit(market, sell_quantity, last).json()
#########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        else:
                            pass

                    else:
                        pass
                else:
                    if bought_price_sql != None:
                        #balance_res = get_balance_from_market(market)
                        #current_balance = balance_res['result']['Available']
                        # print market, bought_price, bought_price_sql

                        # check current balance
                        # print market,  current_balance, sell_quantity

                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # active for SQL testing
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0.0:  # active for SQL testing
                            # print market, current_balance, bought_quantity_sql
                            ##Check if we have completelly green candle
                            if currentopen == currentlow and prevclose <= currentopen:
                                print (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                                try:
                                    printed = (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            elif currentopen == prevclose and last > bought_price_sql * profit:
                                print ("We have good trend for " + market)
                                try:
                                    printed = ("We have good trend for " + market)
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            else:
                                # If  we got our profit, lets sell this shitcoins
                                # !!!!!!!!!!!
                                ## "TAKE PROFIT" MECHANIZM - we can take our percent from profit variable and sell currency
                                if last >= bought_price_sql * profit:  # should be >=  + added status orders for SQL testing

                                    # Lets Sell some
                                        print('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask - bought_price_sql)) + ' BTC')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                            #                      print c.sell_limit(market, sell_quantity, last).json()
                                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


                                            # "STOP LOSS" MECHANIZM. WE should sell failed currency before price goes down and reach min selling limit. If sell now we are losing 50%. If not - we will lose 100% of order`s cost
                                elif last < bought_price_sql and sell_size <= sell_quantity_sql * last:  # added for SQL testing

                                        print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask - bought_price_sql)) + ' BTC')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()

                                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                            #   print c.sell_limit(market, sell_quantity, last).json()
                                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        else:
                            pass

                    else:
                        pass

                #####---------------------#################!!!!!!!!!!!!!!
##
##FIBONACI MODE         !!!!!!!!!!!!!!!!!!!
##
####----------------------################!!!!!!!!!!!!!!!

            else:
                # Bot works in FIBONACI mode. It means that sell orders will be opened by 0.0005 BTC and reopened again and again till he gain his profit
                #################################BUYING ALGORITHM#####################
                ###################################################################################################
                # If the price for some currency rapidly increased from 25% till 50%  let`s buy something too
                if 5 < percent_chg < 50:  # should start from 25
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    active = active_orders(market)
                    # print active
                    # print float(status_orders(market, 2))
                    # print market, current_balance
                    # Check if we have open orders or some unsold currency
                    if has_open_order(market, 'LIMIT_BUY'):
                        print('Order already opened to buy  ' + market)
                        try:
                            printed = ('Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    elif current_balance is not None and current_balance != 0.0:
                        print(
                        'We already have ' + str(format_float(current_balance)) + '  ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(format_float(current_balance)) + '  ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                            # For stop loss ==1
                    elif active == 1:
                        print ('We already have ' + str(
                            float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    else:
                        # Buy some currency
                        # print active
                        print('Purchasing ' + str(format_float(buy_quantity2)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing ' + str(format_float(buy_quantity2)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1"))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, buy_quantity2, last).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################



                            # If we have twice more BIG buy orders then BIG sell Orders, and volume of BUY order is twice bigger then volume of sell orders, it means that price is growing, Let` buy something

                elif buytotalsumm > selltotalsumm and buycountresult > sellcountresult:  # shuld be *2 on both
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    active = active_orders(market)
                    # print active
                    # print float(status_orders(market, 2))
                    # Check if we have open orders or some unsold currency
                    if has_open_order(market, 'LIMIT_BUY'):
                        print('Order already opened to buy  ' + market)
                        try:
                            printed = ('Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    elif current_balance is not None and current_balance != 0.0:
                        print(
                        'We already have ' + str(format_float(current_balance)) + '  ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(format_float(current_balance)) + '  ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                            # For stop loss ==1
                    elif active == 1:
                        print ('We already have ' + str(
                            float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                        try:
                            printed = ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


                    else:
                        # Buy some currency
                        # print active
                        print('Purchasing ' + str(format_float(buy_quantity2)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing ' + str(format_float(buy_quantity2)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1"))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, buy_quantity2, last).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################


                            #################################SELLING ALGORITHM#####################
                            ################################################################################
                            # Check if we have this currency for sell
                if bought_price != None:
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    # check current balance
                    # print market,  current_balance, sell_quantity
                    if current_balance is None or current_balance == 0.0:
                        pass
                    # If curent balance of this currency more then zero
                    elif current_balance > 0:
                        # print market, current_balance, open, low, prevclose
                        ##Check if we have completelly green candle
                        if open == currentlow and prevclose <= currentopen:
                            print (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                            try:
                                printed = (" We have GREEN candle for " + market + " and it is better to wait, before sell")
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            pass

                        elif open == prevclose and last > bought_price * profit:
                            print ("We have good trend for " + market)
                            try:
                                printed = ("We have good trend for " + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            pass

                        else:
                            # If  we got our profit, lets sell this shitcoins
                            # !!!!!!!!!!!
                            ## "TAKE PROFIT" MECHANIZM - we can take our percent from profit variable and sell currency
                            if last >= bought_price * profit:  # should be >=

                                # Lets Sell some
                                if has_open_order(market, 'LIMIT_SELL'):
                                    print('Order already opened to sell  ' + market)
                                    try:
                                        printed = ('Order already opened to sell  ' + market)
                                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                        db.commit()
                                    except MySQLdb.Error, e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()
                                else:
                                    print('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity - bought_price * bought_quantity)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity - bought_price * bought_quantity) * BTC_price)) + ' USD')
                                    try:
                                        printed = ('Selling ' + str(format_float(sell_quantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask - bought_price)) + ' BTC')
                                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                        currtime, printed))
                                        db.commit()
                                    except MySQLdb.Error, e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        #                      print c.sell_limit(market, sell_quantity, last).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                            else:
                                pass


                    else:
                        pass
                else:
                    pass




### FUNCTIONS
###############################################################################################################
#Check active orders in mysql
def active_orders(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE  market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[4])

    return 0


#Check the status of active orders
# 2 - is quantity, 3 -is price, 4 - active/passive
def status_orders(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0



#Allowed currencies function
def market_list(marketname):
    allowed_markets = available_markets
    for markets in allowed_markets:
        if markets['MarketName'] == marketname:
            return True

    return False



#function for getting "Big" values for sell and buy for each market
def buysellorders(marketname, value):
    allowed_markets = available_markets
    for markets in allowed_markets:
        if markets['MarketName'] == marketname:
            return markets[value]

    return False


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



#def get_candles(self, market, tick_interval):
#    return self._api_query(path_dict={
#        'v2.0': '/pub/market/GetTicks'
#    }, options={
#        'marketName': market, 'tickInterval': tick_interval
#    }, protection='pub')


def get_candles(market, tick_interval):
    url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market +'&tickInterval=' + str(tick_interval)
    return signed_request(url)


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()




def format_float(f):
    return "%.8f" % f


if __name__ == "__main__":
    main()