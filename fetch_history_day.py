from yahoo_fin import stock_info as si
import sys, os
import ast
import json

df = si.get_data('BTC-USD')
df = df.iloc[: , :-1]
df = df[-62:]
df = df.reset_index().rename({'index':'date'}, axis = 'columns')

#print (df)
df.rename(columns={ 'date': 'T', 'open': 'O', 'high': 'H', 'low': 'L', 'close': 'C', 'volume': 'V' }, inplace=True)
del df['adjclose']
df['T'] = df['T'].dt.strftime('%Y-%m-%d')
result = df.to_dict('records')
#print (result)
last_date = result[-1]
today_date =last_date['T'] 
#print (today_date)


if result !=[]:
#   try: 
       full_dict =[]
       file = open("data/hist_data_day.txt", "r")
       contents = file.read()
       print(contents)	   
       dictionary = ast.literal_eval(contents)
       last_current_date=dictionary[-1]
       last_written_date = last_current_date['T']	
       if last_written_date == today_date: 	
          dict_without_last_day= dictionary[:-1]
          dict_without_last_day = list(dict_without_last_day)
          dict_without_last_day.append(last_date)
          full_dict = dict_without_last_day
       else:
          dict_with_last_day = list(dictionary)	
          dict_with_last_day.append(last_date)
          full_dict = dict_with_last_day
    
       print ("File was scanned")
       file.close()
       with open('data/hist_data_day.txt', 'w') as filehandle:
          for listitem in full_dict:
             filehandle.write('%s,' % listitem)
       filehandle.close()
       print ("File was written")

       with open('data/hist_data_day.txt', 'r') as file:
            data = file.read()[:-1]
       file.close()
       print ("File was read")
       with open('data/hist_data_day.txt', 'w') as file:
            file.write(data)
       file.close()
       print ("Daily data was updated")
#   except:
#       print("Unable to update the file")



else:
   print ("Result is empty")