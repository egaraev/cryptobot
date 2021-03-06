import MySQLdb
from pybittrex.client import Client

c=Client(api_key='', api_secret='')

def main():
    print('Starting AI checking module')

    AI()


def AI():
    market_summ = c.get_market_summaries().json()['result']
    open('out5.csv', 'w').close()
    open('out6.csv', 'w').close()
    open('out7.csv', 'w').close()
    for summary in market_summ: #Loop trough the market summary
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                if summ_ai(market)>-1:
                    print market, summ_ai(market), count(market)
                    f= open('out5.csv', 'a')
                    print >> f, str(market)
                    f1=open('out6.csv', 'a')
                    print >>f1, summ_ai(market)
                    f2 = open('out7.csv', 'a')
                    print >> f2, count(market)




def summ_ai(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(result) FROM predictlog where market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0




def count(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT COUNT(*) FROM predictlog where market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE enabled =1")
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False






if __name__ == "__main__":
    main()
