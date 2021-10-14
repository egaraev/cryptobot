import time
import config
from pybittrex.client import Client
import pymysql
import requests
import hashlib
import hmac
import matplotlib as mpl
import matplotlib.pyplot as plt
import io, base64, os, json, re, sys 
import glob
import shutil
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from datetime import timedelta, date
currtime = int(round(time.time()))
c=Client(api_key='', api_secret='')
import yfinance as yf
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
days=30



def main():
    print('Starting candle patterns module')
    tick()


def tick():
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    currentdate = now.strftime("%Y-%m-%d")

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                #active_order= status_orders(market, 4)
                last = float(summary['Last'])  # last price
#######################
                # market=(market[0])
                # name=market_full_name(market, 73)
                crypto=market[4:]
                market1 = crypto+"-USD"
                stock = yf.Ticker(market1)
                hist = stock.history(period="{}d".format(days))
                df = pd.DataFrame(hist)
                df = df.reset_index(level=['Date'])   

                #print (df)
                ohlc_df = df.copy()
                ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
                #last_pattern=''		  
                df=candle_df(df)
                #print (df)
                candle_score=market_values(market,68)
                candle_pattern=market_values(market,69)
                candletime=int(market_values(market,70))
                buy_df = df.copy()
                #print (buy_df)
                candle_scored_buy= buy_df[(buy_df['candle_score'] > 0)]
                #print (market, candle_scored_buy)
                candle_scored_sell= df[(df['candle_score'] < 0)]		  
                labels_buy=(candle_scored_buy['candle_pattern'].tolist())
                labels_sell=(candle_scored_sell['candle_pattern'].tolist())	
				
		     
                #print (buy_df)
                ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
                legend_elements = [Line2D([0], [0], marker="^", color='w', label='B_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_w_s -> Three_white_soldiers', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_b -> Tweezer_Bottom', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='M_S -> Morning_Star', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_HR -> Bullish_Harami', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='Bu_E -> Bullish_Engulfing', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='H_M_Bu -> Hanging_Man_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_c -> Three_black_crows', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_g -> Two_black_gapping', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_t -> Tweezer_Top', markersize=15), Line2D([0], [0], marker="v", color='r', label='E_S -> Evening_Star', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_HR -> Bearish_Harami', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_R -> Bearish_Reversal', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BE -> Shooting_Star_Bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='Be_E -> Bearish_Engulfing', markersize=15), Line2D([0], [0], marker="v", color='r', label='H_M_Be -> Hanging_Man_bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BU -> Shooting_Star_Bullish', markersize=15)]		  
		  
		  
                #print (ohlc_df)		  
		  
                fig, ax = plt.subplots(figsize=(20, 15))
                ax.legend(handles=legend_elements, loc='upper left')
                # Converts raw mdate numbers to dates
                ax.xaxis_date()
                plt.xlabel("Date")	  
                # Making candlestick plot
                candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
                plt.ylabel("Price")
                plt.title(market) 	  
                ax2 = ax.twinx()
		  
		  
                candle_scored_buy['Date'] = ohlc_df['Date']
                x=candle_scored_buy['Date'].tolist()
                y=candle_scored_buy['candle_score'].tolist()
                n = labels_buy
      
                #fig, ax2 = plt.subplots()
                ax2.axhline(y=2)
                ax2.plot([x], [2], marker='o', markersize=1)
                ax2.scatter(x, y, c='g', marker="^", s=120)

                for i, txt in enumerate(n):
                   ax2.annotate(txt, (x[i], y[i]))


                x1=candle_scored_sell['Date'].tolist()
                y1=candle_scored_sell['candle_score'].tolist()
                n1 = labels_sell
      
                #fig, ax2 = plt.subplots()
                ax2.scatter(x1, y1, c='r', marker="v", s=120)

                for a, txt1 in enumerate(n1):
                   ax2.annotate(txt1, (x1[a], y1[a]))	
          
                ax2.axhline(y=-2)	
		  
		  

		  
                plt.gcf().autofmt_xdate()   # Beautify the x-labels
                plt.autoscale(tight=True)
                plt.grid()
                ax.grid(True)
                plt.savefig('/root/PycharmProjects/cryptobot/images/candlesticks.png')
		  
                newfilename=("{}_candlesticks.png".format(market))
                my_path = "/root/PycharmProjects/cryptobot/images/candlesticks.png"
                new_name = os.path.join(os.path.dirname(my_path), newfilename)
                os.rename(my_path, new_name)

                print (new_name)



                new_df= (buy_df.iloc[-2:])
                print (new_df)
                sum_score = new_df['candle_score'].sum()

                last_df= buy_df.iloc[-1]
                last_pattern = last_df['candle_pattern']

				
                new_df_check_patten=(buy_df.iloc[-2:])
                previous_day_pattern=(new_df_check_patten.iloc[:1])
                previous_day_pattern=previous_day_pattern.iloc[-1]
                previous_day_pattern=previous_day_pattern['candle_pattern']
                print (sum_score)

                # try:
                    # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                    # cursor = db.cursor()
                    #cursor.execute("update markets set candle_score='%s'  where market='%s'" % (sum_score, market))

                    # db.commit()
                # except pymysql.Error as e:
                    # print ("Error %d: %s" % (e.args[0], e.args[1]))
                    # sys.exit(1)
                # finally:
                    # db.close()	
			  
	
			  
                if (last_pattern =="" and previous_day_pattern!=candle_pattern):
                  try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
                  except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
                  finally:
                     db.close()				  



                if (last_pattern =="" and currtime-candletime>400000):
                  try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s' where market='%s'" % (" ", market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (0, market))					 
                     db.commit()
                  except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
                  finally:
                     db.close()	


				 
                if last_pattern !="":
                  print (last_pattern, previous_day_pattern)

                  try:
                     db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                     cursor = db.cursor()
                     cursor.execute("update markets set candle_pattern='%s', candle_time='%s'  where market='%s'" % (last_pattern, currtime, market))
                     cursor.execute("update markets set candle_score='%s'  where market='%s'" % (sum_score, market))
                     cursor.execute("update history set candle_score='%s', candle_pattern='%s'  where market='%s' and date='%s'" % (sum_score, last_pattern, market, currentdate))					 
                     db.commit()
                  except pymysql.Error as e:
                     print ("Error %d: %s" % (e.args[0], e.args[1]))
                     sys.exit(1)
                  finally:
                     db.close()

                else:
                    pass 	


        except:
            continue



