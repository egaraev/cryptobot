import MySQLdb
from pybittrex.client import Client
import os
c=Client(api_key='', api_secret='')

def main():
    print('Starting market profits checking module')

    SUMM()


def SUMM():
    market_summ = c.get_market_summaries().json()['result']
    open('data/out2_tmp.csv', 'w').close()
    open('data/out3_tmp.csv', 'w').close()
    open('data/out4_tmp.csv', 'w').close()
    for summary in market_summ: #Loop trough the market summary
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                if summ_serf(market)!=0:
                    print market, summ_serf(market), count(market)
                    f= open('data/out2_tmp.csv', 'a')
                    print >> f, str(market)
                    f1=open('data/out3_tmp.csv', 'a')
                    print >>f1, summ_serf(market)-count(market)*0.5
                    f2 = open('data/out4_tmp.csv', 'a')
                    print >> f2, count(market)
    os.rename('data/out2_tmp.csv', 'data/out2.csv')
    os.rename('data/out3_tmp.csv', 'data/out3.csv')
    os.rename('data/out4_tmp.csv', 'data/out4.csv')



def summ_serf(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0




def count(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

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






if __name__ == "__main__":
    main()
