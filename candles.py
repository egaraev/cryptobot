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
#c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')

currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
TICK_INTERVAL = 60  # seconds




def main():
    print('Starting candle patterns module')


    # Running clock forever
    while True:
        start = time.time()
        tick()
        end = time.time()
        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))


def tick():

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                last = float(summary['Last'])  # last price
                #print last
                candles_signal_short = str(heikin_ashi(market, 29))
                candles_signal_long = str(heikin_ashi(market, 30))
                candles_signal_price = float(heikin_ashi(market, 32))
                candles_signal_time=int(heikin_ashi(market, 31))

                thirtylastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                thirtycurrentlow = float(thirtylastcandle[0]['L'])*100000
                thirtycurrenthigh = float(thirtylastcandle[0]['H'])*100000
                thirtycurrentopen = float(thirtylastcandle[0]['O'])*100000
                thirtycurrentclose = float(thirtylastcandle[0]['C'])*100000
                thirtypreviouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                thirtyprevlow = float(thirtypreviouscandle[0]['L'])*100000
                thirtyprevhigh = float(thirtypreviouscandle[0]['H'])*100000
                thirtyprevopen = float(thirtypreviouscandle[0]['O'])*100000
                thirtyprevclose = float(thirtypreviouscandle[0]['C'])*100000
                thirtypreviouscandle2 = get_candles(market, 'thirtymin')['result'][-3:]
                thirtyprevlow2 = float(thirtypreviouscandle2[0]['L'])*100000
                thirtyprevhigh2 = float(thirtypreviouscandle2[0]['H'])*100000
                thirtyprevopen2 = float(thirtypreviouscandle2[0]['O'])*100000
                thirtyprevclose2 = float(thirtypreviouscandle2[0]['C'])*100000
                thirtypreviouscandle3 = get_candles(market, 'thirtymin')['result'][-4:]
                thirtyprevlow3 = float(thirtypreviouscandle3[0]['L'])*100000
                thirtyprevhigh3 = float(thirtypreviouscandle3[0]['H'])*100000
                thirtyprevopen3 = float(thirtypreviouscandle3[0]['O'])*100000
                thirtyprevclose3 = float(thirtypreviouscandle3[0]['C'])*100000
                thirtypreviouscandle4 = get_candles(market, 'thirtymin')['result'][-5:]
                thirtyprevlow4 = float(thirtypreviouscandle4[0]['L'])*100000
                thirtyprevhigh4 = float(thirtypreviouscandle4[0]['H'])*100000
                thirtyprevopen4 = float(thirtypreviouscandle4[0]['O'])*100000
                thirtyprevclose4 = float(thirtypreviouscandle4[0]['C'])*100000
                thirtypreviouscandle5 = get_candles(market, 'thirtymin')['result'][-6:]
                thirtyprevlow5 = float(thirtypreviouscandle5[0]['L'])*100000
                thirtyprevhigh5 = float(thirtypreviouscandle5[0]['H'])*100000
                thirtyprevopen5 = float(thirtypreviouscandle5[0]['O'])*100000
                thirtyprevclose5 = float(thirtypreviouscandle5[0]['C'])*100000






                hlastcandle = get_candles(market, 'hour')['result'][-1:]
                hcurrentlow = float(hlastcandle[0]['L'])*100000
                hcurrenthigh = float(hlastcandle[0]['H'])*100000
                hcurrentopen = float(hlastcandle[0]['O'])*100000
                hcurrentclose = float(hlastcandle[0]['C'])*100000
                hpreviouscandle = get_candles(market, 'hour')['result'][-2:]
                hprevlow = float(hpreviouscandle[0]['L'])*100000
                hprevhigh = float(hpreviouscandle[0]['H'])*100000
                hprevopen = float(hpreviouscandle[0]['O'])*100000
                hprevclose = float(hpreviouscandle[0]['C'])*100000
                hpreviouscandle2 = get_candles(market, 'hour')['result'][-3:]
                hprevlow2 = float(hpreviouscandle2[0]['L'])*100000
                hprevhigh2 = float(hpreviouscandle2[0]['H'])*100000
                hprevopen2 = float(hpreviouscandle2[0]['O'])*100000
                hprevclose2 = float(hpreviouscandle2[0]['C'])*100000
                hpreviouscandle3 = get_candles(market, 'hour')['result'][-4:]
                hprevlow3 = float(hpreviouscandle3[0]['L'])*100000
                hprevhigh3 = float(hpreviouscandle3[0]['H'])*100000
                hprevopen3 = float(hpreviouscandle3[0]['O'])*100000
                hprevclose3 = float(hpreviouscandle3[0]['C'])*100000
                hpreviouscandle4 = get_candles(market, 'hour')['result'][-5:]
                hprevlow4 = float(hpreviouscandle4[0]['L'])*100000
                hprevhigh4 = float(hpreviouscandle4[0]['H'])*100000
                hprevopen4 = float(hpreviouscandle4[0]['O'])*100000
                hprevclose4 = float(hpreviouscandle4[0]['C'])*100000
                hpreviouscandle5 = get_candles(market, 'hour')['result'][-6:]
                hprevlow5 = float(hpreviouscandle5[0]['L'])*100000
                hprevhigh5 = float(hpreviouscandle5[0]['H'])*100000
                hprevopen5 = float(hpreviouscandle5[0]['O'])*100000
                hprevclose5 = float(hpreviouscandle5[0]['C'])*100000






