import requests
import datetime
from datetime import datetime, timezone, date, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import tweepy
import json
import yfinance as yf


def getStockInfo(ticker):
	# Polygon.io API
	api_key = 'Y4rX3YscZ6FnAuzRIVVWaYzneuZJwlTl'

	company_response = requests.get('https://api.polygon.io/v1/meta/symbols/' + ticker
                               + '/company?apiKey=' + api_key)
	stock_info = dict(company_response.json())

	company_response = requests.get('https://api.polygon.io/vX/reference/financials?ticker=' + ticker
                                +'&apiKey=' + api_key)
	stock_financials = dict(company_response.json())

	# Yahoo Finance API
	url = "https://yh-finance.p.rapidapi.com/stock/v2/get-chart"

	querystring = {"interval":"1d","symbol": ticker,"range":"5y","region":"US"}

	headers = {
	    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
	    'x-rapidapi-key': "a8ff9fd49amsh64d09f9fe39d03fp1de1d0jsn90f0fdef076b"
	    }

	response = requests.request("GET", url, headers=headers, params=querystring)

	stock_price_chart = dict(response.json())['chart']['result'][0]

	stock_meta = stock_price_chart['meta']
	stock_dates = [datetime.fromtimestamp(x) for x in stock_price_chart['timestamp']]
	stock_dates = [str(x.year) + '-' + str(x.month) + '-' + str(x.day) for x in stock_dates]
	stock_low = stock_price_chart['indicators']['quote'][0]['low']
	stock_high = stock_price_chart['indicators']['quote'][0]['high']
	stock_open = stock_price_chart['indicators']['quote'][0]['open']
	stock_close = stock_price_chart['indicators']['quote'][0]['close']
	stock_volume = stock_price_chart['indicators']['quote'][0]['volume']
	update_date = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) 

	# yfinance api
	ticker_yf = yf.Ticker(ticker)
	yf_info = ticker_yf.info
	yf_news = ticker_yf.news[0:5]

	# create dict
	stock_dict = {
	    "Ticker":ticker,
	    "Stock Info": stock_info,
	    "YF Info": yf_info, 
	    "YF News": yf_news,
	    "Stock Financials": stock_financials,
	    "Stock Meta": stock_meta,
	    "Stock Dates": stock_dates,
	    "Stock Low": stock_low,
	    "Stock High": stock_high,
	    "Stock Open": stock_open,
	    "Stock Close": stock_close,
	    "Stock Volume": stock_volume,
	    "Last-Update": update_date
	}

	url = 'https://stock-price-predictor-af4ea-default-rtdb.firebaseio.com/'
	ticker_put_url = url + ticker + '.json'
	response = requests.patch( ticker_put_url, data=json.dumps(stock_dict) )

	return stock_dict