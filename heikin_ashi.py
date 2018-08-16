import time
import config
from pybittrex.client import Client
import MySQLdb
import sys
import requests
import hashlib
import hmac
import numpy
import datetime

c = Client(api_key=config.key, api_secret=config.secret)

currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
#print currtime


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


def main():
    print('Starting heikin ashi module')

    HA()



def HA():
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
    btcprevcandle2 = get_candles('USDT-BTC', 'day')['result'][-3:]
    btcprevlow2 = float(btcprevcandle2[0]['L'])
    btcprevopen2 = float(btcprevcandle2[0]['O'])
    btcprevclose2 = float(btcprevcandle2[0]['C'])
    btcprevhigh2 = float(btcprevcandle2[0]['H'])
    btcprevcandle3 = get_candles('USDT-BTC', 'day')['result'][-4:]
    btcprevlow3 = float(btcprevcandle3[0]['L'])
    btcprevopen3 = float(btcprevcandle3[0]['O'])
    btcprevclose3 = float(btcprevcandle3[0]['C'])
    btcprevhigh3 = float(btcprevcandle3[0]['H'])





    #print  btccurrentlow

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
    btcprevcandlehour2 = get_candles('USDT-BTC', 'hour')['result'][-3:]
    btcprevlowhour2 = float(btcprevcandlehour2[0]['L'])
    btcprevopenhour2 = float(btcprevcandlehour2[0]['O'])
    btcprevclosehour2 = float(btcprevcandlehour2[0]['C'])
    btcprevhighhour2 = float(btcprevcandlehour2[0]['H'])





    BTC_HA_PREV_Close3 = (btcprevopen3 + btcprevhigh3 + btcprevlow3 + btcprevclose3) / 4
    BTC_HA_PREV_Open3 = (btcprevopen3 + btcprevclose3) / 2
    BTC_HA_PREV_Low3 = btcprevlow3
    BTC_HA_PREV_High3 = btcprevhigh3

    BTC_HA_PREV_Close2 = (btcprevopen2 + btcprevhigh2 + btcprevlow2 + btcprevclose2) / 4
    BTC_HA_PREV_Open2 = (BTC_HA_PREV_Open3 + BTC_HA_PREV_Close3) / 2
    elements2 = numpy.array([btcprevhigh2, btcprevlow2, BTC_HA_PREV_Open2, BTC_HA_PREV_Close2])
    BTC_HA_PREV_Low2 = elements2.min(0)
    BTC_HA_PREV_High2 = elements2.max(0)


    BTC_HA_PREV_Close = (btcprevopen + btcprevhigh + btcprevlow + btcprevclose) / 4
    BTC_HA_PREV_Open = (BTC_HA_PREV_Open2 + BTC_HA_PREV_Close2) / 2
    elements0 = numpy.array([btcprevhigh, btcprevlow, BTC_HA_PREV_Open, BTC_HA_PREV_Close])
    BTC_HA_PREV_Low = elements0.min(0)
    BTC_HA_PREV_High = elements0.max(0)

    BTC_HA_Close = (btccurrentopen + btccurrenthigh + btccurrentlow + btccurrentclose) / 4
    BTC_HA_Open = (BTC_HA_PREV_Open + BTC_HA_PREV_Close) / 2
    elements1 = numpy.array([btccurrenthigh, btccurrentlow, BTC_HA_Open, BTC_HA_Close])
    BTC_HA_Low = elements1.min(0)
    BTC_HA_High = elements1.max(0)

    try:
        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute(
            "update parameters set btc_ha_close_day = %s, btc_ha_open_day =%s, btc_ha_low_day =%s, btc_ha_high_day =%s, btc_ha_time_day =%s  where id = %s",
            (BTC_HA_Close, BTC_HA_Open, BTC_HA_Low, BTC_HA_High, currtime, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()

    BTC_HA_PREV_Close_hour2 = (btcprevopenhour2 + btcprevhighhour2 + btcprevlowhour2 + btcprevclosehour2) / 4
    BTC_HA_PREV_Open_hour2 = (btcprevopenhour2 + btcprevclosehour2) / 2
    BTC_HA_PREV_Low_hour2 = btcprevlowhour2
    BTC_HA_PREV_High_hour2 = btcprevhighhour2

    BTC_HA_PREV_Close_hour = (btcprevopenhour + btcprevhighhour + btcprevlowhour + btcprevclosehour) / 4
    BTC_HA_PREV_Open_hour = (BTC_HA_PREV_Open_hour2 + BTC_HA_PREV_Close_hour2) / 2
    elements3 = numpy.array([btccurrenthighhour, btccurrentlowhour, BTC_HA_PREV_Open_hour, BTC_HA_PREV_Close_hour])
    BTC_HA_PREV_High_hour = elements3.max(0)
    BTC_HA_PREV_Low_hour = elements3.min(0)

    BTC_HA_Close_hour = (btccurrentopenhour + btccurrenthighhour + btccurrentlowhour + btccurrentclosehour) / 4
    BTC_HA_Open_hour = (BTC_HA_PREV_Open_hour + BTC_HA_PREV_Close_hour) / 2
    elements2 = numpy.array([btccurrenthighhour, btccurrentlowhour, BTC_HA_Open_hour, BTC_HA_Close_hour])
    BTC_HA_High_hour = elements2.max(0)
    BTC_HA_Low_hour = elements2.min(0)

    try:
        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute(
            "update parameters set btc_ha_close_hour = %s, btc_ha_open_hour =%s, btc_ha_low_hour =%s, btc_ha_high_hour =%s, btc_ha_time_hour =%s  where id = %s",
            (BTC_HA_Close_hour, BTC_HA_Open_hour, BTC_HA_Low_hour, BTC_HA_High_hour, currtime, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()

    btc_trend = "NONE"
    btc_trend_hour = "NONE"



    direction_down0 = (BTC_HA_Close < BTC_HA_Open)
    direction_down1 = (BTC_HA_PREV_Close < BTC_HA_PREV_Open)
    direction_down2 = (BTC_HA_PREV_Close2 < BTC_HA_PREV_Open2)
    direction_down_long_0 = (BTC_HA_Open == BTC_HA_High and BTC_HA_Close < BTC_HA_Open)
    direction_down_long_1 = (BTC_HA_PREV_Open == BTC_HA_PREV_High and BTC_HA_PREV_Close < BTC_HA_PREV_Open)
    direction_down_longer = (numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(
        BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_down0 and direction_down1)
    direction_spin0 = (BTC_HA_Open == BTC_HA_Close)
    direction_spin1 = (BTC_HA_PREV_Open == BTC_HA_PREV_Close)

    hour_direction_down0 = (BTC_HA_Close_hour < BTC_HA_Open_hour)
    hour_direction_down1 = (BTC_HA_PREV_Close_hour < BTC_HA_PREV_Open_hour)
    hour_direction_down_long_0 = (BTC_HA_Open_hour == BTC_HA_High_hour and BTC_HA_Close_hour < BTC_HA_Open_hour)
    hour_direction_down_long_1 = (
    BTC_HA_PREV_Open_hour == BTC_HA_PREV_High_hour and BTC_HA_PREV_Close_hour < BTC_HA_PREV_Open_hour)
    hour_direction_down_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(
        BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_down0 and hour_direction_down1)
    hour_direction_spin0 = (BTC_HA_Open_hour == BTC_HA_Close_hour)
    hour_direction_spin1 = (BTC_HA_PREV_Open_hour == BTC_HA_PREV_Close_hour)

    direction_down_short0 = ((BTC_HA_High - BTC_HA_Low) / (BTC_HA_Open - BTC_HA_Close) >= 6) and (
    BTC_HA_Open - BTC_HA_Close != 0)
    direction_down_short1 = ((BTC_HA_PREV_High - BTC_HA_PREV_Low) / (BTC_HA_PREV_Open - BTC_HA_PREV_Close) >= 6) and (
    BTC_HA_PREV_Open - BTC_HA_PREV_Close != 0)
    direction_up_short0 = ((BTC_HA_High - BTC_HA_Low) / (BTC_HA_Close - BTC_HA_Open) >= 6) and (
    BTC_HA_Close - BTC_HA_Open != 0)
    direction_up_short1 = ((BTC_HA_PREV_High - BTC_HA_PREV_Low) / (BTC_HA_PREV_Close - BTC_HA_PREV_Open) >= 6) and (
    BTC_HA_PREV_Close - BTC_HA_PREV_Open != 0)

    hour_direction_down_short0 = ((BTC_HA_High_hour - BTC_HA_Low_hour) / (
    BTC_HA_Open_hour - BTC_HA_Close_hour) >= 6) and (BTC_HA_Open_hour - BTC_HA_Close_hour != 0)
    hour_direction_down_short1 = ((BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) / (
    BTC_HA_PREV_Open_hour - BTC_HA_PREV_Close_hour) >= 6) and (BTC_HA_PREV_Open_hour - BTC_HA_PREV_Close_hour != 0)
    hour_direction_up_short0 = (
                               (BTC_HA_High_hour - BTC_HA_Low_hour) / (BTC_HA_Close_hour - BTC_HA_Open_hour) >= 6) and (
                               BTC_HA_Close_hour - BTC_HA_Open_hour != 0)
    hour_direction_up_short1 = ((BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) / (
    BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) >= 6) and (BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour != 0)

    direction_up0 = (BTC_HA_Close > BTC_HA_Open)
    direction_up1 = (BTC_HA_PREV_Close > BTC_HA_PREV_Open)
    direction_up2 = (BTC_HA_PREV_Close2 > BTC_HA_PREV_Open2)
    direction_up_long_0 = (BTC_HA_Open == BTC_HA_Low and BTC_HA_Close_hour > BTC_HA_Open_hour)
    direction_up_long_1 = (BTC_HA_PREV_Open == BTC_HA_PREV_Low and BTC_HA_PREV_Close > BTC_HA_PREV_Open)
    direction_up_longer = (numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(
        BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_up0 and direction_up1)

    hour_direction_up0 = (BTC_HA_Close_hour > BTC_HA_Open_hour)
    hour_direction_up1 = (BTC_HA_PREV_Close_hour > BTC_HA_PREV_Open_hour)
    hour_direction_up_long_0 = (BTC_HA_Open_hour == BTC_HA_Low_hour and BTC_HA_Close_hour > BTC_HA_Open_hour)
    hour_direction_up_long_1 = (
    BTC_HA_PREV_Open_hour == BTC_HA_PREV_Low_hour and BTC_HA_PREV_Close_hour > BTC_HA_PREV_Open_hour)
    hour_direction_up_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(
        BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_up0 and hour_direction_up1)

    # Hourly HA

    if (((hour_direction_down_long_0 and hour_direction_down0) or (
            hour_direction_down_long_0 and hour_direction_down_long_1 and hour_direction_down0) or (
        hour_direction_down_long_0 or hour_direction_down_long_1 and hour_direction_down_longer) and hour_direction_down0) or (
        hour_direction_down0 and hour_direction_down1)):
        btc_trend_hour = "DOWN"
    elif (((hour_direction_up_long_0 and hour_direction_up0) or (
            hour_direction_up_long_0 and hour_direction_up_long_1 and hour_direction_up0) or (
        hour_direction_up_long_0 or hour_direction_up_long_1 and hour_direction_up_longer) and hour_direction_up0) or (
        hour_direction_up0 and hour_direction_up1)):
        btc_trend_hour = "UP"
    else:
        btc_trend_hour = "STABLE"


        # Daily HA
    if (((direction_down_long_0 and direction_down0) or (
            direction_down_long_0 and direction_down_long_1 and direction_down0) or (
        direction_down_long_0 or direction_down_long_1 and direction_down_longer) and direction_down0) or (
        direction_down0 and direction_down1 and direction_down2)):
        btc_trend = "DOWN"
    elif (((direction_up_long_0 and direction_up0) or (
            direction_up_long_0 and direction_up_long_1 and direction_up0) or (
        direction_up_long_0 or direction_up_long_1 and direction_up_longer) and direction_up0) or (
        direction_up0 and direction_up1 and direction_up2)):
        btc_trend = "UP"
    else:
        btc_trend = "STABLE"

    if btc_trend == "DOWN" and btc_trend_hour == "DOWN":
        btc_trend = "DANGER"





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


    if hour_direction_down0:
        print  "DOWN,", "Latest candle is bearish, HA_Close < HA_Open"
    if hour_direction_down1:
        print "DOWN,", "Previous candle was bearish !  HA_PREV_Close < HA_PREV_Open"
    if hour_direction_down_long_0:
        print  "Strong DOWN, latest candle has no upper wick HA_Open == HA_High"
    if hour_direction_down_long_1:
        print "Strong DOWN bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High"
    if hour_direction_down_longer:
        print "Strong DOWN, latest candle body is longer than previous candle body"
    if hour_direction_spin0:
        print "Change direction, spin"
    if hour_direction_spin1:
        print "Change direction in previous candle, spin"
    if hour_direction_down_short0:
        print "Weak DOWN, latest candle body is short - doji"
    if hour_direction_down_short1:
        print "Weak DOWN, previous candle body is short - doji"
    if hour_direction_up_short0:
        print "Weak UP, latest candle body is short - doji"
    if hour_direction_up_short1:
        print "Weak UP, previous candle body is short - doji"
    if hour_direction_up0:
        print  "UP, latest candle bullish  HA_Close > HA_Open"
    if hour_direction_up1:
        print  "UP, previous candle was bullish  HA_PREV_Close > HA_PREV_Open"
    if hour_direction_up_long_0:
        print  "Strong UP, latest candle has no lower wick HA_Open == HA_Low"
    if hour_direction_up_long_1:
        print  "Strong UP, previous candle has no lower wick HA_PREV_Open == HA_PREV_Low"
    if hour_direction_up_longer:
        print "Strong UP, latest candle body is longer than previous candle body"

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


    if btc_trend=="DOWN" or btc_trend=="DANGER" or btc_trend=="STABLE":
        try:
            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
            cursor = db.cursor()
            cursor.execute("update parameters set ai_ha =%s where id = %s",
                           (1, 1))
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
            cursor.execute("update parameters set ai_ha =%s where id = %s",
                           (0, 1))
            db.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            db.close()






    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price
                ask = float(summary['Ask'])  # buy price
                bought_quantity_sql = float(status_orders(market, 2))
            # Candle analisys
                #lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                #currentlow = float(lastcandle[0]['L'])
                #currentopen = float(lastcandle[0]['O'])
                #currentclose = float(lastcandle[0]['C'])
                #currenthigh = float(lastcandle[0]['H'])
                #previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                #prevlow = float(previouscandle[0]['L'])
                #prevopen = float(previouscandle[0]['O'])
                #prevclose = float(previouscandle[0]['C'])
                #prevhigh = float(previouscandle[0]['H'])

#######################
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
                daypreviouscandle2 = get_candles(market, 'day')['result'][-3:]
                dayprevlow2 = float(daypreviouscandle2[0]['L'])
                dayprevhigh2 = float(daypreviouscandle2[0]['H'])
                dayprevopen2 = float(daypreviouscandle2[0]['O'])
                dayprevclose2 = float(daypreviouscandle2[0]['C'])
#####################

                daymonthcandle1 = get_candles(market, 'day')['result'][-20:]
                daymonthcandle2 = get_candles(market, 'day')['result'][-40:]
                daymonthcandle3 = get_candles(market, 'day')['result'][-60:]
                daymonthcandle4 = get_candles(market, 'day')['result'][-80:]
                daymonthcandle5 = get_candles(market, 'day')['result'][-100:]
                daymonthcandle6 = get_candles(market, 'day')['result'][-120:]
                daymonthcandle7 = get_candles(market, 'day')['result'][-180:]
                daymonthcandle8 = get_candles(market, 'day')['result'][-200:]
                daymonthcandle9 = get_candles(market, 'day')['result'][-220:]
                daymonthcandle10 = get_candles(market, 'day')['result'][-240:]

                daymonthclose1 = float(daymonthcandle1[0]['C'])
                daymonthclose2 = float(daymonthcandle2[0]['C'])
                daymonthclose3 = float(daymonthcandle3[0]['C'])
                daymonthclose4 = float(daymonthcandle4[0]['C'])
                daymonthclose5 = float(daymonthcandle5[0]['C'])
                daymonthclose6 = float(daymonthcandle6[0]['C'])
                daymonthclose7 = float(daymonthcandle7[0]['C'])
                daymonthclose8 = float(daymonthcandle8[0]['C'])
                daymonthclose9 = float(daymonthcandle9[0]['C'])
                daymonthclose10 = float(daymonthcandle10[0]['C'])
####



                hourlastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                hourcurrentlow = float(hourlastcandle[0]['L'])
                hourcurrenthigh = float(hourlastcandle[0]['H'])
                hourcurrentopen = float(hourlastcandle[0]['O'])
                hourcurrentclose = float(hourlastcandle[0]['C'])
                hourpreviouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                hourprevlow = float(hourpreviouscandle[0]['L'])
                hourprevhigh = float(hourpreviouscandle[0]['H'])
                hourprevopen = float(hourpreviouscandle[0]['O'])
                hourprevclose = float(hourpreviouscandle[0]['C'])
                hourpreviouscandle2 = get_candles(market, 'thirtymin')['result'][-3:]
                hourprevlow2 = float(hourpreviouscandle2[0]['L'])
                hourprevhigh2 = float(hourpreviouscandle2[0]['H'])
                hourprevopen2 = float(hourpreviouscandle2[0]['O'])
                hourprevclose2 = float(hourpreviouscandle2[0]['C'])
                hourpreviouscandle3 = get_candles(market, 'thirtymin')['result'][-4:]
                hourprevlow3 = float(hourpreviouscandle3[0]['L'])
                hourprevhigh3 = float(hourpreviouscandle3[0]['H'])
                hourprevopen3 = float(hourpreviouscandle3[0]['O'])
                hourprevclose3 = float(hourpreviouscandle3[0]['C'])
                hourpreviouscandle4 = get_candles(market, 'thirtymin')['result'][-5:]
                hourprevlow4 = float(hourpreviouscandle4[0]['L'])
                hourprevhigh4 = float(hourpreviouscandle4[0]['H'])
                hourprevopen4 = float(hourpreviouscandle4[0]['O'])
                hourprevclose4 = float(hourpreviouscandle4[0]['C'])
                hourpreviouscandle5 = get_candles(market, 'thirtymin')['result'][-6:]
                hourprevlow5 = float(hourpreviouscandle5[0]['L'])
                hourprevhigh5 = float(hourpreviouscandle5[0]['H'])
                hourprevopen5 = float(hourpreviouscandle5[0]['O'])
                hourprevclose5 = float(hourpreviouscandle5[0]['C'])
                hourpreviouscandle6 = get_candles(market, 'thirtymin')['result'][-7:]
                hourprevlow6 = float(hourpreviouscandle6[0]['L'])
                hourprevhigh6 = float(hourpreviouscandle6[0]['H'])
                hourprevopen6 = float(hourpreviouscandle6[0]['O'])
                hourprevclose6 = float(hourpreviouscandle6[0]['C'])

                #print market, hourcurrentlow

                HA_PREV_Close6 = (hourprevopen6 + hourprevhigh6 + hourprevlow6 + hourprevclose6) / 4
                HA_PREV_Open6 = (hourprevopen6 + hourprevclose6) / 2
                HA_PREV_Low6 = hourprevlow6
                HA_PREV_High6 = hourprevhigh6

                HA_PREV_Close5 = (hourprevopen5 + hourprevhigh5 + hourprevlow5 + hourprevclose5) / 4
                HA_PREV_Open5 = (HA_PREV_Open6 + HA_PREV_Close6) / 2
                elements5 = numpy.array([hourprevhigh5, hourprevlow5, HA_PREV_Open6, HA_PREV_Close6])
                HA_PREV_High5 = elements5.max(0)
                HA_PREV_Low5 = elements5.min(0)

                HA_PREV_Close4 = (hourprevopen4 + hourprevhigh4 + hourprevlow4 + hourprevclose4) / 4
                HA_PREV_Open4 = (HA_PREV_Open5 + HA_PREV_Close5) / 2
                elements4 = numpy.array([hourprevhigh4, hourprevlow4, HA_PREV_Open5, HA_PREV_Close5])
                HA_PREV_High4 = elements4.max(0)
                HA_PREV_Low4 = elements4.min(0)


                HA_PREV_Close3 = (hourprevopen3 + hourprevhigh3 + hourprevlow3 + hourprevclose3) / 4
                HA_PREV_Open3 = (HA_PREV_Open4 + HA_PREV_Close4) / 2
                elements3 = numpy.array([hourprevhigh3, hourprevlow3, HA_PREV_Open4, HA_PREV_Close4])
                HA_PREV_High3 = elements3.max(0)
                HA_PREV_Low3 = elements3.min(0)

                HA_PREV_Close2 = (hourprevopen2 + hourprevhigh2 + hourprevlow2 + hourprevclose2) / 4
                HA_PREV_Open2 = (HA_PREV_Open3 + HA_PREV_Close3) / 2
                elements2 = numpy.array([hourprevhigh2, hourprevlow2, HA_PREV_Open3, HA_PREV_Close3])
                HA_PREV_High2 = elements2.max(0)
                HA_PREV_Low2 = elements2.min(0)

                HA_PREV_Close = (hourprevopen + hourprevhigh + hourprevlow + hourprevclose) / 4
                HA_PREV_Open = (HA_PREV_Open2 + HA_PREV_Close2) / 2
                elements1 = numpy.array([hourprevhigh, hourprevlow, HA_PREV_Open, HA_PREV_Close])
                HA_PREV_High = elements1.max(0)
                HA_PREV_Low = elements1.min(0)

                HA_Close = (hourcurrentopen + hourcurrenthigh + hourcurrentlow + hourcurrentclose) / 4
                HA_Open = (HA_PREV_Open + HA_PREV_Close) / 2
                elements0 = numpy.array([hourcurrenthigh, hourcurrentlow, HA_Open, HA_Close])
                HA_High = elements0.max(0)
                HA_Low = elements0.min(0)

###############
                HAD_PREV_Close2 = (dayprevopen2 + dayprevhigh2 + dayprevlow2 + dayprevclose2) / 4
                HAD_PREV_Open2 = (dayprevopen2 + dayprevclose2) / 2
                HAD_PREV_Low2 = dayprevlow2
                HAD_PREV_High2 = dayprevhigh2

                HAD_PREV_Close = (dayprevopen + dayprevhigh + dayprevlow + dayprevclose) / 4
                HAD_PREV_Open = (HAD_PREV_Open2 + HAD_PREV_Close2) / 2
                elements1 = numpy.array([dayprevhigh, dayprevlow, HAD_PREV_Open, HAD_PREV_Close])
                HAD_PREV_High = elements1.max(0)
                HAD_PREV_Low = elements1.min(0)

                HAD_Close = (daycurrentopen + daycurrenthigh + daycurrentlow + daycurrentclose) / 4
                HAD_Open = (HAD_PREV_Open + HAD_PREV_Close) / 2
                elements0 = numpy.array([daycurrenthigh, daycurrentlow, HAD_Open, HAD_Close])
                HAD_High = elements0.max(0)
                HAD_Low = elements0.min(0)
##############




                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set ha_close = %s, ha_open =%s, ha_low =%s, ha_high =%s, ha_time =%s  where market = %s",(HA_Close, HA_Open, HA_Low, HA_High, currenttime, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

                HA_trend = "NONE"

###############
                HAD_trend = "NONE"
###############

                ha_direction_down_short0 =((HA_High - HA_Low) / (HA_Open - HA_Close) >= 2)  and (HA_Open - HA_Close !=0)
                ha_direction_down_short1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Open - HA_PREV_Close) >= 2) and (HA_PREV_Open - HA_PREV_Close !=0)
                ha_direction_down_short2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Open2 - HA_PREV_Close2) >= 2) and (HA_PREV_Open2 - HA_PREV_Close2 !=0)
                ha_direction_down_shorter0 =((HA_High - HA_Low) / (HA_Open - HA_Close) >= 4)  and (HA_Open - HA_Close !=0)
                ha_direction_down_shorter1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Open - HA_PREV_Close) >= 4) and (HA_PREV_Open - HA_PREV_Close !=0)
                ha_direction_down_shorter2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Open2 - HA_PREV_Close2) >= 4) and (HA_PREV_Open2 - HA_PREV_Close2 !=0)
                ha_direction_down0 = (HA_Close < HA_Open)
                ha_direction_down1 = (HA_PREV_Close < HA_PREV_Open)
                ha_direction_down2 = (HA_PREV_Close2 < HA_PREV_Open2)
                ha_direction_down_long_0 = (HA_Open == HA_High and HA_Close < HA_Open)
                ha_direction_down_long_1 = (HA_PREV_Open == HA_PREV_High and HA_PREV_Close < HA_PREV_Open)
                ha_direction_down_long_2 = (HA_PREV_Open2 == HA_PREV_High2 and HA_PREV_Close2 < HA_PREV_Open2)
                ha_direction_down_longer = (numpy.abs(HA_Open - HA_Close) > numpy.abs(HA_PREV_Open - HA_PREV_Close) and ha_direction_down0 and ha_direction_down1)
                ha_direction_down_longermax = (numpy.abs(HA_Open - HA_Close) > numpy.abs(HA_PREV_Open - HA_PREV_Close) and numpy.abs(HA_PREV_Open - HA_PREV_Close) > numpy.abs(HA_PREV_Open2 - HA_PREV_Close2 ) and ha_direction_down0 and ha_direction_down1 and ha_direction_down2)
                ha_direction_down_smaller = (numpy.abs(HA_Open - HA_Close) < numpy.abs(HA_PREV_Open - HA_PREV_Close) and ha_direction_down0 and ha_direction_down1)
                ha_direction_down_smaller1 = (numpy.abs(HA_PREV_Open - HA_PREV_Close) < numpy.abs(HA_PREV_Open2 - HA_PREV_Close2) and ha_direction_down1 and ha_direction_down2)
                ha_direction_down_smallermax = (numpy.abs(HA_Open - HA_Close) < numpy.abs(HA_PREV_Open - HA_PREV_Close) and numpy.abs(HA_PREV_Open - HA_PREV_Close) < numpy.abs(HA_PREV_Open2 - HA_PREV_Close2) and ha_direction_down0 and ha_direction_down1 and ha_direction_down2)

                ha_direction_spin0 = (HA_Open == HA_Close)
                ha_direction_spin1 = (HA_PREV_Open == HA_PREV_Close)
                ha_direction_spin2 = (HA_PREV_Open2 == HA_PREV_Close2)

                ha_direction_up_short0 = ((HA_High - HA_Low) / (HA_Close - HA_Open) >= 2) and (HA_Close - HA_Open !=0)
                ha_direction_up_short1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Close - HA_PREV_Open) >= 2) and (HA_PREV_Close - HA_PREV_Open !=0)
                ha_direction_up_short2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Close2 - HA_PREV_Open2) >= 2) and (HA_PREV_Close2 - HA_PREV_Open2 !=0)
                ha_direction_up_shorter0 = ((HA_High - HA_Low) / (HA_Close - HA_Open) >= 4) and (HA_Close - HA_Open !=0)
                ha_direction_up_shorter1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Close - HA_PREV_Open) >= 4) and (HA_PREV_Close - HA_PREV_Open !=0)
                ha_direction_up_shorter2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Close2 - HA_PREV_Open2) >= 4) and (HA_PREV_Close2 - HA_PREV_Open2 !=0)
                ha_direction_up0 = (HA_Close > HA_Open)
                ha_direction_up1 = (HA_PREV_Close > HA_PREV_Open)
                ha_direction_up2 = (HA_PREV_Close2 > HA_PREV_Open2)
                ha_direction_up_long_0 = (HA_Open == HA_Low and HA_Close > HA_Open)
                ha_direction_up_long_1 = (HA_PREV_Open == HA_PREV_Low and HA_PREV_Close > HA_PREV_Open)
                ha_direction_up_long_2 = (HA_PREV_Open2 == HA_PREV_Low2 and HA_PREV_Close2 > HA_PREV_Open2)
                ha_direction_up_longer = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_up0 and ha_direction_up1)
                ha_direction_up_longermax = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and numpy.abs(HA_PREV_Close - HA_PREV_Open) > numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up0 and ha_direction_up1 and ha_direction_up2)
                ha_direction_up_smaller = (numpy.abs(HA_Close - HA_Open) < numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_up0 and ha_direction_up1)
                ha_direction_up_smaller1 = (numpy.abs(HA_PREV_Close - HA_PREV_Open) < numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up1 and ha_direction_up2)
                ha_direction_up_smallermax = (numpy.abs(HA_Close - HA_Open) < numpy.abs(HA_PREV_Close - HA_PREV_Open) and numpy.abs(HA_PREV_Close - HA_PREV_Open) < numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up0 and ha_direction_up1 and ha_direction_up2)


