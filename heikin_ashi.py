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
c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')

currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")





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



    if (((hour_direction_down_long_0 and hour_direction_down0) or (
            hour_direction_down_long_0 and hour_direction_down_long_1 and hour_direction_down0) or (
        hour_direction_down_long_0 or hour_direction_down_long_1 and hour_direction_down_longer) and hour_direction_down0) or (
        hour_direction_down0 and hour_direction_down1)):
        btc_trend_hour = "DOWN"
    if (((hour_direction_up_long_0 and hour_direction_up0) or (
            hour_direction_up_long_0 and hour_direction_up_long_1 and hour_direction_up0) or (
        hour_direction_up_long_0 or hour_direction_up_long_1 and hour_direction_up_longer) and hour_direction_up0) or (
        hour_direction_up0 and hour_direction_up1)):
        btc_trend_hour = "UP"

    if btc_trend_hour != "DOWN" and btc_trend_hour != "UP":
        btc_trend_hour = "STABLE"


        # Daily HA
    if (((direction_down_long_0 and direction_down0) or (
            direction_down_long_0 and direction_down_long_1 and direction_down0) or (
        direction_down_long_0 or direction_down_long_1 and direction_down_longer) and direction_down0) or (
        direction_down0 and direction_down1 and direction_down2)):
        btc_trend = "DOWN"
    if (((direction_up_long_0 and direction_up0) or (
            direction_up_long_0 and direction_up_long_1 and direction_up0) or (
        direction_up_long_0 or direction_up_long_1 and direction_up_longer) and direction_up0) or (
        direction_up0 and direction_up1 and direction_up2)):
        btc_trend = "UP"

    if btc_trend != "DOWN" and btc_trend != "UP":
        btc_trend = "STABLE"



    if btc_trend == "DOWN" and btc_trend_hour == "DOWN":
        btc_trend = "DANGER"








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







    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                last = float(summary['Last'])  # last price
                bought_quantity_sql = float(status_orders(market, 2))


                hlastcandle = get_candles(market, 'hour')['result'][-1:]
                hcurrentlow = float(hlastcandle[0]['L'])
                hcurrenthigh = float(hlastcandle[0]['H'])
                hcurrentopen = float(hlastcandle[0]['O'])
                hcurrentclose = float(hlastcandle[0]['C'])
                hpreviouscandle = get_candles(market, 'hour')['result'][-2:]
                hprevlow = float(hpreviouscandle[0]['L'])
                hprevhigh = float(hpreviouscandle[0]['H'])
                hprevopen = float(hpreviouscandle[0]['O'])
                hprevclose = float(hpreviouscandle[0]['C'])
                hpreviouscandle2 = get_candles(market, 'hour')['result'][-3:]
                hprevlow2 = float(hpreviouscandle2[0]['L'])
                hprevhigh2 = float(hpreviouscandle2[0]['H'])
                hprevopen2 = float(hpreviouscandle2[0]['O'])
                hprevclose2 = float(hpreviouscandle2[0]['C'])

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


                lastcandlesize = hourcurrenthigh-hourcurrentlow
                previouscandlesize = hourprevhigh-hourprevlow
                previouscandlesize2 = hourprevhigh2-hourprevlow2
                previouscandlesize3 = hourprevhigh3-hourprevlow3
                previouscandlesize4 = hourprevhigh4-hourprevlow4
                previouscandlesize5 = hourprevhigh5-hourprevlow5
                previouscandlesize6 =  hourprevhigh6- hourprevlow6






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


                HAH_PREV_Close2 = (hprevopen2 + hprevhigh2 + hprevlow2 + hprevclose2) / 4
                HAH_PREV_Open2 = (hprevopen2 + hprevclose2) / 2
                HAH_PREV_Low2 = hprevlow2
                HAH_PREV_High2 = hprevhigh2

                HAH_PREV_Close = (hprevopen + hprevhigh + hprevlow + hprevclose) / 4
                HAH_PREV_Open = (HAH_PREV_Open2 + HAH_PREV_Close2) / 2
                elements1 = numpy.array([hprevhigh, hprevlow, HAH_PREV_Open, HAH_PREV_Close])
                HAH_PREV_High = elements1.max(0)
                HAH_PREV_Low = elements1.min(0)

                HAH_Close = (hcurrentopen + hcurrenthigh + hcurrentlow + hcurrentclose) / 4
                HAH_Open = (HAH_PREV_Open + HAH_PREV_Close) / 2
                elements0 = numpy.array([hcurrenthigh, hcurrentlow, HAH_Open, HAH_Close])
                HAH_High = elements0.max(0)
                HAH_Low = elements0.min(0)




                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set ha_close = %s, ha_open =%s, ha_low =%s, ha_high =%s, ha_time =%s, ha_time_second=%s  where market = %s",(HA_Close, HA_Open, HA_Low, HA_High, currenttime, currtime, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

                HA_trend = "NONE"

                HAH_trend = "NONE"


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




                hah_direction_down_short0 =((HAH_High - HAH_Low) / (HAH_Open - HAH_Close) >= 2)  and (HAH_Open - HAH_Close !=0)
                hah_direction_down_short1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Open - HAH_PREV_Close) >= 2) and (HAH_PREV_Open - HAH_PREV_Close !=0)
                hah_direction_down_short2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Open2 - HAH_PREV_Close2) >= 2) and (HAH_PREV_Open2 - HAH_PREV_Close2 !=0)
                hah_direction_down_shorter0 =((HAH_High - HAH_Low) / (HAH_Open - HAH_Close) >= 4)  and (HAH_Open - HAH_Close !=0)
                hah_direction_down_shorter1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Open - HAH_PREV_Close) >= 4) and (HAH_PREV_Open - HAH_PREV_Close !=0)
                hah_direction_down_shorter2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Open2 - HAH_PREV_Close2) >= 4) and (HAH_PREV_Open2 - HAH_PREV_Close2 !=0)
                hah_direction_down0 = (HAH_Close < HAH_Open)
                hah_direction_down1 = (HAH_PREV_Close < HAH_PREV_Open)
                hah_direction_down2 = (HAH_PREV_Close2 < HAH_PREV_Open2)
                hah_direction_down_long_0 = (HAH_Open == HAH_High and HAH_Close < HAH_Open)
                hah_direction_down_long_1 = (HAH_PREV_Open == HAH_PREV_High and HAH_PREV_Close < HAH_PREV_Open)
                hah_direction_down_long_2 = (HAH_PREV_Open2 == HAH_PREV_High2 and HAH_PREV_Close2 < HAH_PREV_Open2)
                hah_direction_down_longer = (numpy.abs(HAH_Open - HAH_Close) > numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and hah_direction_down0 and hah_direction_down1)
                hah_direction_down_longermax = (numpy.abs(HAH_Open - HAH_Close) > numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and numpy.abs(HAH_PREV_Open - HAH_PREV_Close) > numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2 ) and hah_direction_down0 and hah_direction_down1 and hah_direction_down2)
                hah_direction_down_smaller = (numpy.abs(HAH_Open - HAH_Close) < numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and hah_direction_down0 and hah_direction_down1)
                hah_direction_down_smaller1 = (numpy.abs(HAH_PREV_Open - HAH_PREV_Close) < numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2) and hah_direction_down1 and hah_direction_down2)
                hah_direction_down_smallermax = (numpy.abs(HAH_Open - HAH_Close) < numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and numpy.abs(HAH_PREV_Open - HAH_PREV_Close) < numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2) and hah_direction_down0 and hah_direction_down1 and hah_direction_down2)

                hah_direction_spin0 = (HAH_Open == HAH_Close)
                hah_direction_spin1 = (HAH_PREV_Open == HAH_PREV_Close)
                hah_direction_spin2 = (HAH_PREV_Open2 == HAH_PREV_Close2)

                hah_direction_up_short0 = ((HAH_High - HAH_Low) / (HAH_Close - HAH_Open) >= 2) and (HAH_Close - HAH_Open !=0)
                hah_direction_up_short1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Close - HAH_PREV_Open) >= 2) and (HAH_PREV_Close - HAH_PREV_Open !=0)
                hah_direction_up_short2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Close2 - HAH_PREV_Open2) >= 2) and (HAH_PREV_Close2 - HAH_PREV_Open2 !=0)
                hah_direction_up_shorter0 = ((HAH_High - HAH_Low) / (HAH_Close - HAH_Open) >= 4) and (HAH_Close - HAH_Open !=0)
                hah_direction_up_shorter1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Close - HAH_PREV_Open) >= 4) and (HAH_PREV_Close - HAH_PREV_Open !=0)
                hah_direction_up_shorter2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Close2 - HAH_PREV_Open2) >= 4) and (HAH_PREV_Close2 - HAH_PREV_Open2 !=0)
                hah_direction_up0 = (HAH_Close > HAH_Open)
                hah_direction_up1 = (HAH_PREV_Close > HAH_PREV_Open)
                hah_direction_up2 = (HAH_PREV_Close2 > HAH_PREV_Open2)
                hah_direction_up_long_0 = (HAH_Open == HAH_Low and HAH_Close > HAH_Open)
                hah_direction_up_long_1 = (HAH_PREV_Open == HAH_PREV_Low and HAH_PREV_Close > HAH_PREV_Open)
                hah_direction_up_long_2 = (HAH_PREV_Open2 == HAH_PREV_Low2 and HAH_PREV_Close2 > HAH_PREV_Open2)
                hah_direction_up_longer = (numpy.abs(HAH_Close - HAH_Open) > numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and hah_direction_up0 and hah_direction_up1)
                hah_direction_up_longermax = (numpy.abs(HAH_Close - HAH_Open) > numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and numpy.abs(HAH_PREV_Close - HAH_PREV_Open) > numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up0 and hah_direction_up1 and hah_direction_up2)
                hah_direction_up_smaller = (numpy.abs(HAH_Close - HAH_Open) < numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and hah_direction_up0 and hah_direction_up1)
                hah_direction_up_smaller1 = (numpy.abs(HAH_PREV_Close - HAH_PREV_Open) < numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up1 and hah_direction_up2)
                hah_direction_up_smallermax = (numpy.abs(HAH_Close - HAH_Open) < numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and numpy.abs(HAH_PREV_Close - HAH_PREV_Open) < numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up0 and hah_direction_up1 and hah_direction_up2)



                if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longermax and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down2)):
                    HA_trend = "DOWN"


                if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer and ha_direction_up_longermax) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up2)):
                    HA_trend = "UP"


                if ((ha_direction_up_short2 and ha_direction_spin1 and ha_direction_up0) or (ha_direction_down_short2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_down_short1 and ha_direction_spin0) or (ha_direction_down_long_2 and ha_direction_down_short1 and ha_direction_up_long_0) or (ha_direction_down_long_2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_up_long_0 and ha_direction_up1 and ha_direction_up_longer) or (ha_direction_down_long_2 and ha_direction_down_smaller1 and ha_direction_up0) or (ha_direction_down_long_2 and ha_direction_down_short1 and  ha_direction_up_long_0) or (ha_direction_down_longermax and ha_direction_up_short0) and ha_direction_down1 and ha_direction_down2) and ha_direction_down1 and ha_direction_down2:
                    HA_trend = "Revers-UP"


                if ((ha_direction_down_short2 and ha_direction_spin1 and ha_direction_down0) or (ha_direction_up_short2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_up_short1 and ha_direction_spin0) or (ha_direction_up_long_2 and ha_direction_up_short1 and ha_direction_down_long_0) or (ha_direction_up_long_2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_down_long_0 and ha_direction_down1 and ha_direction_down_longer) or (ha_direction_up_long_2 and ha_direction_up_smaller1 and ha_direction_down0) or (ha_direction_up_long_2 and ha_direction_up_short1 and  ha_direction_down_long_0) or (ha_direction_up_longermax and ha_direction_down_short0) and ha_direction_up1 and ha_direction_up2) and ha_direction_up1 and ha_direction_up2:
                    HA_trend = "Revers-DOWN"


                if  HA_trend != "Revers-DOWN" and   HA_trend != "Revers-UP" and  HA_trend != "DOWN" and HA_trend != "UP":
                    HA_trend = "STABLE"





                if (((hah_direction_down_long_0 and hah_direction_down0) or (hah_direction_down_long_0 and hah_direction_down_long_1 and hah_direction_down0) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longer) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longermax and hah_direction_down_longer) and hah_direction_down0) or (hah_direction_down0 and hah_direction_down1 and hah_direction_down2)):
                    HAH_trend = "DOWN"

                if (((hah_direction_up_long_0 and hah_direction_up0) or (hah_direction_up_long_0 and hah_direction_up_long_1 and hah_direction_up0) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer and hah_direction_up_longermax) and hah_direction_up0) or (hah_direction_up0 and hah_direction_up1 and hah_direction_up2)):
                    HAH_trend = "UP"

                if ((hah_direction_up_short2 and hah_direction_spin1 and hah_direction_up0) or (hah_direction_down_short2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_down_short1 and hah_direction_spin0) or (hah_direction_down_long_2 and hah_direction_down_short1 and hah_direction_up_long_0) or (hah_direction_down_long_2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_up_long_0 and hah_direction_up1 and hah_direction_up_longer) or (hah_direction_down_long_2 and hah_direction_down_smaller1 and hah_direction_up0) or (hah_direction_down_long_2 and hah_direction_down_short1 and  hah_direction_up_long_0) or (hah_direction_down_longermax and hah_direction_up_short0) and hah_direction_down1 and hah_direction_down2):
                    HAH_trend = "Revers-UP"

                if ((hah_direction_down_short2 and hah_direction_spin1 and hah_direction_down0) or (hah_direction_up_short2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_up_short1 and hah_direction_spin0) or (hah_direction_up_long_2 and hah_direction_up_short1 and hah_direction_down_long_0) or (hah_direction_up_long_2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_down_long_0 and hah_direction_down1 and hah_direction_down_longer) or (hah_direction_up_long_2 and hah_direction_up_smaller1 and hah_direction_down0) or (hah_direction_up_long_2 and hah_direction_up_short1 and  hah_direction_down_long_0) or (hah_direction_up_longermax and hah_direction_down_short0) and hah_direction_up1 and hah_direction_up2):
                    HAH_trend = "Revers-DOWN"

                if  HAH_trend != "Revers-DOWN" and   HAH_trend != "Revers-UP" and  HAH_trend != "DOWN" and HAH_trend != "UP":
                    HAH_trend = "STABLE"

                print market, HA_trend, HAH_trend



                if ((ha_direction_down0 and ha_direction_down1 and ha_direction_down_long_0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down_long_0 and ha_direction_down_long_1) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down_longer) and bought_quantity_sql > 0):

                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 1 where active=1 and market =("%s")' % market)
                        #if bought_quantity_sql>0:
                        #    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                if ((ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0 and ha_direction_up_long_1) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_longer) and bought_quantity_sql > 0):

                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 0 where active=1 and market =("%s")' % market)
                        #if bought_quantity_sql>0:
                        #    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                #print market, last, HA_trend, HAH_trend




                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()

                    printed = ('      '+ market + '   The HA_hour is  ' + HA_trend + '  and HAH is ' + HAH_trend)
                    cursor.execute("update markets set current_price = %s, ha_direction =%s,  ha_direction_hour=%s  where market = %s and active =1",(last, HA_trend,  HAH_trend, market))
                    #cursor.execute('insert into ha_logs (date, market, HA_hour, log ) values ("%s", "%s", "%s", "%s")' % (currenttime, market, HA_trend, printed))
                    #cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()



                averagecandlesize=(previouscandlesize6+previouscandlesize5+previouscandlesize4)/3
                print market, averagecandlesize, lastcandlesize, previouscandlesize, previouscandlesize2, previouscandlesize3


                if (lastcandlesize/averagecandlesize>3 and last>hourcurrentopen) or (previouscandlesize2/averagecandlesize>3 and hourprevclose>hourprevopen) or (previouscandlesize3/averagecandlesize>3 and hourprevclose2>hourprevopen2):
                    print "We have peak situation, lets wait"
                    printed1=("We have peak situation, lets wait")



                try:
                    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set strike_date=%s, strike_info=%s  where market = %s",(currenttime, printed1, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()





        except:
            continue



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
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0




def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
