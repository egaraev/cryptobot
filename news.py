import sys
import os
import re
import pymysql
import pandas as pd
from dateutil import parser
import requests
from bs4 import BeautifulSoup
import json
import urllib
import urllib.request
from urllib.request import urlopen
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y/%m/%d")

import subprocess
import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

#currentdate="2020/07/24"

###
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT * FROM markets WHERE active=1")
markets=cursor.fetchall()
###

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = {'User-Agent': user_agent}

def main():
    print('Starting news module')

    news()


def news():
    for market in markets: #Loop trough the stock summary
        try:
          market=(market[1])
          market_id=(market[0])
          name=market_full_name(market, 71)
          #name = (market[71])
          print (name)
          subprocess.check_call('curl https://transcriptdaily.com/?s='+name+'>news/news.'+market+'', shell=True)
		  
		  
          #GET LINKS
          f1 = open("news/news."+market+"", "r")
          html=f1.read()
          bs = BeautifulSoup(html , 'html.parser')
          links = bs.findAll("div", {"id": "wrap"})
          links = bs.findAll("div", {"class": "width-limiter main-content"})
          links = bs.findAll("p", {"class": "postmeta"})
          links = bs.findAll("section", {"class": "archive"})
          links = bs.findAll("div", {"class": "entry"})
          #print (links)
          links = bs.findAll('a')
          urls = [link.get('href') for link in links]
          #urls = [url for url in urls if url is not None]
          news_urls = [url for url in urls if   '/'+currentdate+'/' in url]
          stock_urls=news_urls[:1]
          del stock_urls[1::2]
          #print (stock_urls)		  
		  
		  
		  
		  #GET TITLES
          bs = BeautifulSoup(html , 'html.parser')
          titles = bs.findAll("div", {"id": "wrap"})
          titles = bs.findAll("div", {"class": "width-limiter main-content"})
          titles = bs.findAll("p", {"class": "postmeta"})
          titles = bs.findAll("section", {"class": "archive"})
          titles = bs.findAll("div", {"class": "entry"})
          stock_titles_summ=[]
          for i in range (0, 1):
             stock_titles = str(titles[i].text)
             stock_titles=[str(stock_titles.strip())]
             stock_titles_summ +=stock_titles
          stock_titles= str(stock_titles_summ[0])   
          #print (stock_titles)


          #GET DATES
          bs = BeautifulSoup(html , 'html.parser')
          dates = bs.findAll("div", {"id": "wrap"})
          dates = bs.findAll("div", {"class": "width-limiter main-content"})
          dates = bs.findAll("p", {"class": "postmeta"})
          dates = bs.findAll("section", {"class": "archive"})
          dates = bs.findAll("div", {"class": "entry"})
          dates = bs.findAll('a')
          urls = [link.get('href') for link in links]
          urls = [url for url in urls if url is not None]
          dates_urls = [url for url in urls if   '/'+currentdate+'/' in url]
          del dates_urls[1::2]
          stock_dates_summ=''
          for i in range (0, 1):
             dates = dates_urls[i]
             dates = dates[28:]
             dates = dates[:10]
#             dates=[dates]
             stock_dates_summ +=dates
          stock_dates= stock_dates_summ
          #print (stock_dates)		 
		  
		  		  
          #GET NEWS TEXT
          stock_text_summ=[]
          for i in range (0, 1):
             news_html = requests.get(news_urls[i], headers=headers).content	
             news_soup = BeautifulSoup(news_html, 'html.parser')
             paragraphs = [par.text for par in news_soup.find_all('p')]
             paragraphs=[paragraphs[3:]]
         #    print (paragraphs)
             stock_text_summ +=paragraphs
          stock_articles=str(stock_text_summ[0])
          print (stock_articles)		  

          f1.close()


          open("csvs/tmp-sql-2.txt", "w").close()
          open("csvs/tmp-sql.txt", "w").close()
          f = open("/root/PycharmProjects/cryptobot/csvs/tmp-sql.txt", "a")
          print(stock_articles, file=f)
          print ('\n', file=f)
          f.close()
			 
          f = open("/root/PycharmProjects/cryptobot/csvs/tmp-sql.txt", "r", newline="\n")
          news_text= (f.read())
          try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute('update markets set news_text = %s where market=%s',(news_text, market))
                 db.commit()
          except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
          finally:
                 db.close()


          f2 = open("/root/PycharmProjects/cryptobot/csvs/tmp-sql-2.txt", "a")
          print(stock_titles, file=f2)
          print(stock_dates, file=f2)
          passage=(stock_articles)
          print ("Sentiment Score: ", round(sia.polarity_scores(passage)['compound'], 2), file=f2) 
          print('<a href="'+stock_urls[0]+'">'+stock_urls[0]+'</a>', file=f2)
          print ('\n', file=f2)
          f2.close()
          f2 = open("/root/PycharmProjects/cryptobot/csvs/tmp-sql-2.txt", "r", newline="\n")
          news= (f2.read())

          printed = (market, stock_titles)


             
          try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute('update markets set news = %s where market=%s',(news, market))
                 cursor.execute('insert into logs(date, log_entry) values("%s", "%s")', (currenttime, printed))
                 db.commit()
          except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
          finally:
                 db.close()



          f2.close()
          f.close()



        except:
            continue





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