#############
                had_direction_down_short0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 2)  and (HAD_Open - HAD_Close !=0)
                had_direction_down_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 2) and (HAD_PREV_Open - HAD_PREV_Close !=0)
                had_direction_down_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 2) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
                had_direction_down_shorter0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 4)  and (HAD_Open - HAD_Close !=0)
                had_direction_down_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 4) and (HAD_PREV_Open - HAD_PREV_Close !=0)
                had_direction_down_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 4) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
                had_direction_down0 = (HAD_Close < HAD_Open)
                had_direction_down1 = (HAD_PREV_Close < HAD_PREV_Open)
                had_direction_down2 = (HAD_PREV_Close2 < HAD_PREV_Open2)
                had_direction_down_long_0 = (HAD_Open == HAD_High and HAD_Close < HAD_Open)
                had_direction_down_long_1 = (HAD_PREV_Open == HAD_PREV_High and HAD_PREV_Close < HAD_PREV_Open)
                had_direction_down_long_2 = (HAD_PREV_Open2 == HAD_PREV_High2 and HAD_PREV_Close2 < HAD_PREV_Open2)
                had_direction_down_longer = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
                had_direction_down_longermax = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) > numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2 ) and had_direction_down0 and had_direction_down1 and had_direction_down2)
                had_direction_down_smaller = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
                had_direction_down_smaller1 = (numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down1 and had_direction_down2)
                had_direction_down_smallermax = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down0 and had_direction_down1 and had_direction_down2)

                had_direction_spin0 = (HAD_Open == HAD_Close)
                had_direction_spin1 = (HAD_PREV_Open == HAD_PREV_Close)
                had_direction_spin2 = (HAD_PREV_Open2 == HAD_PREV_Close2)

                had_direction_up_short0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 2) and (HAD_Close - HAD_Open !=0)
                had_direction_up_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 2) and (HAD_PREV_Close - HAD_PREV_Open !=0)
                had_direction_up_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 2) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
                had_direction_up_shorter0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 4) and (HAD_Close - HAD_Open !=0)
                had_direction_up_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 4) and (HAD_PREV_Close - HAD_PREV_Open !=0)
                had_direction_up_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 4) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
                had_direction_up0 = (HAD_Close > HAD_Open)
                had_direction_up1 = (HAD_PREV_Close > HAD_PREV_Open)
                had_direction_up2 = (HAD_PREV_Close2 > HAD_PREV_Open2)
                had_direction_up_long_0 = (HAD_Open == HAD_Low and HAD_Close > HAD_Open)
                had_direction_up_long_1 = (HAD_PREV_Open == HAD_PREV_Low and HAD_PREV_Close > HAD_PREV_Open)
                had_direction_up_long_2 = (HAD_PREV_Open2 == HAD_PREV_Low2 and HAD_PREV_Close2 > HAD_PREV_Open2)
                had_direction_up_longer = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
                had_direction_up_longermax = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) > numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
                had_direction_up_smaller = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
                had_direction_up_smaller1 = (numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up1 and had_direction_up2)
                had_direction_up_smallermax = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
