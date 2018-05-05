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
################################################################################################################
#what will be done every loop iteration
def tick():
    buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
    buy_size2 = parameters()[1]  # The size for opening orders for FIBONACI Mode
    #sell_size = parameters()[2]  #Minimal size for closing oders
    profit = parameters()[3]  #The size of profit we want to take
    #stop_loss = parameters()[4]  #If stop_loss==1 we use stop loss mechanism, of not - we use fibonachi mechanism
    maxiteration = parameters()[5]
    order_multiplier = parameters()[6]
    min_percent_chg = float(parameters()[7])
    max_percent_chg = float(parameters()[8])
    last_orders_quantity = int(parameters()[10])
    stop_bot = int(parameters()[11])
    market_summ = c.get_market_summaries().json()['result']
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())


    btclastcandle = get_candles('USDT-BTC', 'day')['result'][-1:]
    btccurrentlow = float(btclastcandle[0]['L'])
    btccurrentopen = float(btclastcandle[0]['O'])
    btccurrentclose = float(btclastcandle[0]['C'])
    btccurrenthigh = float(btclastcandle[0]['H'])
    btcprevcandle = get_candles('USDT-BTC', 'day')['result'][-2:]
    btcprevlow = float(btcprevcandle[0]['L'])
    btcprevopen = float(btcprevcandle[0]['O'])
    btcprevclose = float(btcprevcandle[0]['C'])
    btcprevhigh = float(btcprevcandle[0]['H'])

    btclastcandlehour = get_candles('USDT-BTC', 'hour')['result'][-1:]
    btccurrentlowhour = float(btclastcandlehour[0]['L'])
    btccurrentopenhour = float(btclastcandlehour[0]['O'])
    btccurrentclosehour = float(btclastcandlehour[0]['C'])
    btccurrenthighhour = float(btclastcandlehour[0]['H'])
    btcprevcandlehour = get_candles('USDT-BTC', 'hour')['result'][-2:]
    btcprevlowhour = float(btcprevcandlehour[0]['L'])
    btcprevopenhour = float(btcprevcandlehour[0]['O'])
    btcprevclosehour = float(btcprevcandlehour[0]['C'])
    btcprevhighhour = float(btcprevcandlehour[0]['H'])

    lasttimeday = int(parameters()[17])
    BTC_HA_PREV_Close = int(parameters()[13])
    BTC_HA_PREV_Open = int(parameters()[14])
    BTC_HA_PREV_Low = int(parameters()[15])
    BTC_HA_PREV_High = int(parameters()[16])


    BTC_HA_Close = (btccurrentopen + btccurrenthigh + btccurrentlow + btccurrentclose) / 4
    BTC_HA_Open = (BTC_HA_PREV_Open + BTC_HA_PREV_Close) / 2
    elements1 = numpy.array([btccurrenthigh, btccurrentlow, BTC_HA_Open, BTC_HA_Close])
    BTC_HA_High = elements1.max(0)
    BTC_HA_Low = elements1.min(0)

    if currtime-lasttimeday>86400:
        try:
            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
            cursor = db.cursor()
            cursor.execute("update parameters set btc_ha_close_day = %s, btc_ha_open_day =%s, btc_ha_low_day =%s, btc_ha_high_day =%s, btc_ha_time_day =%s  where id = %s",(BTC_HA_Close, BTC_HA_Open, BTC_HA_Low, BTC_HA_High, currtime, 1))
            db.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            db.close()
    else:
        pass

    lasttimehour = int(parameters()[22])


    BTC_HA_PREV_Close_hour = int(parameters()[18])
    BTC_HA_PREV_Open_hour = int(parameters()[19])
    BTC_HA_PREV_Low_hour = int(parameters()[20])
    BTC_HA_PREV_High_hour = int(parameters()[21])

    BTC_HA_Close_hour = (btccurrentopenhour + btccurrenthighhour + btccurrentlowhour + btccurrentclosehour) / 4
    BTC_HA_Open_hour = (BTC_HA_PREV_Open_hour + BTC_HA_PREV_Close_hour) / 2
    elements2 = numpy.array([btccurrenthighhour, btccurrentlowhour, BTC_HA_Open_hour, BTC_HA_Close_hour])
    BTC_HA_High_hour = elements2.max(0)
    BTC_HA_Low_hour = elements2.min(0)

    if currtime-lasttimehour>3600:
        try:
            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
            cursor = db.cursor()
            cursor.execute("update parameters set btc_ha_close_hour = %s, btc_ha_open_hour =%s, btc_ha_low_hour =%s, btc_ha_high_hour =%s, btc_ha_time_hour =%s  where id = %s",(BTC_HA_Close_hour, BTC_HA_Open_hour, BTC_HA_Low_hour, BTC_HA_High_hour, currtime, 1))
            db.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            db.close()
    else:
        pass


    btc_trend ="NONE"
    btc_trend_hour = "NONE"


    direction_down_short0=False
    direction_down_short1=False
    direction_up_short0=False
    direction_up_short1=False
    direction_down1 = False

    hour_direction_down_short0=False
    hour_direction_down_short1=False
    hour_direction_up_short0=False
    hour_direction_up_short1=False

    #print BTC_HA_PREV_Close, BTC_HA_PREV_Open

    direction_down0=(BTC_HA_Close < BTC_HA_Open)
    direction_down1=(BTC_HA_PREV_Close < BTC_HA_PREV_Open)
    direction_down_long_0=(BTC_HA_Open == BTC_HA_High)
    direction_down_long_1=(BTC_HA_PREV_Open == BTC_HA_PREV_High)
    direction_down_longer=(numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_down0 and direction_down1)
    direction_spin0=(BTC_HA_Open == BTC_HA_Close)
    direction_spin1=(BTC_HA_PREV_Open == BTC_HA_PREV_Close)

    hour_direction_down0 = (BTC_HA_Close_hour < BTC_HA_Open_hour)
    hour_direction_down1 = (BTC_HA_PREV_Close_hour < BTC_HA_PREV_Open_hour)
    hour_direction_down_long_0 = (BTC_HA_Open_hour == BTC_HA_High_hour)
    hour_direction_down_long_1 = (BTC_HA_PREV_Open_hour == BTC_HA_PREV_High_hour)
    hour_direction_down_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_down0 and hour_direction_down1)
    hour_direction_spin0 = (BTC_HA_Open_hour == BTC_HA_Close_hour)
    hour_direction_spin1 = (BTC_HA_PREV_Open_hour == BTC_HA_PREV_Close_hour)

    if BTC_HA_High > BTC_HA_Low:
        direction_down_short0=((BTC_HA_Open - BTC_HA_Close) / (BTC_HA_High - BTC_HA_Low)  >= 6)
    if BTC_HA_PREV_High > BTC_HA_PREV_Low:
        direction_down_short1=((BTC_HA_PREV_Open - BTC_HA_PREV_Close) / (BTC_HA_PREV_High - BTC_HA_PREV_Low) >= 6)
    if BTC_HA_High > BTC_HA_Low:
        direction_up_short0=((BTC_HA_Close - BTC_HA_Open) / (BTC_HA_High - BTC_HA_Low) >= 6)
    if BTC_HA_PREV_High > BTC_HA_PREV_Low:
        direction_up_short1=((BTC_HA_PREV_Close - BTC_HA_PREV_Open) /  (BTC_HA_PREV_High - BTC_HA_PREV_Low) >= 6)


    if BTC_HA_High_hour > BTC_HA_Low_hour:
        hour_direction_down_short0=((BTC_HA_Open_hour - BTC_HA_Close_hour) / (BTC_HA_High_hour - BTC_HA_Low_hour)  >= 6)
    if BTC_HA_PREV_High_hour > BTC_HA_PREV_Low_hour:
        hour_direction_down_short1=((BTC_HA_PREV_Open_hour - BTC_HA_PREV_Close_hour) / (BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) >= 6)
    if BTC_HA_High_hour > BTC_HA_Low_hour:
        hour_direction_up_short0=((BTC_HA_Close_hour - BTC_HA_Open_hour) / (BTC_HA_High_hour - BTC_HA_Low_hour) >= 6)
    if BTC_HA_PREV_High_hour > BTC_HA_PREV_Low_hour:
        hour_direction_up_short1=((BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) /  (BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) >= 6)



    direction_up0=(BTC_HA_Close > BTC_HA_Open)
    direction_up1=(BTC_HA_PREV_Close > BTC_HA_PREV_Open)
    direction_up_long_0=(BTC_HA_Open == BTC_HA_Low)
    direction_up_long_1=(BTC_HA_PREV_Open == BTC_HA_PREV_Low)
    direction_up_longer=(numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_up0 and direction_up1)

    hour_direction_up0 = (BTC_HA_Close_hour > BTC_HA_Open_hour)
    hour_direction_up1 = (BTC_HA_PREV_Close_hour > BTC_HA_PREV_Open_hour)
    hour_direction_up_long_0 = (BTC_HA_Open_hour == BTC_HA_Low_hour)
    hour_direction_up_long_1 = (BTC_HA_PREV_Open_hour == BTC_HA_PREV_Low_hour)
    hour_direction_up_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_up0 and hour_direction_up1)



    if (((hour_direction_down_long_0 and hour_direction_down0) or (hour_direction_down_long_0 and hour_direction_down_long_1 and hour_direction_down0) or (hour_direction_down_long_0 or hour_direction_down_long_1 and hour_direction_down_longer) and hour_direction_down0) or (hour_direction_down0 and hour_direction_down1)):
        btc_trend_hour = "DOWN"
    if (((hour_direction_up_long_0 and hour_direction_up0) or (hour_direction_up_long_0 and hour_direction_up_long_1 and hour_direction_up0) or (hour_direction_up_long_0 or hour_direction_up_long_1 and hour_direction_up_longer) and hour_direction_up0) or (hour_direction_up0 and hour_direction_up1)):
        btc_trend_hour = "UP"
    if (((direction_down_long_0 and direction_down0) or (direction_down_long_0 and direction_down_long_1 and direction_down0) or (direction_down_long_0 or direction_down_long_1 and direction_down_longer) and direction_down0) or (direction_down0 and direction_down1)):
        btc_trend = "DOWN"
    if (((direction_up_long_0 and direction_up0) or (direction_up_long_0 and direction_up_long_1 and direction_up0) or (direction_up_long_0 or direction_up_long_1 and direction_up_longer) and direction_up0) or (direction_up0 and direction_up1)):
        btc_trend = "UP"

    if direction_down_short0:
        btc_trend = "DOWN-0"
    if direction_down_short1:
        btc_trend = "DOWN-0"
    if direction_spin1:
        btc_trend = "DOWN-0"

    if hour_direction_down_short0:
        btc_trend_hour = "DOWN-0"
    if hour_direction_down_short1:
        btc_trend_hour = "DOWN-0"
    if hour_direction_spin1:
        btc_trend_hour = "DOWN-0"

    if direction_up_short0:
        btc_trend = "0-UP"
    if direction_up_short1:
        btc_trend = "0-UP"
    if direction_spin0:
        btc_trend = "0-UP"

    if hour_direction_up_short0:
        btc_trend_hour = "0-UP"
    if hour_direction_up_short1:
        btc_trend_hour = "0-UP"
    if hour_direction_spin0:
        btc_trend_hour = "0-UP"


    if btc_trend == "DOWN" and btc_trend_hour =="DOWN":
        btc_trend = "DANGER"
    if btc_trend == "DOWN-0" and btc_trend_hour =="UP":
        btc_trend ="0-UP"


    print "BTC", btc_trend, btc_trend_hour



    if direction_down0:
        print  "DOWN,", "Latest candle is bearish, HA_Close < HA_Open"
    if direction_down1:
        print "DOWN,", "Previous candle was bearish   HA_PREV_Close < HA_PREV_Open"
    if direction_down_long_0:
        print  "Strong DOWN, latest candle has no upper wick HA_Open == HA_High"
    if direction_down_long_1:
        print "Strong DOWN bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High"
    if direction_down_longer:
        print "Strong DOWN, latest candle body is longer than previous candle body"
    if direction_spin0:
        print "Change direction, spin"
    if direction_spin1:
        print "Change direction in previous candle, spin"
    if direction_down_short0:
        print "Weak DOWN, latest candle body is short - doji"
    if direction_down_short1:
        print "Weak DOWN, previous candle body is short - doji"
    if direction_up_short0:
        print "Weak UP, latest candle body is short - doji"
    if direction_up_short1:
        print "Weak UP, previous candle body is short - doji"
    if direction_up0:
        print  "UP, latest candle bullish  HA_Close > HA_Open"
    if direction_up1:
        print  "UP, previous candle was bullish  HA_PREV_Close > HA_PREV_Open"
    if direction_up_long_0:
        print  "Strong UP, latest candle has no lower wick HA_Open == HA_Low"
    if direction_up_long_1:
        print  "Strong UP, previous candle has no lower wick HA_PREV_Open == HA_PREV_Low"
    if direction_up_longer:
        print "Strong UP, latest candle body is longer than previous candle body"


