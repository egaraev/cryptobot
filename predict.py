from stock_prediction import create_model, load_data, np
from parameters import *
import os
import glob
import shutil
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from yahoo_fin import stock_info as si
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import re
import pymysql
import pandas as pd
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
import requests
import datetime
now = datetime.datetime.now()
from datetime import timedelta, date
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
futuredate = date.today() + timedelta(days=30)


###
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE enabled=1 and ai_active=1")
markets=cursor.fetchall()
#date_now = time.strftime("%Y-%m-%d")
from PIL import Image, ExifTags


def main():
    print('Starting neural-analyse prediction module')

    neural()


def neural():
    for market in markets: #Loop trough the stock summary
        try:
          market=(market[0])
          name=market_full_name(market, 1)
          previous_predicted_price = market_full_name(market, 75)
#          print (previous_predicted_price)
          ticker= market
          print ("Now lets test the model")
#          print (ticker, futuredate)
          ticker_data_filename = os.path.join("/root/PycharmProjects/cryptobot/data", f"{ticker}_{date_now}.csv")
          print ("model name to save")
          model_name = f"{date_now}_{ticker}-{LOSS}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"

          print ("load the data")
          data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS, shuffle=False)

          # construct the model
          model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          model_path = os.path.join("/root/PycharmProjects/cryptobot/results", model_name) + ".h5"
          model.load_weights(model_path)

          # evaluate the model
          mse, mae = model.evaluate(data["X_test"], data["y_test"])
          # calculate the mean absolute error (inverse scaling)
          mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform(mae.reshape(1, -1))[0][0]
          print("Mean Absolute Error:", mean_absolute_error)
          # predict the future price
          future_price = predict(model, data)
          print (future_price, futuredate)
          if future_price<previous_predicted_price:
             ai_direction="DOWN"
          else:
             ai_direction="UP"
          printed = (market, f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
          try:
              db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
              cursor = db.cursor()
              cursor.execute("update markets set predicted_price='%s', ai_direction='%s'  where market='%s'" % (future_price, ai_direction, market))
              cursor.execute('insert into logs(date, log_entry) values("%s", "%s")', (currenttime, printed))			  
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()
			  
          print (date_exist(market, futuredate))
		  
          if date_exist(market, futuredate) != 1:
             try:
                 db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
                 cursor = db.cursor()
                 cursor.execute('insert into history(predicted_price, date, market) values("%s", "%s", "%s")' % (future_price, futuredate, market))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()
		  


          print(f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
          print("Accuracy Score:", get_accuracy(model, data))
          plot_graph(model, data, name)
          newfilename=("{}_result.png".format(market))
          my_path = "/root/PycharmProjects/cryptobot/images/results.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/cryptobot/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)



        except:
            continue


					
def date_exist(marketname, futuredate):
    db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM history WHERE market = '%s' and date='%s'" % (market, futuredate))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return 1

        else:
            return 0


def plot_graph(model, data, name):
    y_test = data["y_test"]
    X_test = data["X_test"]
    y_pred = model.predict(X_test)
    y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(np.expand_dims(y_test, axis=0)))
    y_pred = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(y_pred))
    plt.close()
    plt.plot(y_test[-200:], c='b')
    plt.plot(y_pred[-200:], c='r')
    plt.title(name)
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend(["Actual Price", "Predicted Price"])
    plt.savefig('/root/PycharmProjects/cryptobot/images/results.png')
    plt.show()


def get_accuracy(model, data):
    y_test = data["y_test"]
    X_test = data["X_test"]
    y_pred = model.predict(X_test)
    y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(np.expand_dims(y_test, axis=0)))
    y_pred = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(y_pred))
    y_pred = list(map(lambda current, future: int(float(future) > float(current)), y_test[:-LOOKUP_STEP], y_pred[LOOKUP_STEP:]))
    y_test = list(map(lambda current, future: int(float(future) > float(current)), y_test[:-LOOKUP_STEP], y_test[LOOKUP_STEP:]))
    return accuracy_score(y_test, y_pred)


def predict(model, data, classification=False):
    # retrieve the last sequence from data
    last_sequence = data["last_sequence"][:N_STEPS]
    # retrieve the column scalers
    column_scaler = data["column_scaler"]
    # reshape the last sequence
    last_sequence = last_sequence.reshape((last_sequence.shape[1], last_sequence.shape[0]))
    # expand dimension
    last_sequence = np.expand_dims(last_sequence, axis=0)
    # get the prediction (scaled from 0 to 1)
    prediction = model.predict(last_sequence)
    # get the price (by inverting the scaling)
    predicted_price = column_scaler["adjclose"].inverse_transform(prediction)[0][0]
    return predicted_price


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