#HAMMER
                signal1="NONE"
                signal2="NONE"

                if (thirtyprevhigh==thirtyprevclose) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) >= 2.5)  and (thirtyprevopen - thirtyprevclose !=0) and (thirtyprevopen2 > thirtyprevclose2) and thirtycurrentopen<thirtycurrentclose:
                    signal1="UP_1"
                else:
                    pass


                if (hprevhigh==hprevclose) and ((hprevhigh - hprevlow) / (hprevopen - hprevclose) >= 2.5)  and (hprevopen - hprevclose !=0) and (hprevopen2 > hprevclose2) and hcurrentopen<hcurrentclose:
                    signal2="UP_1"
                else:
                    pass

#HANGING MAN
                if (thirtyprevhigh==thirtyprevopen) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) >= 2.5)  and (thirtyprevopen - thirtyprevclose !=0) and (thirtyprevopen2 < thirtyprevclose2) and thirtycurrentopen>thirtycurrentclose:
                    signal1="DOWN_1"
                else:
                    pass


                if (hprevhigh==hprevopen) and ((hprevhigh - hprevlow) / (hprevopen - hprevclose) >= 2.5)  and (hprevopen - hprevclose !=0) and (hprevopen2 < hprevclose2) and hcurrentopen>hcurrentclose:
                    signal2="DOWN_1"
                else:
                    pass

#INVERTED HAMMER
                if (thirtyprevopen==thirtyprevlow) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) >= 2.5)  and (thirtyprevopen - thirtyprevclose !=0) and (thirtyprevopen2 > thirtyprevclose2) and thirtycurrentopen<thirtycurrentclose:
                    signal1="UP_2"
                else:
                    pass


                if (hprevopen==hprevlow) and ((hprevhigh - hprevlow) / (hprevopen - hprevclose) >= 2.5)  and (hprevopen - hprevclose !=0) and (hprevopen2 > hprevclose2) and hcurrentopen<hcurrentclose:
                    signal2="UP_2"
                else:
                    pass

#SHOOTING STAR

                if (thirtyprevclose==thirtyprevlow) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) >= 2.5)  and (thirtyprevopen - thirtyprevclose !=0) and (thirtyprevopen2 < thirtyprevclose2) and thirtycurrentopen>thirtycurrentclose:
                    signal1="DOWN_2"
                else:
                    pass


                if (hprevclose==hprevlow) and ((hprevhigh - hprevlow) / (hprevopen - hprevclose) >= 2.5)  and (hprevopen - hprevclose !=0) and (hprevopen2 < hprevclose2) and hcurrentopen>hcurrentclose:
                    signal2="DOWN_2"
                else:
                    pass


