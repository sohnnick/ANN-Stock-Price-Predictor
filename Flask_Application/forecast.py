import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost
from xgboost import XGBRegressor
import sklearn
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

from train_nn import *
from next_seven_days import *

def predictStockPrice(stock_dict):
	# create dataframe
	df_stock = pd.DataFrame({
	    "Date": stock_dict['Stock Dates'],
	    "Stock Close": stock_dict['Stock Close']
	})

	# train test split
	df_stock['Year'] = [x.split('-')[0] for x in list(df_stock['Date'])]
	df_stock['Month'] = [x.split('-')[1] for x in list(df_stock['Date'])]
	df_stock['Day'] = [x.split('-')[2] for x in list(df_stock['Date'])]

	df_nn = df_stock.copy()

	df_close = df_nn['Stock Close']
	np_close = df_close.values

	thresh = int(np.ceil(len(np_close)*.7))

	# scale dataset
	scaler = MinMaxScaler(feature_range=(0, 1)) 
	scaled_data = scaler.fit_transform(np_close.reshape(-1, 1))

	#Create the scaled training data set 
	train_data = scaled_data[0:thresh]

	#Split the data into x_train and y_train data sets
	x_train=[]
	y_train = []
	for i in range(60,len(train_data)):
	    x_train.append(train_data[i-60:i,0])
	    y_train.append(train_data[i,0])

	x_train, y_train = np.array(x_train), np.array(y_train)
	x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

	model = trainNN(x_train, y_train)

	# Test Data predictions
	test_data = scaled_data[thresh - 60: , : ]

	x_test = []
	y_test = np_close[thresh:]
	for i in range(60,len(test_data)):
	    x_test.append(test_data[i-60:i,0])

	x_test = np.array(x_test)
	x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

	# get predictions and rmse
	predictions = model.predict(x_test) 
	predictions = scaler.inverse_transform(predictions)
	rmse = np.sqrt(np.mean(((predictions - y_test)**2)))

	seven_days_ahead = next_seven_days(scaled_data, model, scaler)

	return predictions, seven_days_ahead, rmse