def candle_score(lst_0,lst_1,lst_2,lst_3):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]  #current
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]  #previous
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]  #previous2
    O_3,H_3,L_3,C_3=lst_3[0],lst_3[1],lst_3[2],lst_3[3]  #previous3
    
    DojiSize = 0.1

# UP trend: (C_2>C_3)
# Green candles before: (C_3 > O_3) & (C_2 > O_2)
#DOWN trend: (C_2<C_3)
# Red candles before: (C_3 < O_3) & (C_2 < O_2)
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)	
    Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
	
    Inverted_Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    Inverted_Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6))    
    
    Bullish_Reversal = (O_2 > C_2)&(O_1 > C_1)&doji
    Bearish_Reversal = (O_2 < C_2)&(O_1 < C_1)&doji
    
    Evening_Star= (C_3 > O_3) & (C_2 > O_2) & (C_1 < O_1) & (O_1 > C_2) & (O_0 <O_1) & (C_0 < O_0 ) & ((C_2-O_2)>(O_1-C_1)) & ((O_0-C_0)>(O_1-C_1))

    Morning_Star= (C_3 < O_3) & (C_2 < O_2) & (C_1 > O_1) & (O_1 < C_2) & (O_0 > O_1) & (C_0 > O_0 )	 & ((O_2- C_2)>(C_1 - O_1)) & ((C_0-O_0)>(C_1-O_1))
	

    Shooting_Star_Bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer
    
    Shooting_Star_Bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer	
    
    Bearish_Harami =  (O_2 < C_2)&  (C_2<C_1)&  (C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 < C_0) & ((O_0 - C_0) < (C_1 - O_1)) & ((C_1 - O_1)/(O_0 - C_0)>=2)
	
    Bullish_Harami =  (C_2 < O_2)&  (C_1<C_2)&  (O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 < O_0) & ((C_0 - O_0) < (O_1 - C_1)) & ((O_1 - C_1)/(C_0 - O_0)>=2)	
	
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 > C_1) & (O_1 > C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))  & (C_2 > O_2)
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 > O_1) & (C_1 > O_0) & ((C_0 - O_0) > (O_1 - C_1 ))  & (C_2 < O_2)	
	
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)
	
    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer
	
    Tweezer_Top = (C_3 > O_3) & (C_2 > O_2) & (C_1>O_1) & (C_0<O_0) & (C_1==O_0)
	
    Tweezer_Bottom=(C_3 < O_3) & (C_2 < O_2) & (C_1<O_1) & (C_0>O_0) & (O_1==C_0)

    Two_black_gapping = (C_3 > O_3) & (C_2 > O_2) & (C_1<O_1) & (C_0<O_0) & (L_1>H_0)	

    Three_white_soldiers=(C_3 < O_3) & (C_2 > O_2) & (C_1 > O_1) & (C_0 > O_0)  & (O_0>O_1) &(O_1>O_2) & (L_3<L_2)

    Three_black_crows=(C_3 > O_3) & (C_2 < O_2) & (C_1 < O_1) & (C_0 < O_0)	& (O_0<O_1) &(O_1<O_2) & (L_3>L_2)

    strCandle=''
    candle_score=0
    
