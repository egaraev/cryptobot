#Imports from modules, libraries and config files
import config
from pybittrex.client import Client
import requests
import time
import datetime
import hmac
import hashlib
import MySQLdb
import sys
import smtplib
c1 = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file
c=Client(api_key='', api_secret='')

def main():
    print('Starting trader bot')



    tick()

################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
    max_orders = parameters()[5]
    stop_bot = int(parameters()[11])
    market_summ = c.get_market_summaries().json()['result']
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    btc_trend = parameters()[12]
    current_order_count=order_count()
    #print get_balance_from_market("BTC-QTUM")['result']['Available']

    #print summ_serf()




    #global active
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                stop_market = bot_mode(market)
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

                timestamp = int(time.time())
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
            #BOUGHT PRICE


                bought_price = get_closed_orders(market, 'PricePerUnit')

            #Bought Quantity need for sell order, to know at which price we bought some currency
                bought_quantity = get_balance_from_market(market)['result']['Available']
                sell_quantity = bought_quantity
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
                HAH_trend = heikin_ashi(market, 20)
                ha_time_second=heikin_ashi(market, 23)
                percent_sql=int(heikin_ashi(market, 21))
                volume_sql=int(heikin_ashi(market, 22))
                #print market, HA_trend



                if (btc_trend == "DOWN" and HA_trend == "DOWN") or (btc_trend == "DANGER") or (HAD_trend == "DOWN"):
                    profit = parameters()[3] / 1.5
                elif (timestamp - timestamp_old > 43200) and (HA_trend!="UP" or HA_trend!="Revers-UP"):
                    profit = parameters()[3] / 2
                else:
                    profit = parameters()[3]



                print market, profit, HA_trend, HAD_trend

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


#Remove false buy orders
#                if bought_quantity_sql==0 and bought_price_sql>0:
#                    try:
                        #print market
#                        printed = ('    0 Prod -Failed buy order for  ' + market)
#                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#                        cursor = db.cursor()
#                        cursor.execute('update orders set active = 3 where  market =("%s")' % market)
#                        db.commit()
#                    except MySQLdb.Error, e:
#                        print "Error %d: %s" % (e.args[0], e.args[1])
#                        sys.exit(1)
#                    finally:
#                        db.close()
#                    Mail("egaraev@gmail.com", "egaraev@gmail.com", "Order buy failed", printed, "localhost")
#                else:
#                    pass




                #print market, bought_quantity
                if bought_quantity is not None:
                    if has_open_order(market, 'LIMIT_SELL'):
                        print('Order already opened to sell  ' + market)
                        try:
                            printed = ('    1 - Order already opened to sell  ' + market)
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
                            printed = ('    2 - Order already opened to buy  ' + market)
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
                        print market, bought_quantity,
                        if timestamp-timestamp_old<1800:
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
                else:
                    pass





