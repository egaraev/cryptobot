# Imports from modules, libraries and config files
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

# c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file
c = Client(api_key="", api_secret="")
c1 = Client(api_key=config.key,
            api_secret=config.secret)  # Configuring bytrex client with API key/secret from config file

TICK_INTERVAL = 300  # seconds


# The main function
def main():
    print('Starting score module')

    # Running clock forever
    while True:
        start = time.time()
        tick()
        end = time.time()
        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))


################################################################################################################
# what will be done every loop iteration
def tick():
    market_summ = c.get_market_summaries().json()['result']
    btc_trend = parameters()[12]
    currtime = int(round(time.time()))



    for summary in market_summ:  # Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                # Candle analisys
                lastcandle = get_candles(market, 'thirtymin')['result'][-1:]
                currentlow = float(lastcandle[0]['L'])
                currentopen = float(lastcandle[0]['O'])
                currenthigh = float(lastcandle[0]['H'])
                previouscandle = get_candles(market, 'thirtymin')['result'][-2:]
                prevclose = float(previouscandle[0]['C'])
                lastcandle5 = get_candles(market, 'fivemin')['result'][-1:]
                currentlow5 = float(lastcandle5[0]['L'])
                currentopen5 = float(lastcandle5[0]['O'])
                currenthigh5 = float(lastcandle5[0]['H'])
                previouscandle5 = get_candles(market, 'fivemin')['result'][-2:]
                prevclose5 = float(previouscandle5[0]['C'])
                hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                hourcurrentopen = float(hourlastcandle[0]['O'])
                hourcurrenthigh = float(hourlastcandle[0]['H'])
                hourprevcandle = get_candles(market, 'hour')['result'][-2:]
                hourprevopen = float(hourprevcandle[0]['O'])
                hourprevclose = float(hourprevcandle[0]['C'])
                fivemin = 'NONE'
                thirtymin = 'NONE'
                hour = 'NONE'
                candles_signal_short = str(heikin_ashi(market, 29))
                candles_signal_long = str(heikin_ashi(market, 30))

                timestamp = int(time.time())
                day_close = summary['PrevDay']  # Getting day of closing order
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price

                bought_quantity_sql = float(status_orders(market, 2))
                previous_score = float(heikin_ashi(market, 33))
                now = datetime.datetime.now()

                HA_trend = heikin_ashi(market, 10)
                HAD_trend = heikin_ashi(market, 18)
                HAH_trend = heikin_ashi(market, 20)


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




                ######################
                score = 0
                btc_score = 0
                ha1_score = 0
                ha2_score = 0
                ha3_score = 0
                ai_score = 0
                cs_score = 0
                cs1_score = 0
                candle_score = 0
                candle1_score = 0
                candle2_score = 0

                if btc_trend == "UP":
                    btc_score = 1
                else:
                    btc_score = 0

                if HAD_trend == "Revers-UP" or HAD_trend == "UP":
                    ha1_score = 1
                else:
                    ha1_score = 0

                if HA_trend == "Revers-UP" or HA_trend == "UP":
                    ha2_score = 2
                else:
                    ha2_score = 0

                if HAH_trend == "Revers-UP" or HAH_trend == "UP":
                    ha3_score = 2
                else:
                    ha3_score = 0

                if ai_prediction(market) == "UP":
                    ai_score = 2
                else:
                    ai_score = 0

                if candles_signal_short == "Up":
                    cs_score = 2
                else:
                    cs_score = 0

                if candles_signal_long == "Up":
                    cs1_score = 2
                else:
                    cs1_score = 0

                if hour == "U" or hour == "H":
                    candle_score = 1
                else:
                    candle_score = 0

                if thirtymin == "U" or thirtymin == "H":
                    candle1_score = 0.5
                else:
                    candle1_score = 0

                if fivemin == "U" or fivemin == "H":
                    candle2_score = 0.5
                else:
                    candle2_score = 0

                score = btc_score + ha1_score + ha2_score + ha3_score + ai_score + cs_score + cs1_score + candle_score + candle1_score + candle2_score
                print market, "score is ", score

                score_trend = "NONE"
                if score - previous_score > 0:
                    score_trend = "UP"
                elif score - previous_score == 0:
                    score_trend = "NEUTRAL"
                else:
                    score_trend = "DOWN"

                serf = percent_serf(market)


                try:
                    print market, "lets update new score"
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set score=%s, score_direction=%s  where market = %s",
                                   (score, score_trend, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

                if (score_trend =="DOWN" or score_trend =="UP") and status_orders(market, 4)==1:
                    print market, "lets update new score in history"
                    #try:
                        #print market, "lets update new score in history"
                        #db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                        #cursor = db.cursor()
                        #cursor.execute('insert into orderlogs(market, signals, time, orderid) values("%s", "%s", "%s", "%s")' % (market,  str(serf)+ ' Score: ' + str(score)+' Score_trend: ' + str(score_trend), currtime, status_orders(market, 0)))
                        #db.commit()
                    #except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        #sys.exit(1)
                    #finally:
                        #db.close()


        except:
            continue






#Allowed currencies function for SQL

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


def ai_prediction(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT ai_direction FROM markets WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])

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




def parameters():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24])

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


if __name__ == "__main__":
    main()