#    if doji:
#        strCandle='doji'
    if    Three_black_crows:
        strCandle=strCandle+'/ '+'T_b_c-v'
        candle_score=candle_score-1	
    if    Three_white_soldiers:
        strCandle=strCandle+'/ '+'T_w_s-^'
        candle_score=candle_score+1			
    if    Two_black_gapping:
        strCandle=strCandle+'/ '+'T_b_g-v'
        candle_score=candle_score-1		
    if    Tweezer_Top:
        strCandle=strCandle+'/ '+'T_t-v'
        candle_score=candle_score-1
    if    Tweezer_Bottom:
        strCandle=strCandle+'/ '+'T_b-^'
        candle_score=candle_score+1		
    if    Evening_Star:
        strCandle=strCandle+'/ '+'E_S-v'
        candle_score=candle_score-1	
    if    Morning_Star:
        strCandle=strCandle+'/ '+'M_S-^'
        candle_score=candle_score+1		
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'BU_HR-^'
        candle_score=candle_score+1
    if    Bearish_Harami:
        strCandle=strCandle+'/ '+'BE_HR-v'
        candle_score=candle_score-1	
    if    Bullish_Reversal:
        strCandle=strCandle+'/ '+'BU_R-^'
        candle_score=candle_score+1
    if    Bearish_Reversal:
        strCandle=strCandle+'/ '+'BE_R-v'
        candle_score=candle_score-1		
#    if    Hammer:
#        strCandle=strCandle+'/ '+'H'
#    if    Inverted_Hammer:
#        strCandle=strCandle+'/ '+'I_H'
    if Shooting_Star_Bearish:
        strCandle=strCandle+'/ '+'SS_BE-v'
        candle_score=candle_score-1
    if Shooting_Star_Bullish:
        strCandle=strCandle+'/ '+'SS_BU-v'
        candle_score=candle_score-1		
    if    Bearish_Engulfing:
        strCandle=strCandle+'/ '+'Be_E-v'
        candle_score=candle_score-1
    if    Bullish_Engulfing:
        strCandle=strCandle+'/ '+'Bu_E-^'
        candle_score=candle_score+1
    if    Piercing_Line_bullish:
        strCandle=strCandle+'/ '+'P_L-^'
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle=strCandle+'/ '+'H_M_Be-v'
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle=strCandle+'/ '+'H_M_Bu-^'
        candle_score=candle_score+1



		
        
    #return candle_score
    return candle_score,strCandle


def candle_df(df):

    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=''


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_3=[df_candle['Open'].iloc[c-3],df_candle['High'].iloc[c-3],df_candle['Low'].iloc[c-3],df_candle['Close'].iloc[c-3]]
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2,lst_3)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    #df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
    return df_candle			




# def status_orders(marketname, value):
    # db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    # cursor = db.cursor()
    # market=marketname
    # cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    # r = cursor.fetchall()
    # for row in r:
        # if row[1] == marketname:
            # return row[value]

    # return 0



	
def available_market_list(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM `markets` where  enabled=1 and market = '%s'" % market)

    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False


# def get_candles(market, tick_interval):
    # url = ('https://bittrex.com/api/v2.0/pub/market/GetTicks?marketName=' + market +'&tickInterval=' + str(tick_interval))
    # r = requests.get(url)
    # requests.session().close()
    # return r.json()




def heikin_ashi(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False

def status_orders(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0



def percent_serf(marketname):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float("{0:.2f}".format(row[0]))
    return 0


def market_values(marketname, value):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False


def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
