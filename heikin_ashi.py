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

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                serf = percent_serf(market)
                last = float(summary['Last'])  # last price
                bought_quantity_sql = float(status_orders(market, 2))
                HAD_trend = heikin_ashi(market, 18)
                averagecandlesize = float(heikin_ashi(market, 44))

                hourcandles=0
                fivehourcurrentlow=0
                fivehourcurrenthigh=0
                fivehourcurrentopen=0
                fivehourcurrentclose=0
                fivehourprevlow=0
                fivehourprevhigh=0
                fivehourprevopen=0
                fivehourprevclose=0
                fivehourprevlow2=0
                fivehourprevhigh2=0
                fivehourprevopen2=0
                fivehourprevclose2=0
                fivehourprevlow3 = 0
                fivehourprevhigh3 = 0
                fivehourprevopen3 = 0
                fivehourprevclose3 = 0
                HA_PREV_Close4 = 0
                HA_PREV_Open4 = 0
                HA_PREV_Low4 = 0
                HA_PREV_High4 = 0
                HA_PREV_Close3 = 0
                HA_PREV_Open3 = 0
                elements3 = 0
                HA_PREV_High3 = 0
                HA_PREV_Low3 = 0
                HA_PREV_Close2 =0
                HA_PREV_Open2 = 0
                elements2 = 0
                HA_PREV_High2 = 0
                HA_PREV_Low2 = 0
                HA_PREV_Close =0
                HA_PREV_Open =0
                elements1 = 0
                HA_PREV_High = 0
                HA_PREV_Low = 0
                HA_Close = 0
                HA_Open = 0
                elements0 = 0
                HA_High = 0
                HA_Low = 0
                hourcurrentlow = 0
                hourcurrenthigh = 0
                hourcurrentopen = 0
                hourcurrentclose = 0
                hourprevlow = 0
                hourprevhigh = 0
                hourprevopen = 0
                hourprevclose = 0
                hourprevlow2 = 0
                hourprevhigh2 = 0
                hourprevopen2 = 0
                hourprevclose2 = 0
                hourprevlow3 = 0
                hourprevhigh3 = 0



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


                hour_candle = 'NONE'
                prevhour_candle = 'NONE'
                prevhour2_candle = 'NONE'

                if last*100000 > hourcurrentopen:
                    hour_candle = 'U'
                else:
                    hour_candle = 'D'

                if hourprevclose > hourprevopen:
                    prevhour_candle = 'U'
                else:
                    prevhour_candle = 'D'

                if hourprevclose2 > hourprevopen2:
                    prevhour2_candle = 'U'
                else:
                    prevhour2_candle = 'D'


                fivehour_candle = 'NONE'
                fiveprevhour_candle = 'NONE'
                fiveprevhour2_candle = 'NONE'

                if last*100000 > fivehourcurrentopen:
                    fivehour_candle = 'U'
                else:
                    fivehour_candle = 'D'

                if fivehourprevclose > fivehourprevopen:
                    fiveprevhour_candle = 'U'
                else:
                    fiveprevhour_candle = 'D'

                if fivehourprevclose2 > fivehourprevopen2:
                    fiveprevhour2_candle = 'U'
                else:
                    fiveprevhour2_candle = 'D'


                print "Computing HA candles for ", market

                HA_PREV_Close4 = (fivehourprevopen4 + fivehourprevhigh4 + fivehourprevlow4 + fivehourprevclose4) / 4
                HA_PREV_Open4 = (fivehourprevopen4 + fivehourprevclose4) / 2
                HA_PREV_Low4 = fivehourprevlow4
                HA_PREV_High4 = fivehourprevhigh4


                HA_PREV_Close3 = (fivehourprevopen3 + fivehourprevhigh3 + fivehourprevlow3 + fivehourprevclose3) / 4
                HA_PREV_Open3 = (HA_PREV_Open4 + HA_PREV_Close4) / 2
                elements3 = numpy.array([fivehourprevhigh3, fivehourprevlow3, HA_PREV_Open4, HA_PREV_Close4])
                HA_PREV_High3 = elements3.max(0)
                HA_PREV_Low3 = elements3.min(0)

                HA_PREV_Close2 = (fivehourprevopen2 + fivehourprevhigh2 + fivehourprevlow2 + fivehourprevclose2) / 4
                HA_PREV_Open2 = (HA_PREV_Open3 + HA_PREV_Close3) / 2
                elements2 = numpy.array([fivehourprevhigh2, fivehourprevlow2, HA_PREV_Open3, HA_PREV_Close3])
                HA_PREV_High2 = elements2.max(0)
                HA_PREV_Low2 = elements2.min(0)

                HA_PREV_Close = (fivehourprevopen + fivehourprevhigh + fivehourprevlow + fivehourprevclose) / 4
                HA_PREV_Open = (HA_PREV_Open2 + HA_PREV_Close2) / 2
                elements1 = numpy.array([fivehourprevhigh, fivehourprevlow, HA_PREV_Open, HA_PREV_Close])
                HA_PREV_High = elements1.max(0)
                HA_PREV_Low = elements1.min(0)

                HA_Close = (fivehourcurrentopen + fivehourcurrenthigh + fivehourcurrentlow + fivehourcurrentclose) / 4
                HA_Open = (HA_PREV_Open + HA_PREV_Close) / 2
                elements0 = numpy.array([fivehourcurrenthigh, fivehourcurrentlow, HA_Open, HA_Close])
                HA_High = elements0.max(0)
                HA_Low = elements0.min(0)






                HAH_PREV_Close2 = (hourprevopen2 + hourprevhigh2 + hourprevlow2 + hourprevclose2) / 4
                HAH_PREV_Open2 = (hourprevopen2 + hourprevclose2) / 2
                HAH_PREV_Low2 = hourprevlow2
                HAH_PREV_High2 = hourprevhigh2

                HAH_PREV_Close = (hourprevopen + hourprevhigh + hourprevlow + hourprevclose) / 4
                HAH_PREV_Open = (HAH_PREV_Open2 + HAH_PREV_Close2) / 2
                elements1 = numpy.array([hourprevhigh, hourprevlow, HAH_PREV_Open, HAH_PREV_Close])
                HAH_PREV_High = elements1.max(0)
                HAH_PREV_Low = elements1.min(0)

                HAH_Close = (hourcurrentopen + hourcurrenthigh + hourcurrentlow + hourcurrentclose) / 4
                HAH_Open = (HAH_PREV_Open + HAH_PREV_Close) / 2
                elements0 = numpy.array([hourcurrenthigh, hourcurrentlow, HAH_Open, HAH_Close])
                HAH_High = elements0.max(0)
                HAH_Low = elements0.min(0)




                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
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
                
                ha_trend = "NONE"
                hah_trend = "NONE"
                

                HAD_trend = heikin_ashi(market, 18)
                had_trend = heikin_ashi(market, 47)

                print "Generting direction info for ", market

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



                if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longermax and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down2))  and fivehour_candle=='D' and fiveprevhour_candle=='D':
                    HA_trend = "DOWN"

                if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer and ha_direction_up_longermax) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up2)) and fivehour_candle=='U' and fiveprevhour_candle=='U':
                    HA_trend = "UP"

                if ((ha_direction_up_short2 and ha_direction_spin1 and ha_direction_up0) or (ha_direction_down_short2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_down_short1 and ha_direction_spin0) or (ha_direction_down_long_2 and ha_direction_down_short1 and ha_direction_up_long_0) or (ha_direction_down_long_2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_up_long_0 and ha_direction_up1 and ha_direction_up_longer) or (ha_direction_down_long_2 and ha_direction_down_smaller1 and ha_direction_up0) or (ha_direction_down_long_2 and ha_direction_down_short1 and  ha_direction_up_long_0) or (ha_direction_down_longermax and ha_direction_up_short0) and ha_direction_down1 and ha_direction_down2) and ha_direction_down1 and ha_direction_down2 and fivehour_candle=='U':
                    HA_trend = "Revers-UP"

                if ((ha_direction_down_short2 and ha_direction_spin1 and ha_direction_down0) or (ha_direction_up_short2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_up_short1 and ha_direction_spin0) or (ha_direction_up_long_2 and ha_direction_up_short1 and ha_direction_down_long_0) or (ha_direction_up_long_2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_down_long_0 and ha_direction_down1 and ha_direction_down_longer) or (ha_direction_up_long_2 and ha_direction_up_smaller1 and ha_direction_down0) or (ha_direction_up_long_2 and ha_direction_up_short1 and  ha_direction_down_long_0) or (ha_direction_up_longermax and ha_direction_down_short0) and ha_direction_up1 and ha_direction_up2) and ha_direction_up1 and ha_direction_up2 and fivehour_candle=='D':
                    HA_trend = "Revers-DOWN"

                if  HA_trend != "Revers-DOWN" and   HA_trend != "Revers-UP" and  HA_trend != "DOWN" and HA_trend != "UP":
                    HA_trend = "STABLE"


                    
                    
                if (ha_direction_spin0):
                    Ha_current_candle = "ha_direction_spin0"
                    
                if (ha_direction_down_short0):
                    Ha_current_candle = "ha_direction_down_short0"                    
                    
                   
                if (ha_direction_down_long_0):
                    Ha_current_candle = "ha_direction_down_long_0"                    
                    
                if (ha_direction_down0):
                    Ha_current_candle = "ha_direction_down0"

                if (ha_direction_up_short0):
                    Ha_current_candle = "ha_direction_up_short0"                    

                if (ha_direction_up_long_0):
                    Ha_current_candle = "ha_direction_up_long_0"

                    
                if (ha_direction_up0):
                    Ha_current_candle = "ha_direction_up0"




                if (ha_direction_spin1):
                    Ha_previous_candle = "ha_direction_spin1"
                    
                if (ha_direction_down_short1):
                    Ha_previous_candle = "ha_direction_down_short1"                    
                    
                if (ha_direction_down_long_1):
                    Ha_previous_candle = "ha_direction_down_long_1" 

                if (ha_direction_down1):
                    Ha_previous_candle = "ha_direction_down1"

                if (ha_direction_up_short1):
                    Ha_previous_candle = "ha_direction_up_short1"                     
                    
                if (ha_direction_up_long_1):
                    Ha_previous_candle = "ha_direction_up_long_1"

                if (ha_direction_up1):
                    Ha_previous_candle = "ha_direction_up1"



                print Ha_current_candle, Ha_previous_candle










                    
                if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longermax and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down2)):
                    ha_trend = "DOWN"

                if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer and ha_direction_up_longermax) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up2)):
                    ha_trend = "UP"

                if ((ha_direction_up_short2 and ha_direction_spin1 and ha_direction_up0) or (ha_direction_down_short2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_down_short1 and ha_direction_spin0) or (ha_direction_down_long_2 and ha_direction_down_short1 and ha_direction_up_long_0) or (ha_direction_down_long_2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_up_long_0 and ha_direction_up1 and ha_direction_up_longer) or (ha_direction_down_long_2 and ha_direction_down_smaller1 and ha_direction_up0) or (ha_direction_down_long_2 and ha_direction_down_short1 and  ha_direction_up_long_0) or (ha_direction_down_longermax and ha_direction_up_short0) and ha_direction_down1 and ha_direction_down2) and ha_direction_down1 and ha_direction_down2:
                    ha_trend = "Revers-UP"

                if ((ha_direction_down_short2 and ha_direction_spin1 and ha_direction_down0) or (ha_direction_up_short2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_up_short1 and ha_direction_spin0) or (ha_direction_up_long_2 and ha_direction_up_short1 and ha_direction_down_long_0) or (ha_direction_up_long_2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_down_long_0 and ha_direction_down1 and ha_direction_down_longer) or (ha_direction_up_long_2 and ha_direction_up_smaller1 and ha_direction_down0) or (ha_direction_up_long_2 and ha_direction_up_short1 and  ha_direction_down_long_0) or (ha_direction_up_longermax and ha_direction_down_short0) and ha_direction_up1 and ha_direction_up2) and ha_direction_up1 and ha_direction_up2:
                    ha_trend = "Revers-DOWN"

                if  ha_trend != "Revers-DOWN" and   ha_trend != "Revers-UP" and  ha_trend != "DOWN" and ha_trend != "UP":
                    ha_trend = "STABLE"



                if (((hah_direction_down_long_0 and hah_direction_down0) or (hah_direction_down_long_0 and hah_direction_down_long_1 and hah_direction_down0) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longer) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longermax and hah_direction_down_longer) and hah_direction_down0) or (hah_direction_down0 and hah_direction_down1 and hah_direction_down2)) and hour_candle=='D' and prevhour_candle=='D':
                    HAH_trend = "DOWN"

                if (((hah_direction_up_long_0 and hah_direction_up0) or (hah_direction_up_long_0 and hah_direction_up_long_1 and hah_direction_up0) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer and hah_direction_up_longermax) and hah_direction_up0) or (hah_direction_up0 and hah_direction_up1 and hah_direction_up2)) and hour_candle=='U' and prevhour_candle=='U':
                    HAH_trend = "UP"

                if ((hah_direction_up_short2 and hah_direction_spin1 and hah_direction_up0) or (hah_direction_down_short2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_down_short1 and hah_direction_spin0) or (hah_direction_down_long_2 and hah_direction_down_short1 and hah_direction_up_long_0) or (hah_direction_down_long_2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_up_long_0 and hah_direction_up1 and hah_direction_up_longer) or (hah_direction_down_long_2 and hah_direction_down_smaller1 and hah_direction_up0) or (hah_direction_down_long_2 and hah_direction_down_short1 and  hah_direction_up_long_0) or (hah_direction_down_longermax and hah_direction_up_short0) and hah_direction_down1 and hah_direction_down2) and hour_candle=='U':
                    HAH_trend = "Revers-UP"

                if ((hah_direction_down_short2 and hah_direction_spin1 and hah_direction_down0) or (hah_direction_up_short2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_up_short1 and hah_direction_spin0) or (hah_direction_up_long_2 and hah_direction_up_short1 and hah_direction_down_long_0) or (hah_direction_up_long_2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_down_long_0 and hah_direction_down1 and hah_direction_down_longer) or (hah_direction_up_long_2 and hah_direction_up_smaller1 and hah_direction_down0) or (hah_direction_up_long_2 and hah_direction_up_short1 and  hah_direction_down_long_0) or (hah_direction_up_longermax and hah_direction_down_short0) and hah_direction_up1 and hah_direction_up2) and hour_candle=='D':
                    HAH_trend = "Revers-DOWN"

                if  HAH_trend != "Revers-DOWN" and   HAH_trend != "Revers-UP" and  HAH_trend != "DOWN" and HAH_trend != "UP":
                    HAH_trend = "STABLE"

                    
                    
                if (((hah_direction_down_long_0 and hah_direction_down0) or (hah_direction_down_long_0 and hah_direction_down_long_1 and hah_direction_down0) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longer) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longermax and hah_direction_down_longer) and hah_direction_down0) or (hah_direction_down0 and hah_direction_down1 and hah_direction_down2)):
                    hah_trend = "DOWN"

                if (((hah_direction_up_long_0 and hah_direction_up0) or (hah_direction_up_long_0 and hah_direction_up_long_1 and hah_direction_up0) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer and hah_direction_up_longermax) and hah_direction_up0) or (hah_direction_up0 and hah_direction_up1 and hah_direction_up2)):
                    hah_trend = "UP"

                if ((hah_direction_up_short2 and hah_direction_spin1 and hah_direction_up0) or (hah_direction_down_short2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_down_short1 and hah_direction_spin0) or (hah_direction_down_long_2 and hah_direction_down_short1 and hah_direction_up_long_0) or (hah_direction_down_long_2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_up_long_0 and hah_direction_up1 and hah_direction_up_longer) or (hah_direction_down_long_2 and hah_direction_down_smaller1 and hah_direction_up0) or (hah_direction_down_long_2 and hah_direction_down_short1 and  hah_direction_up_long_0) or (hah_direction_down_longermax and hah_direction_up_short0) and hah_direction_down1 and hah_direction_down2):
                    hah_trend = "Revers-UP"

                if ((hah_direction_down_short2 and hah_direction_spin1 and hah_direction_down0) or (hah_direction_up_short2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_up_short1 and hah_direction_spin0) or (hah_direction_up_long_2 and hah_direction_up_short1 and hah_direction_down_long_0) or (hah_direction_up_long_2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_down_long_0 and hah_direction_down1 and hah_direction_down_longer) or (hah_direction_up_long_2 and hah_direction_up_smaller1 and hah_direction_down0) or (hah_direction_up_long_2 and hah_direction_up_short1 and  hah_direction_down_long_0) or (hah_direction_up_longermax and hah_direction_down_short0) and hah_direction_up1 and hah_direction_up2):
                    hah_trend = "Revers-DOWN"

                if  hah_trend != "Revers-DOWN" and   hah_trend != "Revers-UP" and  hah_trend != "DOWN" and hah_trend != "UP":
                    hah_trend = "STABLE"
                    
                    


                print market, HA_trend, HAH_trend, fiveprevhour2_candle, fiveprevhour_candle, fivehour_candle,  prevhour2_candle, prevhour_candle, hour_candle,


                lastcandlesize= fivehourcurrenthigh-fivehourcurrentlow
                prevcandlesize= fivehourprevhigh-fivehourprevlow
                lastcandlebodysize = numpy.abs(fivehourcurrentopen - last*100000)
                prevcandlebodysize = numpy.abs(fivehourprevopen - fivehourprevclose)

                if ((lastcandlesize>prevcandlesize or lastcandlebodysize>prevcandlebodysize) and fivehourcurrentopen>last*100000 and fivehourprevopen<fivehourprevclose and ha_direction_down0 and hah_trend!="UP" and hah_trend!="Revers-UP" and ha_trend!="UP" and ha_trend!="Revers-UP" and had_trend!="UP" and had_trend!="Revers-UP" and had_trend!="STABLE" and HAD_trend!="UP" and HAD_trend!="Revers-UP" and bought_quantity_sql > 0):
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      ' + market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 2 where active=1 and market =("%s")' % market)
                        if status_orders(market, 4)==1:
                            cursor.execute(
                                'insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (
                                market, str(serf) + ' HA_sell_signal ' + str(2),
                                currtime, status_orders(market, 0)))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                
                if ((lastcandlesize>prevcandlesize or lastcandlebodysize>prevcandlebodysize) and fivehourcurrentopen>last*100000 and fivehourprevopen<fivehourprevclose and bought_quantity_sql > 0):
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      ' + market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 1 where active=1 and market =("%s")' % market)
                        if status_orders(market, 4)==1:
                            cursor.execute(
                                'insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (
                                market, str(serf) + ' HA_sell_signal ' + str(1),
                                currtime, status_orders(market, 0)))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                
                
                        
                        
                        
                        
                        
                        
                
                
                lastcandlesize = hourcurrenthigh-hourcurrentlow
                candlesize=(hourcurrenthigh/hourcurrentlow-1)*100
                print "Candle size is:", candlesize
                if ((hourcurrenthigh/hourcurrentlow-1)*100>3 and last*100000>hourcurrentopen): 
                    print "We have peak situation, lets wait"
                    printed1=("We have peak situation, lets wait")
                    
                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                       #cursor.execute("update markets set strike_date=%s, strike_info=%s  where market = %s",(currenttime, printed1, market))
                        cursor.execute(
                            "update markets set strike_date=%s, strike_time2=%s, strike_info=%s  where market = %s",
                            (currenttime, currtime, printed1, market))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()
                    
                
                    

                
                
                
                
                
                
                if ((ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0 and ha_direction_up_long_1) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_longer) or (ha_trend!="DOWN" and ha_trend!="Revers-DOWN" and ha_trend!="STABLE" and hah_trend!="DOWN" and hah_trend!="Revers-DOWN" and hah_trend!="STABLE" ) and bought_quantity_sql > 0):

                    try:
                        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 0 where active=1 and market =("%s")' % market)
                        if status_orders(market, 4)==1:
                            cursor.execute(
                                'insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (
                                market, str(serf) + ' HA_sell_signal ' + str(0),
                                currtime, status_orders(market, 0)))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()




                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()

                    printed = ('      '+ market + '   The HA_hour is  ' + HA_trend + '  and HAH is ' + HAH_trend)
                    cursor.execute("update markets set current_price = %s, ha_direction =%s,  ha_direction_hour=%s, ha_candle_previous=%s, 	ha_candle_current=%s  where market = %s and active =1",(last, HA_trend,  HAH_trend, Ha_previous_candle, Ha_current_candle, market))
                    if status_orders(market, 4) == 1:
                        cursor.execute('insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (market, str(serf)+' HA: ' + str(HA_trend) + ' HAH: ' + str(HAH_trend), currtime, status_orders(market, 0)))
                    else:
                        pass
                    cursor.execute("update markets set  ha_fivehour =%s,  ha_hour=%s  where market = %s and active =1",(ha_trend,  hah_trend, market))
                    #cursor.execute('insert into ha_logs (date, market, HA_hour, log ) values ("%s", "%s", "%s", "%s")' % (currenttime, market, HA_trend, printed))
                    #cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()



        except:
            continue



def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
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
