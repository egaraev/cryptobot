#Imports from modules, libraries and config files
import config
from operator import itemgetter
import json, ast
from pybittrex.client import Client
import requests
import time
import datetime
import yaml
import numpy
import hmac
import hashlib
import MySQLdb
import sys
import subprocess
import smtplib
c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file
#Setup tick interval
#TICK_INTERVAL = 30  # seconds
#The main function
def main():
    print('Starting trader bot')



    tick()
#Running clock forever for testing purposes
#    while True:
#        start = time.time()
#        tick()
#        end = time.time()
        # Sleep the thread if needed
#        if end - start < TICK_INTERVAL:
#            time.sleep(TICK_INTERVAL - (end - start))
################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    buy_size2 = parameters()[1]  # The size for opening orders for FIBONACI Mode
    sell_size = parameters()[2]  #Minimal size for closing oders
    profit = parameters()[3]  #The size of profit we want to take
    stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
    maxiteration = parameters()[5]
    order_multiplier = parameters()[6]
    min_percent_chg = float(parameters()[7])
    max_percent_chg = float(parameters()[8])
    last_orders_quantity = int(parameters()[10])
    stop_bot = int(parameters()[11])
    market_summ = c.get_market_summaries().json()['result']
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    btc_trend = parameters()[12]
    ai_ha_mode = parameters()[23]

    #print c.get_open_orders('BTC-GAME').json()['result'][0]['OrderUuid']

    #print order_uuid('BTC-GAME')


    #uuid = order_uuid('BTC-GAME')
    #print c.market_cancel(uuid)



    #global active
    for summary in market_summ: #Loop trough the market summary
        try:
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
                currenthigh = float(lastcandle[0]['H'])
                previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                prevlow = float(previouscandle[0]['L'])
                prevopen = float(previouscandle[0]['O'])
                prevclose = float(previouscandle[0]['C'])
                prevhigh = float(previouscandle[0]['H'])

                lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                currentlow5 = float(lastcandle5[0]['L'])
                currentopen5 = float(lastcandle5[0]['O'])
                currentclose5 = float(lastcandle5[0]['C'])
                currenthigh5 = float(lastcandle5[0]['H'])
                previouscandle5 = get_candles(market, 'fivemin')['result'][-2:]
                prevlow5 = float(previouscandle5[0]['L'])
                prevopen5 = float(previouscandle5[0]['O'])
                prevclose5 = float(previouscandle5[0]['C'])
                prevhigh5 = float(previouscandle5[0]['H'])


                lastcandleday = get_candles(market, 'day')['result'][-1:]
                currentlowday = float(lastcandleday[0]['L'])
                currentopenday = float(lastcandleday[0]['O'])
                currentcloseday = float(lastcandleday[0]['C'])
                currenthighday = float(lastcandleday[0]['H'])



                timestamp = int(time.time())
                fiboquantity = float(quantity_orders(market))
                fiboquantity2 = float(quantity_orders(market)*2)
                day_close = summary['PrevDay']   #Getting day of closing order
            #Current prices
                last = float(summary['Last'])  #last price
                bid = float(summary['Bid'])    #sell price
                ask = float(summary['Ask'])    #buy price

                newbid=bid - bid*0.002
                newask=ask + ask*0.002
            #How much market has been changed
                percent_chg = float(((last / day_close) - 1) * 100)
            #HOW MUCH TO BUY
                buy_quantity = buy_size / last
                buy_quantity2 = buy_size2 / last
            #BOUGHT PRICE
                bought_price = get_closed_orders(market, 'PricePerUnit')
            #Bought Quantity need for sell order, to know at which price we bought some currency
                #bought_quantity = get_closed_orders(market, 'Quantity')
                bought_quantity = float(get_balance_from_market(market)['result']['Available'])
                #print market, get_closed_orders(market, 'Quantity'), bought_quantity
                sell_quantity = bought_quantity
                ##FOR SQL MODE
                bought_price_sql = float(status_orders(market, 3))
                bought_quantity_sql = float(status_orders(market, 2))
                sell_signal = status_orders(market, 18)
                sell_quantity_sql = bought_quantity_sql
                active = active_orders(market)
                iteration = int(iteration_orders(market))
                timestamp_old = int(timestamp_orders(market))
                now = datetime.datetime.now()
                currenttime = now.strftime("%Y-%m-%d %H:%M")
                HA_trend=heikin_ashi(market, 10)
                HAD_trend=heikin_ashi(market, 18)
                ha_mode=heikin_ashi(market, 19)
                bot_step = bot_mode(market)

                if (btc_trend == "DOWN" and HA_trend == "DOWN") or (btc_trend == "DANGER") or (HAD_trend == "DOWN"):
                    profit = parameters()[3] / 1.5

                elif (timestamp - timestamp_old > 240000) and (HA_trend!="UP" or HA_trend!="Revers-UP") and iteration==1:
                    profit = parameters()[3] / 3

                elif (timestamp - timestamp_old > 240000) and (HA_trend!="UP" or HA_trend!="Revers-UP") and iteration!=1:
                    profit = parameters()[3] / 4

                else:
                    profit = parameters()[3]

                #print market, last, bid, ask, newbid, newask

                #print market, order_uuid(market)

                #print market, profit

                #print market, get_balance_from_market(market)['result']['Available']   #printing total balance of currency in the wallet

                #print open_sell(market), sell_time(market)
                #orderhistory = c.get_order_history().json()['result']
                #print orderhistory['Exchange']
                #for i in orderhistory:
                #    print "The  orders from history for currency: {0} cost is: {1} uuid is: {2}".format(i['Exchange'],i['OrderType'],i['OrderUuid'])




                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()

                    #cursor.execute("update parameters set usdt_btc_price = %s, btc_ha_direction_day =%s where id = %s", (BTC_price, btc_trend, 1))
                    prev_serf = previous_serf(market)
                    serf = (last * bought_quantity_sql - bought_price_sql * bought_quantity_sql+prev_serf)
                    cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
                    cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf*BTC_price, market))