#    if hour_direction_down0:
#        print  "DOWN,", "Latest candle is bearish, HA_Close < HA_Open"
#    if hour_direction_down1:
#        print "DOWN,", "Previous candle was bearish !  HA_PREV_Close < HA_PREV_Open"
#    if hour_direction_down_long_0:
#        print  "Strong DOWN, latest candle has no upper wick HA_Open == HA_High"
#    if hour_direction_down_long_1:
#        print "Strong DOWN bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High"
#    if hour_direction_down_longer:
#        print "Strong DOWN, latest candle body is longer than previous candle body"
#    if hour_direction_spin0:
#        print "Change direction, spin"
#    if hour_direction_spin1:
#        print "Change direction in previous candle, spin"
#    if hour_direction_down_short0:
#        print "Weak DOWN, latest candle body is short - doji"
#    if hour_direction_down_short1:
#        print "Weak DOWN, previous candle body is short - doji"
#    if hour_direction_up_short0:
#        print "Weak UP, latest candle body is short - doji"
#    if hour_direction_up_short1:
#        print "Weak UP, previous candle body is short - doji"
#    if hour_direction_up0:
#        print  "UP, latest candle bullish  HA_Close > HA_Open"
#    if hour_direction_up1:
#        print  "UP, previous candle was bullish  HA_PREV_Close > HA_PREV_Open"
#    if hour_direction_up_long_0:
#        print  "Strong UP, latest candle has no lower wick HA_Open == HA_Low"
#    if hour_direction_up_long_1:
#        print  "Strong UP, previous candle has no lower wick HA_PREV_Open == HA_PREV_Low"
#    if hour_direction_up_longer:
#        print "Strong UP, latest candle body is longer than previous candle body"


    try:
        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute("update parameters set usdt_btc_price = %s, btc_ha_direction_day =%s where id = %s",
                       (BTC_price, btc_trend, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()



    #if btcprevhigh > btccurrenthigh and btccurrentopen > btccurrentclose:
    #    btc_trend ='DOWN'
    #else:
    #    btc_trend='UP'
    #print btc_trend, btcprevhigh, btccurrenthigh






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
            currenthigh = float(lastcandle[0]['H'])
            previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
            prevlow = float(previouscandle[0]['L'])
            prevopen = float(previouscandle[0]['O'])
            prevclose = float(previouscandle[0]['C'])
            prevhigh = float(previouscandle[0]['H'])

            daylastcandle = get_candles(market, 'day')['result'][-1:]
            daycurrentlow = float(daylastcandle[0]['L'])
            daycurrenthigh = float(daylastcandle[0]['H'])
            daycurrentopen = float(daylastcandle[0]['O'])
            daycurrentclose = float(daylastcandle[0]['C'])
            daypreviouscandle = get_candles(market, 'day')['result'][-2:]
            dayprevlow = float(daypreviouscandle[0]['L'])
            dayprevhigh = float(daypreviouscandle[0]['H'])
            dayprevopen = float(daypreviouscandle[0]['O'])
            dayprevclose = float(daypreviouscandle[0]['C'])




            #if (dayprevclose >= daycurrentopen or daycurrentopen == daycurrenthigh) is True:
            #    print market
            #currenttime = time.ctime()
            timestamp = int(time.time())
            fiboquantity = float(quantity_orders(market))
            fiboquantity2 = float(quantity_orders(market)*2)
            day_close = summary['PrevDay']   #Getting day of closing order
        #Current prices
            last = float(summary['Last'])  #last price
            bid = float(summary['Bid'])    #sell price
            ask = float(summary['Ask'])    #buy price
        #How much market has been changed
            percent_chg = float(((last / day_close) - 1) * 100)
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
            now = datetime.datetime.now()
            currenttime = now.strftime("%Y-%m-%d %H:%M")
            #print market, ai_prediction_price(market), ai_prediction(market)
            #print market, percent_chg
            #print market, min_percent_chg, percent_chg, max_percent_chg, last_orders_quantity, stop_bot


#Heiken Ashi


            ha_time = heikin_ashi(market, 15)
            HA_PREV_Close = heikin_ashi(market, 11)
            HA_PREV_Open = heikin_ashi(market, 12)
            HA_PREV_Low = heikin_ashi(market, 13)
            HA_PREV_High = heikin_ashi(market, 14)

            HA_Close = (currentopen + currenthigh + currentlow + currentclose) / 4
            HA_Open = (HA_PREV_Open + HA_PREV_Close) / 2
            elements = numpy.array([currenthigh, currentlow, HA_Open, HA_Close])
            HA_High = elements.max(0)
            HA_Low = elements.min(0)


            if currtime-ha_time>1800:
                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set ha_close = %s, ha_open =%s, ha_low =%s, ha_high =%s, ha_time =%s  where id = %s",(HA_Close, HA_Open, HA_Low, HA_High, currtime, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()
            else:
                pass




            HA_trend = "NONE"


            ha_direction_down_short0 = False
            ha_direction_down_short1 = False
            ha_direction_up_short0 = False
            ha_direction_up_short1 = False

            ha_direction_down0 = (HA_Close < HA_Open)
            ha_direction_down1 = (HA_PREV_Close < HA_PREV_Open)
            ha_direction_down_long_0 = (HA_Open == HA_High)
            ha_direction_down_long_1 = (HA_PREV_Open == HA_PREV_High)
            ha_direction_down_longer = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_down0 and ha_direction_down1)
            ha_direction_spin0 = (HA_Open == HA_Close)
            ha_direction_spin1 = (HA_PREV_Open == HA_PREV_Close)



            if HA_High > HA_Low:
                ha_direction_down_short0 = ((HA_Open - HA_Close) / (HA_High - HA_Low) >= 6)
            if HA_PREV_High > HA_PREV_Low:
                ha_direction_down_short1 = ((HA_PREV_Open - HA_PREV_Close) / (HA_PREV_High - HA_PREV_Low) >= 6)
            if HA_High > HA_Low:
                ha_direction_up_short0 = ((HA_Close - HA_Open) / (HA_High - HA_Low) >= 6)
            if HA_PREV_High > HA_PREV_Low:
                ha_direction_up_short1 = ((HA_PREV_Close - HA_PREV_Open) / (HA_PREV_High - HA_PREV_Low) >= 6)

            ha_direction_up0 = (HA_Close > HA_Open)
            ha_direction_up1 = (HA_PREV_Close > HA_PREV_Open)
            ha_direction_up_long_0 = (HA_Open == HA_Low)
            ha_direction_up_long_1 = (HA_PREV_Open == HA_PREV_Low)
            ha_direction_up_longer = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_up0 and ha_direction_up1)




            if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1)):
                HA_trend = "DOWN"

            if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1)):
                HA_trend = "UP"

            if ha_direction_down_short0:
                HA_trend = "DOWN-0"
            if ha_direction_down_short1:
                HA_trend = "DOWN-0"
            if ha_direction_spin1:
                HA_trend = "DOWN-0"


            if ha_direction_up_short0:
                HA_trend = "0-UP"
            if ha_direction_up_short1:
                HA_trend = "0-UP"
            if ha_direction_spin0:
                HA_trend = "0-UP"


            if ha_direction_down1 and ha_direction_up0:
                HA_trend = "0-UP"

            if  ha_direction_up1 and ha_direction_down0:
                HA_trend = "DOWN-0"


            print market, HA_trend

            if ha_direction_down0:
                print  market, "DOWN,", "Latest candle is bearish, HA_Close < HA_Open"
            if ha_direction_down1:
                print market, "DOWN,", "Previous candle was bearish   HA_PREV_Close < HA_PREV_Open"
            if ha_direction_down_long_0:
                print  market, "Strong DOWN, latest candle has no upper wick HA_Open == HA_High"
            if ha_direction_down_long_1:
                print market, "Strong DOWN bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High"
            if ha_direction_down_longer:
                print market,  "Strong DOWN, latest candle body is longer than previous candle body"
            if ha_direction_spin0:
                print market, "Change direction, spin"
            if ha_direction_spin1:
                print market, "Change direction in previous candle, spin"
            if ha_direction_down_short0:
                print market, "Weak DOWN, latest candle body is short - doji"
            if ha_direction_down_short1:
                print market, "Weak DOWN, previous candle body is short - doji"
            if ha_direction_up_short0:
                print market, "Weak UP, latest candle body is short - doji"
            if ha_direction_up_short1:
                print market, "Weak UP, previous candle body is short - doji"
            if ha_direction_up0:
                print  market, "UP, latest candle bullish  HA_Close > HA_Open"
            if ha_direction_up1:
                print  market, "UP, previous candle was bullish  HA_PREV_Close > HA_PREV_Open"
            if ha_direction_up_long_0:
                print  market, "Strong UP, latest candle has no lower wick HA_Open == HA_Low"
            if ha_direction_up_long_1:
                print  market, "Strong UP, previous candle has no lower wick HA_PREV_Open == HA_PREV_Low"
            if ha_direction_up_longer:
                print market, "Strong UP, latest candle body is longer than previous candle body"



                ########
            #price_for_sql = c.get_ticker(market).json()['result']['Last']
            # print market, price_for_sql
            try:
                db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                cursor = db.cursor()
                #cursor.execute("update parameters set usdt_btc_price = %s, btc_ha_direction_day =%s where id = %s", (BTC_price, btc_trend, 1))
                prev_serf = previous_serf(market)
                serf = (last * bought_quantity_sql - bought_price_sql * bought_quantity_sql+prev_serf)
                cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
                cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf*BTC_price, market))
                cursor.execute("update markets set current_price = %s, ha_direction =%s  where market = %s and active =1",(last, HA_trend, market))
                db.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            finally:
                db.close()
                ########
            #print market,  (bought_price_sql * bought_quantity_sql + prev_serf), bought_price_sql, bought_quantity_sql, prev_serf

            #print btc_trend
