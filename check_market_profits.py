import pymysql
import os
import config
from bittrex_api import Bittrex
bittrex = Bittrex(
    api_key=config.key,              # YOUR API KEY
    secret_key=config.secret,           # YOUR API SECRET
    max_request_try_count=3, # Max tries for a request to succeed
    sleep_time=2,            # sleep seconds between failed requests
    debug_level=3
)
c = bittrex.v3

def main():
    print('Starting market profits checking module')

    SUMM()


def SUMM():
    market_summ = c.get_market_summaries()
    open('data/out2_tmp.csv', 'w').close()
    open('data/out3_tmp.csv', 'w').close()
    open('data/out4_tmp.csv', 'w').close()
    for summary in market_summ: #Loop trough the market summary
            if available_market_list(summary['symbol']):
                market = summary['symbol']
                print (market)
                if summ_serf(market)!=0:
                   f= open('data/out2_tmp.csv', 'a')
                   print (str(market), file=f)
                   f1=open('data/out3_tmp.csv', 'a')
                   print (summ_serf(market), file=f1)
                   f2 = open('data/out4_tmp.csv', 'a')
                   print (count(market), file=f2)
    os.rename('data/out2_tmp.csv', 'data/out2.csv')
    os.rename('data/out3_tmp.csv', 'data/out3.csv')
    os.rename('data/out4_tmp.csv', 'data/out4.csv')



def summ_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0




def count(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def available_market_list(symbol):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = symbol
    cursor.execute("SELECT * FROM markets WHERE enabled =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbol:
            return True

    return False






if __name__ == "__main__":
    main()