#BULLISH ENGULFING

                if ((thirtyprevopen2 > thirtyprevclose2) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevhigh2 - thirtyprevlow2) >= 1.5) and (thirtyprevhigh2 - thirtyprevlow2 !=0) and  (thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) <= 2) and (thirtyprevopen < thirtyprevclose) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_3"
                else:
                    pass



                if ((hprevopen2 > hprevclose2) and ((hprevhigh - hprevlow) / (hprevhigh2 - hprevlow2) >= 1.5) and (hprevhigh2 - hprevlow2 !=0) and  (hprevhigh - hprevlow) / (hprevopen - hprevclose) <= 2) and (hprevopen < hprevclose) and hcurrentopen<hcurrentclose:
                    signal2 = "UP_3"
                else:
                    pass


#BEARISH ENGULFING

                if ((thirtyprevopen2 < thirtyprevclose2) and ((thirtyprevhigh - thirtyprevlow) / (thirtyprevhigh2 - thirtyprevlow2) >= 1.5) and (thirtyprevhigh2 - thirtyprevlow2 !=0) and  (thirtyprevhigh - thirtyprevlow) / (thirtyprevopen - thirtyprevclose) <= 2)  and (thirtyprevopen > thirtyprevclose) and thirtycurrentopen>thirtycurrentclose:
                    signal1 = "DOWN_3"
                else:
                    pass



                if ((hprevopen2 < hprevclose2) and ((hprevhigh - hprevlow) / (hprevhigh2 - hprevlow2) >= 1.5) and (hprevhigh2 - hprevlow2 !=0) and  (hprevhigh - hprevlow) / (hprevopen - hprevclose) <= 2) and (hprevopen > hprevclose) and hcurrentopen>hcurrentclose:
                    signal2 = "DOWN_3"
                else:
                    pass


#TWEEZER BOTTOMS

                if (thirtyprevopen2>thirtyprevclose2 and thirtyprevopen3>thirtyprevclose3 and thirtyprevopen4>thirtyprevclose4) and (thirtyprevopen<thirtyprevclose) and thirtyprevlow==thirtyprevlow2  and ((thirtyprevhigh - thirtyprevlow) - (thirtyprevopen - thirtyprevclose) == (thirtyprevhigh - thirtyprevlow) - (thirtyprevclose - thirtyprevopen) and thirtyprevopen2==thirtyprevhigh2 and thirtyprevhigh==thirtyprevclose) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_4"
                else:
                    pass



                if (hprevopen2>hprevclose2 and hprevopen3>thirtyprevclose3 and hprevopen4>hprevclose4) and (hprevopen<hprevclose) and hprevlow==hprevlow2  and ((hprevhigh - hprevlow) - (hprevopen - hprevclose) == (hprevhigh - hprevlow) - (hprevclose - hprevopen)  and hprevopen2==hprevhigh2 and hprevhigh==hprevclose) and hcurrentopen<hcurrentclose:
                    signal2 = "UP_4"
                else:
                    pass


# TWEEZER TOPS


                if (thirtyprevopen2<thirtyprevclose2 and thirtyprevopen3<thirtyprevclose3 and thirtyprevopen4<thirtyprevclose4) and (thirtyprevopen>thirtyprevclose) and  thirtyprevhigh==thirtyprevhigh2 and ((thirtyprevhigh - thirtyprevlow) - (thirtyprevopen - thirtyprevclose) == (thirtyprevhigh - thirtyprevlow) - (thirtyprevclose - thirtyprevopen) and thirtyprevopen==thirtyprevhigh and thirtyprevhigh2==thirtyprevclose2) and thirtycurrentopen>thirtycurrentclose:
                    signal1 = "DOWN_4"
                else:
                    pass




                if (hprevopen2<hprevclose2 and hprevopen3<hprevclose3 and hprevopen4<hprevclose4) and (hprevopen>hprevclose) and  hprevhigh==hprevhigh2 and ((hprevhigh - hprevlow) - (hprevopen - hprevclose) == (hprevhigh - hprevlow) - (hprevclose - hprevopen) and hprevopen==hprevhigh and hprevhigh2==hprevclose2) and hcurrentopen>hcurrentclose:
                    signal2 = "DOWN_4"
                else:
                    pass


