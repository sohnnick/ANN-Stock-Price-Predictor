import pandas as pd
import json
import numpy as np

def sendDict(pred_results, stock_dict, ticker, yahoo_flag, update_time):
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

	print(stock_dict.keys())

	# descriptive information
	send_companyname = stock_dict['Stock Info']['name']
	send_exchange = stock_dict['Stock Info']['exchange']
	send_ceo = stock_dict['Stock Info']['ceo']
	send_address = stock_dict['Stock Info']['hq_country']

	# financial information
	market_cap = np.round(stock_dict['YF Info']['marketCap']/1000000000, 2)
	pe_ratio = stock_dict['YF Info']['trailingPE']
	sector = stock_dict['YF Info']['sector']
	high_52w = stock_dict['YF Info']['fiftyTwoWeekHigh']
	low_52w = stock_dict['YF Info']['fiftyTwoWeekLow']
	day_open = stock_dict['YF Info']['open']
	day_low = stock_dict['YF Info']['dayLow']
	day_high = stock_dict['YF Info']['dayHigh']
	if 'trailingAnnualDividendYield' not in stock_dict['YF Info'].keys():
		div_yield = 0
	else:
		div_yield = stock_dict['YF Info']['trailingAnnualDividendYield']*100

	news = stock_dict["YF News"]


	fiscal_period = stock_dict['Stock Financials']['results'][0]['fiscal_period']
	fiscal_year = stock_dict['Stock Financials']['results'][0]['fiscal_year']
	revenue = np.round(stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['revenues']['value']/1000000000, 2)
	gross_profit = np.round(stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['gross_profit']['value']
		/1000000000, 2)
	eps = stock_dict['Stock Financials']['results'][0]['financials']['income_statement']['basic_earnings_per_share']['value']

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
		'eps': eps

	}

	return send_all