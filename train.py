from parameters import *
from stock_prediction import create_model, load_data
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
import pandas as pd
from os import path
import glob
import shutil
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import re
import pymysql
import pandas as pd
from dateutil import parser
import requests
###
db = pymysql.connect("database-service", "cryptouser", "123456", "cryptodb")
cursor = db.cursor()
cursor.execute("SELECT market FROM markets WHERE enabled=1 and ai_active=1")
markets=cursor.fetchall()





def main():
    print('Starting neural-analyse training module')

    neural()


def neural():
    for market in markets: #Loop trough the stock summary
        try:
          market=(market[0])
          name=market_full_name(market, 3)
        # create these folders if they does not exist
          if not os.path.isdir("/root/PycharmProjects/cryptobot/results"):
             os.mkdir("/root/PycharmProjects/cryptobot/results")
          if not os.path.isdir("/root/PycharmProjects/cryptobot/logs"):
             os.mkdir("/root/PycharmProjects/cryptobot/logs")
          if not os.path.isdir("/root/PycharmProjects/cryptobot/data"):
             os.mkdir("/root/PycharmProjects/cryptobot/data")

          crypto=market[4:]
          market = crypto+"-USD"
          		  


          ticker = market
          ticker_data_filename = os.path.join("/root/PycharmProjects/cryptobot/data", f"{ticker}_{date_now}.csv")
          # model name to save
          model_name = f"{date_now}_{ticker}-{LOSS}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
          fileexist=("/root/PycharmProjects/cryptobot/results/"+ model_name+ ".h5")
          if path.exists(fileexist):
              print ("Model already trained")
          else:
              print ("Starting to train model")		 




#          # load the CSV file from disk (dataset) if it already exists (without downloading)
              if os.path.isfile(ticker_data_filename):
                  ticker = pd.read_csv(ticker_data_filename)

              print ("load the data")
              data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS)

              if not os.path.isfile(ticker_data_filename):
          # save the CSV file (dataset)
                 data["df"].to_csv(ticker_data_filename)

          # construct the model
              model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          # some tensorflow callbacks
              checkpointer = ModelCheckpoint(os.path.join("/root/PycharmProjects/cryptobot/results", model_name), save_weights_only=True, save_best_only=True, verbose=1)
              tensorboard = TensorBoard(log_dir=os.path.join("/root/PycharmProjects/cryptobot/logs", model_name))

              history = model.fit(data["X_train"], data["y_train"],
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_data=(data["X_test"], data["y_test"]),
                        callbacks=[checkpointer, tensorboard],
                        verbose=1)

              model.save(os.path.join("/root/PycharmProjects/cryptobot/results", model_name) + ".h5")
		  
              print ("Model trained")
		  
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