#EVENING STAR
                                                # upper trend                                                                           #current candle is down                             #short candle or doji
                if (thirtyprevopen3<thirtyprevclose3 and thirtyprevopen4<thirtyprevclose4 and thirtyprevopen5<thirtyprevclose5) and (thirtyprevopen>thirtyprevclose) and   (thirtyprevopen2==thirtyprevclose2 or ((thirtyprevhigh2 - thirtyprevlow2) / numpy.abs(thirtyprevclose2 - thirtyprevopen2) >= 4 and (thirtyprevclose2 - thirtyprevopen2 !=0))) and (thirtyprevopen-thirtyprevclose >=(thirtyprevclose3-thirtyprevopen3)/2) and thirtycurrentopen>thirtycurrentclose:
                    signal1 = "DOWN_5"
                else:
                    pass



                if (hprevopen3<hprevclose3 and hprevopen4<hprevclose4 and hprevopen5<hprevclose5) and (hprevopen>hprevclose) and   (hprevopen2==hprevclose2 or ((hprevhigh2 - hprevlow2) / numpy.abs(hprevclose2 - hprevopen2) >= 4 and (hprevclose2 - hprevopen2 !=0))) and (hprevopen-hprevclose >=(hprevclose3-hprevopen3)/2) and hcurrentopen>hcurrentclose:
                    signal2 = "DOWN_5"
                else:
                    pass


#MORNING STAR

                if (thirtyprevopen3>thirtyprevclose3 and thirtyprevopen4>thirtyprevclose4 and thirtyprevopen5>thirtyprevclose5) and (thirtyprevopen<thirtyprevclose) and   (thirtyprevopen2==thirtyprevclose2 or ((thirtyprevhigh2 - thirtyprevlow2) / numpy.abs(thirtyprevclose2 - thirtyprevopen2) >= 4 and (thirtyprevclose2 - thirtyprevopen2 !=0))) and (thirtyprevclose - thirtyprevopen >=(thirtyprevopen3 - thirtyprevclose3)/2) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_5"
                else:
                    pass



                if (hprevopen3>hprevclose3 and hprevopen4>hprevclose4 and hprevopen5>hprevclose5) and (hprevopen<hprevclose) and   (hprevopen2==hprevclose2 or ((hprevhigh2 - hprevlow2) / numpy.abs(hprevclose2 - hprevopen2) >= 4 and (hprevclose2 - hprevopen2 !=0))) and (hprevclose - hprevopen >=(hprevopen3 - hprevclose3)/2) and hcurrentopen<hcurrentclose :
                    signal2 = "UP_5"
                else:
                    pass


#THREE WHITE SOLDIERS

                if ((thirtyprevopen<thirtyprevclose and thirtyprevopen2<thirtyprevclose2 and thirtyprevopen3<thirtyprevclose3 and thirtyprevopen4>thirtyprevclose4 and thirtyprevopen5>thirtyprevopen5)  and  (thirtyprevhigh2-thirtyprevlow2>thirtyprevclose3-thirtyprevopen3) and  thirtyprevhigh2==thirtyprevclose2  and thirtyprevhigh-thirtyprevlow >=thirtyprevhigh2-thirtyprevlow2  and thirtyprevhigh==thirtyprevclose and thirtyprevopen==thirtyprevlow ) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_6"
                else:
                    pass



                if ((hprevopen<hprevclose and hprevopen2<hprevclose2 and hprevopen3<hprevclose3 and hprevopen4>hprevclose4 and hprevopen5>hprevopen5)  and  (hprevhigh2-hprevlow2>hprevclose3-hprevopen3) and  hprevhigh2==hprevclose2  and hprevhigh-hprevlow >=hprevhigh2-hprevlow2  and hprevhigh==hprevclose and hprevopen==hprevlow ) and hcurrentopen<hcurrentclose:
                    signal2 = "UP_6"
                else:
                    pass