##############

                if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longermax and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down2)):
                    HA_trend = "DOWN"


                if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer and ha_direction_up_longermax) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up2)):
                    HA_trend = "UP"


                if ((ha_direction_up_short2 and ha_direction_spin1 and ha_direction_up0) or (ha_direction_down_short2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_down_short1 and ha_direction_spin0) or (ha_direction_down_long_2 and ha_direction_down_short1 and ha_direction_up_long_0) or (ha_direction_down_long_2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_up_long_0 and ha_direction_up1 and ha_direction_up_longer) or (ha_direction_down_long_2 and ha_direction_down_smaller1 and ha_direction_up0) or (ha_direction_down_long_2 and ha_direction_down_short1 and  ha_direction_up_long_0) or (ha_direction_down_longermax and ha_direction_up_short0)):
                    HA_trend = "Revers-UP"


                if ((ha_direction_down_short2 and ha_direction_spin1 and ha_direction_down0) or (ha_direction_up_short2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_up_short1 and ha_direction_spin0) or (ha_direction_up_long_2 and ha_direction_up_short1 and ha_direction_down_long_0) or (ha_direction_up_long_2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_down_long_0 and ha_direction_down1 and ha_direction_down_longer) or (ha_direction_up_long_2 and ha_direction_up_smaller1 and ha_direction_down0) or (ha_direction_up_long_2 and ha_direction_up_short1 and  ha_direction_down_long_0) or (ha_direction_up_longermax and ha_direction_down_short0)):
                    HA_trend = "Revers-DOWN"


                if  HA_trend != "Revers-DOWN" and   HA_trend != "Revers-UP" and  HA_trend != "DOWN" and HA_trend != "UP":
                    HA_trend = "STABLE"

                #else:
                                        #   HA_trend = "STABLE"


