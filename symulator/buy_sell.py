import pandas as pd
import numpy as np
import ast
import time
import pymysql


#Read the data for fivemin
dictionary = []
try:
    file = open("../data/hist_data_fivemin.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary.append(i)
    file.close()
except:
    print("Unable to read the file")
	
df = pd.DataFrame(dictionary, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])

df['T'] = pd.to_datetime(df['T'])
arr = df["T"].to_numpy()
arr = np.datetime_as_string(arr, unit='D')
dates_list = arr.tolist()
df['day'] = dates_list



#Read the data for day
dictionary_day = []
try:
    file = open("../data/hist_data_day.txt", "r")
    contents = file.read()
    tuples = ast.literal_eval(contents)
    for i in tuples:	
        dictionary_day.append(i)
    file.close()
except:
    print("Unable to read the file")
	
df_day = pd.DataFrame(dictionary_day, columns=['O', 'H', 'L', 'C', 'V', 'T', 'BV'])	
df_day['T'] = pd.to_datetime(df_day['T'])


#Start the main function
def main():
    for index, row in df.iterrows():
       fivemin_day = str(df.iloc[index]['day'])
       buy(row)
       if index % 3 == 0:
          #heikin_ashi(df_day, fivemin_day, row)
          #candles(df_day, fivemin_day, row)	
          #obv(df_day, fivemin_day, row)
          #macd(df_day, fivemin_day, row)	  
          time.sleep(5)




def buy(row):
        print ("Starting buying mechanizm")
        buy_size = parameters()[0]	
        market= "USD-BTC"
        #timestamp = int(time.time())
        #day_close = summary['PrevDay']   #Getting day of closing order
    #Current prices
        last = float(row['C'])  #last price
    #HOW MUCH TO BUY
        buy_quantity = buy_size / last
        print (row['T'], last)		



def heikin_ashi(df_day, fivemin_day, row):
        print ("Starting heikin ashi module")
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-14:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date 		
        #print (df_day)




def candles(df_day, fivemin_day, row):
        print ("Starting candles module")
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-15:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume' }, axis=1, inplace=True)
        df_day = df_day[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date  		
        #print (df_day)


def obv(df_day, fivemin_day, row):
        print ("Starting obv module")
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-15:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name		
        #print (df_day)


def macd(df_day, fivemin_day, row):
        print ("Starting macd module")
        df_day_today = df_day.loc[df_day['T'] == fivemin_day]
        df_day_index = int(df_day_today.index.tolist()[0])
        df_day = df_day.iloc[df_day_index-15:df_day_index]	
        df_day = df_day.append(row, ignore_index=True)
        del df_day["day"]
        del df_day["BV"]
        df_day.rename({ 'T': 'date', 'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close', 'V': 'volume' }, axis=1, inplace=True)
        df_day['adjclose'] = df_day['close'].values
        df_day = df_day[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df_day['date'] = pd.to_datetime(df_day['date']).dt.date 
        del df_day.index.name
        df_day.set_index('date', inplace=True)
        del df_day.index.name
        #print (df_day)





def parameters():
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb_simulator")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21]), (row[22]), (row[23]), (row[24]), (row[25]), (row[26]), (row[27]), (row[28]), (row[29]), (row[30]), (row[31]), (row[32])

    return 0



if __name__ == "__main__":
    main()
