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


#Setup tick interval
#TICK_INTERVAL = 60  # seconds


#The main function
def main():
    print('Starting trader bot')

    tick()

#Running clock forever for testing purposes
    #while True:
        #start = time.time()
        #tick()
        #end = time.time()
        # Sleep the thread if needed
        #if end - start < TICK_INTERVAL:
        #    time.sleep(TICK_INTERVAL - (end - start))



##################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    buy_size2 = parameters()[1]  # The size for opening orders for FIBONACI Mode
    sell_size = parameters()[2]  #Minimal size for closing oders
    profit = parameters()[3]  #The size of profit we want to take
    stop_loss = parameters()[4]  #If stop_loss==1 we use stop loss mechanism, of not - we use fibonachi mechanism
    maxiteration = parameters()[5]
    order_multiplier = parameters()[6]
    min_percent_chg = parameters()[7]
    max_percent_chg = parameters()[8]
    last_orders_quantity = int(parameters()[9])
    stop_bot = int(parameters()[10])

    market_summ = c.get_market_summaries().json()['result']
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']



    #global active
    for summary in market_summ: #Loop trough the market summary
        if available_market_list(summary['MarketName']):
            market = summary['MarketName']
            buyorders = buysellorders_sql(market, 2)
            sellorders = buysellorders_sql(market, 3)
            #print market, buyorders, sellorders
            buyorderbook = c.get_orderbook(market, 'buy').json()['result'][:last_orders_quantity]  #getting buy orders history last 150 orders
            buycount = 0
            buysum = 0
            for buyorder in buyorderbook:  #Counting how much big buy orders we have in history
                buyamount = buyorder['Quantity']
                if buyamount >= buyorders:
                    buycount += 1
                    buysum = buyamount + buysum
            buytotalsumm = buysum  #total summ of BUY orders on the market
            buycountresult = buycount

            sellorderbook = c.get_orderbook(market, 'sell').json()['result'][:last_orders_quantity]  #getting sell orders history last 150 orders
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
            fiboquantity = float(quantity_orders(market))
            fiboquantity2 = float(quantity_orders(market)*2)
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
            bought_quantity_sql = float(status_orders(market, 2))
            sell_quantity_sql = bought_quantity_sql
            active = active_orders(market)
            iteration = int(iteration_orders(market))
            timestamp_old = int(timestamp_orders(market))




           # print market, ai_prediction(market)
            #print market, percent_chg


            ########
            #price_for_sql = c.get_ticker(market).json()['result']['Last']
            # print market, price_for_sql
            try:
                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                cursor = db.cursor()
                cursor.execute("update parameters set usdt_btc_price = %s where id = %s", (BTC_price, 1))
                prev_serf = previous_serf(market)
                serf = (last * bought_quantity_sql - bought_price_sql * bought_quantity_sql+prev_serf)
                cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
                cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf*BTC_price, market))
                db.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            finally:
                db.close()
                ########

            #print market, prev_serf, serf


#####---------------------################################
##
##STOP LOSS MODE     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###
####----------------------################################
            # Bot works in STOP_LOSS mode. It means that sell orders will be opened by 0.001 BTC and closed after losing 50%.
            if stop_loss == 1:

                        #################################BUYING ALGORITHM#####################
            ###################################################################################################
#If the price for some currency rapidly increased from 25% till 50%  let`s buy something too
                if min_percent_chg < percent_chg < max_percent_chg and stop_bot == 0:  # 0.8 - 3.5
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
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



                    elif active == 1:
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
                        print('Purchasing ' + str(format_float(buy_quantity)) +' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing (by market analize) ' + str(format_float(percent_chg)) + ' percent changed ' + str(format_float(buy_quantity)) + '  |  ' + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1", 'Market Analize:  % change ' + str(format_float(percent_chg))))
                            #cursor.execute('insert into orders(market_id, quantity, price, active, date, timestamp, iteration) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (select id from markets where name=market, buy_quantity, bid, "1", currtime, timestamp, "1")))
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

                elif buytotalsumm > selltotalsumm*order_multiplier and buycountresult > sellcountresult*order_multiplier and buytotalsumm !=0 and selltotalsumm !=0 and buycountresult !=0 and sellcountresult !=0 and stop_bot == 0:  #should be *2 on both
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    buysummpercent = float(buytotalsumm/selltotalsumm)
                    buycountpercent = float(buycountresult/sellcountresult)

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
                    elif active == 1:
                        print ('We already have ' + str(float(status_orders(market, 2))) + ' units of this ' + market + ' on our balance')
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
                        print('Purchasing ' + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(bid)))
                        try:
                            printed = ('Purchasing (by order analize) '+ ' Total Summ ' + str(format_float(buycountpercent)) + ' Total Count ' + str(format_float(buy_quantity)) + '  |  ' + ' units of ' + market + ' for ' + str(format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed ))
                            cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, bid, "1", currtime, timestamp, "1", 'OA: '+ str(format_float(buysummpercent)) + ' TSumm ' + str(format_float(buycountpercent)) + ' TCount '))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                    # print c.buy_limit(market, buy_quantity, last).json()
