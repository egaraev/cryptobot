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
#c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file
c=Client(api_key="", api_secret="")
c1 = Bittrex(config.key, config.secret, api_version=API_V1_1)   #Configuring bytrex client with API key/secret from config file




#The main function
def main():
    print('Starting sell module')

    tick()


################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
    stop_bot = int(parameters()[11])
    market_summ = c.get_market_summaries().json()['result']
    #BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    btc_trend = parameters()[12]
    max_sell_timeout = parameters()[2]
    debug_mode=parameters()[10]
    bot_mode = parameters()[23]
    bot_token= parameters()[30]
    bot_chatID= parameters()[31]
    #print market_summ
    print "Global sell parameters configured, moving to market loop"


    #global active
    if bot_mode==0:
        for summary in market_summ: #Loop trough the market summary
            try:
                if available_market_list(summary['MarketName']):
                    market = summary['MarketName']
                    print market
                    previous_order_sell_time = previous_order(market)
                    previous_order_serf = previous_serf(market)
                    #print previous_order_sell_time, previous_order_serf
                    #Candle analisys
                    lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                    currentlow = float("{0:.4f}".format(lastcandle[0]['L']))
                    currentopen = float("{0:.4f}".format(lastcandle[0]['O']))
                    currenthigh = float("{0:.4f}".format(lastcandle[0]['H']))
                    previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                    prevhigh = float("{0:.4f}".format(previouscandle[0]['H']))
                    prevclose = float("{0:.4f}".format(previouscandle[0]['C']))
                    # lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                    # currentlow5 = float("{0:.4f}".format(lastcandle5[0]['L']))
                    # currentopen5 = float("{0:.4f}".format(lastcandle5[0]['O']))
                    # currenthigh5 = float("{0:.4f}".format(lastcandle5[0]['H']))
                    # previouscandle5 = get_candles(market, 'fivemin')['result'][-2:]
                    # prevhigh5 = float("{0:.4f}".format(previouscandle5[0]['H']))
                    # prevclose5 = float("{0:.4f}".format(previouscandle5[0]['C']))
                    # hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                    # hourcurrentopen = float("{0:.4f}".format(hourlastcandle[0]['O']))
                    # hourcurrenthigh = float("{0:.4f}".format(hourlastcandle[0]['H']))
                    # daylastcandle = get_candles(market, 'day')['result'][-1:]
                    # daycurrentopen = float(daylastcandle[0]['O'])

                    candles_signal_short = str(heikin_ashi(market, 29))
                    candles_signal_long = str(heikin_ashi(market, 30))
                    hourcurrentopen = float(heikin_ashi(market, 83))
                    daycurrentopen = float(heikin_ashi(market, 84))
                    timestamp = int(time.time())
                    day_close = summary['PrevDay']   #Getting day of closing order
                #Current prices
                    last = float("{0:.4f}".format(summary['Last']))  #last price
                    bid = float("{0:.4f}".format(summary['Bid']))    #sell price
                    ask = float("{0:.4f}".format(summary['Ask']))    #buy price


                #BOUGHT PRICE
                    newbid=float("{:.5f}".format(bid - bid*0.002))

                    #print market
                #Bought Quantity need for sell order, to know at which price we bought some currency
                    bought_price_sql = float(status_orders(market, 3))
                    bought_quantity_sql = float(status_orders(market, 2))
                    danger_order=int(status_orders(market, 29))
                    sell_signal=status_orders(market, 23)
                    sell_quantity_sql = bought_quantity_sql
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
                    #Candle analisys

                    # fivemin='NONE'
                    thirtymin='NONE'
                    hour='NONE'
                    day='NONE'

                    # if last>currentopen5:
                       # fivemin='U'
                    # else:
                       # fivemin='D'

                    if last>currentopen:
                       thirtymin='U'
                    else:
                       thirtymin='D'

                    if last>hourcurrentopen:
                       hour='U'
                    else:
                       hour='D'

                    if last>daycurrentopen:
                       day='U'
                    else:
                       day='D'

                    if  candle_direction=='U' and hour_candle_direction=='U':
                        candles_status='OK'
                    elif candle_direction=='D' and hour_candle_direction=='D':
                        candles_status='DOWN'
                    else:
                        candles_status='STABLE'

                    print "Market parameters configured, moving to selling for ", market
                    try:
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()

                        serf = float("{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
                        #serf_usd = float("{0:.4f}".format(serf * BTC_price))
                        if bought_price_sql!=0:

                            #procent_serf = float(((newbid / bought_price_sql) - 1) * 100)
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
                        
                        if (percent_serf_min(market)<(-7.5)) or (previous_order_serf>0.0 and currtime-previous_order_sell_time<86400):
                            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (1, market))
                        if percent_serf_max(market)>5:
                            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (0, market))
                            
                        cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))   #- for usd trading

                        cursor.execute(
                            "update markets set current_price = %s  where market = %s and active =1",
                            (newbid, market))
                        #print "5"
                        db.commit()
                    except pymysql.Error as e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                        ########

                    #max_percent_sql = status_orders(market, 15)
                    max_percent_sql = float("{0:.2f}".format(status_orders(market, 15)))
                    min_percent_sql = float("{0:.2f}".format(status_orders(market, 24)))
                    #print market, procent_serf
                    print "Updated sell serf and procent serf stuff for", market

                    print market, procent_serf,  max_percent_sql, danger_order,  candle_direction,  hour_candle_direction                  

    # Force Stop
                    if stop_bot_force==1 and (bought_quantity_sql is not None and bought_quantity_sql != 0.0):
                            print "Checking reason 1"
                            try:
                                netto_value=float(procent_serf-0.5)
                                print ('    1 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or loosing  '     + ' and ' + str(netto_value) +'  %')
                                printed = ('    1 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or loosing  '     + ' and ' + str(netto_value) +'  %')
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("1 , Force_stop_bot p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								+ '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								+ ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) + ' MACD: ' + str(macd) + ' OBV: ' +str(obv) + ' OBV: ' +str(obv)  ,currtime, market))
                                cursor.execute('update orders set active = 0 where market =("%s")' % market)      
                                cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                newvalue = summ_serf() + (procent_serf-0.5)
                                cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")




    ### BUY FOR HA_AI mode - END

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


    # AI_HA MODE SELL START
                    print "Starting selling mechanizm for ", market
                    if bought_price_sql != None:
                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0:
                            ##Check if we have completelly green candle
                            

                            print "Checking reason 2"
                            if ((procent_serf>=2.0 and danger_order==1 and (max_percent_sql - procent_serf > 1)) or  ((max_percent_sql - procent_serf >= 1.5) and 10.0>=procent_serf >= 4.0 and candle_direction=='D' )   or ((max_percent_sql - procent_serf >= 3) and 18.0>=procent_serf >= 10.0 and candles_status=='DOWN')):
                                
                                #print "Reason 2 is OK"
                                
                                try:
                                    netto_value=float(procent_serf-0.5)
                                    print ('    2  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + ' and ' + str(netto_value) +'  %')
                                    printed = ('    2 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + ' and ' + str(netto_value) +'  %')
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("2 , Floating_TP   p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								    + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								    + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) + ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                    cursor.execute('update orders set active = 0 where market =("%s")' % market)      
                                    cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                    newvalue = summ_serf() + (procent_serf-0.5)
                                    cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"database-service")


                            if procent_serf > 0  and (((currentopen == currentlow and prevhigh <= currentopen and currentopen < currenthigh and last > prevhigh and thirtymin=='U') or (currentopen == currentlow and currentopen < currenthigh and last > prevhigh and thirtymin=='U') )):  #and slow_market==1

                                    print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                                    try:
                                        printed = (
                                            "    2.1 - We have GREEN candle for " + market + " and let`s wait it to be up")
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
                                    pass




                            # elif procent_serf > 0  and (((currentopen5 == currentlow5 and prevhigh5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevhigh5 and fivemin=='U') or (currentopen5 == currentlow5 and currentopen5 < currenthigh5 and last > prevhigh5 and fivemin=='U'))): #and normal_candles==1
                                    # print ("We have good trend for " + market)

                                    # try:
                                        # printed = ("   2.2  - We have good short term trend for " + market)
                                        # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        # cursor = db.cursor()
                                        # cursor.execute(
                                            # 'insert into logs(date, log_entry) values("%s", "%s")' % (
                                                # currenttime, printed))
                                        # db.commit()
                                    # except pymysql.Error as e:
                                        # print "Error %d: %s" % (e.args[0], e.args[1])
                                        # sys.exit(1)
                                    # finally:
                                        # db.close()
                                    # pass


                            else:
                                print "Checking reason 3"
                                #if  procent_serf>=18: 
                                if  procent_serf>=18 and (max_percent_sql - procent_serf > 1):

                                    try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    3  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    3 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + ' and ' + str(netto_value) +'  %')
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("3 , Fixed_TP p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute(
                                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                            currenttime, newvalue, market))
                                        db.commit()
                                    except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()
                                    Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")





                            print "Checking reason 4"
                            if procent_serf <= -15  and  percent_serf_max(market) < 0.1  and candle_direction=='D' and HAD_trend!="UP" and HAD_trend!="Revers-UP" and candle_score<=0:
                                try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    4  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    4 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + ' and ' + str(netto_value) +'  %')

                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("4 , Floating_SL  p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend)  + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                                        db.commit()
                                except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                finally:
                                        db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")





                            print "Checking reason 5" 
                            if procent_serf <= -20  and  macd=="Sell"  and candle_direction=='D' and HAD_trend!="UP" and HAD_trend!="Revers-UP" and HAD_trend!="STABLE" and candle_score<=0:
                                try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    4  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    4 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + ' and ' + str(netto_value) +'  %')

                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("4 , MACD_SL  p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend)  + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                                        db.commit()
                                except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                finally:
                                        db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")






                            print "Checking reason 6"
                            if procent_serf <= -30:
                                try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    5  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    5 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting   '     + ' and ' + str(netto_value) +'  %')
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("5 , Fixed_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute(
                                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                            currenttime, newvalue, market))
                                        db.commit()
                                except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                finally:
                                        db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")
									
									
									

                            print "Checking reason 7"
                            if (1.0>procent_serf>=-10 and danger_order==1 and candle_direction=='D' and percent_serf_min(market) <= -20 and timestamp-timestamp_old >=2500000) or (1.0>procent_serf>=-15 and danger_order==1 and candle_direction=='D' and hour_candle_direction=='D' and percent_serf_min(market) <= -20 and timestamp-timestamp_old >=3500000 and (candle_score<0 or news_score<0)):
                                try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    6  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and losing  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    6 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and losing   '     + ' and ' + str(netto_value) +'  %')
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("6 , Long_lasting_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute(
                                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                            currenttime, newvalue, market))
                                        db.commit()
                                except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                finally:
                                        db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")




                            print "Checking reason 8"
                            if (macd=="Sell"):
                                try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    7  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting or losing  '   + ' and ' + str(netto_value) +'  %')
                                        printed = ('    7 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or losing   '     + ' and ' + str(netto_value) +'  %')
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("7 , MACD_SELL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend)+ ' MACD: ' + str(macd) + ' OBV: ' +str(obv)  ,currtime, market))
                                        cursor.execute('update orders set active = 0 where market =("%s")' % market)   
                                        cursor.execute(
                                            'update orders set active = 0 where market =("%s")' % market)
                                        cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                        newvalue = summ_serf() + (procent_serf-0.5)
                                        cursor.execute(
                                            'insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (
                                            currenttime, newvalue, market))
                                        db.commit()
                                except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                finally:
                                        db.close()
                                Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")




                            else:
                                pass

                        else:
                            pass
                    else:
                         pass					

                else:
                    pass
            except:
                continue


    else:
        for summary in market_summ:  # Loop trough the market summary
            try:
                if available_market_list(summary['MarketName']):
                    market = summary['MarketName']

                    #Candle analisys
                    lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                    currentlow = float("{0:.4f}".format(lastcandle[0]['L']))
                    currentopen = float("{0:.4f}".format(lastcandle[0]['O']))
                    currenthigh = float("{0:.4f}".format(lastcandle[0]['H']))
                    previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                    prevclose = float("{0:.4f}".format(previouscandle[0]['C']))
                    lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                    currentlow5 = float("{0:.4f}".format(lastcandle5[0]['L']))
                    currentopen5 = float("{0:.4f}".format(lastcandle5[0]['O']))
                    currenthigh5 = float("{0:.4f}".format(lastcandle5[0]['H']))
                    previouscandle5 = get_candles(market, 'fivemin')['result'][-2:]
                    prevclose5 = float("{0:.4f}".format(previouscandle5[0]['C']))
                    hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                    hourcurrentopen = float("{0:.4f}".format(hourlastcandle[0]['O']))
                    hourcurrenthigh = float("{0:.4f}".format(hourlastcandle[0]['H']))
                    hourprevcandle = get_candles(market, 'hour')['result'][-2:]
                    hourprevopen = float("{0:.4f}".format(hourprevcandle[0]['O']))
                    hourprevclose = float("{0:.4f}".format(hourprevcandle[0]['C']))
                    candles_signal_short = str(heikin_ashi(market, 29))
                    candles_signal_long = str(heikin_ashi(market, 30))
                    timestamp = int(time.time())
                    day_close = summary['PrevDay']   #Getting day of closing order
                #Current prices
                    last = float("{0:.5f}".format(summary['Last']))  #last price
                    bid = float("{0:.5f}".format(summary['Bid']))    #sell price
                    ask = float("{0:.5f}".format(summary['Ask']))    #buy price
                    newbid=float("{:.3f}".format(bid - bid*0.002))
                    newask=float("{:.3f}".format(ask + ask*0.002))

                #Bought Quantity need for sell order, to know at which price we bought some currency
                    # BOUGHT PRICE
                    bought_quantity = get_balance_from_market(market)['result']['Available']
                    sell_quantity = bought_quantity
                    bought_price = get_closed_orders(market, 'PricePerUnit')
                    bought_price_sql = float(status_orders(market, 3))
                    bought_quantity_sql = float(status_orders(market, 2))
                    danger_order=int(status_orders(market, 29))
                    sell_signal=status_orders(market, 23)
                    sell_quantity_sql = bought_quantity_sql
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
                    slow_market = heikin_ashi(market, 3)
                    profit = parameters()[3]					

                    #Candle analisys
                    lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                    currentopen = float(lastcandle[0]['O'])
                    lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                    currentopen5 = float(lastcandle5[0]['O'])
                    hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                    hourcurrentopen = float(hourlastcandle[0]['O'])
                    daylastcandle = get_candles(market, 'day')['result'][-1:]
                    daycurrentopen = float(daylastcandle[0]['O'])
                    fivemin='NONE'
                    thirtymin='NONE'
                    hour='NONE'
                    day='NONE'
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

                    if last>daycurrentopen:
                       day='U'
                    else:
                       day='D'







                    try:
                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        # prev_serf = previous_serf(market)
                        serf = float(
                            "{0:.8f}".format(newbid * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
                        serf_usd = float("{0:.4f}".format(serf))
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
                        # print market, procent_serf
                        cursor.execute("update orders set serf = %s where market = %s and active =1 and open_sell=0 ",
                                       (serf, market))
                        if percent_serf_min(market)<(-5):
                            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (1, market))
                        if percent_serf_max(market)>2.5:
                            cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (0, market))   
                        cursor.execute(
                            "update orders set serf_usd = %s where market = %s and active =1  and open_sell=0 ",
                            (serf , market))
                        cursor.execute("update markets set current_price = %s  where market = %s and active =1",
                                       (newbid, market))
                        db.commit()
                    except pymysql.Error as e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                        ########
                    # max_percent_sql = float(status_orders(market, 15))
                    max_percent_sql = float("{0:.2f}".format(status_orders(market, 15)))
                    min_percent_sql = float("{0:.2f}".format(status_orders(market, 24)))
                    # print market, max_percent_sql, procent_serf, last, fivehourprevopen, last, currentopen
                    # print serf_usd

                    # orderid = status_orders(market, 0)
                    # history = ""
                    # print('Updating history for ' + market)
                    # try:
                        # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                        # cursor = db.cursor()
                        # cursor.execute('SELECT GROUP_CONCAT(signals) FROM orderlogs where orderid=("%s")' % orderid)
                        # history = cursor.fetchone()
                        # cursor.execute('update orders set history=%s where order_id=%s', (history, orderid))
                        # db.commit()
                    # except pymysql.Error as e:
                        # print "Error %d: %s" % (e.args[0], e.args[1])
                        # sys.exit(1)
                    # finally:
                        # db.close()

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
                            # print market, bought_quantity,
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





                        # Force Stop the bot
                    if stop_bot_force == 1 and (bought_quantity_sql != 0.0):
                        # print bought_quantity_sql
                        if has_open_order(market, 'LIMIT_SELL'):
                            print('Order already opened to sell  ' + market)
                            try:
                                printed = ('    3 - Order already opened to sell  ' + market)
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
                            try:
                                netto_value=float(procent_serf-0.5)
                                print ('    1 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or loosing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                printed = ('    1 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting or loosing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("1 , Force_stop_bot p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								+ '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								+ ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                db.commit()	
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")
                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                            print c1.sell_limit(market, sell_quantity, newbid)
                            #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                    else:
                        pass




                        # What if we have sent the sell order to bittrex?
                    if open_sell(market) == 1:
                        # print get_balance_from_market(market)['result']['Available']
                        quantity_left = float(get_balance_from_market(market)['result']['Available'])
                        btc_quantity = float(quantity_left * newbid)

                        # print btc_quantity

                        if has_open_order(market, 'LIMIT_SELL'):
                            if currtime - sell_time(market) < max_sell_timeout:
                                print('Order already opened to sell  ' + market)
                                try:
                                    printed = ('    5 - Order already opened to sell  ' + market)
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
                                    printed = ('    6- Order has been cancelled  ' + market)
                                    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    cursor = db.cursor()
                                    cursor.execute(
                                        'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                    cursor.execute(
                                        "update orders set open_sell = 0, timestamp=%s  where active=1 and market = %s ",
                                        (timestamp, market))
                                    db.commit()
                                except pymysql.Error as e:
                                    print "Error %d: %s" % (e.args[0], e.args[1])
                                    sys.exit(1)
                                finally:
                                    db.close()
                                #########################################CANCEL OLD ORDER#####
                                uuid = order_uuid(market)
                                print c1.market_cancel(uuid)
                                #Mail("egaraev@gmail.com", "egaraev@gmail.com", "Cancel order", printed,"database-service")
                                #############################################################


                        elif get_balance_from_market(market)['result']['Available'] > 0 and btc_quantity > 0.0005:
                            print(' Order failed  ' + market)
                            rest_balance = get_balance_from_market(market)['result']['Available']
                            try:
                                printed = ('    6- Order has been failed to sell  ' + market)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute(
                                    'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                cursor.execute(
                                    'update orders set open_sell = 0  where active=1 and market =("%s")' % market)
                                cursor.execute("update orders set quantity = %s where market = %s and active =1",
                                               (rest_balance, market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            #Mail("egaraev@gmail.com", "egaraev@gmail.com", "Failed order", printed, "database-service")



                        else:
                            try:
                                print ('    7 Prod -This currency has been sold ' + market)
                                printed = ('    7 Prod -This currency has been sold   ' + market)
                                netto_value=float(procent_serf-0.5)
                                db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                cursor = db.cursor()
                                cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                newquantity = get_closed_orders(market, 'Quantity')
                                cursor.execute("update orders set quantity = %s where market = %s and active =1",(newquantity, market))
                                cursor.execute('update orders set active = 0, open_sell = 0  where active =1 and market =("%s")' % market)  # -this is deactivating the order  !!!!
                                newvalue = summ_serf() + (procent_serf-0.5)
                                cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                                cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                                db.commit()
                            except pymysql.Error as e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                            finally:
                                db.close()
                            #Mail("egaraev@gmail.com", "egaraev@gmail.com", "Currency sold", printed, "database-service")

                            break
                            # print market

  

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






                            # AI_HA MODE SELL START
                    if bought_price_sql != None or bought_price != None:  # added OR

                        if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                            # print market, bought_quantity_sql, current_balance
                            pass
                            # If curent balance of this currency more then zero
                        elif bought_quantity_sql > 0:  # Need to add bought_quantity without sql
                            ##Check if we have completelly green candle


                            #####################################################
                            if ((2.0>procent_serf>=0.7 and danger_order==1 and max_percent_sql - procent_serf >= 0.3) or  (max_percent_sql - procent_serf >= 0.8 and 5>=max_percent_sql >= 2 and candle_direction=='D' )   or (max_percent_sql - procent_serf >= 1.5 and 9>=max_percent_sql >= 5 and candle_direction=='D' and hour_candle_direction=='D')):
                                # if we have already opened order to sell								
                                if has_open_order(market, 'LIMIT_SELL'):
                                    # print('Order already opened to sell  ' + market)
                                    try:
                                        printed = ('    5 - Order already opened to sell  ' + market)
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                            currenttime, printed))
                                        db.commit()
                                    except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()


                                else:
                                    # Lets Sell some
                                    
                                    try:
                                        netto_value=float(procent_serf-0.5)
                                        print ('    2 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                        printed = ('    2 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                        db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                        cursor = db.cursor()
                                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                        cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("2 , Floating p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								        + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								        + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                        cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                        db.commit()									
                                    except pymysql.Error as e:
                                        print "Error %d: %s" % (e.args[0], e.args[1])
                                        sys.exit(1)
                                    finally:
                                        db.close()
                                    #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                    print c1.sell_limit(market, sell_quantity, newbid)
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                    break

                                    #####################################################

                            if serf_usd > 0 and (((
                                                                      currentopen == currentlow and prevclose <= currentopen and currentopen < currenthigh and last > prevclose and thirtymin == 'U') or (
                                            currentopen == currentlow and currentopen < currenthigh and last > prevclose and thirtymin == 'U'))):

                                print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                                try:
                                    printed = (
                                        "    7 - We have GREEN candle for " + market + " and let`s wait it to be up")
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
                                pass




                            # elif serf_usd > 0 and (((
                                                                        # currentopen5 == currentlow5 and prevclose5 <= currentopen5 and currentopen5 < currenthigh5 and last > prevclose5 and fivemin == 'U') or (
                                            # currentopen5 == currentlow5 and currentopen5 < currenthigh5 and last > prevclose5 and fivemin == 'U'))):
                                # print ("We have good trend for " + market)

                                # try:
                                    # printed = ("   8  - We have good short term trend for " + market)
                                    # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                    # cursor = db.cursor()
                                    # cursor.execute(
                                        # 'insert into logs(date, log_entry) values("%s", "%s")' % (
                                            # currenttime, printed))
                                    # db.commit()
                                # except pymysql.Error as e:
                                    # print "Error %d: %s" % (e.args[0], e.args[1])
                                    # sys.exit(1)
                                # finally:
                                    # db.close()
                                # pass




                            else:

                                if procent_serf>=10:
                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    11 - Order already opened to sell  ' + market)
                                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                                currenttime, printed))
                                            db.commit()
                                        except pymysql.Error as e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()


                                    else:
                                        # Lets Sell some
                                        try:
                                            netto_value=float(procent_serf-0.5)
                                            print ('    3 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            printed = ('    3 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and getting  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                            cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("3 , Fixed_TP p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								            + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								            + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                            cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                            db.commit()
                                        except pymysql.Error as e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid)
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        break




                                        # AI changed to down and we have our profit, so lets sell it in time
                                elif procent_serf <= -7.5  and  percent_serf_max(market) < 0.1  and candle_direction=='D' and HAD_trend!="UP" and HAD_trend!="Revers-UP" and candle_score<=0:
                                    if has_open_order(market, 'LIMIT_SELL'):
                                        # print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('    13 - Order already opened to sell  ' + market)
                                            db = pymysql.connect("database-service", "cryptouser", "123456",
                                                                 "cryptodb")
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

                                        # print ('23 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                        try:
                                            netto_value=float(procent_serf-0.5)
                                            print ('    4 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and losing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            printed = ('    4 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and loosing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                            cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("4 , Floating_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								            + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								            + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                            cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                            db.commit()
                                        except pymysql.Error as e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"database-service")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid)
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        break



                                elif procent_serf <= -15:

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('Order already opened to sell  ' + market)
                                        try:
                                            printed = ('  15 Order already opened to sell  ' + market)
                                            db = pymysql.connect("database-service", "cryptouser", "123456",
                                                                 "cryptodb")
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
 
                                        try:
                                            netto_value=float(procent_serf-0.5)
                                            print ('    5 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and losing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            printed = ('    5 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and loosing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                            cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("5 , Fixed_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								            + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								            + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                            cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                            db.commit()
                                        except pymysql.Error as e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "database-service")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid)
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        break


                                        # We have sell signal and profit a little bit more then zero, so lets sell it in time
                                elif (1.0>procent_serf>=-5 and danger_order==1 and candle_direction=='D' and percent_serf_min(market) <= -10 and timestamp-timestamp_old >=2500000) or (1.0>procent_serf>=-7.5 and danger_order==1 and candle_direction=='D' and hour_candle_direction=='D' and percent_serf_min(market) <= -12 and timestamp-timestamp_old >=3500000 and (candle_score<0 or news_score<0)):

                                    if has_open_order(market, 'LIMIT_SELL'):
                                        print('  17 Order already opened to sell  ' + market)
                                        try:
                                            printed = ('  17 Order already opened to sell  ' + market)
                                            db = pymysql.connect("database-service", "cryptouser", "123456",
                                                                 "cryptodb")
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

                                        try:
                                            netto_value=float(procent_serf-0.5)
                                            print ('    6 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and losing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            printed = ('    6 - Trying to sell ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(newbid)) + '  and loosing  ' + str(format_float(serf)) + ' USD'    + ' and ' + str(netto_value) +'  %')
                                            db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                                            cursor = db.cursor()
                                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                                            cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("6 , Long_lasting_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(HAD_trend) 
								            + '  Day_candle_direction ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) 
								            + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' Hour_candle_direction: ' + str(hour_candle_direction) + ' Trend: ' + str(trend),currtime, market))  
                                            cursor.execute("update orders set open_sell = %s  where market = %s and active =1",(1, market))
                                            db.commit()
                                        except pymysql.Error as e:
                                            print "Error %d: %s" % (e.args[0], e.args[1])
                                            sys.exit(1)
                                        finally:
                                            db.close()
                                        #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"database-service")
                                        #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                        print c1.sell_limit(market, sell_quantity, newbid)
                                    #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                    break








                                else:
                                    pass






                    else:
                        pass



                else:
                    pass
            except:
                continue


### FUNCTIONS
###############################################################################################################

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
    cursor.execute("SELECT * FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False





def previous_order(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT sell_time FROM `orders` WHERE  market = '%s' and active=0 ORDER BY order_id DESC LIMIT 1" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0


def previous_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT percent_serf FROM `orders` WHERE  market = '%s' and active=0 ORDER BY order_id DESC LIMIT 1" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0


def parameters():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24]), (row[25]), (row[26]), (row[27]), (row[28]), (row[29]), (row[30]), (row[31]), (row[32])

    return 0



def ai_prediction(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_direction FROM markets WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])

    return 0

def ai_prediction_price(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_price FROM markets WHERE active =1 and ai_direction='UP' and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])

    return 0





def percent_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0




def percent_serf_max(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_max FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0


def percent_serf_min(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_min FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0


def open_sell(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT open_sell FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0







def sell_time(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



#Check first iteration orders in mysql
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




def summ_serf():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    # market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0")
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float("{0:.2f}".format(row[0]))
            # return 0
        else:
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




def format_float(f):
    return "%.4f" % f


if __name__ == "__main__":
    main()

