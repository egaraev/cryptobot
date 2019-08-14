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


TICK_INTERVAL = 600  # seconds




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
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                #active_order= status_orders(market, 4)
                last = float(summary['Last'])  # last price
                serf = percent_serf(market)
                #print last
                candles_signal_short = str(heikin_ashi(market, 29))
                candles_signal_long = str(heikin_ashi(market, 30))
                candles_signal_price = float(heikin_ashi(market, 32))
                candles_signal_time=int(heikin_ashi(market, 31))
                
                
                print "Gather 5hour HA candle info for ", market

                ############
                hourcandles = get_candles(market, 'hour')['result'][-25:]
                hourcurrentlow = float(hourcandles[24]['L'])*100000
                hourcurrenthigh = float(hourcandles[24]['H'])*100000
                hourcurrentopen = float(hourcandles[24]['O'])*100000
                hourcurrentclose = float(hourcandles[24]['C'])*100000

                hourprevlow = float(hourcandles[23]['L'])*100000
                hourprevhigh = float(hourcandles[23]['H'])*100000
                hourprevopen = float(hourcandles[23]['O'])*100000
                hourprevclose = float(hourcandles[23]['C'])*100000

                hourprevlow2 = float(hourcandles[22]['L'])*100000
                hourprevhigh2 = float(hourcandles[22]['H'])*100000
                hourprevopen2 = float(hourcandles[22]['O'])*100000
                hourprevclose2 = float(hourcandles[22]['C'])*100000

                hourprevlow3 = float(hourcandles[21]['L'])*100000
                hourprevhigh3 = float(hourcandles[21]['H'])*100000
                #hourprevopen3 = float(hourcandles[21]['O'])*100000
                #hourprevclose3 = float(hourcandles[21]['C'])*100000


                hourprevlow4 = float(hourcandles[20]['L'])*100000
                hourprevhigh4 = float(hourcandles[20]['H'])*100000
                hourprevopen4 = float(hourcandles[20]['O'])*100000
                #hourprevclose4 = float(hourcandles[20]['C'])*100000


                hourprevlow5 = float(hourcandles[19]['L'])*100000
                hourprevhigh5 = float(hourcandles[19]['H'])*100000
                #hourprevopen5 = float(hourcandles[19]['O'])*100000
                hourprevclose5 = float(hourcandles[19]['C'])*100000



                hourprevlow6 = float(hourcandles[18]['L'])*100000
                hourprevhigh6 = float(hourcandles[18]['H'])*100000
                #hourprevopen6 = float(hourcandles[18]['O'])*100000
                #hourprevclose6 = float(hourcandles[18]['C'])*100000


                hourprevlow7 = float(hourcandles[17]['L'])*100000
                hourprevhigh7 = float(hourcandles[17]['H'])*100000
                #hourprevopen7 = float(hourcandles[17]['O'])*100000
                #hourprevclose7 = float(hourcandles[17]['C'])*100000


                hourprevlow8 = float(hourcandles[16]['L'])*100000
                hourprevhigh8 = float(hourcandles[16]['H'])*100000
                #hourprevopen8 = float(hourcandles[16]['O'])*100000
                #hourprevclose8 = float(hourcandles[16]['C'])*100000


                hourprevlow9 = float(hourcandles[15]['L'])*100000
                hourprevhigh9 = float(hourcandles[15]['H'])*100000
                hourprevopen9 = float(hourcandles[15]['O'])*100000
                #hourprevclose9 = float(hourcandles[15]['C'])*100000

                hourprevlow10 = float(hourcandles[14]['L'])*100000
                hourprevhigh10 = float(hourcandles[14]['H'])*100000
                #hourprevopen10 = float(hourcandles[14]['O'])*100000
                hourprevclose10 = float(hourcandles[14]['C'])*100000


                hourprevlow11 = float(hourcandles[13]['L'])*100000
                hourprevhigh11 = float(hourcandles[13]['H'])*100000
                #hourprevopen11 = float(hourcandles[13]['O'])*100000
                #hourprevclose11 = float(hourcandles[13]['C'])*100000


                hourprevlow12 = float(hourcandles[12]['L'])*100000
                hourprevhigh12 = float(hourcandles[12]['H'])*100000
                #hourprevopen12 = float(hourcandles[12]['O'])*100000
                #hourprevclose12 = float(hourcandles[12]['C'])*100000



                hourprevlow13 = float(hourcandles[11]['L'])*100000
                hourprevhigh13 = float(hourcandles[11]['H'])*100000
                #hourprevopen13 = float(hourcandles[11]['O'])*100000
                #hourprevclose13 = float(hourcandles[11]['C'])*100000


                hourprevlow14 = float(hourcandles[10]['L'])*100000
                hourprevhigh14 = float(hourcandles[10]['H'])*100000
                hourprevopen14 = float(hourcandles[10]['O'])*100000
                #hourprevclose14 = float(hourcandles[10]['C'])*100000



                hourprevlow15 = float(hourcandles[9]['L'])*100000
                hourprevhigh15 = float(hourcandles[9]['H'])*100000
                #hourprevopen15 = float(hourcandles[9]['O'])*100000
                hourprevclose15 = float(hourcandles[9]['C'])*100000


                hourprevlow16 = float(hourcandles[8]['L'])*100000
                hourprevhigh16 = float(hourcandles[8]['H'])*100000
                #hourprevopen16 = float(hourcandles[8]['O'])*100000
                #hourprevclose16 = float(hourcandles[8]['C'])*100000


                hourprevlow17 = float(hourcandles[7]['L'])*100000
                hourprevhigh17 = float(hourcandles[7]['H'])*100000
                #hourprevopen17 = float(hourcandles[7]['O'])*100000
                #hourprevclose17 = float(hourcandles[7]['C'])*100000



                hourprevlow18 = float(hourcandles[6]['L'])*100000
                hourprevhigh18 = float(hourcandles[6]['H'])*100000
                #hourprevopen18 = float(hourcandles[6]['O'])*100000
                #hourprevclose18 = float(hourcandles[6]['C'])*100000


                hourprevlow19 = float(hourcandles[5]['L'])*100000
                hourprevhigh19 = float(hourcandles[5]['H'])*100000
                hourprevopen19 = float(hourcandles[5]['O'])*100000
                #hourprevclose19 = float(hourcandles[5]['C'])*100000



                hourprevlow20 = float(hourcandles[4]['L'])*100000
                hourprevhigh20 = float(hourcandles[4]['H'])*100000
                #hourprevopen20 = float(hourcandles[4]['O'])*100000
                hourprevclose20 = float(hourcandles[4]['C'])*100000



                hourprevlow21 = float(hourcandles[3]['L'])*100000
                hourprevhigh21 = float(hourcandles[3]['H'])*100000
                #hourprevopen21 = float(hourcandles[3]['O'])*100000
                #hourprevclose21 = float(hourcandles[3]['C'])*100000



                hourprevlow22 = float(hourcandles[2]['L'])*100000
                hourprevhigh22 = float(hourcandles[2]['H'])*100000
                #hourprevopen22 = float(hourcandles[2]['O'])*100000
                #hourprevclose22 = float(hourcandles[2]['C'])*100000


                hourprevlow23 = float(hourcandles[1]['L'])*100000
                hourprevhigh23 = float(hourcandles[1]['H'])*100000
                #hourprevopen23 = float(hourcandles[1]['O'])*100000
                #hourprevclose23 = float(hourcandles[1]['C'])*100000


                hourprevlow24 = float(hourcandles[0]['L'])*100000
                hourprevhigh24 = float(hourcandles[0]['H'])*100000
                hourprevopen24 = float(hourcandles[0]['O'])*100000
                #hourprevclose24 = float(hourcandles[0]['C'])*100000

                               ###########

                fivehourcurrentlow = min(hourcurrentlow, hourprevlow, hourprevlow2, hourprevlow3, hourprevlow4)
                fivehourcurrenthigh = max(hourcurrenthigh, hourprevhigh, hourprevhigh2, hourprevhigh3, hourprevhigh4)
                fivehourcurrentopen = hourprevopen4
                fivehourcurrentclose = hourcurrentclose

                fivehourprevlow = min(hourprevlow5, hourprevlow6, hourprevlow7, hourprevlow8, hourprevlow9)
                fivehourprevhigh = max(hourprevhigh5,hourprevhigh6, hourprevhigh7, hourprevhigh8, hourprevhigh9)
                fivehourprevopen = hourprevopen9
                fivehourprevclose = hourprevclose5
                
                fivehourprevlow2 = min(hourprevlow10, hourprevlow11, hourprevlow12, hourprevlow13, hourprevlow14)
                fivehourprevhigh2 = max(hourprevhigh10,hourprevhigh11, hourprevhigh12, hourprevhigh13, hourprevhigh14)
                fivehourprevopen2 = hourprevopen14
                fivehourprevclose2 = hourprevclose10


                fivehourprevlow3 = min(hourprevlow15, hourprevlow16, hourprevlow17, hourprevlow18, hourprevlow19)
                fivehourprevhigh3 = max(hourprevhigh15,hourprevhigh16, hourprevhigh17, hourprevhigh18, hourprevhigh19)
                fivehourprevopen3 = hourprevopen19
                fivehourprevclose3 = hourprevclose15


                fivehourprevlow4 = min(hourprevlow20, hourprevlow21, hourprevlow22, hourprevlow23, hourprevlow24)
                fivehourprevhigh4 = max(hourprevhigh20,hourprevhigh21, hourprevhigh22, hourprevhigh23, hourprevhigh24)
                fivehourprevopen4 = hourprevopen24
                fivehourprevclose4 = hourprevclose20





                print "Starting candle patterns check for ", market
