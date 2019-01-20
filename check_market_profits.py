import MySQLdb
from pybittrex.client import Client

c=Client(api_key='', api_secret='')

def main():
    print('Starting summ checking module')

    SUMM()


def SUMM():
    market_summ = c.get_market_summaries().json()['result']
    open('data/out2.csv', 'w').close()
    open('data/out3.csv', 'w').close()
    open('data/out4.csv', 'w').close()
    for summary in market_summ: #Loop trough the market summary
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                if summ_serf(market)!=0:
                    print market, summ_serf(market), count(market)
                    f= open('data/out2.csv', 'a')
                    print >> f, str(market)
                    f1=open('data/out3.csv', 'a')
                    print >>f1, summ_serf(market)
                    f2 = open('data/out4.csv', 'a')
                    print >> f2, count(market)




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
