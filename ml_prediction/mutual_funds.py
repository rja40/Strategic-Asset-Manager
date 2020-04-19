from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from sklearn import preprocessing
from datetime import datetime, timedelta
import time
from collections import Counter
import os
os.chdir('..')
from sqlalchemy import create_engine
import pickle
plt.rcParams["figure.figsize"] = (14,7)


import pandas as pd
from sqlalchemy import create_engine
from datetime import date
symbols = ['UMPSX', 'UMPIX', 'CGMRX', 'CSRSX', 'CSRIX', 'RYCVX', 'RYLDX', 'RYCYX', 'ARYCX', 'BREFX', 'FANIX', 'ORECX', 'ORENX', 'FAGNX', 'PAREX', 'FRESX', 'HFCIX', 'FARCX', 'FRSSX', 'HFCSX', 'FREAX', 'UBVSX', 'UBVAX', 'UBVLX', 'UBVRX', 'FSENX', 'VSTCX', 'FLCGX', 'KMDVX', 'QNTAX']
        
def inv_price_transform(normalized_data, scaler):
    m = scaler.mean_[0]
    s = scaler.scale_[0]
    return s*np.array(normalized_data)+m


mutual_df = pd.read_csv('/home/asus/Downloads/Top30MFdata.csv',header = 0)

def prepare_data(symbol,data):
     
    mask1 = data['symbol'] == symbol
    data = data.loc[mask1]
    print("data shape is",data.shape)
    data = data.set_index('formatted_date')
    data.index = pd.to_datetime(data.index)
    print(data.head(5))
    return data[['mean']]


def prepare_timeseries_data(symbol,data):
    
    print("Processing for company {}".format(symbol))
    n_train = 1104
    past_values = 30
    print(data.shape)
    print(data.tail(1))
    test_data = data.iloc[n_train:]
    scaler = preprocessing.StandardScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1,1))
    dataX, dataY = [], []
    for timepoint in range(scaled_data.shape[0]-past_values):
        dataX.append(scaled_data[timepoint:timepoint+past_values,:])
        dataY.append(scaled_data[timepoint+past_values,0])
    X_train, X_test = dataX[:n_train], dataX[n_train:]
    y_train, y_test = dataY[:n_train], dataY[n_train:]
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test), scaler


def plot_test_data(symbol,y_train,y_test,scaler):
    plt.rcParams["figure.figsize"] = (14,7)
    print("Processing for company {}".format(symbol))
    print("%i training examples, %i test examples" % (len(y_train), len(y_test)))
    plt.plot(range(len(y_train)), inv_price_transform(y_train, scaler), c='b', label='Training Data')
    plt.plot(range(len(y_train),len(y_test)+len(y_train)), inv_price_transform(y_test, scaler), c='r', label='Test Data')
    plt.title('Normalized mutual funds price data for {0}'.format(symbol))
    plt.xlabel('Day')
    plt.ylabel('Mean price')
    plt.legend()
    plt.savefig("/home/asus/file_project/mutual_funds/train_test_plot_{0}.png".format(symbol))
    plt.show(block=False)
    plt.pause(3)
    plt.close()


# build model
model = Sequential()
model.add(LSTM(128, input_shape=(30,1), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))    
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='rmsprop')
model.summary()



def run_model_and_save(symbol,X_train,y_train):
    plt.rcParams["figure.figsize"] = (14,7)
    t0 = time.time()
    history = model.fit(X_train,y_train,batch_size=32,epochs=100,validation_split=0.05)
    model.save('/home/asus/file_project/mutual_funds/model_{0}.h5'.format(symbol))
    print("TRAINING DONE. %i seconds to train." % int(time.time()-t0))
    #plot loss and validation loss
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title('Training Losses')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.legend()
    plt.savefig("/home/asus/file_project/mutual_funds/training_plot_{0}.png".format(symbol))
    plt.show(block=False)
    plt.pause(3)
    plt.close()



def calculate_rmse(x_test,y_test):# predict test set
    plt.rcParams["figure.figsize"] = (14,7)
    predictions = model.predict(x_test)
    print("RMSE: ", np.sqrt(np.mean((predictions-y_test)**2)))
    plt.plot(predictions, c='b', label='predictions')
    plt.plot(y_test, c='r', label='actual')
    plt.ylabel('Normalized mean price')
    plt.xlabel('Day')
    plt.title('Test Set Predictions for {0}'.format(symbol))
    plt.legend()
    plt.savefig("/home/asus/file_project/mutual_funds/RMSE_{0}.png".format(symbol))
    plt.show(block=False)
    plt.pause(3)
    plt.close()

for symbol in symbols:
    print("Processing for company {}".format(symbol))
    mutual_funds_data = prepare_data(symbol,mutual_df) 
    print(mutual_funds_data.shape)
    x_train,y_train,x_test,y_test,scaler = prepare_timeseries_data(symbol,mutual_funds_data)
    print("1: ",x_train.shape)
    print("2: ",y_train.shape)
    print("3: ",x_test.shape)
    print("4: ",y_test.shape)
    plot_test_data(symbol,y_train,y_test,scaler)
    run_model_and_save(symbol,x_train,y_train)
    calculate_rmse(x_test,y_test)
    
    pickle.dump(x_test, open("/home/asus/file_project/mutual_funds/x_test_{0}.pkl".format(symbol), "wb" ) )
    pickle.dump(y_test, open("/home/asus/file_project/mutual_funds/y_test_{0}.pkl".format(symbol), "wb" ) )
    pickle.dump(scaler,open("/home/asus/file_project/mutual_funds/scaler_{0}.pkl".format(symbol), "wb" ) )

