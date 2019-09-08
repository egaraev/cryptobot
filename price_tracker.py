import config
from pybittrex.client import Client
import MySQLdb
import sys
import datetime
import time

c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')
currtime = int(time.time())
#TICK_INTERVAL = 300  # seconds

def main():
    print('Starting stat module')

    # Running clock forever
#    while True:
#        start = time.time()
    tick()
#        end = time.time()
        # Sleep the thread if needed
#        if end - start < TICK_INTERVAL:
#            time.sleep(TICK_INTERVAL - (end - start))



def tick():
    market_summ = c.get_market_summaries().json()['result']
    #print market_count()
    #print c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                last = float(summary['Last'])  # last price
                now = datetime.datetime.now()
                currenttime = now.strftime("%Y-%m-%d %H:%M")
                
                print "Beginning of the minute: ", last
                time.sleep(10)
                print "First 10 seconds of the minute: ", float(summary['Last'])
                time.sleep(10)
                print "First 20 seconds of the minute: ", float(summary['Last'])
                time.sleep(10)
                print "First 30 seconds of the minute: ", float(summary['Last'])
                time.sleep(10)
                print "First 40 seconds of the minute: ", float(summary['Last'])
                time.sleep(10)
                print "First 50 seconds of the minute: ", float(summary['Last'])
                time.sleep(10)
                print "End of the minute: ", float(summary['Last'])
                
                
                



#                try:
#                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
#                    cursor = db.cursor()
#                    cursor.execute(
#                        "update markets set date= %s  where market = %s",
#                        (currenttime, market))
#                    cursor.execute('INSERT INTO stat (market, date, current_price, ai_price, ai_direction, ha_direction_hour, ha_direction, ha_direction_daily, percent_chg, volume, candles, candle_signal_short, score, score_direction, positive_sentiments, negative_sentiments, buy_orders_sum, sell_orders_sum, buy_orders_count, sell_orders_count, ha_hour, ha_fivehour, ha_day, ha_candle_previous, ha_candle_current, spread, grow_hour, grow_history, active) SELECT market, date, current_price, ai_price, ai_direction, ha_direction_hour, ha_direction, ha_direction_daily, percent_chg, volume, candles, candle_signal_short,  score, score_direction, positive_sentiments, negative_sentiments, buy_orders_sum, sell_orders_sum, buy_orders_count, sell_orders_count, ha_hour, ha_fivehour, ha_day, ha_candle_previous, ha_candle_current, spread, grow_hour, grow_history, active FROM markets WHERE market="%s"' % (market))
#                    db.commit()
#                except MySQLdb.Error, e:
#                    print "Error %d: %s" % (e.args[0], e.args[1])
#                    sys.exit(1)
#                finally:
#                    db.close()







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






def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE  enabled=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False




if __name__ == "__main__":
    main()