#############
                if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
                    HAD_trend = "DOWN"

                if (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
                    HAD_trend = "UP"

                if ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0)):
                    HAD_trend = "Revers-UP"

                if ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0)):
                    HAD_trend = "Revers-DOWN"

                if  HAD_trend != "Revers-DOWN" and   HAD_trend != "Revers-UP" and  HAD_trend != "DOWN" and HAD_trend != "UP":
                    HAD_trend = "STABLE"

                #else:
                 #   HAD_trend = "STABLE"

############
                #print market, HA_trend, HA_Open, HA_Close, HA_Low, HA_High

                #printed = ""

                if ha_direction_down0:
                    print  market, "DOWN, ha_direction_down0", "Latest candle is bearish, HA_Close < HA_Open"
                    printed = (market, "    DOWN, ha_direction_down0", "Latest candle is bearish, HA_Close < HA_Open")
                if ha_direction_down1:
                    print market, "DOWN, ha_direction_down1", "Previous candle was bearish   HA_PREV_Close < HA_PREV_Open"
                    printed =(market, " DOWN, ha_direction_down1", "Previous candle was bearish   HA_PREV_Close < HA_PREV_Open")
                if ha_direction_down2:
                    print market, "DOWN, ha_direction_down2", "Previous2 candle was bearish   HA_PREV_Close2 < HA_PREV_Open2"
                    printed =(market, " DOWN, ha_direction_down2", "Previous2 candle was bearish   HA_PREV_Close2 < HA_PREV_Open2")
                if ha_direction_down_long_0:
                    print  market, "Strong DOWN, ha_direction_down_long_0 latest candle has no upper wick HA_Open == HA_High"
                    printed = (market," Strong DOWN, ha_direction_down_long_0 latest candle has no upper wick HA_Open == HA_High")
                if ha_direction_down_long_1:
                    print market, "Strong DOWN ha_direction_down_long_1 bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High"
                    printed = (market, "    Strong DOWN ha_direction_down_long_1 bearish, previous candle has no upper wick HA_PREV_Open == HA_PREV_High")
                if ha_direction_down_long_2:
                    print market, "Strong DOWN ha_direction_down_long_2 bearish, previous2 candle has no upper wick HA_PREV_Open2 == HA_PREV_High2"
                    printed = (market, "Strong DOWN ha_direction_down_long_2 bearish, previous2 candle has no upper wick HA_PREV_Open2 == HA_PREV_High2")
                if ha_direction_down_longer:
                    print market,  "Strong DOWN, ha_direction_down_longer latest candle body is longer than previous candle body"
                    printed = (market, "    Strong DOWN, ha_direction_down_longer latest candle body is longer than previous candle body")
                if ha_direction_down_longermax:
                    print market,  "Strong DOWN, ha_direction_down_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2"
                    printed = (market, "    Strong DOWN, ha_direction_down_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2")
                if ha_direction_spin0:
                    print market, "Change direction, ha_direction_spin0 spin"
                if ha_direction_spin1:
                    print market, "Change direction ha_direction_spin1 in previous candle, spin"
                if ha_direction_down_short0:
                    print market, "Weak DOWN, ha_direction_down_short0 latest candle body is short - doji"
                if ha_direction_down_short1:
                    print market, "Weak DOWN, ha_direction_down_short1 previous candle body is short - doji"
                if ha_direction_up_short0:
                    print market, "Weak UP, ha_direction_up_short0 latest candle body is short - doji"
                if ha_direction_up_short1:
                    print market, "Weak UP, ha_direction_up_short1 previous candle body is short - doji"
                if ha_direction_up0:
                    print  market, "UP, ha_direction_up0 latest candle bullish  HA_Close > HA_Open"
                if ha_direction_up1:
                    print  market, "UP, ha_direction_up1 previous candle was bullish  HA_PREV_Close > HA_PREV_Open"
                if ha_direction_up2:
                    print  market, "UP, ha_direction_up2 previous2 candle was bullish  HA_PREV_Close2 > HA_PREV_Open2"
                if ha_direction_up_long_0:
                    print  market, "Strong UP, ha_direction_up_long_0 latest candle has no lower wick HA_Open == HA_Low"
                if ha_direction_up_long_1:
                    print  market, "Strong UP, ha_direction_up_long_1 previous candle has no lower wick HA_PREV_Open == HA_PREV_Low"
                if ha_direction_up_long_2:
                    print  market, "Strong UP, ha_direction_up_long_2 previous candle2 has no lower wick HA_PREV_Open2 == HA_PREV_Low2"
                if ha_direction_up_longer:
                    print market, "Strong UP, ha_direction_up_longer latest candle body is longer than previous candle body"
                if ha_direction_up_longermax:
                    print market, "Strong UP, ha_direction_up_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2"
                if ha_direction_up_shorter0:
                    print market, "Weak UP, ha_direction_down_shorter0 latest candle body is very short - doji"
                if ha_direction_up_shorter1:
                    print market, "Weak UP, ha_direction_down_shorter1 latest candle body is very short - doji"
                if ha_direction_up_shorter2:
                    print market, "Weak UP, ha_direction_down_shorter2 latest candle body is very short - doji"
                if ha_direction_up_smaller:
                    print market, "Strong UP, ha_direction_down_smaller latest candle  is shorter than previous candle"
                if ha_direction_up_smallermax:
                    print market, "Strong UP, ha_direction_up_shortermax latest candle is shorter than previous candle and previous candle shorter then previous2"
                if ha_direction_down_shorter0:
                    print market, "Weak DOWN, ha_direction_down_shorter0 latest candle body is very short - doji"
                if ha_direction_down_shorter1:
                    print market, "Weak DOWN, ha_direction_down_shorter1 latest candle body is very short - doji"
                if ha_direction_down_shorter2:
                    print market, "Weak DOWN, ha_direction_down_shorter2 latest candle body is very short - doji"
                if ha_direction_down_smaller:
                    print market, "Strong DOWN, ha_direction_down_smaller latest candle is shorter than previous candle"
                if ha_direction_down_smallermax:
                    print market, "Strong DOWN, ha_direction_down_shortermax latest candle is shorter than previous candle and previous candle shorter then previous2"