#                    cursor.execute("update markets set current_price = %s, ha_direction =%s  where market = %s and active =1",(last, HA_trend, market))
                    cursor.execute(
                        "update markets set current_price = %s  where market = %s and active =1",
                        (last, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
                    ########



                #print market, bought_quantity
                if bought_quantity is not None:
                    if has_open_order(market, 'LIMIT_SELL'):
                        # print('Order already opened to sell  ' + market)
                        try:
                            printed = ('    001 - Order already opened to sell  ' + market)
                            uuid = order_uuid(market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            cursor.execute('update orders set uuid =%s where active=1 and open_sell=1 and market =%s', (uuid,market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    elif has_open_order(market, 'LIMIT_BUY'):
                        print('Order already opened to buy  ' + market)
                        try:
                            printed = ('    002 - Order already opened to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                    else:
                        try:
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute("update orders set quantity = %s where market = %s and active =1",(bought_quantity, market))

                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                            ########
                else:
                    pass





# Force Stop
                if stop_bot_force==1 and (bought_quantity_sql != 0.0):
                    #print bought_quantity_sql
                    if has_open_order(market, 'LIMIT_SELL'):
                        print('Order already opened to sell  ' + market)
                        try:
                            printed = ('    32 - Order already opened to sell  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()


                    else:
                        #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                        try:
                            printed = ('    33 Prod -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or losing  ' + str(format_float(serf * BTC_price)) + ' USD')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            # cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                            cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("33 , Force_stop_bot p:    " + str(format_float(newbid)) + "    t:   " + str(currenttime),market))
                            cursor.execute('update orders set active = 0 where market =("%s")' % market)
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        print c.sell_limit(market, sell_quantity, newbid).json()
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                else:
                    pass





                if open_sell(market)==1:

                    if has_open_order(market, 'LIMIT_SELL'):
                        if currtime - sell_time(market) < 4000:
                            #print('Order already opened to sell  ' + market)
                            try:
                                printed = ('    34 - Order already opened to sell  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                        else:
                            #print(' Order cancelled  ' + market)
                            try:
                                printed = ('    35- Order has been cancelled  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'update orders set open_sell = 0  where active=1 and market =("%s")' % market)
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            #########################################CANCEL OLD ORDER#####
                            uuid = order_uuid(market)
                            print c.market_cancel(uuid)
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
                            #############################################################


                    else:
                        try:
                            #print ('    12.1 Prod -This currency has been sold ' + market )
                            printed = ('    36 Prod -This currency has been sold   ' + market )
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            newquantity = get_closed_orders(market, 'Quantity')
                            cursor.execute("update orders set quantity = %s where market = %s and active =1",(newquantity, market))
                            cursor.execute('update orders set active = 0, open_sell = 0  where active =1 and market =("%s")' % market)       # -this is deactivating the order  !!!!
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency sold", printed, "localhost")


                else:
                    pass








                if open_buy(market)==2:

                    if has_open_order(market, 'LIMIT_BUY'):
                        if currtime - buy_time(market) < 600:
                            #print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    34.1 - Order already opened to buy  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                        else:
                            #print(' Order cancelled  ' + market)
                            try:
                                printed = ('    35.1- Order has been cancelled  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'delete from orders  where active=2 and market =("%s")' % market)
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            #########################################CANCEL OLD ORDER#####
                            uuid = order_uuid(market)
                            print c.market_cancel(uuid)
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
                            #############################################################


                    else:
                        try:
                            #print ('    36.1 Prod -This currency has been bought ' + market )
                            printed = ('    36.1 Prod -This currency has been bought   ' + market )
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            cursor.execute("update orders set quantity = %s, price=%s, active=1, date=%s, timestamp=%s, iteration=1, btc_direction=%s, params=%s, heikin_ashi=%s  where market = %s and active =2",(buy_quantity2, last, currenttime, timestamp,btc_trend, 'MA:  % chng ' + str(format_float(percent_chg)) + '  AI   ' + str(ai_prediction(market)) + '  BTC ' + btc_trend, HA_trend, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency bought", printed, "localhost")


                else:
                    pass




                if bought_quantity*1.5<bought_quantity_sql and second_buy(market)==1:
                    if has_open_order(market, 'LIMIT_BUY'):
                       if currtime-second_buy_time(market)<600:
                            #print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    36.3 - Order already opened to buy  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                       else:
                            try:
                                printed = ('    36.4- Order has been cancelled  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                newiteration = iteration - 1
                                cursor.execute("update orders set  iteration = %s, open_buy=0, prev_serf=0, open_buy_time=0 where market = %s and active = 1",(newiteration, market))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                                #########################################CANCEL OLD ORDER#####
                            uuid = order_uuid(market)
                            print c.market_cancel(uuid)
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
                            #############################################################



                    else:
                            try:
                                printed = ('    36.2 Prod - Purchase was not approved for '  + market )
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                newiteration=iteration-1
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute("update orders set  iteration = %s, prev_serf=0, where market = %s and active = 1",
                                    (newiteration, market))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Purchase not approved", printed, "localhost")

                else:
                    pass



#FIRST ITERATION - BUY

### BUY FOR HA_AI mode
                    if ((ha_mode==1 or ai_ha_mode==1) and (stop_bot == 0) and (HA_trend == "UP" or HA_trend == "Revers-UP") and (HAD_trend=="UP" or HAD_trend == "Revers-UP" or HAD_trend == "STABLE") and stop_bot_force == 0):  # and ((dayprevclose>=daycurrentopen or daycurrentopen==daycurrenthigh) is not True) and (currenthigh>currentopen or currentopen<currentclose):  # 0.8 - 3.5  #
                        balance_res = get_balance_from_market(market)
                        current_balance = balance_res['result']['Available']
                        print market
                        # If we have opened order on bitrex
                        if has_open_order(market, 'LIMIT_BUY'):
                            # print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    00001 - Order already opened to buy  ' + market)
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        # If we have some currency on the balance
                        elif current_balance is not None and current_balance != 0.0:
                            # print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                            try:
                                printed = ('    00002 - We already have ' + str(
                                    format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        # if we have some active orders in sql
                        elif active == 1 and iteration != 0:
                            # print ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            try:
                                printed = ('    00003 - We already have ' + str(
                                    float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        else:
                            # Buy some currency by market analize first time
                            try:
                                printed = ('    00004- Trying to Purchase (by ai_ha) ' + str(
                                    format_float(buy_quantity2)) + ' units of ' + market + ' for ' + str(
                                    format_float(bid)))
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                        market, buy_quantity2, bid, "1", currenttime, timestamp, "1", btc_trend,
                                        '  AI   ' + str(
                                            ai_prediction(market)) + '  BTC ' + btc_trend,
                                        HA_trend))  # + '  AI   ' + str(ai_prediction(market))
                                cursor.execute(
                                    "update orders set serf = %s, one_step_active =1 where market = %s and active =2",
                                    (serf, market))
                                db.commit()
                            except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, fiboquantity*2, last).json()
                            print c.buy_limit(market, buy_quantity2, newask).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!##################################

 ### FOR HA_AI mode - END


 # AI_HA MODE SELL START
                    if bought_price_sql != None or bought_price != None and ai_ha_mode == 1:  # added OR
                        balance_res = get_balance_from_market(market)
                        current_balance = balance_res['result']['Available']

                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0 and iteration == 1:  # Need to add bought_quantity without sql
                            ##Check if we have completelly green candle
                            if (
                                            currentopen <= currentlow and prevclose <= currentopen and currentopen < currenthigh and last > prevclose) or (
                                        currentopen <= currentlow and currentopen < currenthigh and last > prevclose):

                                # print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                                try:
                                    printed = (
                                        "    00009 - We have GREEN candle for " + market + " and let`s wait it to be up")
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (
                                            currenttime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            # elif currentopen5 == prevclose5 and currenthigh5 > currentopen5:  ## Need to add bought_price without sql
                            elif (
                                            currentopen5 <= currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5) or (
                                        currentopen5 <= currentlow5 and currentopen5 < currenthigh5 and last > prevclose5):
                                # print ("We have good trend for " + market)

                                try:
                                    printed = ("    000010 - We have good short term trend for " + market)
                                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (
                                            currenttime, printed))
                                    db.commit()
                                except MySQLdb.Error, e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                pass

                            else:

                                if (active == 1) and (
                                                HA_trend == 'DOWN' or HA_trend == 'Revers-DOWN') and last > bought_price_sql * (
                                            1 + profit / 2) and bot_step==1:  # # WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    0000241 - Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    0000251 -Trying to sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and get   ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                (
                                                    "0000251 HA SELL, p:   " + str(
                                                        format_float(last)) + "   t:    " + str(currenttime),
                                                    market))
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            newvalue = summ_serf() + serf * BTC_price
                                            cursor.execute(
                                                'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                             "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                                elif (active == 1) and (
                                                            market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCH' and ai_prediction(
                                                market) != 'NEUTRAL' and ai_prediction(
                                            market) == 'DOWN') and last > bought_price_sql * (
                                            1 + profit / 2) and bot_step==1:  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    00013 - Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    00014 -Trying to sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and get   ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                (
                                                    "000014 AI SELL, price:  " + str(
                                                        format_float(last)) + "  time:   " + str(
                                                        currenttime), market))
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                             "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################



                                elif (active == 1) and last > bought_price_sql * (
                                        1 + profit / 2) and bot_step == 1:  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    00015 - Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    00016 -Trying to Sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and get   ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                (
                                                    "000016 TP SELL, price:  " + str(
                                                        format_float(last)) + "  time:   " + str(
                                                        currenttime), market))
                                            cursor.execute(
                                                'update orders set active = 0 where market =("%s")' % market)
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            newvalue = summ_serf() + serf * BTC_price
                                            cursor.execute(
                                                'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                    currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                             "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


                                elif (active == 1) and (last * bought_quantity_sql * (1 + profit / 2) < (
                                            bought_price_sql * bought_quantity_sql)) and bot_step == 1 and sell_signal == 1:  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('   00001615 Trying to Sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and lose  ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                ("00001615  SL, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))
                                            cursor.execute(
                                                'update orders set active = 0 where market =("%s")' % market)
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            newvalue = summ_serf() + serf * BTC_price
                                            cursor.execute(
                                                'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                    currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                             "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                                elif (active == 1) and serf > 0 and bot_step == 1 and sell_signal == 1:  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('  00001620 Trying to Sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and get  ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currenttime, printed))
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                ("00001620  ha TP, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))
                                            cursor.execute(
                                                'update orders set active = 0 where market =("%s")' % market)
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            newvalue = summ_serf() + serf * BTC_price
                                            cursor.execute(
                                                'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                    currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                             "localhost")
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






## AI_HA MODE SL
                                elif   (active == 1) and (last * bought_quantity_sql * (1 + profit * 1.5) < (
                                bought_price_sql * bought_quantity_sql)) and bot_step == 1:  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('Order already opened to sell  ' + market)
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currtime, printed))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:

                                        # print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('0000161 Trying to sell ' + str(
                                                format_float(
                                                    sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                format_float(ask)) + '  and lose  ' + str(
                                                format_float(serf * BTC_price)) + ' USD')
                                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                                 "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute(
                                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                    currtime, printed))
                                            cursor.execute(
                                                'update orders set reason_close =%s where active=1 and market =%s',
                                                ("0000161  SL, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            newvalue = summ_serf() + serf * BTC_price
                                            cursor.execute(
                                                'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                    currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


 ## AI_HA MODE END SELL



#################################################################


#BUY for 3 step mode

                 # If the price for some currency rapidly increased from 0.8% till 3.5%  let`s buy something too
                if (min_percent_chg < percent_chg < max_percent_chg)  and (stop_bot == 0) and HA_trend!="DOWN" and HA_trend!="Revers-DOWN" and HAD_trend!="DOWN"  and stop_bot_force==0  and (ha_mode==0):
                     balance_res = get_balance_from_market(market)
                     current_balance = balance_res['result']['Available']
                 #If we have opened order on bitrex
                     if has_open_order(market, 'LIMIT_BUY'):
                         #print('Order already opened to buy  ' + market)
                         try:
                             printed = ('    1  - Order already opened to buy  ' + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()

                     elif has_open_order(market, 'LIMIT_SELL'):
                             #print('Order already opened to sell  ' + market)
                             try:
                                 printed = ('    1.1 - Order already opened to sell  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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
                             printed = ('    2 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market +  ' on our balance')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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
                             printed = ('    3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                     else:
                         # Buy some currency by market analize first time
                         try:
                             printed = ('    4 Prod - trying to purchase (by market analize) ' + str(
                                 format_float(percent_chg)) + ' percent changed ' + '  |  ' + str(
                                 format_float(buy_quantity2))  + ' units of ' + market + ' for ' + str(
                                 format_float(newask)) + ' HA ' + HA_trend )
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            ## cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity2, bid, "1", currenttime, timestamp, "1", btc_trend ,'MA:  % chng ' + str(format_float(percent_chg)) + '  AI   ' + str(ai_prediction(market)) + '  BTC ' + btc_trend, HA_trend ))
                             cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity2, last, "2", currenttime, timestamp, "1", btc_trend,'MA:  % chng ' + str(format_float(percent_chg)) + '  AI   ' + str(ai_prediction(market)) + '  BTC ' + btc_trend,HA_trend))
                             cursor.execute("update orders set serf = %s where market = %s and active =2",(serf, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase",printed, "localhost")
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                             # print c.buy_limit(market, fiboquantity*2, last).json()
                         print c.buy_limit(market, buy_quantity2, newask).json()
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!##################################
                             # If we have twice more BIG buy orders then BIG sell Orders, and volume of BUY order is twice bigger then volume of sell orders, it means that price is growing, Let` buy somethin
                elif (buytotalsumm > selltotalsumm * order_multiplier) and (buycountresult > sellcountresult * order_multiplier and buytotalsumm != 0 and selltotalsumm != 0 and buycountresult != 0 and sellcountresult != 0) and (stop_bot ==0) and HA_trend!="DOWN" and HA_trend!="Revers-DOWN" and HAD_trend != "DOWN" and stop_bot_force==0  and HAD_trend!="DOWN"  and (ha_mode==0):
                     balance_res = get_balance_from_market(market)
                     current_balance = balance_res['result']['Available']
                     buysummpercent = float(buytotalsumm / selltotalsumm)
                     buycountpercent = float(buycountresult / sellcountresult)

                     # Check if we have open orders or some unsold currency
                     if has_open_order(market, 'LIMIT_BUY'):
                         #print('Order already opened to buy  ' + market)
                         try:
                             printed = ('    5 - Order already opened to buy  ' + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()


                     elif has_open_order(market, 'LIMIT_SELL'):
                             #print('Order already opened to sell  ' + market)
                             try:
                                 printed = ('    5.1 - Order already opened to sell  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()

                     elif current_balance is not None and current_balance != 0.0:
                         #print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                         try:
                             printed = ('    6 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market +  ' on our balance')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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
                             printed = ('    7 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()


                     else:
                         # Buy some currency by order analize for first time
                         try:
                             printed = ('    8  Prod - trying to purchase (by order analize) ' + ' Total Summ ' + str(
                                 format_float(buycountpercent)) + ' Total Count ' + str(
                                 format_float(buy_quantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                                 format_float(newask))+ ' HA ' + HA_trend)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             cursor.execute(
                                 'insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                 market, buy_quantity2, last, "2", currenttime, timestamp, "1", btc_trend,
                                 'OA: ' + str(format_float(buysummpercent)) + ' TSumm ' + str(
                                     format_float(buycountpercent)) + ' TCount ' + '  AI   ' + str(ai_prediction(market)) + '  BTC ' + btc_trend,HA_trend ))  ## + '  AI   ' + str(ai_prediction(market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                         print c.buy_limit(market, buy_quantity2, newask).json()

                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

                else:
                     pass

#######SELLINLGORITHM##########################SELLING ALGORITHM#####################
########    #####################################################################
# Check     if weve this currency for sell

#FIRST ITERATION - SELL: CHECK GREEN CANDLES AND TAKE PROFIT
                if bought_price_sql != None or bought_price != None and (ha_mode==0):  # added OR
                     balance_res = get_balance_from_market(market)
                     current_balance = balance_res['result']['Available']


                     if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                         # print market, bought_quantity_sql, current_balance
                         pass
                         # If curent balance of this currency more then zero
                     elif bought_quantity_sql > 0 and iteration == 1:  # Need to add bought_quantity without sql
                         ##Check if we have completelly green candle
                         if (currentopen <= currentlow and prevclose <= currentopen and currentopen < currenthigh and last > prevclose) or (currentopen <= currentlow and currentopen < currenthigh and last > prevclose) and last > bought_price_sql * (1+profit):

                             #print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                             try:
                                 printed = ("    9 - We have GREEN candle for " + market + " and let`s wait it to be up")
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             pass

                         elif (currentopen5 <= currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5) or (currentopen5 <= currentlow5 and currentopen5 < currenthigh5 and last > prevclose5) and last > bought_price_sql * (1+profit):  ## Need to add bought_price without sql
                             #print ("We have good trend for " + market)

                             try:
                                 printed = ("    10 - We have good short term trend for " + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             pass

                         else:
#


 ## "TAKE PROFIT" MECHANIZM FOR FIRST ITERATION

                             if newbid >= bought_price_sql * (1+profit) and (serf*BTC_price > 0)  and (ha_mode==0):  ## Need to add bought_price without sql
                                 #if we have already opened order to sell
                                 if has_open_order(market, 'LIMIT_SELL'):
                                     print('Order already opened to sell  ' + market)
                                     try:
                                         printed = ('    11 - Order already opened to sell  ' + market)
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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
                                         printed = ('    12 Prod -Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and get  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                         #cursor.execute('update orders set active = 0, reason_close = "12 Take profit" where market =("%s")' % market)
                                         cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ( "12 TP, price:    " + str(format_float(newbid)) + "    time:   " + str(currenttime), market))
                                         cursor.execute("update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",(1, currtime, market))
                                         #cursor.execute('update orders set active = 0 where market =("%s")' % market)       # -this is deactivating the order
                                         db.commit()
                                     except MySQLdb.Error, e:
                                         print "Error %d: %s" % (e.args[0], e.args[1])
                                         sys.exit(1)
                                     finally:
                                         db.close()
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     print c.sell_limit(market, sell_quantity, newbid).json()
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")



#HA_DOWN Take profit
                             elif serf >= buy_size2*profit/2  and (btc_trend=="DANGER" or btc_trend=="DOWN" or HAD_trend=="DOWN" ) and (ha_mode==0):  ## Need to add bought_price without sql
                                     # if we have already opened order to sell
                                     if has_open_order(market, 'LIMIT_SELL'):
                                         #print('Order already opened to sell  ' + market)
                                         try:
                                             printed = ('    111 - Order already opened to sell  ' + market)
                                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                             cursor = db.cursor()
                                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                                 currenttime, printed))
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
                                             printed = ('    121 Prod -Trying to sell ' + str(format_float(
                                                 sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                 format_float(newbid)) + '  and getting  +' + str(format_float(
                                                 ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(
                                                 format_float((newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                             cursor = db.cursor()
                                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                                 currenttime, printed))
                                             # cursor.execute('update orders set active = 0, reason_close = "12 Take profit" where market =("%s")' % market)
                                             cursor.execute(
                                                 'update orders set reason_close =%s where active=1 and market =%s', (
                                                     "121 TP, price:    " + str(
                                                         format_float(newbid)) + "    time:   " + str(currenttime),
                                                     market))
                                             #cursor.execute(
                                             #    'update orders set active = 0 where market =("%s")' % market)
                                             cursor.execute(
                                                 "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                 (1, currtime, market))
                                             newvalue = summ_serf() + serf * BTC_price
                                             cursor.execute(
                                                 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                     currenttime, newvalue, market))
                                             db.commit()
                                         except MySQLdb.Error, e:
                                             print "Error %d: %s" % (e.args[0], e.args[1])
                                             sys.exit(1)
                                         finally:
                                             db.close()
                                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                              "localhost")
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                         print c.sell_limit(market, sell_quantity, newbid).json()
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                             elif  serf >= buy_size2 * profit / 3 and (HAD_trend == "DOWN" or HA_trend == "DOWN" or HA_trend == "Revers-DOWN"):  ## Need to add bought_price without sql
                                         # if we have already opened order to sell
                                         if has_open_order(market, 'LIMIT_SELL'):
                                             # print('Order already opened to sell  ' + market)
                                             try:
                                                 printed = ('    1111 - Order already opened to sell  ' + market)
                                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                                 cursor = db.cursor()
                                                 cursor.execute(
                                                     'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                         currenttime, printed))
                                                 db.commit()
                                             except MySQLdb.Error, e:
                                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                                 sys.exit(1)
                                             finally:
                                                 db.close()


                                         else:
                                             # Lets Sell some
                                             # print('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                             try:
                                                 printed = ('    1331 Prod -Trying to sell ' + str(format_float(
                                                     sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                                     format_float(newbid)) + '  and getting  +' + str(format_float(
                                                     ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(
                                                     format_float((
                                                                  newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                                 cursor = db.cursor()
                                                 cursor.execute(
                                                     'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                         currenttime, printed))
                                                 # cursor.execute('update orders set active = 0, reason_close = "12 Take profit" where market =("%s")' % market)
                                                 cursor.execute(
                                                     'update orders set reason_close =%s where active=1 and market =%s',
                                                     (
                                                         "1331 HA TP, price:    " + str(
                                                             format_float(newbid)) + "    time:   " + str(currenttime),
                                                         market))
                                                 # cursor.execute(
                                                 #    'update orders set active = 0 where market =("%s")' % market)
                                                 cursor.execute(
                                                     "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                     (1, currtime, market))
                                                 newvalue = summ_serf() + serf * BTC_price
                                                 cursor.execute(
                                                     'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                         currenttime, newvalue, market))
                                                 db.commit()
                                             except MySQLdb.Error, e:
                                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                                 sys.exit(1)
                                             finally:
                                                 db.close()
                                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,
                                                  "localhost")
                                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                             print c.sell_limit(market, sell_quantity, newbid).json()
                                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






                                     #

##
#AI TAKE PROFIT FOR FIRST ITERATION
##

                             elif (last >= ai_prediction_price(market) and (serf >= buy_size2*profit/3)  and market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCH' and ai_prediction(market) != 'NEUTRAL' and ai_prediction(market) == 'DOWN') and (last >= bought_price_sql * (1+profit-0.03)) and iteration==1 and (ha_mode==0):  # and (newbid >= bought_price_sql * (1+profit))

                                 if has_open_order(market, 'LIMIT_SELL'):
                                     #print('Order already opened to sell  ' + market)
                                     try:
                                         printed = ('    13 - Order already opened to sell  ' + market)
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                         db.commit()
                                     except MySQLdb.Error, e:
                                         print "Error %d: %s" % (e.args[0], e.args[1])
                                         sys.exit(1)
                                     finally:
                                         db.close()


                                 else:

                                     #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                     try:
                                         printed = ('    14 Prod -Trying to sell ' + str(
                                             format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                             format_float(newbid)) + '  and get  ' + str(
                                             format_float(serf * BTC_price)) + ' USD')
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute(
                                             'insert into logs(date, log_entry) values("%s", "%s")' % (
                                             currenttime, printed))
                                         # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                         cursor.execute(
                                             'update orders set reason_close =%s where active=1 and market =%s', (
                                             "14 AI TP, price:  " + str(format_float(newbid)) + "  time:   " + str(
                                                 currenttime), market))
                                         #cursor.execute(
                                         #    'update orders set active = 0 where market =("%s")' % market)
                                         cursor.execute(
                                             "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                             (1, currtime, market))
                                         newvalue = summ_serf() + serf * BTC_price
                                         cursor.execute(
                                             'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                 currenttime, newvalue, market))
                                         db.commit()
                                     except MySQLdb.Error, e:
                                         print "Error %d: %s" % (e.args[0], e.args[1])
                                         sys.exit(1)
                                     finally:
                                         db.close()
                                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")

                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     print c.sell_limit(market, sell_quantity, newbid).json()
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


#
#
# AI STOP LOSS FIRST ITERATION

                             elif (last >= ai_prediction_price(market) and  (serf <= buy_size2*profit*(-2))   and market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCH' and ai_prediction(market) != 'NEUTRAL' and ai_prediction(market) == 'DOWN') and (ha_mode==0):
                                 if has_open_order(market, 'LIMIT_SELL'):
                                     print('Order already opened to sell  ' + market)
                                     try:
                                         printed = ('    15 - Order already opened to sell  ' + market)
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute(
                                             'insert into logs(date, log_entry) values("%s", "%s")' % (
                                             currenttime, printed))
                                         db.commit()
                                     except MySQLdb.Error, e:
                                         print "Error %d: %s" % (e.args[0], e.args[1])
                                         sys.exit(1)
                                     finally:
                                         db.close()


                                 else:

                                     #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                     try:
                                         printed = ('    16 Prod -Trying to sell ' + str(
                                             format_float(
                                                 sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                             format_float(newbid)) + '  and lose  ' + str(
                                             format_float(serf * BTC_price)) + ' USD')
                                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                         cursor = db.cursor()
                                         cursor.execute(
                                             'insert into logs(date, log_entry) values("%s", "%s")' % (
                                             currenttime, printed))
                                         # cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                                         cursor.execute(
                                             'update orders set reason_close =%s where active=1 and market =%s',
                                             ("16 AI SL, p:   " + str(
                                                 format_float(newbid)) + " t:    " + str(currenttime), market))
                                         #cursor.execute(
                                         #    'update orders set active = 0 where market =("%s")' % market)
                                         cursor.execute(
                                             "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                             (1, currtime, market))
                                         newvalue = summ_serf() + serf * BTC_price
                                         cursor.execute(
                                             'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                 currenttime, newvalue, market))
                                         db.commit()
                                     except MySQLdb.Error, e:
                                         print "Error %d: %s" % (e.args[0], e.args[1])
                                         sys.exit(1)
                                     finally:
                                         db.close()
                                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     print c.sell_limit(market, sell_quantity, newbid).json()
                                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


# "STOP  LOSS" MECHANIZM. WE should sell failed currency before price goes down and reach min selling limit. If sell now we are losing 50%. If not - we will lose 100% of order`s cost
                             elif newbid < bought_price_sql and sell_size >= sell_quantity_sql * last and (btc_trend=="DANGER" or btc_trend=="DOWN" or HAD_trend=="DOWN" ) and (HA_trend=="DOWN" or HA_trend=="Revers-DOWN") and (ha_mode==0 ):  # # Need to add bought_price without sql and sell_quantity without sql

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

                                            #print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                            try:
                                                printed = ('161  Prod Trying to sell '  + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and lose  ' + str(format_float(serf * BTC_price)) + ' USD')
                                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                                cursor = db.cursor()
                                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currtime, printed))
                                                cursor.execute(
                                                    'update orders set reason_close =%s where active=1 and market =%s',
                                                    ("161  SL, p:   " + str(
                                                        format_float(newbid)) + " t:    " + str(currenttime), market))
                                                #cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                                cursor.execute(
                                                    "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                    (1, currtime, market))
                                                newvalue = summ_serf() + serf * BTC_price
                                                cursor.execute(
                                                    'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                        currenttime, newvalue, market))
                                                db.commit()
                                            except MySQLdb.Error, e:
                                                print "Error %d: %s" % (e.args[0], e.args[1])
                                                sys.exit(1)
                                            finally:
                                                db.close()

                                                #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                            print c.sell_limit(market, sell_quantity, newbid).json()
                                                #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################








                             else:
                                 pass





#


#DOING SECOND AND THIRD BUY

                if serf < 0 and (timestamp - timestamp_old > 6000) and active == 1 and iteration < maxiteration  and HA_trend != "DOWN" and HA_trend != "Revers-DOWN" and HAD_trend != "DOWN"  and bot_step == 0   and (last < bought_price_sql and last * bought_quantity_sql*(1+profit-0.03) < (bought_price_sql * bought_quantity_sql + prev_serf)):
                     #print market, "Has old order"
                     #run_prediction = "python2.7 run_predict.py " + market
                     #p = subprocess.Popen(run_prediction, stdout=subprocess.PIPE, shell=True)
                     #(output, err) = p.communicate()
                     #p_status = p.wait()


                     if (min_percent_chg < percent_chg < max_percent_chg) and (HAD_trend=="UP" or HAD_trend=="revers-UP"):
                         #print "Buying by Market analize"
                         if has_open_order(market, 'LIMIT_BUY'):
                             #print('13 - Order already opened to buy  ' + market)
                             try:
                                 printed = ('    Order already opened to buy  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()

                         else:
                             newiteration = iteration + 1
                             # Buy some currency
                             #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(ask)))
                             try:
                                 printed = ('    17 Prod - Purchasing (by market analize) ' + str(format_float(percent_chg)) + ' percent changed ' + '  |  ' +  str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  AI   ' + str(ai_prediction(market)) + ' BTC ' + btc_trend + ' USD serf ' + str(serf*BTC_price)  + ' Iteration ' + str(iteration) + ' HA ' + HA_trend)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 current_serf = previous_serf(market)
                                 prev_serf = ((newask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                                 cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                                 cursor.execute("update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s, btc_direction_1 = %s, heikin_ashi_1 = %s, open_buy=1, open_buy_time=%s   where market = %s and active = 1", (fiboquantity+fiboquantity2, newask, timestamp, newiteration, btc_trend, HA_trend, currtime, market))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                             #quant= fiboquantity+fiboquantity2
                                 #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                             print c.buy_limit(market, fiboquantity2, newask).json()
                                 #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

                     elif buytotalsumm > selltotalsumm*order_multiplier and buycountresult > sellcountresult*order_multiplier and buytotalsumm !=0 and selltotalsumm !=0 and buycountresult !=0 and sellcountresult !=0 and (HAD_trend=="UP" or HAD_trend=="revers-UP"): #
                         #print "Buying by order analize"

                         if has_open_order(market, 'LIMIT_BUY'):
                             print('Order already opened to buy  ' + market)
                             try:
                                 printed = ('    18 - Order already opened to buy  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()

                         else:
                             newiteration = iteration + 1
                             # Buy some currency
                             #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(ask)))
                             try:
                                 printed = ('    19 Prod - Purchasing (by market analize) ' + str(
                                     format_float(percent_chg)) + ' percent changed ' + str(
                                     format_float(fiboquantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                                     format_float(newask)) + ' USD serf ' + str(serf*BTC_price) + ' Iteration ' + str(iteration)+ ' HA ' + HA_trend)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 current_serf = previous_serf(market)
                                 prev_serf = ((last * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                                 cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                                 cursor.execute(
                                     "update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s, btc_direction_1 = %s, heikin_ashi_1 = %s, open_buy=1, open_buy_time=%s   where market = %s and active = 1",
                                     (fiboquantity + fiboquantity2, newask, timestamp, newiteration, btc_trend, HA_trend,
                                      currtime, market))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                             #quant = fiboquantity + fiboquantity2
                                 #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                             print c.buy_limit(market, fiboquantity2, newask).json()
                                 #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                     else:
                         pass
#

# SECOND  AND THIRD ITERATION -SELL: TAKE PROFITS

                elif serf >= buy_size2*profit and (active == 1) and (iteration != 1):
                     #if (currentopen == currentlow and prevclose <= currentopen) or (currentopen == currenthigh):


                     if (currentopen5 <= currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5) or (currentopen5 <= currentlow5 and currentopen5 < currenthigh5 and last > prevclose5):  ## Need to add bought_price without sql
                         print (" We have good trend for " + market)
                         try:
                             printed = ("    21 -We have good short term trend for " + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         pass

                     else:  ## Need to add bought_price without sql
                         # If  we got our profit, lets sell this shitcoins
                         # !!!!!!!!!!!
                         ## "TAKE PROFIT" MECHANIZM - we can take our percent from profit variable and sell currency
                             if has_open_order(market, 'LIMIT_SELL'):
                                 print('Order already opened to sell  ' + market)
                                 try:
                                     printed = ('    22 - Order already opened to sell  ' + market)
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()


                             else:
                                 # Lets Sell some
                                # print('Selling ' + str(format_float(fiboquantity)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(format_float((ask * fiboquantity - bought_price_sql * fiboquantity) * BTC_price)) + ' USD')
                                 try:
                                     printed = ('    23 Prod - Trying to sell ' + str(
                                         format_float(bought_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                         format_float(newbid)) + '  and get  +' + str(
                                         format_float(
                                             last * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(
                                         format_float(
                                             serf * BTC_price)) + ' USD')
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))

                                     cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("23 TP, p:    " + str(format_float(newbid)) + "    t:   " + str(currenttime), market))
                                     #cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                     cursor.execute(
                                         "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                         (1, currtime, market))
                                     newvalue = summ_serf() + serf * BTC_price
                                     cursor.execute(
                                         'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                             currenttime, newvalue, market))
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()
                                 Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                 print c.sell_limit(market, sell_quantity, newbid).json()
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                     #else:
                      #   pass

                elif serf >= buy_size2*profit/2 and (active == 1) and (iteration != 1) and (btc_trend=="DANGER" or btc_trend=="DOWN" or HAD_trend=="DOWN" or HA_trend=="Revers-DOWN" or HA_trend=="DOWN" ):

                     if (currentopen5 <= currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5) or (currentopen5 <= currentlow5 and currentopen5 < currenthigh5 and last > prevclose5):  ## Need to add bought_price without sql
                         #print (" We have good trend for " + market)
                         try:
                             printed = ("    211 -We have good short term trend for " + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         pass

                     else:  ## Need to add bought_price without sql
                         # If  we got our profit, lets sell this shitcoins
                         # !!!!!!!!!!!
                         ## "TAKE PROFIT" MECHANIZM - we can take our percent from profit variable and sell currency
                         if has_open_order(market, 'LIMIT_SELL'):
                             #print('Order already opened to sell  ' + market)
                             try:
                                 printed = ('    221 - Order already opened to sell  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
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
                                 printed = ('    231 Prod - Trying to sell ' + str(
                                     format_float(bought_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                     format_float(last)) + '  and get  +' + str(
                                     format_float(
                                         newbid * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(
                                     format_float(
                                         serf * BTC_price)) + ' USD')
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                 # cursor.execute('update orders set active = 0, reason_close = "23 Take profit " where market =("%s")' % market)
                                 cursor.execute('update orders set reason_close =%s where active=1 and market =%s', (
                                 "231 HA TP, p:    " + str(format_float(newbid)) + "    t:   " + str(currenttime), market))
                                 #cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                 cursor.execute(
                                     "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                     (1, currtime, market))
                                 newvalue = summ_serf() + serf * BTC_price
                                 cursor.execute(
                                     'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                         currenttime, newvalue, market))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                             print c.sell_limit(market, sell_quantity, newbid).json()
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






#DOING THIRD SELLs


#AI take profit for last order

                elif (newbid >= ai_prediction_price(market) and (serf >= buy_size2*profit/4) and iteration == maxiteration and (active == 1) and market!='BTC-OMG' and market!='BTC-LSK' and market!='BTC-BCH' and ai_prediction(market)!='NEUTRAL' and ai_prediction(market)=='DOWN'):  # # Need to add bought_price without sql and sell_quantity without sql

                         if has_open_order(market, 'LIMIT_SELL'):
                             #print('Order already opened to sell  ' + market)
                             try:
                                 printed = ('    24 - Order already opened to sell  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()


                         else:

                             #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                             try:
                                 printed = ('    25  Prod -Trying to sell ' + str(
                                     format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                     format_float(newbid)) + '  and get  ' + str(
                                     format_float(serf*BTC_price)) + ' USD')
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 #cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                 cursor.execute('update orders set reason_close =%s where active=1 and market =%s',("25 AI TP, p:   " + str(format_float(newbid))+"   t:    "+str(currenttime), market))
                                # cursor.execute(
                                 #    'update orders set active = 0 where market =("%s")' % market)
                                 cursor.execute(
                                     "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                     (1, currtime, market))
                                 newvalue = summ_serf() + serf * BTC_price
                                 cursor.execute(
                                     'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                         currenttime, newvalue, market))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                             print c.sell_limit(market, sell_quantity, newbid).json()
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


# HA take profit for last order

                elif (newbid >= ai_prediction_price(market) and (serf >= buy_size2*profit/4) and iteration == maxiteration and (active == 1) and (HA_trend == 'DOWN' or HA_trend == 'Revers-DOWN' or HAD_trend=="DOWN" )):  # # Need to add bought_price without sql and sell_quantity without sql

                             if has_open_order(market, 'LIMIT_SELL'):
                                 #print('Order already opened to sell  ' + market)
                                 try:
                                     printed = ('    241 - Order already opened to sell  ' + market)
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()


                             else:

                                 #print ('22 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                 try:
                                     printed = ('    251 Prod -Selling ' + str(
                                         format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                         format_float(newbid)) + '  and get  ' + str(
                                         format_float(serf * BTC_price)) + ' USD')
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                     # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                     cursor.execute('update orders set reason_close =%s where active=1 and market =%s', (
                                     "251 HA TP, p:   " + str(format_float(newbid)) + "   t:    " + str(currenttime), market))
                                     #cursor.execute(
                                     #    'update orders set active = 0 where market =("%s")' % market)
                                     cursor.execute(
                                         "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                         (1, currtime, market))
                                     newvalue = summ_serf() + serf * BTC_price
                                     cursor.execute(
                                         'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                             currenttime, newvalue, market))
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()
                                 Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                 print c.sell_limit(market, sell_quantity, newbid).json()
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################



#STOP LOSS FOR last iteration

                elif (newbid < bought_price_sql) and (serf <= buy_size2*profit*(-10)) and (iteration == maxiteration) and (active == 1):  # # Need to add bought_price without sql and sell_quantity without sql

                         if has_open_order(market, 'LIMIT_SELL'):
                             print('Order already opened to sell  ' + market)
                             try:
                                 printed = ('    26 - Order already opened to sell  ' + market)
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()


                         else:

                             #print ('22 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                             try:
                                 printed = ('    27 Prod -Selling ' + str(
                                     format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                     format_float(newbid)) + '  and lose  ' + str(
                                     format_float(serf*BTC_price)) + ' USD')
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                 #cursor.execute('update orders set reason_close = "27 Stop loss" where active=1 and market =("%s")' % market)
                                 cursor.execute('update orders set reason_close =%s where active=1 and market =%s', (
                                 "27 Stop loss, price:    " + str(format_float(newbid)) + "    time:   " + str(
                                     currenttime), market))
                                 #cursor.execute(
                                 #    'update orders set active = 0 where market =("%s")' % market)
                                 cursor.execute(
                                     "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                     (1, currtime, market))
                                 newvalue = summ_serf() + serf * BTC_price
                                 cursor.execute(
                                     'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                         currenttime, newvalue, market))
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                             print c.sell_limit(market, sell_quantity, newbid).json()
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


#AI STOP LOSS

                elif (newbid >= ai_prediction_price(market) and (active == 1)  and (serf <= buy_size2*profit*(-4)) and (serf*BTC_price < 0) and iteration == maxiteration and market!='BTC-OMG' and market!='BTC-LSK' and market!='BTC-BCC' and ai_prediction(market)!='NEUTRAL' and ai_prediction(market)=='DOWN'):
                     if has_open_order(market, 'LIMIT_SELL'):
                         #print('Order already opened to sell  ' + market)
                         try:
                             printed = ('    28 - Order already opened to sell  ' + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()


                     else:

                         #print ('22 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                         try:
                             printed = ('    29 Prod - Trying to sell ' + str(
                                 format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                 format_float(newbid)) + '  and lose  ' + str(
                                 format_float(serf * BTC_price)) + ' USD')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             #cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                             cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("29 AI SL, p:    "+str(format_float(newbid))+"    t:   "+str(currenttime), market))
                             #cursor.execute(
                             #    'update orders set active = 0 where market =("%s")' % market)
                             cursor.execute(
                                 "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                 (1, currtime, market))
                             newvalue = summ_serf() + serf * BTC_price
                             cursor.execute(
                                 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                     currenttime, newvalue, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                         print c.sell_limit(market, sell_quantity, newbid).json()
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


# HA STOP LOSS
                elif (newbid >= ai_prediction_price(market) and (active == 1) and (serf <= buy_size2*profit*(-4)) and iteration == maxiteration and (HA_trend == 'DOWN' or HA_trend=="Revers-DOWN" or HAD_trend=="DOWN" or btc_trend=="DANGER") and (currentcloseday<currentopenday and currentlowday<currenthighday) and btc_trend=="DANGER"):
                     if has_open_order(market, 'LIMIT_SELL'):
                         print('Order already opened to sell  ' + market)
                         try:
                             printed = ('    281 - Order already opened to sell  ' + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()


                     else:

                         #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                         try:
                             printed = ('    291 Prod -Trying to sell' + str(
                                 format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                 format_float(newbid)) + '  and lose  ' + str(
                                 format_float(serf * BTC_price)) + ' USD')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             # cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                             cursor.execute('update orders set reason_close =%s where active=1 and market =%s', (
                             "291 HA SL, p:    " + str(format_float(newbid)) + "    t:   " + str(currenttime), market))
                             #cursor.execute(
                             #    'update orders set active = 0 where market =("%s")' % market)
                             cursor.execute(
                                 "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                 (1, currtime, market))
                             newvalue = summ_serf() + serf * BTC_price
                             cursor.execute(
                                 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                     currenttime, newvalue, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                         print c.sell_limit(market, sell_quantity, newbid).json()
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






#Candle Take profit
                elif ((currentlow == currentclose)  and serf >= buy_size2*profit/2  and iteration == maxiteration) and (active == 1) and (HA_trend=="DOWN" or HA_trend=="Revers-DOWN" or btc_trend=="DANGER"):
                     if has_open_order(market, 'LIMIT_SELL'):
                         #print('Order already opened to sell  ' + market)
                         try:
                             printed = ('    30 - Order already opened to sell  ' + market)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()


                     else:

                         #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                         try:
                             printed = ('    31 Prod -Trying to sell ' + str(
                                 format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                 format_float(newbid)) + '  and get  ' + str(
                                 format_float(serf * BTC_price)) + ' USD')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             #cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                             cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("31 Candle TP, p:    "+str(format_float(newbid))+"    t:   "+str(currenttime), market))
                             #cursor.execute('update orders set active = 0 where market =("%s")' % market)
                             cursor.execute(
                                 "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                 (1, currtime, market))
                             newvalue = summ_serf() + serf * BTC_price
                             cursor.execute(
                                 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                     currenttime, newvalue, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                         print c.sell_limit(market, sell_quantity, newbid).json()
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






                else:
                    pass






            else:
                pass
        except:
            continue

### FUNCTIONS
###############################################################################################################




def heikin_ashi(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False






def Mail(FROM,TO,SUBJECT,TEXT,SERVER):

# Prepare actual message
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, TO, SUBJECT, TEXT)
# Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()



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



#def total_summ():
#    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#    cursor = db.cursor()
#    cursor.execute("SELECT SUM(serf_usd) FROM orders where active = 0")
#    r = cursor.fetchall()
#    for row in r:
#        return (row[0])




def parameters():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24])

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

def ai_prediction_price(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_price FROM markets WHERE active =1 and ai_direction='UP' and market = '%s'" % market)
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





def open_sell(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT open_sell FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0




def open_buy(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT active FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0


def second_buy(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT open_buy FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def second_buy_time(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT open_buy_time FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def sell_time(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def buy_time(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT timestamp FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
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




def summ_serf():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT SUM(serf_usd) FROM orders where active=0")
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0



def bot_mode(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT one_step_active FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0

#def usd_serf(marketname):
#    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#    cursor = db.cursor()
#    market=marketname
#    cursor.execute("SELECT serf FROM orders WHERE active =1 and market = '%s'" % market)
#    r = cursor.fetchall()
#    for row in r:
#        return float(row[0])
#    return 0


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


def order_uuid(market):
    orders_res = c.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
    else:
        return c.get_open_orders(market).json()['result'][0]['OrderUuid']







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
    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, market))
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
