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
days=15



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
                # daylastcandle = get_candles(market, 'day')['result'][-1:]
                # daycurrentdate = (daylastcandle[0]['T'])
                # split_string = daycurrentdate.split("T", 1)
                # daycurrentdate = split_string[0]
                # daycurrentdate = datetime.date(*(int(s) for s in daycurrentdate.split('-')))
                # daycurrentlow = float(daylastcandle[0]['L'])
                # daycurrenthigh = float(daylastcandle[0]['H'])
                # daycurrentopen = float(daylastcandle[0]['O'])
                # daycurrentclose = float(daylastcandle[0]['C'])
                # daypreviouscandle = get_candles(market, 'day')['result'][-2:]
                # dayprevdate = (daypreviouscandle[0]['T'])
                # split_string = dayprevdate.split("T", 1)
                # dayprevdate = split_string[0]
                # dayprevdate = datetime.date(*(int(s) for s in dayprevdate.split('-')))
                # dayprevlow = float(daypreviouscandle[0]['L'])
                # dayprevhigh = float(daypreviouscandle[0]['H'])
                # dayprevopen = float(daypreviouscandle[0]['O'])
                # dayprevclose = float(daypreviouscandle[0]['C'])
                # daypreviouscandle2 = get_candles(market, 'day')['result'][-3:]
                # dayprevdate2 = (daypreviouscandle2[0]['T'])
                # split_string = dayprevdate2.split("T", 1)
                # dayprevdate2 = split_string[0]
                # dayprevdate2 = datetime.date(*(int(s) for s in dayprevdate2.split('-')))
                # dayprevlow2 = float(daypreviouscandle2[0]['L'])
                # dayprevhigh2 = float(daypreviouscandle2[0]['H'])
                # dayprevopen2 = float(daypreviouscandle2[0]['O'])
                # dayprevclose2 = float(daypreviouscandle2[0]['C'])
                # daypreviouscandle3 = get_candles(market, 'day')['result'][-4:]
                # dayprevdate3 = (daypreviouscandle3[0]['T'])
                # split_string = dayprevdate3.split("T", 1)
                # dayprevdate3 = split_string[0]
                # dayprevdate3 = datetime.date(*(int(s) for s in dayprevdate3.split('-')))
                # dayprevlow3 = float(daypreviouscandle3[0]['L'])
                # dayprevhigh3 = float(daypreviouscandle3[0]['H'])
                # dayprevopen3 = float(daypreviouscandle3[0]['O'])
                # dayprevclose3 = float(daypreviouscandle3[0]['C'])				
                # daypreviouscandle4 = get_candles(market, 'day')['result'][-5:]
                # dayprevdate4 = (daypreviouscandle4[0]['T'])
                # split_string = dayprevdate4.split("T", 1)
                # dayprevdate4 = split_string[0]
                # dayprevdate4 = datetime.date(*(int(s) for s in dayprevdate4.split('-')))
                # dayprevlow4 = float(daypreviouscandle4[0]['L'])
                # dayprevhigh4 = float(daypreviouscandle4[0]['H'])
                # dayprevopen4 = float(daypreviouscandle4[0]['O'])
                # dayprevclose4 = float(daypreviouscandle4[0]['C'])				
                # daypreviouscandle5 = get_candles(market, 'day')['result'][-6:]
                # dayprevdate5 = (daypreviouscandle5[0]['T'])
                # split_string = dayprevdate5.split("T", 1)
                # dayprevdate5 = split_string[0]
                # dayprevdate5 = datetime.date(*(int(s) for s in dayprevdate5.split('-')))
                # dayprevlow5 = float(daypreviouscandle5[0]['L'])
                # dayprevhigh5 = float(daypreviouscandle5[0]['H'])
                # dayprevopen5 = float(daypreviouscandle5[0]['O'])
                # dayprevclose5 = float(daypreviouscandle5[0]['C'])				
                # daypreviouscandle6 = get_candles(market, 'day')['result'][-7:]
                # dayprevdate6 = (daypreviouscandle6[0]['T'])
                # split_string = dayprevdate6.split("T", 1)
                # dayprevdate6 = split_string[0]
                # dayprevdate6 = datetime.date(*(int(s) for s in dayprevdate6.split('-')))
                # dayprevlow6 = float(daypreviouscandle6[0]['L'])
                # dayprevhigh6 = float(daypreviouscandle6[0]['H'])
                # dayprevopen6 = float(daypreviouscandle6[0]['O'])
                # dayprevclose6 = float(daypreviouscandle6[0]['C'])				
                # daypreviouscandle7 = get_candles(market, 'day')['result'][-8:]
                # dayprevdate7 = (daypreviouscandle7[0]['T'])
                # split_string = dayprevdate7.split("T", 1)
                # dayprevdate7 = split_string[0]
                # dayprevdate7 = datetime.date(*(int(s) for s in dayprevdate7.split('-')))
                # dayprevlow7 = float(daypreviouscandle7[0]['L'])
                # dayprevhigh7 = float(daypreviouscandle7[0]['H'])
                # dayprevopen7 = float(daypreviouscandle7[0]['O'])
                # dayprevclose7 = float(daypreviouscandle7[0]['C'])				
                # daypreviouscandle8 = get_candles(market, 'day')['result'][-9:]
                # dayprevdate8 = (daypreviouscandle8[0]['T'])
                # split_string = dayprevdate8.split("T", 1)
                # dayprevdate8 = split_string[0]
                # dayprevdate8 = datetime.date(*(int(s) for s in dayprevdate8.split('-')))
                # dayprevlow8 = float(daypreviouscandle8[0]['L'])
                # dayprevhigh8 = float(daypreviouscandle8[0]['H'])
                # dayprevopen8 = float(daypreviouscandle8[0]['O'])
                # dayprevclose8 = float(daypreviouscandle8[0]['C'])					
                # daypreviouscandle9 = get_candles(market, 'day')['result'][-10:]
                # dayprevdate9 = (daypreviouscandle9[0]['T'])
                # split_string = dayprevdate9.split("T", 1)
                # dayprevdate9 = split_string[0]
                # dayprevdate9 = datetime.date(*(int(s) for s in dayprevdate9.split('-')))
                # dayprevlow9 = float(daypreviouscandle9[0]['L'])
                # dayprevhigh9 = float(daypreviouscandle9[0]['H'])
                # dayprevopen9 = float(daypreviouscandle9[0]['O'])
                # dayprevclose9 = float(daypreviouscandle9[0]['C'])				
                # daypreviouscandle10 = get_candles(market, 'day')['result'][-11:]
                # dayprevdate10 = (daypreviouscandle10[0]['T'])
                # split_string = dayprevdate10.split("T", 1)
                # dayprevdate10 = split_string[0]
                # dayprevdate10 = datetime.date(*(int(s) for s in dayprevdate10.split('-')))
                # dayprevlow10 = float(daypreviouscandle10[0]['L'])
                # dayprevhigh10 = float(daypreviouscandle10[0]['H'])
                # dayprevopen10 = float(daypreviouscandle10[0]['O'])
                # dayprevclose10 = float(daypreviouscandle10[0]['C'])				
                # daypreviouscandle11 = get_candles(market, 'day')['result'][-12:]
                # dayprevdate11 = (daypreviouscandle11[0]['T'])
                # split_string = dayprevdate11.split("T", 1)
                # dayprevdate11 = split_string[0]
                # dayprevdate11 = datetime.date(*(int(s) for s in dayprevdate11.split('-')))
                # dayprevlow11 = float(daypreviouscandle11[0]['L'])
                # dayprevhigh11 = float(daypreviouscandle11[0]['H'])
                # dayprevopen11 = float(daypreviouscandle11[0]['O'])
                # dayprevclose11 = float(daypreviouscandle11[0]['C'])				
                # daypreviouscandle12 = get_candles(market, 'day')['result'][-13:]
                # dayprevdate12 = (daypreviouscandle12[0]['T'])
                # split_string = dayprevdate12.split("T", 1)
                # dayprevdate12 = split_string[0]
                # dayprevdate12 = datetime.date(*(int(s) for s in dayprevdate12.split('-')))
                # dayprevlow12 = float(daypreviouscandle12[0]['L'])
                # dayprevhigh12 = float(daypreviouscandle12[0]['H'])
                # dayprevopen12 = float(daypreviouscandle12[0]['O'])
                # dayprevclose12 = float(daypreviouscandle12[0]['C'])				
                # daypreviouscandle13 = get_candles(market, 'day')['result'][-14:]
                # dayprevdate13 = (daypreviouscandle13[0]['T'])
                # split_string = dayprevdate13.split("T", 1)
                # dayprevdate13 = split_string[0]
                # dayprevdate13 = datetime.date(*(int(s) for s in dayprevdate13.split('-')))
                # dayprevlow13 = float(daypreviouscandle13[0]['L'])
                # dayprevhigh13 = float(daypreviouscandle13[0]['H'])
                # dayprevopen13 = float(daypreviouscandle13[0]['O'])
                # dayprevclose13 = float(daypreviouscandle13[0]['C'])				
                # daypreviouscandle14 = get_candles(market, 'day')['result'][-15:]
                # dayprevdate14 = (daypreviouscandle14[0]['T'])
                # split_string = dayprevdate14.split("T", 1)
                # dayprevdate14 = split_string[0]
                # dayprevdate14 = datetime.date(*(int(s) for s in dayprevdate14.split('-')))
                # dayprevlow14 = float(daypreviouscandle14[0]['L'])
                # dayprevhigh14 = float(daypreviouscandle14[0]['H'])
                # dayprevopen14 = float(daypreviouscandle14[0]['O'])
                # dayprevclose14 = float(daypreviouscandle14[0]['C'])				

				
				
                # data = [[dayprevdate14, dayprevopen14, dayprevhigh14, dayprevlow14, dayprevclose14], [dayprevdate13, dayprevopen13, dayprevhigh13, dayprevlow13, dayprevclose13], [dayprevdate12, dayprevopen12, dayprevhigh12, dayprevlow12, dayprevclose12], [dayprevdate11, dayprevopen11, dayprevhigh11, dayprevlow11, dayprevclose11], [dayprevdate10, dayprevopen10, dayprevhigh10, dayprevlow10, dayprevclose10], [dayprevdate9, dayprevopen9, dayprevhigh9, dayprevlow9, dayprevclose9], [dayprevdate8, dayprevopen8, dayprevhigh8, dayprevlow8, dayprevclose8], [dayprevdate7, dayprevopen7, dayprevhigh7, dayprevlow7, dayprevclose7], [dayprevdate6, dayprevopen6, dayprevhigh6, dayprevlow6, dayprevclose6], [dayprevdate5, dayprevopen5, dayprevhigh5, dayprevlow5, dayprevclose5], [dayprevdate4, dayprevopen4, dayprevhigh4, dayprevlow4, dayprevclose4], [dayprevdate3, dayprevopen3, dayprevhigh3, dayprevlow3, dayprevclose3], [dayprevdate2, dayprevopen2, dayprevhigh2, dayprevlow2, dayprevclose2], [dayprevdate, dayprevopen, dayprevhigh, dayprevlow, dayprevclose], [daycurrentdate, daycurrentopen, daycurrenthigh, daycurrentlow, daycurrentclose]]
                # df = pd.DataFrame(list(data), columns=['Date', 'Open', 'High', 'Low', 'Close'])
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

                # src_dir = "/root/PycharmProjects/cryptobot/images/"
                # dst_dir = "/var/www/html/images/"
                # for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
                    # shutil.copy(pngfile, dst_dir)

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