#HAMMER
                signal1="NONE"


                if (fivehourprevhigh==fivehourprevclose) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) >= 2.5)  and (fivehourprevopen - fivehourprevclose !=0) and (fivehourprevopen2 > fivehourprevclose2) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1="Up-1"
                else:
                    pass



#HANGING MAN
                if (fivehourprevhigh==fivehourprevopen) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) >= 2.5)  and (fivehourprevopen - fivehourprevclose !=0) and (fivehourprevopen2 < fivehourprevclose2) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1="Down-1"
                else:
                    pass



#INVERTED HAMMER
                if (fivehourprevopen==fivehourprevlow) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) >= 2.5)  and (fivehourprevopen - fivehourprevclose !=0) and (fivehourprevopen2 > fivehourprevclose2) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1="Up-2"
                else:
                    pass



#SHOOTING STAR

                if (fivehourprevclose==fivehourprevlow) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) >= 2.5)  and (fivehourprevopen - fivehourprevclose !=0) and (fivehourprevopen2 < fivehourprevclose2) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1="Down-2"
                else:
                    pass





#BULLISH ENGULFING

                if ((fivehourprevopen2 > fivehourprevclose2) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevhigh2 - fivehourprevlow2) >= 1.5) and (fivehourprevhigh2 - fivehourprevlow2 !=0) and  (fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) <= 2) and (fivehourprevopen < fivehourprevclose) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-3"
                else:
                    pass




