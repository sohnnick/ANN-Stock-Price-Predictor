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

def next_seven_days(scaled_data, model, scaler):
	# get the most recent past 60 days
	running_60_days = list(scaled_data[len(scaled_data)-60:].reshape(-1))

	for i in range(0, 7):
		running_np = np.array(running_60_days).reshape(1,-1,1)
		next_day = model.predict(running_np)[0][0]
		running_60_days.pop(0)
		running_60_days.append(next_day)

	next_seven_days = scaler.inverse_transform(
		np.array(running_60_days[len(running_60_days)-7:]).reshape(-1,1))

	next_seven_days = list(next_seven_days.reshape(-1))

	return next_seven_days