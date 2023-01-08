import re
import pandas as pd
import pymysql
import numpy as np
from sklearn.model_selection import train_test_split
import csv
pd.options.mode.chained_assignment = None
from sklearn.naive_bayes import GaussianNB

header = ["'HA", 'Day_candle_direction', 'Candle_score', 'AI_direction', 'Tweet_positive', 'Tweet_negative', 'Tweet_ratio', 'Tweet_polarity', 'Candle_pattern', 'News_score', 'Hour_candle_direction', 'Trend', 'MACD', 'OBV']



orderlist = []
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
cursor = db.cursor()
cursor.execute("SELECT params FROM orders where active = 0")
orders=cursor.fetchall()
for i in orders:
   orderlist.append(str(i))

#print(orderlist)

resultlist = []
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
cursor = db.cursor()
cursor.execute("SELECT percent_serf, percent_serf_max FROM orders where active = 0")
results=cursor.fetchall()
for i in results:
   resultlist.append(str(i))

#print (resultlist)

final_result_list = []
for i in resultlist:
    words = (i.replace('(', ''))
    words = (words.replace(')', ''))	
    splited= words.split(",")
    serf =  float(splited[0])
    max = 	float(splited[1])
    #print (serf, max)	
    if serf <0 and max <2:
       success = 0
    else:
       success = 1	
    final_result_list.append(success)
	
#print (final_result_list)

new_order_list = []
for order in orderlist:
    #print (order)
    words = (order.replace('(', ''))
    words = (words.replace(',)', ''))
    clean = str(words[:1] + words[3:])
    clean = clean.rstrip(clean[-1])
    new_string = clean.replace("Candle_pattern:  ", "Candle_pattern: 0" )	
    #print (new_string)	
    words_new = re.split(':|/| ', new_string)

    str_list = list(filter(None, words_new))
    #print(str_list)
    K = '%'
    test_list = [i for i in str_list if i != K]
    #print(test_list)    
    try:
       for i in  header:
           test_list.remove(i)
           #print(test_list)		   
       #print(test_list)
       new_order_list.append(test_list)	   
  		   
    except ValueError:
       pass  # do nothing!	

    
#print(new_order_list)

final_list = []
for f, b in zip(new_order_list, final_result_list):
    res = [str(b)]
    new_order = f + res
    final_list.append(new_order)	
	
    
#print (final_list)	   


columnz = ['HA', 'Day_candle_direction', 'Candle_score', 'AI_direction', 'Tweet_positive', 'Tweet_negative', 'Tweet_ratio', 'Tweet_polarity', 'Candle_pattern', 'News_score', 'Hour_candle_direction', 'Trend', 'Trend_percent', 'MACD', 'OBV', 'Result']




with open("out.csv", 'w') as fileObj:
    writerObj = csv.writer(fileObj)
    # Add header to csv file
    writerObj.writerow(columnz)
    # Add list of lists as rows to the csv file
    writerObj.writerows(final_list)

data = pd.read_csv('out.csv',sep=',')


data.HA[data.HA =='DOWN'] = 1
data.HA[data.HA =='Revers-DOWN'] = 2
data.HA[data.HA =='STABLE'] = 3
data.HA[data.HA =='Revers-UP'] = 4
data.HA[data.HA =='UP'] = 5

data.Day_candle_direction[data.Day_candle_direction =='D'] = 1
data.Day_candle_direction[data.Day_candle_direction =='U'] = 2

data.AI_direction[data.AI_direction =='DOWN'] = 1
data.AI_direction[data.AI_direction =='UP'] = 2

# data.Candle_pattern[data.Candle_pattern =='T_b_c-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='T_w_s-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='T_b_g-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='T_t-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='T_b-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='E_S-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='M_S-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='BU_HR-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='BE_HR-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='BU_R-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='BE_R-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='SS_BE-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='SS_BU-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='Be_E-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='Bu_E-^'] = 2
# data.Candle_pattern[data.Candle_pattern =='P_L-^'] = 1
# data.Candle_pattern[data.Candle_pattern =='H_M_Be-v'] = 1
# data.Candle_pattern[data.Candle_pattern =='H_M_Bu-^'] = 2

data.Hour_candle_direction[data.Hour_candle_direction =='D'] = 1
data.Hour_candle_direction[data.Hour_candle_direction =='U'] = 2

data.Trend[data.Trend =='Fluctuating'] = 1
data.Trend[data.Trend =='Peak'] = 2
data.Trend[data.Trend =='Afterpeak'] = 3

data.MACD[data.MACD =='Buy'] = 1
data.MACD[data.MACD =='Sell'] = 2

data.OBV[data.OBV =='Buy'] = 1
data.OBV[data.OBV =='Sell'] = 2


df = data


df = df.drop(['Candle_pattern'],axis=1)

#df = df.drop(['Trend_percent'],axis=1)
df = df.drop(['Tweet_negative'],axis=1)
df = df.drop(['Tweet_positive'],axis=1)



# shift column 'C' to first position
first_column = df.pop('Result')
  
# insert column using insert(position,column_name,first_column) function
df.insert(0, 'Result', first_column)


newdf = df.copy()
df = df.append(newdf, ignore_index = True)


print (df.to_string())

####################################################################
###################################################################
# Separate the dataframe into X and y data
X = df.values
y = df['Result'].values

# Delete the Result column from X
X = np.delete(X,0,axis=1)


# Split the dataset into 70% Training and 30% Test
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4,random_state=0)


# Using simple Naive Bayes classifier
nb_clf = GaussianNB()
nb_clf.fit(X_train, y_train)
print(nb_clf.score(X_test, y_test))


# HA =='DOWN' = 1
# HA =='Revers-DOWN' = 2
# HA =='STABLE' = 3
# HA =='Revers-UP' = 4
# HA =='UP' = 5
# Candle_direction =='D' = 1
# Candle_direction =='U' = 2
# AI_direction =='DOWN' = 1
# AI_direction =='UP' = 2
# Candle_pattern =='T_b_c-v', 'T_b_g-v', 'T_t-v', 'E_S-v', 'BE_HR-v', 'BE_R-v', 'SS_BE-v', 'SS_BU-v', 'Be_E-v', 'H_M_Be-v' = 1
# Candle_pattern =='T_w_s-^', 'T_b-^', 'M_S-^', 'BU_HR-^', 'BU_R-^', 'Bu_E-^', 'P_L-^', 'H_M_Bu-^' = 2
# H_candle_dir =='D' = 1
# H_candle_dir =='U' = 2
# Trend =='Fluctuating' = 1
# Trend =='Peak' = 2
# Trend =='Afterpeak' = 3
# MACD =='Buy' = 1
# MACD =='Sell' = 2
# OBV =='Buy' = 1
# OBV =='Sell' = 2



ha = 3
candle_dir = 1
candle_score = 0
ai_dir = 1
# tw_pos = 10.82
# tw_neg = 25.25
tw_ratio = 1
tw_pol = 0.25
# tw_score = 1.0
# candle_pat = 1
news_score = 0.9
h_candle_dir = 1
trend = 2
trend_perc = 10
macd = 1
obv = 1


    
#HA Candle_direction Candle_score AI_direction Tweet_positive Tweet_negative Tweet_ratio Tweet_polarity Tweet_score Candle_pattern News_score H_candle_dir Trend Trend_percent MACD OBV

y_pred = nb_clf.predict([[ha,candle_dir,candle_score,tw_ratio,tw_pol,news_score,h_candle_dir,trend,trend_perc,macd,obv]])


  
print(y_pred)





