#########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

                else:
                    pass
                        #################################SELLING ALGORITHM#####################
                    ################################################################################
#Check if we have this currency for sell

                if bought_price_sql != None or bought_price != None:   #added OR
                        balance_res = get_balance_from_market(market)
                        current_balance = balance_res['result']['Available']


                        # check current balance

                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0:  # Need to add bought_quantity without sql
                            ##Check if we have completelly green candle
                            if currentopen == currentlow and prevclose <= currentopen:
                                print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
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

                            elif currentopen == prevclose and last > bought_price_sql * profit:  ## Need to add bought_price without sql
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
                                if last >= bought_price_sql * profit:  ## Need to add bought_price without sql

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
                                    # Lets Sell some
                                        print('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask - bought_price_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            cursor.execute('update orders set active = 0, reason_close = "Take profit" where market =("%s")' % market)
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
                                elif last < bought_price_sql and sell_size >= sell_quantity_sql * last:  # # Need to add bought_price without sql and sell_quantity without sql

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
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


                                    else:

                                        print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask - bought_price_sql)) + ' BTC')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                            cursor.execute('update orders set active = 0, reason_close = "Stop Loss" where market =("%s")' % market)
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


#####---------------------##################################
##
##FIBONACCI MODE     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###
####----------------------################################
#Bot works in FIBONACCI MODE. It means that sell orders will be opeened by 0.0005 BTC and if fail, will be reopened with twice bigger quantity of the same currency
            elif stop_loss == 0:
                # Bot works in FIBONACI mode. It means that sell orders will be opened by 0.0005 BTC and reopened again and again till he gain his profit
                #################################BUYING ALGORITHM#####################
                ###################################################################################################
                # If the price for some currency rapidly increased from 0.8% till 3.5%  let`s buy something too
                if min_percent_chg < percent_chg < max_percent_chg  and stop_bot == 0:  # 0.8 - 3.5  #and ai_prediction(market)=='UP'
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']

                #If we have opened order on bitrex
                    if has_open_order(market, 'LIMIT_BUY'):
                        #print('Order already opened to buy  ' + market)
                        try:
                            printed = ('1 - Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    #If we have some currency on the balance
                    elif current_balance is not None and current_balance != 0.0:
                        #print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                        try:
                            printed = ('2 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market +  ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


                    #if we have some active orders in sql
                    elif active == 1 and iteration != 0:
                        #print ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                        try:
                            printed = ('3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
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
                        # Buy some currency by market analize first time
                        try:
                            printed = ('4- Purchasing (by market analize) ' + str(
                                format_float(percent_chg)) + ' percent changed ' + '  |  ' + str(
                                format_float(buy_quantity2))  + ' units of ' + market + ' for ' + str(
                                format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity2, bid, "1", currtime, timestamp, "1",'Market Analize:  % change ' + str(format_float(percent_chg)) + '  AI   ' + str(ai_prediction(market)) ))   #+ '  AI   ' + str(ai_prediction(market))
                            cursor.execute("update orders set serf = %s where market = %s and active =1",(serf, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, fiboquantity*2, last).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################



                            # If we have twice more BIG buy orders then BIG sell Orders, and volume of BUY order is twice bigger then volume of sell orders, it means that price is growing, Let` buy something

                elif buytotalsumm > selltotalsumm * order_multiplier and buycountresult > sellcountresult * order_multiplier and buytotalsumm != 0 and selltotalsumm != 0 and buycountresult != 0 and sellcountresult != 0 and stop_bot ==0 :  # should be *2 on both  ##and ai_prediction(market)=='UP'
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']
                    buysummpercent = float(buytotalsumm / selltotalsumm)
                    buycountpercent = float(buycountresult / sellcountresult)

                    # Check if we have open orders or some unsold currency
                    if has_open_order(market, 'LIMIT_BUY'):
                        #print('Order already opened to buy  ' + market)
                        try:
                            printed = ('5 - Order already opened to buy  ' + market)
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
                        #print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                        try:
                            printed = ('6 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market +  ' on our balance')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                        # For SQL storing (TESTING)
                    elif active == 1 and iteration != 0:
                        # print market, active
                        #print ('We already have ' + str(float(status_orders(market, 2))) + ' units of this ' + market + ' on our balance')
                        try:
                            printed = ('7 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
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
                        # Buy some currency by order analize for first time
                        try:
                            printed = ('8 - Purchasing (by order analize) ' + ' Total Summ ' + str(
                                format_float(buycountpercent)) + ' Total Count ' + str(
                                format_float(buy_quantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                                format_float(bid)))
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            cursor.execute(
                                'insert into orders(market, quantity, price, active, date, timestamp, iteration, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                market, buy_quantity2, bid, "1", currtime, timestamp, "1",
                                'OA: ' + str(format_float(buysummpercent)) + ' TSumm ' + str(
                                    format_float(buycountpercent)) + ' TCount ' + '  AI   ' + str(ai_prediction(market))))  ## + '  AI   ' + str(ai_prediction(market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, buy_quantity2, last).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################



                else:
                    pass

                    #################################SELLING ALGORITHM#####################
                    ################################################################################
                    # Check if we have this currency for sell


                if bought_price_sql != None or bought_price != None:  # added OR
                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Available']


                    if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                        # print market, bought_quantity_sql, current_balance
                        pass
                        # If curent balance of this currency more then zero
                    elif bought_quantity_sql > 0 and iteration == 1:  # Need to add bought_quantity without sql
                        ##Check if we have completelly green candle
                        if currentopen == currentlow and prevclose <= currentopen:

                            #print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                            try:
                                printed = (
                                "9 - We have GREEN candle for " + market + " and it is better to wait, before sell")
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            pass

                        elif currentopen == prevclose and last > bought_price_sql * profit:  ## Need to add bought_price without sql
                            #print ("We have good trend for " + market)

                            try:
                                printed = ("10 - We have good trend for " + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            pass

                        # If  we got our profit, lets sell this shitcoins
                        # !!!!!!!!!!!
                        ## "TAKE PROFIT" MECHANIZM FOR FIRST ITERATION - we can take our percent from profit variable and sell currency

                        else:

                            if last >= bought_price_sql * profit:  ## Need to add bought_price without sql
                                #if we have already opened order to sell
                                if has_open_order(market, 'LIMIT_SELL'):
                                    #print('Order already opened to sell  ' + market)
                                    try:
                                        printed = ('11 - Order already opened to sell  ' + market)
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


                                else:
                                    # Lets Sell some
                                    #print('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                    try:
                                        printed = ('12 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                        currtime, printed))
                                        cursor.execute('update orders set active = 0, reason_close = "Take profit" where market =("%s")' % market)
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



                #print market, last*bought_quantity_sql*2, bought_price_sql*bought_quantity_sql+prev_serf

                if serf < 0 and (timestamp-timestamp_old > 60000) and active == 1 and  iteration < maxiteration :  #should be 600000 , check if we have active order with minus profit and older then 1 week   :   and last*1.1 < bought_price_sql
                    #print market, "Has old order"
                    run_prediction = "python2.7 run_predict.py " + market
                    p = subprocess.Popen(run_prediction, stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p_status = p.wait()
                    print "Command output: " + output

                    if (min_percent_chg < percent_chg < max_percent_chg) and (ai_prediction(market)=='UP' or ai_prediction(market)=='NEUTRAL'):
                        #print "Buying by Market analize"
                        if has_open_order(market, 'LIMIT_BUY'):
                            #print('13 - Order already opened to buy  ' + market)
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

                        else:
                            newiteration = iteration + 1
                            # Buy some currency
                            #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)))
                            try:
                                printed = ('14 - Purchasing (by market analize) ' + str(format_float(percent_chg)) + ' percent changed ' + '  |  ' +  str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  AI   ' + str(ai_prediction(market)))
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                current_serf = previous_serf(market)
                                prev_serf = ((last * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                                cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                                cursor.execute("update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s where market = %s and active = 1", (fiboquantity+fiboquantity2, last, timestamp, newiteration, market))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                                #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                                # print c.buy_limit(market, fiboquantity2, last).json()
                                #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

                    elif buytotalsumm > selltotalsumm*order_multiplier and buycountresult > sellcountresult*order_multiplier and buytotalsumm !=0 and selltotalsumm !=0 and buycountresult !=0 and sellcountresult !=0 and (ai_prediction(market)=='UP' or ai_prediction(market)=='NEUTRAL'):  #
                        #print "Buying by order analize"

                        if has_open_order(market, 'LIMIT_BUY'):
                            #print('Order already opened to buy  ' + market)
                            try:
                                printed = ('15 - Order already opened to buy  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                        else:
                            newiteration = iteration + 1
                            # Buy some currency
                            #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)))
                            try:
                                printed = ('16 - Purchasing (by market analize) ' + str(
                                    format_float(percent_chg)) + ' percent changed ' + str(
                                    format_float(fiboquantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                                    format_float(last)))
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                current_serf = previous_serf(market)
                                prev_serf = ((last * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                                cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                                cursor.execute(
                                    "update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s where market = %s and active = 1",
                                    (fiboquantity + fiboquantity2, last, timestamp, newiteration, market))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                                #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                                # print c.buy_limit(market, fiboquantity2, last).json()
                                #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                    else:
                        pass

                    if iteration != 1:  #
                        # print market, current_balance, bought_quantity_sql
                        ##Check if we have completelly green candle
                        if currentopen == currentlow and prevclose <= currentopen:
                            #print ("We have GREEN candle for " + market + " and let`s wait it to be up")
                            try:
                                printed = (
                                    "17 - We have GREEN candle for " + market + " and let`s wait it to be up")
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            pass

                        elif currentopen == prevclose:  ## Need to add bought_price without sql
                            #print (" We have good trend for " + market)
                            try:
                                printed = ("18 - We have good trend for " + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
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
                            if last*bought_quantity_sql >= bought_price_sql*bought_quantity_sql*profit+prev_serf:  ## Need to add bought_price without sql

                                if has_open_order(market, 'LIMIT_SELL'):
                                    #print('Order already opened to sell  ' + market)
                                    try:
                                        printed = ('19 - Order already opened to sell  ' + market)
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
                                    # Lets Sell some
                                    #print('Selling ' + str(format_float(fiboquantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(format_float((ask * fiboquantity - bought_price_sql * fiboquantity) * BTC_price)) + ' USD')
                                    try:
                                        printed = ('20 - Selling ' + str(format_float(bought_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(format_float((ask * fiboquantity - bought_price_sql * fiboquantity) * BTC_price)) + ' USD')
                                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                        cursor.execute('update orders set active = 0, reason_close = "Take profit " where market =("%s")' % market)
                                        db.commit()
                                    except MySQLdb.Error, e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        #                      print c.sell_limit(market, fiboquantity, last).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                            else:
                                pass

                elif last < bought_price_sql and last * bought_quantity_sql*1.05 < (bought_price_sql * bought_quantity_sql + prev_serf) and iteration == maxiteration:  # # Need to add bought_price without sql and sell_quantity without sql

                        if has_open_order(market, 'LIMIT_SELL'):
                            #print('Order already opened to sell  ' + market)
                            try:
                                printed = ('21 - Order already opened to sell  ' + market)
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

                            #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                            try:
                                printed = ('22 -Selling ' + str(
                                    format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                    format_float(ask)) + '  and losing  ' + str(
                                    format_float(serf)) + ' USD')
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                cursor.execute('update orders set reason_close = "Stop loss" where active=1 and market =("%s")' % market)
                                cursor.execute(
                                    'update orders set active = 0 where market =("%s")' % market)
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                                #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                #   print c.sell_limit(market, sell_quantity, last).json()
                                #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################



                elif serf > 0 and active == 1 and iteration !=1:
                    if currentopen == currentlow and prevclose <= currentopen:
                        #print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                        try:
                            printed = (
                                "23 - We have GREEN candle for " + market + " and it is better to wait, before sell")
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        pass

                    elif currentopen == prevclose and last*bought_quantity_sql >= bought_price_sql*bought_quantity_sql*profit+prev_serf:  ## Need to add bought_price without sql
                        #print (" We have good trend for " + market)
                        try:
                            printed = ("24 -We have good trend for " + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
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
                        if last*bought_quantity_sql >= bought_price_sql*bought_quantity_sql*profit+prev_serf:  ## Need to add bought_price without sql

                            if has_open_order(market, 'LIMIT_SELL'):
                                #print('Order already opened to sell  ' + market)
                                try:
                                    printed = ('25 - Order already opened to sell  ' + market)
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()


                            else:
                                # Lets Sell some
                                #print('Selling ' + str(format_float(fiboquantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(format_float((ask * fiboquantity - bought_price_sql * fiboquantity) * BTC_price)) + ' USD')
                                try:
                                    printed = ('26 - Selling ' + str(
                                        format_float(bought_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                        format_float(ask)) + '  and getting  +' + str(
                                        format_float(ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(format_float(
                                        serf)) + ' USD')
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                    cursor.execute(
                                        'update orders set active = 0, reason_close = "Take profit " where market =("%s")' % market)
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                    #                      print c.sell_limit(market, fiboquantity, last).json()
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        else:
                            pass

                else:
                    pass


##Fibonacci mode ends
            else:
                pass

        else:
            pass


### FUNCTIONS
###############################################################################################################
#Allowed currencies function for SQL
def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


def buysellorders_sql(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False




def parameters():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[10]), (row[11]), (row[12])

    return 0



def ai_prediction(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_direction FROM markets WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])

    return 0




def quantity_orders(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[2])

    return 0


def previous_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT prev_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0


def last_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0



#Check active orders in mysql
def timestamp_orders(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[6])

    return 0


#Check first iteration orders in mysql
def iteration_orders(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[7])

    return 0


#Check active orders in mysql
def active_orders(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
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
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0






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


def format_float(f):
    return "%.4f" % f


if __name__ == "__main__":
    main()
