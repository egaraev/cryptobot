#import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import config
from keras.layers.core import Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import urllib2
import os
import json
import pandas as pd
from pybittrex.client import Client
import MySQLdb
import sys


c = Client(api_key=config.key, api_secret=config.secret)

currtime = int(round(time.time()))
starttime = str(currtime - 16000000) #for 1800 period 6 month
#starttime = str(millis - 64000000) #for 7200 period 24 month
period = str(1800)
epochs = 50



for arg in sys.argv[1:]:
    #print arg
    market = arg
    #if market =='BTC-QTUM' or market == 'BTC-NEO' or market == 'BTC-XLM' or market =='BTC-VTC' or market =='BTC-XRP':
     #   pass



def prediction_info(marketname):
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT ai_price, ai_time, ai_direction FROM markets WHERE active =1 and ai_active=1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0]), (row[1]), (row[2])
    return 0



def convertSeriesToMatrix(vectorSeries, sequence_length):
    matrix = []
    for i in range(len(vectorSeries) - sequence_length + 1):
        matrix.append(vectorSeries[i:i + sequence_length])
    return matrix


# random seed
np.random.seed(1234)


def main():
    print('Starting deep learning module')

    learn()


def learn():
    #market = 'BTC-XLM'
    currency = market.split('-')[1]
    #currtime = int(round(time.time()))
    current_price = c.get_ticker('BTC-' + currency).json()['result']['Last']
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    #print market, currtime, prediction_info(market)[1]

    if (int(currtime) - int(prediction_info(market)[1])) >= 3600:
        # print market, prediction_info(market)[2]
        #          ---------================DATA COLLECTION====================------------
        # connect to poloniex's API
        if currency == 'BCC':
            url = (
            'https://poloniex.com/public?command=returnChartData&currencyPair=' + 'BTC_BCH' + '&start=' + starttime + '&end=9999999999&period=' + period)  # 1800
        # url = ('https://poloniex.com/public?command=returnChartData&currencyPair='+currency+'&start='+starttime+'&end=9999999999&period=14400')
        else:
            url = (
            'https://poloniex.com/public?command=returnChartData&currencyPair=' + 'BTC_' + currency + '&start=' + starttime + '&end=9999999999&period=' + period)

        # url = ('https://poloniex.com/public?command=returnChartData&currencyPair='+currency+'&start='+starttime+'&end=9999999999&period=14400')

        # parse json returned from the API to Pandas DF
        openUrl = urllib2.urlopen(url)
        r = openUrl.read()
        openUrl.close()
        d = json.loads(r.decode())
        df = pd.DataFrame(d)

        datPath = 'data/'
        if not os.path.exists(datPath):
            os.mkdir(datPath)

        original_columns = [u'date', u'high', u'low', u'open', u'close']
        new_columns = ['date', 'high', 'low', 'open', 'close']
        df = df.loc[:, original_columns]
        df.columns = new_columns
        cols = list(df)
        cols.insert(1, cols.pop(cols.index('open')))
        df = df.reindex(columns=cols)

        df.to_csv('data/cryptodata' + 'BTC-' + currency + '.csv', index=None)

        path_to_dataset = ('data/cryptodata' + 'BTC-' + currency + '.csv')
        sequence_length = 20

        # vector to store the time series
        vector_vix = []
        with open(path_to_dataset) as f:
            next(f)  # skip the header row
            for line in f:
                fields = line.split(',')
                vector_vix.append(float(fields[4]) * 10)

                # convert the vector to a 2D matrix
        matrix_vix = convertSeriesToMatrix(vector_vix, sequence_length)

        # shift all data by mean
        matrix_vix = np.array(matrix_vix)
        shifted_value = matrix_vix.mean()
        matrix_vix -= shifted_value
        print "Data  shape: ", matrix_vix.shape

        # split dataset: 90% for training and 10% for testing
        train_row = int(round(0.9 * matrix_vix.shape[0]))
        train_set = matrix_vix[:train_row, :]

        # shuffle the training set (but do not shuffle the test set)
        np.random.shuffle(train_set)
        # the training set
        X_train = train_set[:, :-1]
        # the last column is the true value to compute the mean-squared-error loss
        y_train = train_set[:, -1]
        # the test set
        X_test = matrix_vix[train_row:, :-1]
        y_test = matrix_vix[train_row:, -1]

        # the input to LSTM layer needs to have the shape of (number of samples, the dimension of each element)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        # build the model
        model = Sequential()
        # layer 1: LSTM
        model.add(LSTM(input_dim=1, output_dim=50, return_sequences=True))
        model.add(Dropout(0.2))
        # layer 2: LSTM
        model.add(LSTM(output_dim=100, return_sequences=False))
        model.add(Dropout(0.2))
        # layer 3: dense
        # linear activation: a(x) = x
        model.add(Dense(output_dim=1, activation='linear'))
        # compile the model
        model.compile(loss="mse", optimizer="rmsprop")

        # train the model
        model.fit(X_train, y_train, batch_size=512, nb_epoch=epochs, validation_split=0.05, verbose=1)

        # evaluate the result
        test_mse = model.evaluate(X_test, y_test, verbose=1)
        # print '\nThe mean squared error (MSE) on the test data set is %.3f over %d test samples.' % (test_mse, len(y_test))

        # get the predicted values
        predicted_values = model.predict(X_test)
        num_test_samples = len(predicted_values)
        predicted_values = np.reshape(predicted_values, (num_test_samples, 1))

        # plot the results
        # fig = plt.figure()
        # plt.plot(y_test + shifted_value)
        # plt.plot(predicted_values + shifted_value)
        # plt.xlabel('Date')
        # plt.ylabel('BTC-' + currency)
        # plt.show()


        # save the result into txt file
        test_result = zip(predicted_values, y_test) + shifted_value
        np.savetxt('results/output_result_' + 'BTC_' + currency + '.txt', test_result)

        # with open('results/output_result_'+'BTC_'+currency+'.txt', 'a') as myfile:
        #    myfile.write(str(current_price)+'      '+str(currenttime+'\n'))


        with open('results/output_result_' + 'BTC_' + currency + '.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]  # should be -1
            last_word = last_line.split()[0]
            last_word2 = last_line.split()[1]
            # mean_price = (float(last_word) + float(last_word2)) / 2
            mean_price = float(last_word) / 10
            predicted_price = format(float(mean_price), '.6f')

        last_word = float(last_word) / 10

        if last_word > current_price:
            direction = 'UP'
        elif last_word < current_price:
            direction = 'DOWN'
        else:
            direction = 'NEUTRAL'

        with open('results/output_result_' + 'BTC_' + currency + '.txt', 'a') as myfile:
            myfile.write(
                '2 The predicted  price is  ' + str(predicted_price) + '    Current time is:  ' + str(
                    currenttime + '   Current price is:   ' + str(
                        current_price) + '    Direction is: ' + direction + '\n'))

        print market, predicted_price, direction, last_word

        try:
            printed = ('      ' + str(currency) + '  2 The predicted  price is  ' + str(
                predicted_price) + '  Current time is:  ' + str(
                currenttime + '  Current price is:   ' + str(
                    current_price) + '   Direction is: ' + direction))
            db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
            cursor = db.cursor()
            cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
            cursor.execute(
                'update markets set ai_price = %s, ai_time = %s, ai_direction =%s where market =%s',
                (predicted_price, currtime, direction, market))
            db.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            db.close()
    else:
        pass


if __name__ == "__main__":
    main()
