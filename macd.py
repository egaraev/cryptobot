from yahoo_fin import stock_info as si
import datetime
import time 
from datetime import timedelta, date
import os, sys
import pandas as pd
import numpy as np
from math import floor
import pymysql
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20, 15)
plt.style.use('fivethirtyeight')

currtime = int(round(time.time()))
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE  enabled=1")
markets=cursor.fetchall()

def main():
    print('Starting cryto-charts module')

    macd_analyze()
	
	


def macd_analyze():
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    currentdate = now.strftime("%Y-%m-%d")
    for market in markets: #Loop trough the crypto summary
        try:
          market=(market[0])
          crypto=market[4:]
          market1 = crypto+"-USD"
          print (market1)
          df = si.get_data(market1)
          df = df.iloc[: , :-1]
          df = df[-300:]
          #print (df)
          new_macd = get_macd(df['close'], 26, 12, 6)
         # print (new_macd)
          buy_price, sell_price, macd_signal = implement_macd_strategy(df['close'], new_macd)

          ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
          ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
          ax1.plot(df['close'], color = 'skyblue', linewidth = 2, label = market1)
          ax1.plot(df.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
          ax1.plot(df.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
          ax1.legend()
          ax1.set_title('MACD SIGNALS')
          ax2.plot(new_macd['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
          ax2.plot(new_macd['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

          for i in range(len(new_macd)):
              if str(new_macd['hist'][i])[0] == '-':
                 ax2.bar(new_macd.index[i], new_macd['hist'][i], color = '#ef5350')
              else:
                 ax2.bar(new_macd.index[i], new_macd['hist'][i], color = '#26a69a')
    
          plt.legend(loc = 'lower right')
          plt.savefig('/root/PycharmProjects/cryptobot/images/macd_results.png', bbox_inches='tight')    
          newfilename=("{}_macd_results.png".format(market))
          my_path = "/root/PycharmProjects/cryptobot/images/macd_results.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          position = []
          for i in range(len(macd_signal)):
            if macd_signal[i] > 1:
                position.append(0)
            else:
                position.append(1)
        
          for i in range(len(df['close'])):
            if macd_signal[i] == 1:
               position[i] = 1
            elif macd_signal[i] == -1:
               position[i] = 0
            else:
               position[i] = position[i-1]
        
          macd = new_macd['macd']
          signal = new_macd['signal']
          close_price = df['close']
          macd_signal = pd.DataFrame(macd_signal).rename(columns = {0:'macd_signal'}).set_index(df.index)
          position = pd.DataFrame(position).rename(columns = {0:'macd_position'}).set_index(df.index)

          frames = [close_price, macd, signal, macd_signal, position]
          strategy = pd.concat(frames, join = 'inner', axis = 1)

          #print (strategy)
          row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
          first_max = strategy.values[row_ix, range(strategy.shape[1])]
          out = pd.DataFrame([first_max], columns=strategy.columns)
          #print (out)
          last_macd_signal = int(out['macd_signal'])
          print (last_macd_signal)
		  
          macd_signal= strategy.iloc[-1]
          macd_signal = int(macd_signal['macd_signal'])
          if macd_signal == 0:
             print ("MACD is 0, nothing to do")
          else:
             if macd_signal == 1:
                signal = "Buy"
             else:
                signal = "Sell"
             try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
                 cursor.execute("update history set macd_signal='%s'  where market='%s' and date='%s'" % (signal, market, currentdate))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()



          if last_macd_signal == 1:
                signal = "Buy"
          else:
                signal = "Sell"
          try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute("update markets set macd_signal='%s'  where market='%s'" % (signal, market))
                 db.commit()
          except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
          finally:
                 db.close()


		  


        except:
            continue





def implement_macd_strategy(prices, data):    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal





def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df




def market_full_name(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False




if __name__ == "__main__":
    main()