#BEARISH ENGULFING

                if ((fivehourprevopen2 < fivehourprevclose2) and ((fivehourprevhigh - fivehourprevlow) / (fivehourprevhigh2 - fivehourprevlow2) >= 1.5) and (fivehourprevhigh2 - fivehourprevlow2 !=0) and  (fivehourprevhigh - fivehourprevlow) / (fivehourprevopen - fivehourprevclose) <= 2)  and (fivehourprevopen > fivehourprevclose) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1 = "Down-3"
                else:
                    pass




#TWEEZER BOTTOMS

                if (fivehourprevopen2>fivehourprevclose2 and fivehourprevopen3>fivehourprevclose3 and fivehourprevopen4>fivehourprevclose4) and (fivehourprevopen<fivehourprevclose) and fivehourprevlow==fivehourprevlow2  and ((fivehourprevhigh - fivehourprevlow) - (fivehourprevopen - fivehourprevclose) == (fivehourprevhigh - fivehourprevlow) - (fivehourprevclose - fivehourprevopen) and fivehourprevopen2==fivehourprevhigh2 and fivehourprevhigh==fivehourprevclose) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-4"
                else:
                    pass





# TWEEZER TOPS


                if (fivehourprevopen2<fivehourprevclose2 and fivehourprevopen3<fivehourprevclose3 and fivehourprevopen4<fivehourprevclose4) and (fivehourprevopen>fivehourprevclose) and  fivehourprevhigh==fivehourprevhigh2 and ((fivehourprevhigh - fivehourprevlow) - (fivehourprevopen - fivehourprevclose) == (fivehourprevhigh - fivehourprevlow) - (fivehourprevclose - fivehourprevopen) and fivehourprevopen==fivehourprevhigh and fivehourprevhigh2==fivehourprevclose2) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1 = "Down-4"
                else:
                    pass




