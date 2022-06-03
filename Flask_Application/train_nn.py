import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import xgboost
# from xgboost import XGBRegressor
import sklearn
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

def trainNN(x_train, y_train):

	model = Sequential()
	model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
	model.add(LSTM(units=50, return_sequences=False))
	model.add(Dense(units=25))
	model.add(Dense(units=1))

	model.compile(optimizer='adam', loss='mean_squared_error')

	model.fit(x_train, y_train, batch_size=1, epochs=1)

	return model