#THREE BLACK CROWS


                if ((thirtyprevopen>thirtyprevclose and thirtyprevopen2>thirtyprevclose2 and thirtyprevopen3>thirtyprevclose3 and thirtyprevopen4<thirtyprevclose4 and thirtyprevopen5<thirtyprevopen5)  and  (thirtyprevhigh2-thirtyprevlow2>thirtyprevopen3 - thirtyprevclose3) and  thirtyprevlow2==thirtyprevclose2  and thirtyprevhigh-thirtyprevlow >=thirtyprevhigh2-thirtyprevlow2  and thirtyprevhigh==thirtyprevclose and thirtyprevopen==thirtyprevlow ) and thirtycurrentopen>thirtycurrentclose:
                    signal1 = "DOWN_6"
                else:
                    pass



                if ((hprevopen>hprevclose and hprevopen2>hprevclose2 and hprevopen3>hprevclose3 and hprevopen4<hprevclose4 and hprevopen5<hprevopen5)  and  (hprevhigh2-hprevlow2>hprevopen3 - hprevclose3) and  hprevlow2==hprevclose2  and hprevhigh-hprevlow >=hprevhigh2-hprevlow2  and hprevhigh==hprevclose and hprevopen==hprevlow ) and hcurrentopen>hcurrentclose:
                    signal2 = "DOWN_6"
                else:
                    pass


#PIERCING LINE

                if (thirtyprevopen2>thirtyprevclose2 and thirtyprevopen<thirtyprevclose  and thirtyprevopen<thirtyprevclose2 and thirtyprevopen==thirtyprevlow) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_7"
                else:
                    pass



                if (hprevopen2>hprevclose2 and hprevopen<hprevclose  and hprevopen<hprevclose2 and hprevopen==hprevlow) and hcurrentopen<hcurrentclose:
                    signal2 = "UP_7"
                else:
                    pass


#THREE LINE STRIKE
                if ((thirtyprevopen<thirtyprevclose and thirtyprevopen2>thirtyprevclose2 and thirtyprevopen3>thirtyprevclose3 and thirtyprevopen4>thirtyprevclose4 and thirtyprevopen5>thirtyprevopen5)  and thirtyprevopen==thirtyprevlow and thirtyprevclose> thirtyprevhigh4) and thirtycurrentopen<thirtycurrentclose:
                    signal1 = "UP_8"
                else:
                    pass


                if ((hprevopen<hprevclose and hprevopen2>hprevclose2 and hprevopen3>hprevclose3 and hprevopen4>hprevclose4 and hprevopen5>hprevopen5)  and hprevopen==hprevlow and hprevclose> hprevhigh4) and hcurrentopen<hcurrentclose:
                    signal2 = "UP_8"
                else:
                    pass


#TWO BLACK GAPING
                if (thirtyprevopen>thirtyprevclose and thirtyprevopen==thirtyprevhigh and thirtyprevopen2>thirtyprevclose2 and thirtyprevopen3>thirtyprevclose3 and thirtyprevopen4<thirtyprevclose4  and (thirtyprevhigh2-thirtyprevlow2)/(thirtyprevhigh3-thirtyprevlow3)>=1.5 and thirtyprevhigh2<thirtyprevlow3) and thirtycurrentopen>thirtycurrentclose :
                    signal1 = "DOWN_7"
                else:
                    pass

                if (hprevopen>hprevclose and hprevopen==hprevhigh and hprevopen2>hprevclose2 and hprevopen3>hprevclose3 and hprevopen4<hprevclose4  and (hprevhigh2-hprevlow2)/(hprevhigh3-hprevlow3)>=1.5 and hprevhigh2<hprevlow3) and hcurrentopen>hcurrentclose :
                    signal2 = "DOWN_7"
                else:
                    pass





                print market, signal1, signal2