#EVENING STAR
                                                # upper trend                                                                           #current candle is Down                             #short candle or doji
                if (fivehourprevopen3<fivehourprevclose3 and fivehourprevopen4<fivehourprevclose4 and fivehourprevopen5<fivehourprevclose5) and (fivehourprevopen>fivehourprevclose) and   (fivehourprevopen2==fivehourprevclose2 or ((fivehourprevhigh2 - fivehourprevlow2) / numpy.abs(fivehourprevclose2 - fivehourprevopen2) >= 4 and (fivehourprevclose2 - fivehourprevopen2 !=0))) and (fivehourprevopen-fivehourprevclose >=(fivehourprevclose3-fivehourprevopen3)/2) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1 = "Down-5"
                else:
                    pass




#MORNING STAR

                if (fivehourprevopen3>fivehourprevclose3 and fivehourprevopen4>fivehourprevclose4 and fivehourprevopen5>fivehourprevclose5) and (fivehourprevopen<fivehourprevclose) and   (fivehourprevopen2==fivehourprevclose2 or ((fivehourprevhigh2 - fivehourprevlow2) / numpy.abs(fivehourprevclose2 - fivehourprevopen2) >= 4 and (fivehourprevclose2 - fivehourprevopen2 !=0))) and (fivehourprevclose - fivehourprevopen >=(fivehourprevopen3 - fivehourprevclose3)/2) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-5"
                else:
                    pass




#THREE WHITE SOLDIERS

                if ((fivehourprevopen<fivehourprevclose and fivehourprevopen2<fivehourprevclose2 and fivehourprevopen3<fivehourprevclose3 and fivehourprevopen4>fivehourprevclose4 and fivehourprevopen5>fivehourprevopen5)  and  (fivehourprevhigh2-fivehourprevlow2>fivehourprevclose3-fivehourprevopen3) and  fivehourprevhigh2==fivehourprevclose2  and fivehourprevhigh-fivehourprevlow >=fivehourprevhigh2-fivehourprevlow2  and fivehourprevhigh==fivehourprevclose and fivehourprevopen==fivehourprevlow ) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-6"
                else:
                    pass




#THREE BLACK CROWS


                if ((fivehourprevopen>fivehourprevclose and fivehourprevopen2>fivehourprevclose2 and fivehourprevopen3>fivehourprevclose3 and fivehourprevopen4<fivehourprevclose4 and fivehourprevopen5<fivehourprevopen5)  and  (fivehourprevhigh2-fivehourprevlow2>fivehourprevopen3 - fivehourprevclose3) and  fivehourprevlow2==fivehourprevclose2  and fivehourprevhigh-fivehourprevlow >=fivehourprevhigh2-fivehourprevlow2  and fivehourprevhigh==fivehourprevclose and fivehourprevopen==fivehourprevlow ) and fivehourcurrentopen>fivehourcurrentclose:
                    signal1 = "Down-6"
                else:
                    pass



#PIERCING LINE

                if (fivehourprevopen2>fivehourprevclose2 and fivehourprevopen<fivehourprevclose  and fivehourprevopen<fivehourprevclose2 and fivehourprevopen==fivehourprevlow) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-7"
                else:
                    pass




#THREE LINE STRIKE
                if ((fivehourprevopen<fivehourprevclose and fivehourprevopen2>fivehourprevclose2 and fivehourprevopen3>fivehourprevclose3 and fivehourprevopen4>fivehourprevclose4 and fivehourprevopen5>fivehourprevopen5)  and fivehourprevopen==fivehourprevlow and fivehourprevclose> fivehourprevhigh4) and fivehourcurrentopen<fivehourcurrentclose:
                    signal1 = "Up-8"
                else:
                    pass


