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



# The main function
def main():
    print('Starting grow_percent  module')
    tick()



################################################################################################################
# what will be done every loop iteration
def tick():
    market_summ = c.get_market_summaries().json()['result']
    currtime = int(round(time.time()))



    for summary in market_summ:  # Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                timestamp = int(time.time())
                day_close = summary['PrevDay']  # Getting day of closing order
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price

                bought_quantity_sql = float(status_orders(market, 2))
                previous_score = float(heikin_ashi(market, 33))
                now = datetime.datetime.now()
           
                lasthour = get_candles(market, 'fivemin')['result'][-13:]
                currentmin = float(lasthour[12]['C'])*100000
                prev5min = float(lasthour[11]['C'])*100000
                prev5min1 = float(lasthour[10]['C'])*100000
                prev5min2 = float(lasthour[9]['C'])*100000
                prev5min3 = float(lasthour[8]['C'])*100000
                prev5min4 = float(lasthour[7]['C'])*100000
                prev5min5 = float(lasthour[6]['C'])*100000
                prev5min6 = float(lasthour[5]['C'])*100000
                prev5min7 = float(lasthour[4]['C'])*100000
                prev5min8 = float(lasthour[3]['C'])*100000
                prev5min9 = float(lasthour[2]['C'])*100000
                prev5min10 = float(lasthour[1]['C'])*100000
                prev5min11 = float(lasthour[0]['C'])*100000
                    
                    
                    
	        print last*100000, currentmin, prev5min, prev5min1, prev5min2, prev5min3, prev5min4, prev5min5, prev5min6, prev5min7, prev5min8, prev5min9, prev5min10, prev5min11




 #               try:
 #                   print market, "lets update new score"
 #                   db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
 #                  cursor = db.cursor()
 #                   cursor.execute("update markets set score=%s, score_direction=%s  where market = %s",
 #                                  (score, score_trend, market))
 #                   db.commit()
 #               except MySQLdb.Error, e:
 #                   print "Error %d: %s" % (e.args[0], e.args[1])
 #                   sys.exit(1)
 #               finally:
 #                   db.close()


        except:
            continue






#Allowed currencies function for SQL

def available_market_list(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled=1 and  market = '%s'" % market)
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