# Force Stop the bot
                if stop_bot_force==1 and (bought_quantity_sql != 0.0):
                    #print bought_quantity_sql
                    if has_open_order(market, 'LIMIT_SELL'):
                        print('Order already opened to sell  ' + market)
                        try:
                            printed = ('    3 - Order already opened to sell  ' + market)
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
                            printed = ('    4 Prod -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or losing  ' + str(format_float(serf * BTC_price)) + ' USD')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            # cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                            cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("33 , Force_stop_bot p:    " + str(format_float(newbid)) + "    t:   " + str(currenttime),market))

                            cursor.execute("update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",(1, currtime, market))
                            #newvalue = summ_serf() + serf * BTC_price
                            #cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                            #cursor.execute('update orders set active = 0 where market =("%s")' % market)
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        print c1.sell_limit(market, sell_quantity, newbid).json()
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                else:
                    pass





                if stop_market==1 and (bought_quantity_sql != 0.0):
                    #print bought_quantity_sql
                    if has_open_order(market, 'LIMIT_SELL'):
                        print('Order already opened to sell  ' + market)
                        try:
                            printed = ('    3.1 - Order already opened to sell  ' + market)
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

                        # print ('Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                        try:
                            printed = ('    4.1  Prod -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or losing  ' + str(format_float(serf * BTC_price)) + ' USD')
                            db = MySQLdb.connect("localhost", "cryptouser", "123456",
                                                 "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                    currenttime, printed))
                            cursor.execute(
                                'update orders set reason_close =%s where active=1 and market =%s',
                                ("4.1  Force stop market, p:   " + str(
                                    format_float(last)) + " t:    " + str(currenttime), market))
                            cursor.execute(
                                "update markets set ai_ha=%s  where market = %s and active =1",
                                (0, market))
                            cursor.execute(
                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                (1, currtime, market))
                            #newvalue = summ_serf() + serf * BTC_price
                            #cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                        print c1.sell_limit(market, sell_quantity, newbid).json()
                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                else:
                    pass

                #print market, open_sell(market), get_balance_from_market(market)['result']['Available']
                #print market, get_balance_from_market(market)['result']




#What if we have sent the sell order to bittrex?
                if open_sell(market)==1:

                    if has_open_order(market, 'LIMIT_SELL'):
                        if currtime - sell_time(market) < 1500:
                            print('Order already opened to sell  ' + market)
                            try:
                                printed = ('    5 - Order already opened to sell  ' + market)
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
                            print(' Order cancelled  ' + market)
                            try:
                                printed = ('    6- Order has been cancelled  ' + market)
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
                            print c1.market_cancel(uuid)
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
                            #############################################################


                    elif get_balance_from_market(market)['result']['Available'] >0:
                        print(' Order failed  ' + market)
                        rest_balance=get_balance_from_market(market)['result']['Available']
                        try:
                            printed = ('    6- Order has been failed to sell  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            cursor.execute(
                                'update orders set open_sell = 0  where active=1 and market =("%s")' % market)
                            cursor.execute("update orders set quantity = %s where market = %s and active =1",(rest_balance, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")



                    else:
                        try:
                            print ('    7 Prod -This currency has been sold ' + market )
                            printed = ('    7 Prod -This currency has been sold   ' + market )
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            newquantity = get_closed_orders(market, 'Quantity')
                            cursor.execute("update orders set quantity = %s where market = %s and active =1",(newquantity, market))
                            cursor.execute('update orders set active = 0, open_sell = 0  where active =1 and market =("%s")' % market)       # -this is deactivating the order  !!!!
                            newvalue = summ_serf() + serf * BTC_price
                            cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                            currenttime, newvalue, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency sold", printed, "localhost")


                else:
                    pass


# What if we have sent the buy order to bittrex?

                if open_buy(market)==2:

                    if has_open_order(market, 'LIMIT_BUY'):
                        if currtime - buy_time(market) < 1000:
                            print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    8 - Order already opened to buy  ' + market)
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
                            print(' Order cancelled  ' + market)
                            try:
                                printed = ('    9 - Order has been cancelled  ' + market)
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
                            print c1.market_cancel(uuid)
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
                            #############################################################


                    elif get_balance_from_market(market)['result']['Available'] ==0 or get_balance_from_market(market)['result']['Available'] == None:
                        print(' Order failed  ' + market)
                        try:
                            printed = ('    6- Order has been failed to buy  ' + market)
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            cursor.execute(
                                'update orders set active= 3  where active=2 and market =("%s")' % market)
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")



                    else:
                        try:
                            print ('    10 Prod -This currency has been bought ' + market )
                            printed = ('    10 Prod -This currency has been bought   ' + market )
                            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                            cursor.execute("update orders set quantity = %s, price=%s, active=1, date=%s, timestamp=%s, iteration=1, btc_direction=%s, params=%s, heikin_ashi=%s  where market = %s and active =2",(buy_quantity, last, currenttime, timestamp,btc_trend, '  BTC: ' + str(btc_trend) + '  HAD: ' + str(HAD_trend) + ' HAH: ' + str(HAH_trend) + ' HA: ' + str(HA_trend) + '  %  ' + str(percent_sql) + '  vol  ' + str(volume_sql), HA_trend, market))
                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()
                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency bought", printed, "localhost")


                else:
                    pass

                    #print market
#                if bought_quantity*1.5<bought_quantity_sql and second_buy(market)==1:
#                    if has_open_order(market, 'LIMIT_BUY'):
#                       if currtime-second_buy_time(market)<600:
#                            #print('Order already opened to buy  ' + market)
#                            try:
#                                printed = ('    11 - Order already opened to buy  ' + market)
#                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#                                cursor = db.cursor()
#                                cursor.execute(
#                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
#                                db.commit()
#                            except MySQLdb.Error, e:
#                                print "Error %d: %s" % (e.args[0], e.args[1])
#                                sys.exit(1)
#                            finally:
#                                db.close()
#                       else:
#                            try:
#                                printed = ('    12 Prod- Order has been cancelled  ' + market)
#                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#                                cursor = db.cursor()
#                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
#                                newiteration = iteration - 1
#                                cursor.execute("update orders set  iteration = %s, open_buy=0, prev_serf=0, open_buy_time=0 where market = %s and active = 1",(newiteration, market))
#                                db.commit()
#                            except MySQLdb.Error, e:
#                                print "Error %d: %s" % (e.args[0], e.args[1])
#                                sys.exit(1)
#                            finally:
#                                db.close()
#                                #########################################CANCEL OLD ORDER#####
#                            uuid = order_uuid(market)
#                            print c.market_cancel(uuid)
#                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed, "localhost")
#                            #############################################################
#
#
#
#                    else:
#                            try:
#                                printed = ('    13 Prod - Purchase was not approved for '  + market )
#                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#                                cursor = db.cursor()
#                                newiteration=iteration-1
#                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
#                                cursor.execute("update orders set  iteration = %s, prev_serf=0, where market = %s and active = 1",
#                                    (newiteration, market))
#                                db.commit()
#                            except MySQLdb.Error, e:
#                                print "Error %d: %s" % (e.args[0], e.args[1])
#                                sys.exit(1)
#                            finally:
#                                db.close()
#                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Purchase not approved", printed, "localhost")
#
#                else:
#                    pass
#


#FIRST ITERATION - BUY

### BUY FOR HA_AI mode

                    #print market, profit

                    if ((stop_bot == 0) and (HA_trend == "UP" or HA_trend == "Revers-UP") and (HAD_trend=="UP" or HAD_trend == "Revers-UP" or HAD_trend == "STABLE") and stop_bot_force == 0) and last>currentopen5 and percent_chg>0 and (currtime-ha_time_second<1500) and current_order_count<=max_orders:  # and ((dayprevclose>=daycurrentopen or daycurrentopen==daycurrenthigh) is not True) and (currenthigh>currentopen or currentopen<currentclose):  # 0.8 - 3.5  #
                        balance_res = get_balance_from_market(market)
                        current_balance = balance_res['result']['Available']


                        # If we have opened order on bitrex
                        if has_open_order(market, 'LIMIT_BUY'):
                            # print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    14 - Order already opened to buy  ' + market)
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
                                printed = ('    15 - We already have ' + str(
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
                                printed = ('    16 - We already have ' + str(
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
                                printed = ('    17 - Prod - Trying to Purchase  ' + str(
                                    format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(
                                    format_float(bid)))
                                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                        market, buy_quantity, bid, "2", currenttime, timestamp, "1", btc_trend, '  BTC: ' + str(btc_trend) + '  HAD: ' + str(HAD_trend) + ' HAH: ' + str(HAH_trend) + ' HA: ' + str(HA_trend) + '  %  ' + str(percent_sql) + '  vol  ' + str(volume_sql), HA_trend))  # + '  AI   ' + str(ai_prediction(market))
                                cursor.execute(
                                    "update orders set serf = %s where market = %s and active =2",
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
                            print c1.buy_limit(market, buy_quantity, newask).json()
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!##################################

 ### FOR HA_AI mode - END


 # AI_HA MODE SELL START
                    if bought_price_sql != None or bought_price != None :  # added OR
                        #balance_res = get_balance_from_market(market)
                        #current_balance = balance_res['result']['Available']

                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0 and iteration == 1:  # Need to add bought_quantity without sql
                            ##Check if we have completelly green candle

                            #print ('  28 Prod - Trying to Sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str((ask)) + '  and get  ' + str(format_float(serf * BTC_price)) + ' USD')

                            if (currentopen <= currentlow and prevclose <= currentopen and currentopen < currenthigh and last > prevclose) or (currentopen <= currentlow and currentopen < currenthigh and last > prevclose):

                                print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                                try:
                                    printed = (
                                        "    18 - We have GREEN candle for " + market + " and let`s wait it to be up")
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
                            elif (currentopen5 <= currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5) or (currentopen5 <= currentlow5 and currentopen5 < currenthigh5 and last > prevclose5):
                                print ("We have good trend for " + market)

                                try:
                                    printed = ("    19 - We have good short term trend for " + market)
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
                                            1 + profit / 2):  # # WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    20 - Order already opened to sell  ' + market)
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

                                        #print ('21 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    21 Prod -Trying to sell ' + str(
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
                                                    "21 HA SELL, p:   " + str(
                                                        format_float(last)) + "   t:    " + str(currenttime),
                                                    market))
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            #newvalue = summ_serf() + serf * BTC_price
                                            #cursor.execute(
                                               # 'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                                #currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                                elif (active == 1) and (
                                                            market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCH' and ai_prediction(
                                                market) != 'NEUTRAL' and ai_prediction(
                                            market) == 'DOWN') and last > bought_price_sql * (
                                            1 + profit / 2):  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    22 - Order already opened to sell  ' + market)
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

                                        #print ('23 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    23 - Prod - Trying to sell ' + str(
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
                                                    "24 AI SELL, price:  " + str(
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
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################



                                elif (active == 1) and last > bought_price_sql * (
                                        1 + profit / 2):  # #WAS profit2

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    25 - Order already opened to sell  ' + market)
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

                                        #print ('26 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('    26 Prod - Trying to Sell ' + str(
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
                                                    "26 TP SELL, price:  " + str(
                                                        format_float(last)) + "  time:   " + str(
                                                        currenttime), market))

                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            #newvalue = summ_serf() + serf * BTC_price
                                            #cursor.execute(
                                             #   'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                              #      currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


                                elif (active == 1) and (last * bought_quantity_sql * (1 + profit / 2) < (
                                            bought_price_sql * bought_quantity_sql)) and sell_signal == 1:  # #WAS profit2

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

                                        #print ('27 Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('   27 Prod -Trying to Sell ' + str(
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
                                                ("27  SL, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))

                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            #newvalue = summ_serf() + serf * BTC_price
                                            #cursor.execute(
                                             #   'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                              #      currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

                                elif (active == 1) and serf > 0 and sell_signal == 1:  # #WAS profit2

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

                                        #print ('28 Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            printed = ('  28 Prod - Trying to Sell ' + str(
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
                                                ("28  ha TP, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))

                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            #newvalue = summ_serf() + serf * BTC_price
                                           # cursor.execute(
                                             #   'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                             #       currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################






## AI_HA MODE SL
                                elif   (active == 1) and (last * bought_quantity_sql * (1 + profit * 1.5) < (
                                bought_price_sql * bought_quantity_sql)):  # #WAS profit2

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

                                        #print ('29 Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        #print summ_serf(), serf , BTC_price
                                        try:
                                            printed = ('29 Prod - Trying to sell ' + str(
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
                                                ("29  SL, p:   " + str(
                                                    format_float(last)) + " t:    " + str(currenttime), market))
                                            cursor.execute(
                                                "update orders set open_sell = %s, sell_time=%s  where market = %s and active =1",
                                                (1, currtime, market))
                                            #newvalue = summ_serf() + serf * BTC_price
                                            #cursor.execute(
                                             #   'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                             #       currenttime, newvalue, market))
                                            db.commit()
                                        except MySQLdb.Error, e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid).json()
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################








 ## AI_HA MODE END SELL

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







def order_count():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0


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



def bot_mode(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT ai_ha FROM markets WHERE active =1 and enabled=1 and market = '%s'" % market)
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


def summ_serf():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT SUM(serf_usd) FROM orders where active=0")
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float(row[0])
    #return 0
        else:
            return 0


#Function for checking the history of orders
def get_closed_orders(currency, value):
    orderhistory = c1.get_order_history(currency).json()
    orders = orderhistory['result']
    for order in orders:
        if order['Exchange'] == currency:
                return order[value]
        else:
            return False


#Check the market prices
def get_balance_from_market(market_type):
    markets_res = c1.get_markets().json()
    markets = markets_res['result']
    #print markets
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])
            # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}

#Getting balance for currency
def get_balance(currency):
    res =c1.get_balance(currency).json()
    if res['result'] is not None and len(res['result']) > 0:
        return res
        # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}



#get the orders
def get_open_orders(market):
    return c1.get_open_orders(market).json()


#check if order opened or not
def has_open_order(market, order_type):
    orders_res = c1.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
# Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True
    return False


def order_uuid(market):
    orders_res = c1.get_open_orders(market).json()
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
    else:
        return c1.get_open_orders(market).json()['result'][0]['OrderUuid']





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
    return "%.4f" % f


if __name__ == "__main__":
    main()