#TWO BLACK GAPING
                if (fivehourprevopen>fivehourprevclose and fivehourprevopen==fivehourprevhigh and fivehourprevopen2>fivehourprevclose2 and fivehourprevopen3>fivehourprevclose3 and fivehourprevopen4<fivehourprevclose4  and (fivehourprevhigh2-fivehourprevlow2)/(fivehourprevhigh3-fivehourprevlow3)>=1.5 and fivehourprevhigh2<fivehourprevlow3) and fivehourcurrentopen>fivehourcurrentclose :
                    signal1 = "Down-7"
                else:
                    pass





                print market, signal1
                if signal1=="Down-1" or signal1=="Down-2" or signal1=="Down-3"  or signal1=="Down-4" or signal1=="Down-5"  or signal1=="Down-6" or signal1=="Down-7"  or signal1=="Up-1"  or signal1=="Up-2" or signal1=="Up-3" or signal1=="Up-4" or signal1=="Up-5" or signal1=="Up-6" or signal1=="Up-7" or signal1=="Up-8":
                    try:
                        printed=('      ' + str(market) + '  has candle signal '+signal1)
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        if status_orders(market, 4)==1:
                            cursor.execute(
                                    'insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (market,  str(serf)+ ' fivehour: ' + str(signal1), currtime, status_orders(market, 0)))
                        else:
                            pass
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
#

                if (candles_signal_short=="Up-1" or candles_signal_short=="Up-2" or candles_signal_short=="Up-3" or candles_signal_short=="Up-4" or candles_signal_short=="Up-5" or candles_signal_short=="Up-6" or candles_signal_short=="Up-7" or candles_signal_short=="Up-8") and (signal1!="NONE" or currtime-candles_signal_time>18000) and last>candles_signal_price:
                    print market, "prediction was successfull"

                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_short=="Up-1" or candles_signal_short=="Up-2" or candles_signal_short=="Up-3" or candles_signal_short=="Up-4" or candles_signal_short=="Up-5" or candles_signal_short=="Up-6" or candles_signal_short=="Up-7" or candles_signal_short=="Up-8") and (signal1!="NONE" or currtime-candles_signal_time>18000) and last<candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1,  currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                elif (candles_signal_short=="Down-1" or candles_signal_short=="Down-2" or candles_signal_short=="Down-3" or candles_signal_short=="Down-4" or candles_signal_short=="Down-5" or candles_signal_short=="Down-6" or candles_signal_short=="Down-7") and (
                        signal1 != "NONE" or currtime - candles_signal_time > 18000) and last < candles_signal_price:
                    print market, "prediction was successfull"
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 1, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s,   candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                elif (candles_signal_short=="Down-1" or candles_signal_short=="Down-2" or candles_signal_short=="Down-3" or candles_signal_short=="Down-4" or candles_signal_short=="Down-5" or candles_signal_short=="Down-6" or candles_signal_short=="Down-7") and (
                        signal1 != "NONE" or currtime - candles_signal_time > 18000) and last > candles_signal_price:
                    print market, "prediction was failed"
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456","cryptodb")
                        cursor = db.cursor()
                        cursor.execute('insert into candlepredict(market, result, signals) values("%s", "%s", "%s")' % (market, 0, signal1))
                        cursor.execute(
                            "update markets set candle_signal_short = %s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",
                            (signal1, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                elif (signal1=="NONE") and currtime - candles_signal_time > 18000 :

                    try:
                        print market, "lets update new predictions"
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()

                        #printed = ('      '+ market + '   The HA_hour is  '  + '  and HAH is ' )
                        cursor.execute("update markets set candle_signal_short = %s,  candle_signal_time=%s, candle_signal_price=%s  where market = %s",(signal1, currtime, last, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


                elif (signal1=="Down-1"  or signal1=="Down-2" or signal1=="Down-3"  or signal1=="Down-4" or signal1=="Down-5"  or signal1=="Down-6"  or signal1=="Down-7" or signal1=="Up-1" or signal1=="Up-2"  or signal1=="Up-3" or signal1=="Up-4" or signal1=="Up-5"  or signal1=="Up-6"  or signal1=="Up-7" or signal1=="Up-8") :

                    if signal1!="NONE":

                        try:
                            print market, "lets update new predictions"
                            db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                            cursor = db.cursor()

                            #printed = ('      '+ market + '   The HA_hour is  '  + '  and HAH is ' )
                            cursor.execute("update markets set candle_signal_short = %s,  candle_signal_price=%s  where market = %s",(signal1, last, market))

                            db.commit()
                        except MySQLdb.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)
                        finally:
                            db.close()

                    else:
                        pass


                else:
                    pass







        except:
            continue




def status_orders(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
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
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False

def status_orders(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0



def percent_serf(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0



def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
