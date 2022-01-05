#Imports from modules, libraries and config files
from bittrex.bittrex import *
import config
import pybittrex
from pybittrex.client import Client
import requests
import time
import datetime
import hmac
import hashlib
import pymysql
import sys
import smtplib
import calendar
import json

c = Client(api_key="", api_secret="")
c1 = Bittrex(config.key, config.secret, api_version=API_V1_1)   #Configuring bytrex client with API key/secret from config file

#The main function
def main():
    print('Starting buy module')
    tick()

################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    max_buy_timeout = parameters()[1]
    stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
    stop_bot = int(parameters()[11])
    market_summ = c.get_market_summaries().json()['result']
    #print (market_summ)
    #BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    debug_mode=parameters()[10]
    max_orders = int(parameters()[5])
    current_order_count = int(order_count())
    bot_mode=parameters()[23]
    bot_token= parameters()[30]
    bot_chatID= parameters()[31]
    #print (bot_token, bot_chatID)
    now = datetime.datetime.now()
    currentdate = now.strftime("%Y-%m-%d")


    print "Global buy parameters configured, moving to market loop"
    dayofweek=weekday()

    #global active
    if bot_mode==0:	
        for summary in market_summ: #Loop trough the market summary
            try:
                if available_market_list(summary['MarketName']):
                    market = summary['MarketName']
                    print (market)
                    timestamp = int(time.time())
                    day_close = summary['PrevDay']   #Getting day of closing order
                #Current prices
                    last = float(summary['Last'])  #last price
                    bid = float(summary['Bid'])    #sell price
                    ask = float(summary['Ask'])    #buy price
                    #print market, last, bid, ask
                #How much market has been changed
                    percent_chg = float(((last / day_close) - 1) * 100)

                #HOW MUCH TO BUY
                    buy_quantity = buy_size / last

                #BOUGHT PRICE
                    newbid=float("{:.5f}".format(bid - bid*0.002))
                    newask=float("{:.5f}".format(ask + ask*0.002))
                   # print newask

                #Bought Quantity need for sell order, to know at which price we bought some currency
                    bought_price_sql = float(status_orders(market, 3))
                    bought_quantity_sql = float(status_orders(market, 2))
                    active = active_orders(market)
                    iteration = int(iteration_orders(market))
                    timestamp_old = int(timestamp_orders(market))
                    now = datetime.datetime.now()
                    currenttime = now.strftime("%Y-%m-%d %H:%M")
                    HAD_trend=heikin_ashi(market, 18)
                    candle_direction=heikin_ashi(market, 77)
                    tweet_positive=float(heikin_ashi(market, 36))
                    hour_candle_direction=heikin_ashi(market, 76)
                    tweet_negative=float(heikin_ashi(market, 37))
                    tweet_ratio = float("{0:.2f}".format(tweet_positive/tweet_negative))
                    ai_price=heikin_ashi(market,7)
                    ai_direction=str(heikin_ashi(market,9))
                    tweet_polarity=heikin_ashi(market,65)
                    tweet_score=heikin_ashi(market,66)
                    candle_score=heikin_ashi(market,68)
                    news_score=heikin_ashi(market,72)
                    candle_pattern=heikin_ashi(market,69)
                    previous_date = str(heikin_ashi(market,46))
                    trend = str(heikin_ashi(market,78))					
                    macd = str(heikin_ashi(market,79))
                    kov = str(heikin_ashi(market,80))					
                    obv = str(heikin_ashi(market,81))
					

                    candles_status='NONE'
                    #print (percent_sql)
					
                    macd_fluc = macd_fluctuation(market)
                    macd_first_day=macd_fluc[0]
                    macd_second_day=macd_fluc[1]
                    macd_third_day=macd_fluc[2]
                    if (macd_third_day!='none' and macd_second_day!='none' and macd_first_day!='none') or  (macd_third_day!='none' and macd_second_day!='none')  or (macd_third_day!='none'  and macd_first_day!='none') or (macd_third_day!=macd_first_day) or (macd_second_day!=macd_third_day):
                       macd_fluct_status = 'fluctuation'
                    else:
                       macd_fluct_status = 'not-fluctuation'	

                    obv_fluc = obv_fluctuation(market)
                    obv_first_day=obv_fluc[0]
                    obv_second_day=obv_fluc[1]
                    obv_third_day=obv_fluc[2]
                    if (obv_third_day!='none' and obv_second_day!='none' and obv_first_day!='none') or  (obv_third_day!='none' and obv_second_day!='none')  or (obv_third_day!='none'  and obv_first_day!='none') or (obv_third_day!=obv_first_day) or (obv_second_day!=obv_third_day):
                       obv_fluct_status = 'fluctuation'
                    else:
                       obv_fluct_status = 'not-fluctuation'	

                    print macd_fluct_status, obv_fluct_status	
                    print macd_third_day, macd_second_day, macd_first_day
                    print obv_third_day, obv_second_day, obv_first_day 					
                 
                    

                    if  candle_direction=='U' and hour_candle_direction=='U':
                        candles_status='OK'
                    elif candle_direction=='D' and hour_candle_direction=='D':
                        candles_status='DOWN'
                    else:
                        candles_status='STABLE'
                    
                    print market, candles_status, HAD_trend
                        
  
                    



                    print "Market parameters configured, moving to buy for ", market
                    try:
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        serf = float("{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
                        if bought_price_sql!=0:
                            procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))
                            if procent_serf>=percent_serf_max(market):
                                cursor.execute("update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                            elif procent_serf<percent_serf_min(market):
                                cursor.execute(
                                "update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",
                                (procent_serf, market))
                            else:
                                cursor.execute("update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                        cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
                        cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))   ##- for usd trading
                        #cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf*BTC_price, market))
                        cursor.execute(
                            "update markets set current_price = %s  where market = %s and active =1",
                            (newbid,  market))
                        db.commit()
                    except pymysql.Error as e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                        ########

                    max_percent_sql = status_orders(market, 15)
                    print "Updated serf and procent serf stuff for" , market



    #FIRST ITERATION - BUY
                    #spread=((ask/bid)-1)*100
                    print "Starting buying mechanizm for " , market
                    #print tweet_positive, tweet_negative, HAD_trend, candle_score, tweet_polarity, candles_status, macd, current_order_count, max_orders
                    if ((stop_bot == 0) and stop_bot_force == 0) and tweet_positive>tweet_negative and HAD_trend!="DOWN" and HAD_trend!="Revers-DOWN" and candle_score>=0 and tweet_polarity>0.14  and candles_status=='OK' and macd=="Buy" and current_order_count <= max_orders  and obv=="Buy" and macd_fluct_status=='not-fluctuation' and obv_fluct_status=='not-fluctuation': # and news_score>=0.9
                    #if ((stop_bot == 0) and stop_bot_force == 0):
                            # If we have some currency on the balance
                            if bought_quantity_sql !=0.0:
                                print ('    2 - We already have ' + str(
                                        format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                                try:
                                    printed = ('    2 - We already have ' + str(
                                        format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                            # if we have some active orders in sql
                            elif active == 1 and iteration != 0:
                                print  ('    3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                                try:
                                    printed = ('    3 - We already have ' + str(
                                        float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                            else:
                                # Buy some currency by market analize first time
                                try:
                                    print ('    4- Purchasing '  + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(newask)))
                                    printed = ('    4- Purchasing '  + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(newask)))
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, last, "1", currenttime, timestamp,  '  HA: ' + str(HAD_trend) + '  Day_candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+' MACD: ' +str(macd)  +' OBV: ' +str(obv)))
                                    cursor.execute("update orders set serf = %s, one_step_active =1 where market = %s and active =1",(serf, market))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "database-service")
                                break



                                ##DEBUG MESSAGE
                    if debug_mode == 1:
                        try:
                            printed = ("    XXX - Bot is working with " + market)
                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                    currenttime, printed))
                            db.commit()
                        except pymysql.Error as e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()





                else:
                    pass
            except:
                continue


##############################################################################
###############################################################################

    else:

        for summary in market_summ:  # Loop trough the market summary
            try:
                if available_market_list(summary['MarketName']):
                    market = summary['MarketName']
                    print (market)
                    # Candle analisys
                    lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                    currentopen = float(lastcandle[0]['O'])
                    currenthigh = float(lastcandle[0]['H'])
                    hourpreviouscandle4 = get_candles(market, 'hour')['result'][-5:]
                    hourprevopen4 = float(hourpreviouscandle4[0]['O'])
                    fivehourcurrentopen = hourprevopen4
                    hourpreviouscandle9 = get_candles(market, 'hour')['result'][-10:]
                    hourprevopen9 = float(hourpreviouscandle9[0]['O'])
                    hourpreviouscandle5 = get_candles(market, 'hour')['result'][-6:]
                    hourprevclose5 = float(hourpreviouscandle5[0]['C'])
                    fivehourprevopen = hourprevopen9
                    fivehourprevclose = hourprevclose5
                    lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                    currentlow5 = float(lastcandle5[0]['L'])
                    currentopen5 = float(lastcandle5[0]['O'])
                    currenthigh5 = float(lastcandle5[0]['H'])
                    hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                    hourcurrentopen = float(hourlastcandle[0]['O'])
                    hourcurrenthigh = float(hourlastcandle[0]['H'])
                    timestamp = int(time.time())

                    # Current prices
                    last = float(summary['Last'])  # last price
                    bid = float(summary['Bid'])  # sell price
                    ask = float(summary['Ask'])  # buy price
                    newbid=float("{:.3f}".format(bid - bid*0.002))
                    newask=float("{:.3f}".format(ask + ask*0.002))
                    #print newask
                    # How much market has been changed

                    # HOW MUCH TO BUY
                    buy_quantity = buy_size / last
                    bought_quantity = get_balance_from_market(market)['result']['Available']

                    balance_res = get_balance_from_market(market)
                    current_balance = balance_res['result']['Balance']
                    current_available = balance_res['result']['Available']

                    bought_price_sql = float(status_orders(market, 3))
                    bought_quantity_sql = float(status_orders(market, 2))
                    active = active_orders(market)
                    iteration = int(iteration_orders(market))
                    timestamp_old = int(timestamp_orders(market))
                    now = datetime.datetime.now()
                    currenttime = now.strftime("%Y-%m-%d %H:%M")
                    HAD_trend=heikin_ashi(market, 18)
                    candle_direction=heikin_ashi(market, 77)
                    tweet_positive=float(heikin_ashi(market, 36))
                    hour_candle_direction=heikin_ashi(market, 76)
                    tweet_negative=float(heikin_ashi(market, 37))
                    tweet_ratio = float("{0:.2f}".format(tweet_positive/tweet_negative))
                    ai_price=heikin_ashi(market,7)
                    ai_direction=str(heikin_ashi(market,9))
                    tweet_polarity=heikin_ashi(market,65)
                    tweet_score=heikin_ashi(market,66)
                    candle_score=heikin_ashi(market,68)
                    news_score=heikin_ashi(market,72)
                    candle_pattern=heikin_ashi(market,69)
                    previous_date = str(heikin_ashi(market,46))
                    trend = str(heikin_ashi(market,78))		


                    fivemin = 'NONE'
                    thirtymin = 'NONE'
                    hour = 'NONE'
                    candles_status = 'OK'

                    if last > currentopen5:
                        fivemin = 'U'
                    elif last == currenthigh5:
                        fivemin = 'H'
                    else:
                        fivemin = 'D'

                    if last > currentopen:
                        thirtymin = 'U'
                    elif last == currenthigh:
                        thirtymin = 'H'
                    else:
                        thirtymin = 'D'

                    if last > hourcurrentopen:
                        hour = 'U'
                    elif last == hourcurrenthigh:
                        hour = 'H'
                    else:
                        hour = 'D'

                    if fivemin == 'D' and thirtymin == 'D' and fivemin == 'D':
                        candles_status = 'DOWN'
                    else:
                        candles_status = 'OK'


                    #print ("test")
                    try:
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        # cursor.execute("update parameters set usdt_btc_price = %s, btc_ha_direction_day =%s where id = %s", (BTC_price, btc_trend, 1))
                        # prev_serf = previous_serf(market)
                        serf = float(
                            "{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
                        if bought_price_sql != 0:
                            procent_serf = float("{0:.2f}".format(((newbid / bought_price_sql) - 1) * 100))
                            cursor.execute(
                                "update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",
                                (procent_serf, market))
                            if procent_serf >= percent_serf_max(market):
                                cursor.execute(
                                    "update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",
                                    (procent_serf, market))
                            elif procent_serf < percent_serf_min(market):
                                cursor.execute(
                                    "update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",
                                    (procent_serf, market))
                            else:
                                cursor.execute(
                                    "update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",
                                    (procent_serf, market))

                        cursor.execute("update orders set serf = %s where market = %s and active =1 and open_sell=0 ",
                                       (serf, market))
                        # cursor.execute(
                            # "update orders set serf_usd = %s where market = %s and active =1  and open_sell=0 ",
                            # (serf * BTC_price, market))

                        cursor.execute("update markets set current_price = %s  where market = %s and active =1",
                                       (newbid, market))

                        db.commit()
                    except pymysql.Error as e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                        ########
                    max_percent_sql = status_orders(market, 15)

                    #print market, bought_quantity



                    # print market, bought_quantity
                    if bought_quantity is not None:
                        if has_open_order(market, 'LIMIT_SELL'):
                            print('Order already opened to sell  ' + market)
                            try:
                                printed = ('    1 - Order already opened to sell  ' + market)
                                uuid = order_uuid(market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'update orders set uuid =%s where active=1 and open_sell=1 and market =%s',
                                    (uuid, market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()

                        elif has_open_order(market, 'LIMIT_BUY'):
                            print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    2 - Order already opened to buy  ' + market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        else:
                            #print market, bought_quantity
                            if timestamp - timestamp_old < 1800:
                                try:
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute("update orders set quantity = %s where market = %s and active =1",
                                                   (bought_quantity, market))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                    ########
                            else:
                                pass
                    else:
                        pass

                        # print market, candles


                        # What if we have sent the buy order to bittrex?

                    if open_buy(market) == 2:
                        #print market

                        if has_open_order(market, 'LIMIT_BUY'):
                            if currtime - buy_time(market) < max_buy_timeout:
                                print('Order already opened to buy  ' + market)
                                try:
                                    printed = ('    8 - Order already opened to buy  ' + market)
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()

                            else:
                                print(' Order cancelled  ' + market)
                                try:
                                    printed = ('    9 - Order has been cancelled  ' + market)
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    cursor.execute(
                                        'delete from orders  where active=2 and market =("%s")' % market)
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                #########################################CANCEL OLD ORDER#####
                                uuid = order_uuid(market)
                                print c1.market_cancel(uuid)
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed,
                                     "database-service")
                                #############################################################


                        elif current_available == 0.0 or current_balance == 0.0 and currtime - buy_time(
                                market) > max_buy_timeout:
                            print(' Order failed  ' + market)
                            try:
                                printed = ('    6- Order has been failed to buy  ' + market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'update orders set active= 3  where active=2 and market =("%s")' % market)
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Failed order", printed, "database-service")



                        else:
                            try:
                                print ('    10 Prod -This currency has been bought ' + market)
                                printed = ('    10 Prod -This currency has been bought   ' + market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    "update orders set quantity = %s, price=%s, active=1, date=%s, timestamp=%s, iteration=1, params=%s, heikin_ashi=%s  where market = %s and active =2",
                                    (buy_quantity, newbid, currenttime, timestamp,
                                     '  HA: ' + str(HAD_trend) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ', HAD_trend, market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency bought", printed,
                                 "database-service")

                            break
                            # print market


                    if  ((stop_bot == 0) and stop_bot_force == 0):
                    #if ((stop_bot == 0) and stop_bot_force == 0) and tweet_positive>tweet_negative and HAD_trend!="DOWN" and HAD_trend!="Revers-DOWN" and candle_score>=0 and tweet_polarity>0.14 and news_score>=0.9 and candle_direction=="U" and hour_candle_direction=="U":
                        # If we have opened order on bitrex
                        #print (order_uuid(market)
                        if has_open_order(market, 'LIMIT_BUY'):
                            # print('Order already opened to buy  ' + market)
                            try:
                                printed = ('    2 .1 - Order already opened to buy  ' + market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        # If we have some currency on the balance

                        elif ((current_balance != 0.0) and (current_available != 0.0)):
                            #print market, current_balance, current_available
                            print('We already have ' + str(format_float(current_balance)) + ' units of  ' + market + ' on our balance')
                            try:
                                printed = ('    3.1 - We already have ' + str(
                                    format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        # if we have some active orders in sql
                        elif active == 1 or (active == 1 and order_uuid(market) != 0):
                            # print ('We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                            try:
                                printed = ('    3.2 - We already have ' + str(
                                    float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                        else:
                            # Buy some currency by market analize first time
                            try:
                                #print newask
                                printed = ('    4.1 - Prod - Trying to Purchase  ' + str(
                                    format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(
                                    format_float(bid)))
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'insert into orders(market, quantity, price, active, date, timestamp, iteration, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                        market, buy_quantity, newask, "2", currenttime, timestamp, "1",
                                        '  HA: ' + str(HAD_trend) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ', HAD_trend))
                                cursor.execute(
                                    "update orders set serf = %s where market = %s and active =2",
                                    (serf, market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "database-service")
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                            # print c.buy_limit(market, fiboquantity*2, last).json()
                            print c1.buy_limit(market, buy_quantity, newask)
                            #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!##################################
                            break

                            ### FOR HA_AI mode - END
                            # print market, percent_sql
                            ##DEBUG MESSAGE
                    if debug_mode == 1:
                        try:
                            printed = ("    XXX - Bot is working with " + market)
                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()
                            cursor.execute(
                                'insert into logs(date, log_entry) values("%s", "%s")' % (
                                    currenttime, printed))
                            db.commit()
                        except pymysql.Error as e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()





                else:
                    pass
            except:
                continue


### FUNCTIONS
###############################################################################################################

def macd_fluctuation(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT GROUP_CONCAT(macd_signal) FROM `history` WHERE market='%s' order by id desc" % market)
    res = cursor.fetchall()
    for row in res:
       r = list(row[0].split(","))
       r = r[-3:]
       return (r)
    return 0


def obv_fluctuation(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT GROUP_CONCAT(obv_signal) FROM `history` WHERE market='%s' order by id desc" % market)
    res = cursor.fetchall()
    for row in res:
       r = list(row[0].split(","))
       r = r[-3:]
       return (r)
    return 0



def heikin_ashi(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
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
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE active =1 and enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False







def order_count():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0


def parameters():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24]), (row[25]), (row[26]), (row[27]), (row[28]), (row[29]), (row[30]), (row[31]), (row[32])

    return 0





def percent_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0




def percent_serf_max(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_max FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0


def percent_serf_min(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_min FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0







def open_buy(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT active FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0









def buy_time(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT timestamp FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0







#Check active orders in mysql
def timestamp_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[6])

    return 0





#Check active orders in mysql
def active_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
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
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
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
    orderhistory = c1.get_order_history(currency)
    orders = orderhistory['result']
    for order in orders:
        if order['Exchange'] == currency:
                return order[value]
        else:
            return False

def ai_prediction(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_direction FROM markets  WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])

    return 0


#Check the market prices
def get_balance_from_market(market_type):
    markets_res = c1.get_markets()
    markets = markets_res['result']
    #print markets
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])
            # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}

#Getting balance for currency
def get_balance(currency):
    res =c1.get_balance(currency)
    if res['result'] is not None and len(res['result']) > 0:
        return res
        # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}



#get the orders
def get_open_orders(market):
    return c1.get_open_orders(market)


#check if order opened or not
def has_open_order(market, order_type):
    orders_res = c1.get_open_orders(market)
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
# Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True
    return False


def order_uuid(market):
    orders_res = c1.get_open_orders(market)
    orders = orders_res['result']
    if orders is None or len(orders) == 0:
        return False
    else:
        return c1.get_open_orders(market)['result'][0]['OrderUuid']





# def get_candles(market, tick_interval):
    # url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market +'&tickInterval=' + str(tick_interval)
    # return signed_request(url)

def get_candles(market, tick_interval):
    url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    r = requests.get(url)
    requests.session().close()
    return r.json()


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()

def iteration_orders(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[7])

    return 0


def weekday():
    now = datetime.datetime.now()
    check = calendar.weekday(now.year, now.month, now.day)
    if check is 0:
        return "Monday"
    elif check is 1:
        return "Tuesday"
    elif check is 2:
        return "Wednesday"
    elif check is 3:
        return "Thursday"
    elif check is 4:
        return "Friday"
    elif check is 5:
        return "Saturday"
    elif check is 6:
        return "Sunday"
    else:
        return "WTF??"


#def dow(date):
#    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#    dayNumber=date.weekday()



def format_float(f):
    return "%.4f" % f


if __name__ == "__main__":
    main()

