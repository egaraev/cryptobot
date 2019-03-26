#Imports from modules, libraries and config files
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
#c = Client(api_key=config.key, api_secret=config.secret)   #Configuring bytrex client with API key/secret from config file
c=Client(api_key="", api_secret="")
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")



#The main function
def main():
    print('Starting orders count module')

    tick()


def tick():
    market_summ = c.get_market_summaries().json()['result']
    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())
    debug_mode=parameters()[10]
    last_orders_quantity = 50


    print "Global buy parameters configured, moving to market loop"


    #global active
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                buyorders = buysellorders_sql(market, 38)
                #print market
                sellorders = buysellorders_sql(market, 39)

                buyorderbook = c.get_orderbook(market, 'buy').json()['result'][:last_orders_quantity]  #getting buy orders history last 150 orders
                buycount = 0
                buysum = 0

                for buyorder in buyorderbook:  #Counting how much big buy orders we have in history
                    buyamount = buyorder['Quantity']
                    if buyamount >= buyorders:
                        buycount += 1
                        buysum = buyamount + buysum
                buytotalsumm = float("{0:.2f}".format(buysum))  #total summ of BUY orders on the market
                buycountresult = buycount

                sellorderbook = c.get_orderbook(market, 'sell').json()['result'][:last_orders_quantity]  #getting sell orders history last 150 orders
                sellcount = 0
                sellsum = 0
                for sellorder in sellorderbook:   #Counting how much big buy orders we have in history
                    sellamount = sellorder['Quantity']
                    if sellamount >= sellorders:
                        sellcount += 1
                        sellsum = sellamount + sellsum
                selltotalsumm = float("{0:.2f}".format(sellsum))  #total summ of SELL orders on the market
                sellcountresult = sellcount

                #print market, " buy summ is: "+buytotalsumm, "  buy total count: "+buycountresult, " sell summ is: "+selltotalsumm, "sell count is: "+sellcountresult
                print market, buytotalsumm, buycountresult, selltotalsumm, sellcountresult
                printed = market, "Buy summ is: {} %".format(buytotalsumm), "Buy total count is: {} %".format(buycountresult),  "Sell summ is: {} %".format(selltotalsumm), "Sell total count is: {} %".format(sellcountresult)
                try:
                    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set buy_orders_sum = %s, sell_orders_sum =%s, buy_orders_count =%s, sell_orders_count=%s  where market = %s",(buytotalsumm,selltotalsumm, buycountresult, sellcountresult, market))
                    #cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
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










#Allowed currencies function for SQL
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




def parameters():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24])

    return 0



def buysellorders_sql(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled=1 and market = '%s'" % market)
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







if __name__ == "__main__":
    main()
