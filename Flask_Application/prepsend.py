import pandas as pd
import json
import numpy as np
from datetime import datetime, timezone, date, timedelta

def sendDict(pred_results, stock_dict, ticker, yahoo_flag, update_time, next_seven_days, rmse):
	# prep historical graph
	historical_date = stock_dict['Stock Dates']
	historical_price = stock_dict['Stock Close']
	send_historical_dict = {}
	for i in range( 0, len(historical_date) ):
		send_historical_dict[str( historical_date[i] )] = stock_dict['Stock Close'][i]

	#prep analysis graph
	thresh = int(np.ceil(len(historical_date)*0.7))
	analysis_date = list(historical_date[thresh:])
	print(len(analysis_date))
	analysis_price = list(pred_results)
	print(len(analysis_price))
	send_analysis_dict = {}
	for i in range( 0, len(analysis_date) ):
		send_analysis_dict[str( analysis_date[i] )] = float(analysis_price[i][0])

	send_historical_json = json.dumps(send_historical_dict)
	send_analysis_json = json.dumps(send_analysis_dict)

	# print(stock_dict.keys())

	# descriptive information
	# if there exists an error w/ Polygon.io
	if 'error' in stock_dict['Stock Info'].keys():
		send_companyname = stock_dict['YF Info']['shortName']
		send_exchange = stock_dict['YF Info']['exchange']
		send_ceo = 'N/A (Unavailable from Polygon.io)'
		send_address = stock_dict['YF Info']['country']

	else:
		send_companyname = stock_dict['Stock Info']['name']
		send_exchange = stock_dict['Stock Info']['exchange']
		send_ceo = stock_dict['Stock Info']['ceo']
		send_address = stock_dict['Stock Info']['hq_country']

	# financial daily information
	market_cap = np.round(stock_dict['YF Info']['marketCap']/1000000000, 2)
	if 'trailingPE' in stock_dict['YF Info'].keys():
		pe_ratio = stock_dict['YF Info']['trailingPE']
	else:
		pe_ratio = 'N/A'
	sector = stock_dict['YF Info']['sector']
	high_52w = stock_dict['YF Info']['fiftyTwoWeekHigh']
	low_52w = stock_dict['YF Info']['fiftyTwoWeekLow']
	day_open = stock_dict['YF Info']['open']
	day_low = stock_dict['YF Info']['dayLow']
	day_high = stock_dict['YF Info']['dayHigh']
	
	div_yield = 0
	if 'trailingAnnualDividendYield' in stock_dict['YF Info'].keys():
		try:
			div_yield = int(stock_dict['YF Info']['trailingAnnualDividendYield'])*100
		except TypeError:
			pass

	news = json.dumps(stock_dict["YF News"])

	# 10-Q statements
	fiscal_period = stock_dict['Stock Financials']['results'][0]['fiscal_period']
	fiscal_year = stock_dict['Stock Financials']['results'][0]['fiscal_year']
	revenue = np.round(stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['revenues']['value']/1000000000, 2)
	gross_profit = np.round(stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['gross_profit']['value']
		/1000000000, 2)
	eps = stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['basic_earnings_per_share']['value']

	# prepare the next seven days document
	seven_dates = []
	datetime_today = datetime.now() + timedelta(days=1)
	count = 0
	while(count < 7):
	    if datetime_today.weekday() not in [5, 6]:
	        date_str = (str(datetime_today.year) + '-' + 
	                    str(datetime_today.month) + '-' + str(datetime_today.day))
	        seven_dates.append(date_str)
	        count = count + 1
	    datetime_today = datetime_today + timedelta(days=1)

	next_seven_forecast_dict = {}
	for i in range(0, 7):
		next_seven_forecast_dict[seven_dates[i]] = str(next_seven_days[i])

	send_next_seven_forecast = json.dumps(next_seven_forecast_dict)

	send_historical_table = []
	# prepare to send historical table
	for i in range(0, len(stock_dict["Stock Dates"])):
		row_temp = []
		row_temp.append(stock_dict["Stock Dates"][i])
		row_temp.append(stock_dict["Stock Low"][i])
		row_temp.append(stock_dict["Stock High"][i])
		row_temp.append(stock_dict["Stock Open"][i])
		row_temp.append(stock_dict["Stock Close"][i])
		row_temp.append(stock_dict["Stock Volume"][i])
		send_historical_table.append(tuple(row_temp))
	send_historical_table = tuple(send_historical_table)

	send_historical_height = len(stock_dict["Stock Dates"])

	send_all = {
		'ticker': ticker, 
		'yahoo': yahoo_flag,
		'historical': send_historical_json, 
		'analysis': send_analysis_json, 
		'update_time': update_time,
		'companyname': send_companyname,
		'exchange': send_exchange,
		'ceo': send_ceo,
		'address': send_address,
		'market_cap': market_cap,
		'pe_ratio': pe_ratio,
		'sector': sector,
		'high_52w': high_52w,
		'low_52w': low_52w,
		'day_open': day_open,
		'day_low': day_low,
		'day_high': day_high,
		'div_yield': div_yield,
		'news': news,
		'fiscal_period': fiscal_period,
		'fiscal_year': fiscal_year,
		'revenue': revenue,
		'gross_profit': gross_profit,
		'eps': eps,
		'rmse': rmse,
		'next_seven_forecast': send_next_seven_forecast,
		'historical_table': send_historical_table,
		'historical_height': send_historical_height
	}

	return send_all