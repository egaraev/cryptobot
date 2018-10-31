import MySQLdb
import sys
from pybittrex.client import Client

c=Client(api_key='', api_secret='')

def main():
    print('Starting summ checking module')

    SUMM()


def SUMM():
    market_summ = c.get_market_summaries().json()['result']
    open('out8.csv', 'w').close()
    open('out9.csv', 'w').close()
    open('out10.csv', 'w').close()
    open('out11.csv', 'w').close()
    open('out12.csv', 'w').close()
    open('out13.csv', 'w').close()
    open('out14.csv', 'w').close()
    open('out15.csv', 'w').close()
    open('out16.csv', 'w').close()
    open('out-max.csv', 'w').close()


#    try:
#        db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
#        cursor = db.cursor()
#        cursor.execute("SELECT DISTINCT `sell` FROM `orders` order by sell asc")
#        numrows = cursor.rowcount
#        for x in xrange(0, numrows):
#            r = cursor.fetchone()
#            #print r[0]
#            f1 = open('out9.csv', 'a')
#            print >> f1, r[0]
#    except MySQLdb.Error, e:
#        print "Error %d: %s" % (e.args[0], e.args[1])
#        sys.exit(1)
#    finally:
#        db.close()









    for summary in market_summ: #Loop trough the market summary
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                max_loss=aftercount_serf(market)-summ_serf(market)
                sell_loss_0 = aftercount_serf_sell(market, 0) - summ_serf_sell(market, 0)
                sell_loss_1 = aftercount_serf_sell(market, 1) - summ_serf_sell(market, 1)
                sell_loss_2 = aftercount_serf_sell(market, 2) - summ_serf_sell(market, 2)
                sell_loss_3 = aftercount_serf_sell(market, 3) - summ_serf_sell(market, 3)
                sell_loss_4 = aftercount_serf_sell(market, 4) - summ_serf_sell(market, 4)
                sell_loss_5 = aftercount_serf_sell(market, 5) - summ_serf_sell(market, 5)
                sell_loss_6 = aftercount_serf_sell(market, 6) - summ_serf_sell(market, 6)
                #if summ_serf(market)!=0:
                 #   print market, summ_serf(market), count(market)
                f= open('out8.csv', 'a')
                print >> f, str(market)
                f3 = open('out11.csv', 'a')
                print >> f3, sell_loss_0
                f4 = open('out12.csv', 'a')
                print >> f4, sell_loss_1
                f5 = open('out13.csv', 'a')
                print >> f5, sell_loss_2
                f2 = open('out10.csv', 'a')
                print >> f2, sell_loss_3
                f6 = open('out14.csv', 'a')
                print >> f6, sell_loss_4
                f7 = open('out15.csv', 'a')
                print >> f7, sell_loss_5
                f8 = open('out16.csv', 'a')
                print >> f8, sell_loss_6
                f9 = open('out-max.csv', 'a')
                print >> f9, max_loss




def summ_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and percent_serf>0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def aftercount_serf(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(aftercount) FROM orders where active=0 and aftercount>0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0



def aftercount_serf_sell(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    sell=value
    cursor.execute("SELECT SUM(aftercount) FROM orders where active=0 and market= '%s' and sell='%s'" % (market, sell))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float(row[0])

    return 0



def summ_serf_sell(marketname, value):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    sell=value
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and market= '%s' and sell='%s'" % (market, sell))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float(row[0])

    return 0





def available_market_list(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
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