#

                if (candles_signal_short=="UP_1" or candles_signal_short=="UP_2" or candles_signal_short=="UP_3" or candles_signal_short=="UP_4" or candles_signal_short=="UP_5" or candles_signal_short=="UP_6" or candles_signal_short=="UP_7" or candles_signal_short=="UP_8") and (signal1!="NONE" or currtime-candles_signal_time>3600) and last>candles_signal_price:
                    print market, "prediction was successfull"

                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_short=="UP_1" or candles_signal_short=="UP_2" or candles_signal_short=="UP_3" or candles_signal_short=="UP_4" or candles_signal_short=="UP_5" or candles_signal_short=="UP_6" or candles_signal_short=="UP_7" or candles_signal_short=="UP_8") and (signal1!="NONE" or currtime-candles_signal_time>3600) and last<candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                elif (candles_signal_short == "DOWN_1" or candles_signal_short == "DOWN_2" or candles_signal_short == "DOWN_3" or candles_signal_short == "DOWN_4" or candles_signal_short == "DOWN_5" or candles_signal_short == "DOWN_6" or candles_signal_short == "DOWN_7") and (
                        signal1 != "NONE" or currtime - candles_signal_time > 3600) and last < candles_signal_price:
                    print market, "prediction was successfull"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_short == "DOWN_1" or candles_signal_short == "DOWN_2" or candles_signal_short == "DOWN_3" or candles_signal_short == "DOWN_4" or candles_signal_short == "DOWN_5" or candles_signal_short == "DOWN_6" or candles_signal_short == "DOWN_7") and (
                        signal1 != "NONE" or currtime - candles_signal_time > 3600) and last > candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()



                elif (candles_signal_long == "UP_1" or candles_signal_long == "UP_2" or candles_signal_long == "UP_3" or candles_signal_long == "UP_4" or candles_signal_long == "UP_5" or candles_signal_long == "UP_6" or candles_signal_long == "UP_7" or candles_signal_long == "UP_8") and (
                        signal2 != "NONE" or currtime - candles_signal_time > 7200) and last > candles_signal_price:
                    print market, "prediction was successfull"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal2))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_long == "UP_1" or candles_signal_long == "UP_2" or candles_signal_long == "UP_3" or candles_signal_long == "UP_4" or candles_signal_long == "UP_5" or candles_signal_long == "UP_6" or candles_signal_long == "UP_7" or candles_signal_long == "UP_8") and (
                        signal2 != "NONE" or currtime - candles_signal_time > 7200) and last < candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal2))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_long == "DOWN_1" or candles_signal_long == "DOWN_2" or candles_signal_long == "DOWN_3" or candles_signal_long == "DOWN_4" or candles_signal_long == "DOWN_5" or candles_signal_long == "DOWN_6" or candles_signal_long == "DOWN_7") and (
                                signal2 != "NONE" or currtime - candles_signal_time > 7200) and last < candles_signal_price:
                    print market, "prediction was successfull"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal2))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_long == "DOWN_1" or candles_signal_long == "DOWN_2" or candles_signal_long == "DOWN_3" or candles_signal_long == "DOWN_4" or candles_signal_long == "DOWN_5" or candles_signal_long == "DOWN_6" or candles_signal_long == "DOWN_7") and (
                                signal2 != "NONE" or currtime - candles_signal_time > 7200) and last > candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("localhost", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal2))
                        cursor.execute(
                            "update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, signal2, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (signal1=="NONE" or signal2=="NONE") and currtime - candles_signal_time > 3600 :

                    try:
                        print market, "lets update new predictions"
                        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()

                        #printed = ('      '+ market + '   The HA_hour is  '  + '  and HAH is ' )
                        cursor.execute("update markets set candle_signal_short = %s, candle_signal_long =%s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",(signal1, signal2, currtime, last, market))

                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                else:
                    pass







        except:
            continue



def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled =1 and market = '%s'" % market)
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
