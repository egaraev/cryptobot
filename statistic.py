import MySQLdb
import sys
from pybittrex.client import Client
import os
c=Client(api_key='', api_secret='')

def main():
    print('Starting summ checking module')

    SUMM()


def SUMM():
    market_summ = c.get_market_summaries().json()['result']
    open('data/out8.csv', 'w').close()
    open('data/out9.csv', 'w').close()
    open('data/out10.csv', 'w').close()
    open('data/out11.csv', 'w').close()
    open('data/out12.csv', 'w').close()
    open('data/out13.csv', 'w').close()
    open('data/out14.csv', 'w').close()
    open('data/out15.csv', 'w').close()
    open('data/out16.csv', 'w').close()
    open('data/out17.csv', 'w').close()
    open('data/out-max.csv', 'w').close()


#    try:
#        db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
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
                f= open('data/out8_tmp.csv', 'a')
                print >> f, str(market)
                if (aftercount_serf_sell(market, 0) - summ_serf_sell(market, 0))>0:
                    sell_loss_0 = aftercount_serf_sell(market, 0) - summ_serf_sell(market, 0)
                    f3 = open('data/out11_tmp.csv', 'a')
                    print >> f3, sell_loss_0
                else:
                    f3 = open('data/out11_tmp.csv', 'a')
                    print >> f3, 0.0
                if (aftercount_serf_sell(market, 1) - summ_serf_sell(market, 1))>0:
                    sell_loss_1 = aftercount_serf_sell(market, 1) - summ_serf_sell(market, 1)
                    f4 = open('data/out12_tmp.csv', 'a')
                    print >> f4, sell_loss_1
                else:
                    f4 = open('data/out12_tmp.csv', 'a')
                    print >> f4, 0.0
                if (aftercount_serf_sell(market, 2) - summ_serf_sell(market, 2))>0:
                    sell_loss_2 = aftercount_serf_sell(market, 2) - summ_serf_sell(market, 2)
                    f5 = open('data/out13_tmp.csv', 'a')
                    print >> f5, sell_loss_2
                else:
                    f5 = open('data/out13_tmp.csv', 'a')
                    print >> f5, 0.0
                if (aftercount_serf_sell(market, 3) - summ_serf_sell(market, 3))>0:
                    sell_loss_3 = aftercount_serf_sell(market, 3) - summ_serf_sell(market, 3)
                    f2 = open('data/out10_tmp.csv', 'a')
                    print >> f2, sell_loss_3
                else:
                    f2 = open('data/out10_tmp.csv', 'a')
                    print >> f2, 0.0
                if (aftercount_serf_sell(market, 4) - summ_serf_sell(market, 4))>0:
                    sell_loss_4 = aftercount_serf_sell(market, 4) - summ_serf_sell(market, 4)
                    f6 = open('data/out14_tmp.csv', 'a')
                    print >> f6, sell_loss_4
                else:
                    f6 = open('data/out14_tmp.csv', 'a')
                    print >> f6, 0.0
                if (aftercount_serf_sell(market, 5) - summ_serf_sell(market, 5))>0:
                    sell_loss_5 = aftercount_serf_sell(market, 5) - summ_serf_sell(market, 5)
                    f7 = open('data/out15_tmp.csv', 'a')
                    print >> f7, sell_loss_5
                else:
                    f7 = open('data/out15_tmp.csv', 'a')
                    print >> f7, 0.0
                if (aftercount_serf_sell(market, 6) - summ_serf_sell(market, 6))>0:
                    sell_loss_6 = aftercount_serf_sell(market, 6) - summ_serf_sell(market, 6)
                    f8 = open('data/out16_tmp.csv', 'a')
                    print >> f8, sell_loss_6
                else:
                    f8 = open('data/out16_tmp.csv', 'a')
                    print >> f8, 0.0
                if (aftercount_serf_sell(market, 7) - summ_serf_sell(market, 7))>0:
                    sell_loss_7 = aftercount_serf_sell(market, 7) - summ_serf_sell(market, 7)   # was 8, changed to 7
                    f9 = open('data/out17_tmp.csv', 'a')
                    print >> f9, sell_loss_7
                else:
                    f9 = open('data/out17_tmp.csv', 'a')
                    print >> f9, 0.0

                f10 = open('data/out-max_tmp.csv', 'a')
                print >> f10, max_loss

    os.rename('data/out8_tmp.csv', 'data/out8.csv')
    os.rename('data/out10_tmp.csv', 'data/out10.csv')
    os.rename('data/out11_tmp.csv', 'data/out11.csv')
    os.rename('data/out12_tmp.csv', 'data/out12.csv')
    os.rename('data/out13_tmp.csv', 'data/out13.csv')
    os.rename('data/out14_tmp.csv', 'data/out14.csv')
    os.rename('data/out15_tmp.csv', 'data/out15.csv')
    os.rename('data/out16_tmp.csv', 'data/out16.csv')
    os.rename('data/out17_tmp.csv', 'data/out17.csv')
    os.rename('data/out-max_tmp.csv', 'data/out-max.csv')




def summ_serf(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and percent_serf>0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


def aftercount_serf(marketname):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(aftercount) FROM orders where active=0 and aftercount>0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0



def aftercount_serf_sell(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    sell=value
    cursor.execute("SELECT SUM(aftercount) FROM orders where active=0 and aftercount>0 and market= '%s' and sell='%s'" % (market, sell))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float(row[0])

    return 0



def summ_serf_sell(marketname, value):
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    sell=value
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and percent_serf>0 and market= '%s' and sell='%s'" % (market, sell))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float(row[0])

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