#####---------------------################################


# Bot works in FIBONACI mode. It means that sell orders will be opened by 0.0005 BTC and reopened again and again till he gain his profit
#######BUYING ALGORITHM##########################BUYING ALGORITHM#####################
###################################################################################################

#FIRST ITERATION - BUY

             # If the price for some currency rapidly increased from 0.8% till 3.5%  let`s buy something too
            if (min_percent_chg < percent_chg < max_percent_chg)  and (stop_bot == 0): #and ((dayprevclose>=daycurrentopen or daycurrentopen==daycurrenthigh) is not True) and (currenthigh>currentopen or currentopen<currentclose):  # 0.8 - 3.5  #and ai_prediction(market)=='UP'
                 balance_res = get_balance_from_market(market)
                 current_balance = balance_res['result']['Available']
             #If we have opened order on bitrex
                 if has_open_order(market, 'LIMIT_BUY'):
                     #print('Order already opened to buy  ' + market)
                     try:
                         printed = ('    1 - Order already opened to buy  ' + market)
                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                         cursor = db.cursor()
                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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
                         printed = ('    4- Purchasing (by market analize) ' + str(
                             format_float(percent_chg)) + ' percent changed ' + '  |  ' + str(
                             format_float(buy_quantity2))  + ' units of ' + market + ' for ' + str(
                             format_float(bid)) + ' HA ' + HA_trend)
                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                         cursor = db.cursor()
                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                         cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity2, bid, "1", currenttime, timestamp, "1", btc_trend ,'MA:  % chng ' + str(format_float(percent_chg)) + '  AI   ' + str(ai_prediction(market)) + '  BTC ' + btc_trend, HA_trend ))   #+ '  AI   ' + str(ai_prediction(market))
                         cursor.execute("update orders set serf = %s where market = %s and active =1",(serf, market))
                         db.commit()
                     except MySQLdb.Error, e:
                         print "Error %d: %s" % (e.args[0], e.args[1])
                         sys.exit(1)
                     finally:
                         db.close()
                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase",printed, "localhost")
                         #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                         # print c.buy_limit(market, fiboquantity*2, last).json()
                         #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!##################################
                         # If we have twice more BIG buy orders then BIG sell Orders, and volume of BUY order is twice bigger then volume of sell orders, it means that price is growing, Let` buy somethin
            elif (buytotalsumm > selltotalsumm * order_multiplier) and (buycountresult > sellcountresult * order_multiplier and buytotalsumm != 0 and selltotalsumm != 0 and buycountresult != 0 and sellcountresult != 0) and (stop_bot ==0):# and ((dayprevclose >= daycurrentopen or daycurrentopen == daycurrenthigh) is not True) and (currenthigh>currentopen or currentopen<currentclose):  # should be *2 on both  ##and ai_prediction(market)=='UP'
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
                         printed = ('    8 - Purchasing (by order analize) ' + ' Total Summ ' + str(
                             format_float(buycountpercent)) + ' Total Count ' + str(
                             format_float(buy_quantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                             format_float(bid))+ ' HA ' + HA_trend)
                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                         cursor = db.cursor()
                         cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                         cursor.execute(
                             'insert into orders(market, quantity, price, active, date, timestamp, iteration, btc_direction, params, heikin_ashi) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                             market, buy_quantity2, bid, "1", currenttime, timestamp, "1", btc_trend,
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
                         # print c.buy_limit(market, buy_quantity2, last).json()
                         #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

            else:
                 pass

#######SELLINLGORITHM##########################SELLING ALGORITHM#####################
#############################################################################
# Check if weve this currency for sell

#FIRST ITERATION - SELL: CHECK GREEN CANDLES AND TAKE PROFIT
            if bought_price_sql != None or bought_price != None:  # added OR
                 balance_res = get_balance_from_market(market)
                 current_balance = balance_res['result']['Available']


                 if bought_quantity_sql is None or bought_quantity_sql == 0.0:  # Need to add bought_quantity without sql
                     # print market, bought_quantity_sql, current_balance
                     pass
                     # If curent balance of this currency more then zero
                 elif bought_quantity_sql > 0 and iteration == 1:  # Need to add bought_quantity without sql
                     ##Check if we have completelly green candle
                     if (currentopen == currentlow and prevclose <= currentopen) or currentopen == currenthigh:

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

                     elif currentopen == prevclose and last > bought_price_sql * (1+profit):  ## Need to add bought_price without sql
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

                         if last >= bought_price_sql * (1+profit) and (serf*BTC_price > 0):  ## Need to add bought_price without sql
                             #if we have already opened order to sell
                             if has_open_order(market, 'LIMIT_SELL'):
                                 #print('Order already opened to sell  ' + market)
                                 try:
                                     printed = ('    11 - Order already opened to sell  ' + market)
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
                                     printed = ('    12 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and getting  +' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' + ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (
                                     currenttime, printed))
                                     #cursor.execute('update orders set active = 0, reason_close = "12 Take profit" where market =("%s")' % market)
                                     cursor.execute(
                                         'update orders set reason_close =%s where active=1 and market =%s', (
                                         "12 TP, price:    " + str(
                                             format_float(last)) + "    time:   " + str(currenttime), market))
                                     cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()
                                 Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     #                      print c.sell_limit(market, sell_quantity, last).json()
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################

#

##
#AI TAKE PROFIT FOR FIRST ITERATION
##

                         elif (last >= ai_prediction_price(market) and (serf * BTC_price > 0) and (last >= bought_price_sql * (1+profit))  and market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCC' and ai_prediction(market) != 'NEUTRAL' and ai_prediction(market) == 'DOWN'):  # # Need to add bought_price without sql and sell_quantity without sql

                             if has_open_order(market, 'LIMIT_SELL'):
                                 # print('Order already opened to sell  ' + market)
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

                                 # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                 try:
                                     printed = ('    14 -Selling ' + str(
                                         format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                         format_float(ask)) + '  and getting  ' + str(
                                         format_float(serf * BTC_price)) + ' USD')
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                     # cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                                     cursor.execute(
                                         'update orders set reason_close =%s where active=1 and market =%s', (
                                         "14 AI TP, price:  " + str(format_float(last)) + "  time:   " + str(
                                             currenttime), market))
                                     cursor.execute(
                                         'update orders set active = 0 where market =("%s")' % market)
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()
                                 Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")

                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     #   print c.sell_limit(market, sell_quantity, last).json()
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


#
#
# AI STOP LOSS FIRST ITERATION

                         elif (last >= ai_prediction_price(market) and (last * bought_quantity_sql*1.5 < (bought_price_sql * bought_quantity_sql * (1+profit))) and (serf * BTC_price < 0)  and market != 'BTC-OMG' and market != 'BTC-LSK' and market != 'BTC-BCC' and ai_prediction(market) != 'NEUTRAL' and ai_prediction(market) == 'DOWN'):
                             if has_open_order(market, 'LIMIT_SELL'):
                                 # print('Order already opened to sell  ' + market)
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

                                 # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                                 try:
                                     printed = ('    16 -Selling ' + str(
                                         format_float(
                                             sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                         format_float(ask)) + '  and losing  ' + str(
                                         format_float(serf * BTC_price)) + ' USD')
                                     db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                     cursor = db.cursor()
                                     cursor.execute(
                                         'insert into logs(date, log_entry) values("%s", "%s")' % (
                                         currenttime, printed))
                                     # cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                                     cursor.execute(
                                         'update orders set reason_close =%s where active=1 and market =%s',
                                         ("16 AI Stop loss, price:   " + str(
                                             format_float(last)) + " time:    " + str(currenttime), market))
                                     cursor.execute(
                                         'update orders set active = 0 where market =("%s")' % market)
                                     db.commit()
                                 except MySQLdb.Error, e:
                                     print "Error %d: %s" % (e.args[0], e.args[1])
                                     sys.exit(1)
                                 finally:
                                     db.close()
                                 Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed,"localhost")
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                     #   print c.sell_limit(market, sell_quantity, last).json()
                                     #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


                         else:
                             pass





