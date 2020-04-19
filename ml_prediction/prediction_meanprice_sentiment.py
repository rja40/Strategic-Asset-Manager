
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


symbols = ['ABT','AXP','CAT','KO','CL','TGT','XOM','F','LLY','MCD','CVS','PEP','CVX','TXN','TMO','UNP','WMT','JNJ','NKE','AAPL','HD','VZ','T','MO','HON','MSFT','ADBE','CSCO','GS','PM','BLK','FB','DUK','COP','RTX']
        
def inv_price_transform(normalized_data, scaler):
    ''' inverse from normalized price to raw price '''
    m = scaler.mean_[0]
    s = scaler.scale_[0]
    return s*np.array(normalized_data)+m

engine = create_engine('postgresql://postgres:postgres@localhost:5432/stocks')


stocks_df = pd.read_sql_query('select * from "stocks_prices"',con=engine)
econ_df = pd.read_csv('/home/asus/github_stockprediction/Stock-Prediction/demos/oecd.csv',header = 0)
sentiment_df = pd.read_csv('/home/asus/github_stockprediction/Stock-Prediction/demos/sentiment_score_0704.csv',header = 0)
news_df = pd.read_csv('/home/asus/github_stockprediction/Stock-Prediction/demos/news_sentiment.csv')

similarity_df = pd.read_csv('/home/asus/github_stockprediction/Stock-Prediction/demos/similarity_legalp.csv')

#stocks_df = stocks_df.loc[stocks_df['symbol'].isin(['AAPL'])]
similarity_df['date'] =  pd.to_datetime(similarity_df['date'])
similarity_df['year'] = similarity_df['date'].dt.year

stocks_df['formatted_date'] = pd.to_datetime(stocks_df['formatted_date'])
econ_df['TIME'] = pd.to_datetime(econ_df['TIME']+'-01')
sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
news_df['news_date'] = pd.to_datetime(news_df['news_date'])


sentiment_df = sentiment_df[['year','cik','uncertainity_score','positive_score','negative_score','polarity_score']]
stocks_df = pd.merge(stocks_df,sentiment_df,left_on = ['year','cik'],right_on = ['year','cik'],how = 'left')

stocks_df['BCI'] = stocks_df['formatted_date'].map(lambda x: x.replace(day=1)).map(econ_df.set_index('TIME')['BCI'])

stocks_df['CCI'] = stocks_df['formatted_date'].map(lambda x: x.replace(day=1)).map(econ_df.set_index('TIME')['CCI'])

stocks_df['CLI'] = stocks_df['formatted_date'].map(lambda x: x.replace(day=1)).map(econ_df.set_index('TIME')['CLI'])


stocks_df = pd.merge(stocks_df,news_df,left_on = 'formatted_date',right_on = 'news_date', how= 'left')
stocks_df = stocks_df.fillna(0)

stocks_df = pd.merge(stocks_df,similarity_df,left_on = ['year','cik'],right_on = ['year','cik'],how = "left")


def prepare_data(symbol,data):
     
    mask1 = data['symbol'] == symbol
    data = data.loc[mask1]
    print(data.shape)
    data = data.set_index('formatted_date')
    data.index = pd.to_datetime(data.index)
    print(data.head(10))
    data['mean_price'] = (data['open'] + data['close'] +data['low']+data['high'])/4
    return data[['mean_price','uncertainity_score','polarity_score','news_polarity_score','cosine_similar']]

def prepare_timeseries_data(symbol,data):
    
    print("Processing for company {}".format(symbol))
    n_train = 1104
    lookback = 30
    print(data.shape)
    print(data.tail(1))
    test_data = data.iloc[n_train:]
    data = data.values
    scaler = preprocessing.StandardScaler()
    scaler.fit(data[:n_train,:])
    data = scaler.transform(data)
    dataX, dataY = [], []
    
    for timepoint in range(data.shape[0]-lookback):
        dataX.append(data[timepoint:timepoint+lookback,:])
        dataY.append(data[timepoint+lookback,0])
    X_train, X_test = dataX[:n_train], dataX[n_train:]
    y_train, y_test = dataY[:n_train], dataY[n_train:]
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test), scaler

def plot_test_data(symbol,y_train,y_test,scaler):
    plt.rcParams["figure.figsize"] = (14,7)
    print("Processing for company {}".format(symbol))
    print("%i training examples, %i test examples" % (len(y_train), len(y_test)))
    plt.plot(range(len(y_train)), inv_price_transform(y_train, scaler), c='b', label='Training Data')
    plt.plot(range(len(y_train),len(y_test)+len(y_train)), inv_price_transform(y_test, scaler), c='r', label='Test Data')
    plt.title('Normalized Stock Price Data for {0}'.format(symbol))
    plt.xlabel('Day')
    plt.ylabel('Mean price')
    plt.legend()
    plt.savefig("/home/asus/file_project/train_test_plot_{0}.png".format(symbol))
    plt.show(block=False)
    plt.pause(3)
    plt.close()


# build model
model = Sequential()
model.add(LSTM(128, input_shape=(30,5), return_sequences=True))
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
    model.save('/home/asus/file_project/model_{0}.h5'.format(symbol))
    print("TRAINING DONE. %i seconds to train." % int(time.time()-t0))
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title('Training Losses')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.legend()
    plt.savefig("/home/asus/file_project/training_plot_{0}.png".format(symbol))
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
    plt.savefig("/home/asus/file_project/RMSE_{0}.png".format(symbol))
    plt.show(block=False)
    plt.pause(3)
    plt.close()


for symbol in symbols:
    print("Processing for company {}".format(symbol))
    stocks_data = prepare_data(symbol,stocks_df) 
    print(stocks_data.shape)
    x_train,y_train,x_test,y_test,scaler = prepare_timeseries_data(symbol,stocks_data)
    print("1: ",x_train.shape)
    print("2: ",y_train.shape)
    print("3: ",x_test.shape)
    print("4: ",y_test.shape)
    plot_test_data(symbol,y_train,y_test,scaler)
    run_model_and_save(symbol,x_train,y_train)
    calculate_rmse(x_test,y_test)
    
    pickle.dump(x_test, open("/home/asus/file_project/x_test_{0}.pkl".format(symbol), "wb" ) )
    pickle.dump(y_test, open("/home/asus/file_project/y_test_{0}.pkl".format(symbol), "wb" ) )
    pickle.dump(scaler,open("/home/asus/file_project/scaler_{0}.pkl".format(symbol), "wb" ) )