#####


                if had_direction_down0:
                    print  market, "DOWN, had_direction_down0", "Latest candle is bearish, HAD_Close < HAD_Open"
                    printed = (market, "    DOWN, had_direction_down0", "Latest candle is bearish, HAD_Close < HAD_Open")
                if had_direction_down1:
                    print market, "DOWN, had_direction_down1", "Previous candle was bearish   HAD_PREV_Close < HAD_PREV_Open"
                    printed =(market, " DOWN, had_direction_down1", "Previous candle was bearish   HAD_PREV_Close < HAD_PREV_Open")
                if had_direction_down2:
                    print market, "DOWN, had_direction_down2", "Previous2 candle was bearish   HAD_PREV_Close2 < HAD_PREV_Open2"
                    printed =(market, " DOWN, had_direction_down2", "Previous2 candle was bearish   HAD_PREV_Close2 < HAD_PREV_Open2")
                if had_direction_down_long_0:
                    print  market, "Strong DOWN, had_direction_down_long_0 latest candle has no upper wick HAD_Open == HAD_High"
                    printed = (market," Strong DOWN, had_direction_down_long_0 latest candle has no upper wick HAD_Open == HAD_High")
                if had_direction_down_long_1:
                    print market, "Strong DOWN had_direction_down_long_1 bearish, previous candle has no upper wick HAD_PREV_Open == HAD_PREV_High"
                    printed = (market, "    Strong DOWN had_direction_down_long_1 bearish, previous candle has no upper wick HAD_PREV_Open == HAD_PREV_High")
                if had_direction_down_long_2:
                    print market, "Strong DOWN had_direction_down_long_2 bearish, previous2 candle has no upper wick HAD_PREV_Open2 == HAD_PREV_High2"
                    printed = (market, "Strong DOWN had_direction_down_long_2 bearish, previous2 candle has no upper wick HAD_PREV_Open2 == HAD_PREV_High2")
                if had_direction_down_longer:
                    print market,  "Strong DOWN, had_direction_down_longer latest candle body is longer than previous candle body"
                    printed = (market, "    Strong DOWN, had_direction_down_longer latest candle body is longer than previous candle body")
                if had_direction_down_longermax:
                    print market,  "Strong DOWN, had_direction_down_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2"
                    printed = (market, "    Strong DOWN, had_direction_down_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2")
                if had_direction_spin0:
                    print market, "Change direction, had_direction_spin0 spin"
                if had_direction_spin1:
                    print market, "Change direction had_direction_spin1 in previous candle, spin"
                if had_direction_down_short0:
                    print market, "Weak DOWN, had_direction_down_short0 latest candle body is short - doji"
                if had_direction_down_short1:
                    print market, "Weak DOWN, had_direction_down_short1 previous candle body is short - doji"
                if had_direction_up_short0:
                    print market, "Weak UP, had_direction_up_short0 latest candle body is short - doji"
                if had_direction_up_short1:
                    print market, "Weak UP, had_direction_up_short1 previous candle body is short - doji"
                if had_direction_up0:
                    print  market, "UP, had_direction_up0 latest candle bullish  HAD_Close > HAD_Open"
                if had_direction_up1:
                    print  market, "UP, had_direction_up1 previous candle was bullish  HAD_PREV_Close > HAD_PREV_Open"
                if had_direction_up2:
                    print  market, "UP, had_direction_up2 previous2 candle was bullish  HAD_PREV_Close2 > HAD_PREV_Open2"
                if had_direction_up_long_0:
                    print  market, "Strong UP, had_direction_up_long_0 latest candle has no lower wick HAD_Open == HAD_Low"
                if had_direction_up_long_1:
                    print  market, "Strong UP, had_direction_up_long_1 previous candle has no lower wick HAD_PREV_Open == HAD_PREV_Low"
                if had_direction_up_long_2:
                    print  market, "Strong UP, had_direction_up_long_2 previous candle2 has no lower wick HAD_PREV_Open2 == HAD_PREV_Low2"
                if had_direction_up_longer:
                    print market, "Strong UP, had_direction_up_longer latest candle body is longer than previous candle body"
                if had_direction_up_longermax:
                    print market, "Strong UP, had_direction_up_longermax latest candle body is longer than previous candle body and previous candle body longer then previous2"
                if had_direction_up_shorter0:
                    print market, "Weak UP, had_direction_down_shorter0 latest candle body is very short - doji"
                if had_direction_up_shorter1:
                    print market, "Weak UP, had_direction_down_shorter1 latest candle body is very short - doji"
                if had_direction_up_shorter2:
                    print market, "Weak UP, had_direction_down_shorter2 latest candle body is very short - doji"
                if had_direction_up_smaller:
                    print market, "Strong UP, had_direction_down_smaller latest candle  is shorter than previous candle"
                if had_direction_up_smallermax:
                    print market, "Strong UP, had_direction_up_shortermax latest candle is shorter than previous candle and previous candle shorter then previous2"
                if had_direction_down_shorter0:
                    print market, "Weak DOWN, had_direction_down_shorter0 latest candle body is very short - doji"
                if had_direction_down_shorter1:
                    print market, "Weak DOWN, had_direction_down_shorter1 latest candle body is very short - doji"
                if had_direction_down_shorter2:
                    print market, "Weak DOWN, had_direction_down_shorter2 latest candle body is very short - doji"
                if had_direction_down_smaller:
                    print market, "Strong DOWN, had_direction_down_smaller latest candle is shorter than previous candle"
                if had_direction_down_smallermax:
                    print market, "Strong DOWN, had_direction_down_shortermax latest candle is shorter than previous candle and previous candle shorter then previous2"

                #print market, bought_quantity_sql

                if ((ha_direction_down0 and ha_direction_down1 and ha_direction_down_long_0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down_long_0 and ha_direction_down_long_1) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down_longer) and bought_quantity_sql > 0):

                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 1 where active=1 and market =("%s")' % market)
                        if bought_quantity_sql>0:
                            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                    # print market, daymonthclose8, daymonthclose7, daymonthclose6, daymonthclose5, daymonthclose4, daymonthclose3, daymonthclose2, daymonthclose1, last
                    dayprice8 = int(daymonthclose8 * 100 / daymonthclose8)
                    dayprice7 = int(daymonthclose7 * 100 / daymonthclose8)
                    dayprice6 = int(daymonthclose6 * 100 / daymonthclose8)
                    dayprice5 = int(daymonthclose5 * 100 / daymonthclose8)
                    dayprice4 = int(daymonthclose4 * 100 / daymonthclose8)
                    dayprice3 = int(daymonthclose3 * 100 / daymonthclose8)
                    dayprice2 = int(daymonthclose2 * 100 / daymonthclose8)
                    dayprice1 = int(daymonthclose1 * 100 / daymonthclose8)

                    #    quarter_direction="NULL"

                    if (dayprice8 >= dayprice7 and dayprice7 >= dayprice6 and dayprice6 >= dayprice5 and dayprice5 >= dayprice4 and dayprice4 >= dayprice3 and dayprice3 >= dayprice2 and dayprice2 >= dayprice1) or (dayprice7 >= dayprice6 and dayprice6 >= dayprice5 and dayprice5 >= dayprice4 and dayprice4 >= dayprice3 and dayprice3 >= dayprice2 and dayprice2 >= dayprice1) or (dayprice5 >= dayprice4 and dayprice4 >= dayprice3 and dayprice3 >= dayprice2 and dayprice2 >= dayprice1):
                        quarter_direction = "DOWN"
                    else:
                        quarter_direction = "STABLE"

                    #print market, quarter_direction



                if HAD_trend=="DOWN" or HAD_trend=="STABLE" or HAD_trend=="Revers-DOWN" or quarter_direction == "DOWN":
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('update markets set ai_ha = 1 where active=1 and market =("%s")' % market)
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
                        cursor.execute('update markets set ai_ha = 0 where active=1 and market =("%s")' % market)
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                #print market, HA_trend, HAD_trend

                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    #cursor.execute(
                     #   'insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    printed = ('      '+ market + '   The HA_hour is  ' + HA_trend + '  and HA_day is:  ' + HAD_trend )
                    cursor.execute("update markets set current_price = %s, ha_direction =%s, ha_direction_daily=%s  where market = %s and active =1",(last, HA_trend, HAD_trend, market))
                    cursor.execute('insert into ha_logs (date, market, HA_hour, HA_day, log ) values ("%s", "%s", "%s", "%s", "%s")' % (currenttime, market, HA_trend, HAD_trend, printed))
                    #cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()






        except:
            continue

def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