#


#DOING SECOND AND THIRD BUY

            if serf < 0 and (timestamp-timestamp_old > 6000) and active == 1 and  iteration < maxiteration  and (last < bought_price_sql and last * bought_quantity_sql*1.02 < (bought_price_sql * bought_quantity_sql + prev_serf)):# and ((dayprevclose >= daycurrentopen or daycurrentopen == daycurrenthigh) is not True) and (currenthigh>currentopen or currentopen<currentclose):  #should be 600000 , check if we have active order with minus profit and older then 1 week   :   and last*1.1 < bought_price_sql
                 #print market, "Has old order"
                 run_prediction = "python2.7 run_predict.py " + market
                 p = subprocess.Popen(run_prediction, stdout=subprocess.PIPE, shell=True)
                 (output, err) = p.communicate()
                 p_status = p.wait()
                 #print "Command output: " + output

                 if (min_percent_chg < percent_chg < max_percent_chg) and (ai_prediction(market)=='UP' or ai_prediction(market)=='NEUTRAL') and (currenthigh>currentopen or currentopen<currentclose):
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
                         #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)))
                         try:
                             printed = ('    17 - Purchasing (by market analize) ' + str(format_float(percent_chg)) + ' percent changed ' + '  |  ' +  str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  AI   ' + str(ai_prediction(market)) + ' BTC ' + btc_trend + ' USD serf ' + str(serf*BTC_price)  + ' Iteration ' + str(iteration) + ' HA ' + HA_trend)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             current_serf = previous_serf(market)
                             prev_serf = ((last * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                             cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                             cursor.execute("update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s, btc_direction_1 = %s, heikin_ashi_1 = %s where market = %s and active = 1", (fiboquantity+fiboquantity2, last, timestamp, newiteration, btc_trend, HA_trend, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")

                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                             # print c.buy_limit(market, fiboquantity2, last).json()
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################

                 elif buytotalsumm > selltotalsumm*order_multiplier and buycountresult > sellcountresult*order_multiplier and buytotalsumm !=0 and selltotalsumm !=0 and buycountresult !=0 and sellcountresult !=0 and (ai_prediction(market)=='UP' or ai_prediction(market)=='NEUTRAL') and (currenthigh>currentopen or currentopen<currentclose):  #
                     #print "Buying by order analize"

                     if has_open_order(market, 'LIMIT_BUY'):
                         #print('Order already opened to buy  ' + market)
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
                         #print('Purchasing ' + str(format_float(fiboquantity2)) + ' units of ' + market + ' for ' + str(format_float(last)))
                         try:
                             printed = ('    19 - Purchasing (by market analize) ' + str(
                                 format_float(percent_chg)) + ' percent changed ' + str(
                                 format_float(fiboquantity2)) + '  |  ' + ' units of ' + market + ' for ' + str(
                                 format_float(last)) + ' USD serf ' + str(serf*BTC_price) + ' Iteration ' + str(iteration)+ ' HA ' + HA_trend)
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             current_serf = previous_serf(market)
                             prev_serf = ((last * bought_quantity_sql - bought_price_sql * bought_quantity_sql) + current_serf)
                             cursor.execute("update orders set prev_serf = %s where market = %s and active = 1", (prev_serf, market ))
                             cursor.execute(
                                 "update orders set quantity = %s, price = %s, timestamp = %s, iteration = %s, btc_direction_1 =%s, heikin_ashi_1 =%s where market = %s and active = 1",
                                 (fiboquantity + fiboquantity2, last, timestamp, newiteration, btc_trend, HA_trend, market))
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                             # print c.buy_limit(market, fiboquantity2, last).json()
                             #########!!!!!!!!! BUYING MECHANIZM, DANGER !!!!###################################
                 else:
                     pass
#

# SECOND AND THIRD ITERATION -SELL: TAKE PROFITS

            elif (serf > 0) and ((last * bought_quantity_sql) >= (bought_price_sql * bought_quantity_sql + prev_serf)*(1+profit*1.7)) and (active == 1) and (iteration != 1):
                 if (currentopen == currentlow and prevclose <= currentopen) or (currentopen == currenthigh):
                     # print ("We have GREEN candle for " + market + " and it is better to wait, before sell")
                     try:
                         printed = (
                             "   20 - We have GREEN candle for " + market + " and let`s wait it to be up ")
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

                 elif (currentopen == prevclose):  ## Need to add bought_price without sql
                     # print (" We have good trend for " + market)
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
                             # print('Order already opened to sell  ' + market)
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
                                 printed = ('    23 - Selling ' + str(
                                     format_float(bought_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                     format_float(ask)) + '  and getting  +' + str(
                                     format_float(
                                         ask * fiboquantity - bought_price_sql * fiboquantity)) + ' BTC' + ' or ' + str(
                                     format_float(
                                         serf * BTC_price)) + ' USD')
                                 db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                                 cursor = db.cursor()
                                 cursor.execute(
                                     'insert into logs(date, log_entry) values("%s", "%s")' % (
                                     currenttime, printed))
                                 #cursor.execute('update orders set active = 0, reason_close = "23 Take profit " where market =("%s")' % market)
                                 cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("23 TP, p:    " + str(format_float(last)) + "    t:   " + str(currenttime), market))
                                 cursor.execute('update orders set active = 0 where market =("%s")' % market)
                                 db.commit()
                             except MySQLdb.Error, e:
                                 print "Error %d: %s" % (e.args[0], e.args[1])
                                 sys.exit(1)
                             finally:
                                 db.close()
                             Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                                 #                      print c.sell_limit(market, fiboquantity, last).json()
                                 #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                 #else:
                  #   pass








#DOING THIRD SELLs


#AI take profit for last order

            elif (last >= ai_prediction_price(market) and (serf*BTC_price >= 0) and iteration == maxiteration and (active == 1) and market!='BTC-OMG' and market!='BTC-LSK' and market!='BTC-BCC' and ai_prediction(market)!='NEUTRAL' and ai_prediction(market)=='DOWN'):  # # Need to add bought_price without sql and sell_quantity without sql

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
                             printed = ('    25 -Selling ' + str(
                                 format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                 format_float(ask)) + '  and getting  ' + str(
                                 format_float(serf*BTC_price)) + ' USD')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             #cursor.execute('update orders set reason_close = "225 AI take profit" where active=1 and market =("%s")' % market)
                             cursor.execute('update orders set reason_close =%s where active=1 and market =%s',("25 AI TP, p:   " + str(format_float(last))+"   t:    "+str(currenttime), market))
                             cursor.execute(
                                 'update orders set active = 0 where market =("%s")' % market)
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                             #   print c.sell_limit(market, sell_quantity, last).json()
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################




#STOP LOSS FOR last iteration

            elif (last < bought_price_sql) and (last * bought_quantity_sql*(1+profit-0.01)) < (bought_price_sql * bought_quantity_sql + prev_serf) and (iteration == maxiteration) and (active == 1):  # # Need to add bought_price without sql and sell_quantity without sql

                     if has_open_order(market, 'LIMIT_SELL'):
                         #print('Order already opened to sell  ' + market)
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

                         #print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                         try:
                             printed = ('    27 -Selling ' + str(
                                 format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                                 format_float(ask)) + '  and losing  ' + str(
                                 format_float(serf*BTC_price)) + ' USD')
                             db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                             cursor = db.cursor()
                             cursor.execute(
                                 'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                             #cursor.execute('update orders set reason_close = "27 Stop loss" where active=1 and market =("%s")' % market)
                             cursor.execute('update orders set reason_close =%s where active=1 and market =%s', (
                             "27 Stop loss, price:    " + str(format_float(last)) + "    time:   " + str(
                                 currenttime), market))
                             cursor.execute(
                                 'update orders set active = 0 where market =("%s")' % market)
                             db.commit()
                         except MySQLdb.Error, e:
                             print "Error %d: %s" % (e.args[0], e.args[1])
                             sys.exit(1)
                         finally:
                             db.close()
                         Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                             #   print c.sell_limit(market, sell_quantity, last).json()
                             #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


#AI STOP LOSS

            elif (last >= ai_prediction_price(market) and (active == 1)  and (last * bought_quantity_sql*(1+profit-0.02) < (bought_price_sql * bought_quantity_sql + prev_serf)*(1+profit)) and (serf*BTC_price < 0) and iteration == maxiteration and market!='BTC-OMG' and market!='BTC-LSK' and market!='BTC-BCC' and ai_prediction(market)!='NEUTRAL' and ai_prediction(market)=='DOWN'):
                 if has_open_order(market, 'LIMIT_SELL'):
                     # print('Order already opened to sell  ' + market)
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

                     # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                     try:
                         printed = ('    29 -Selling ' + str(
                             format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                             format_float(ask)) + '  and losing  ' + str(
                             format_float(serf * BTC_price)) + ' USD')
                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                         cursor = db.cursor()
                         cursor.execute(
                             'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                         #cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                         cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("29 AI Stop loss, price:    "+str(format_float(last))+"    time:   "+str(currenttime), market))
                         cursor.execute(
                             'update orders set active = 0 where market =("%s")' % market)
                         db.commit()
                     except MySQLdb.Error, e:
                         print "Error %d: %s" % (e.args[0], e.args[1])
                         sys.exit(1)
                     finally:
                         db.close()
                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                         #   print c.sell_limit(market, sell_quantity, last).json()
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################



#Candle Take profit
            elif ((currentlow == currentclose)  and (last * bought_quantity_sql > (bought_price_sql * bought_quantity_sql + prev_serf)*(1+profit-0.01)) and (serf*BTC_price > 0) and iteration == maxiteration) and (active == 1):
                 if has_open_order(market, 'LIMIT_SELL'):
                     # print('Order already opened to sell  ' + market)
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

                     # print ('22 - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(ask)) + '  and losing  ' + str(format_float(ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql)) + ' BTC' ' or ' + str(format_float((ask * bought_quantity_sql - bought_price_sql * bought_quantity_sql) * BTC_price)) + ' USD')
                     try:
                         printed = ('    31 -Selling ' + str(
                             format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(
                             format_float(ask)) + '  and getting  ' + str(
                             format_float(serf * BTC_price)) + ' USD')
                         db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                         cursor = db.cursor()
                         cursor.execute(
                             'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                         #cursor.execute('update orders set reason_close = "22 AI Stop loss" where active=1 and market =("%s")' % market)
                         cursor.execute('update orders set reason_close =%s where active=1 and market =%s', ("31 Candle TP, p:    "+str(format_float(last))+"    t:   "+str(currenttime), market))
                         cursor.execute('update orders set active = 0 where market =("%s")' % market)
                         db.commit()
                     except MySQLdb.Error, e:
                         print "Error %d: %s" % (e.args[0], e.args[1])
                         sys.exit(1)
                     finally:
                         db.close()
                     Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################
                         #   print c.sell_limit(market, sell_quantity, last).json()
                         #########!!!!!!!!! SELLING MECHANIZM, DANGER !!!!###################################


            else:
                 pass




        else:
            pass


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




def parameters():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23])

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


def last_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
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
