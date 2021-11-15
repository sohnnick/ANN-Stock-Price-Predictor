# Flask Libraries
from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from stockinfo import *
from forecast import *
from prepsend import *


app = Flask(__name__, static_url_path='/static')

app.config.update(
    # DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)

### Constants
date_today = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)

# open page
@app.route("/")
def index():
	print('hello')
	return render_template( 'index.html', date=date_today )

@app.route("/predict", methods=['POST', 'GET'])
def predict():
	if request.method == 'POST':
		# include error message if ticker or something else is not valid

		# obtain ticker information
		ticker = request.form['stock-tickers']

		# check last update time
		url = 'https://stock-price-predictor-af4ea-default-rtdb.firebaseio.com/'
		ticker_get_url = url + ticker + '/Last-Update.json'
		response = requests.get( ticker_get_url )
		update_time = str(response.json())

		# yahoo finance api flag TEMPORARY
		yahoo_flag = "No"

		# if update time is today -> no need to get data from API since it is already in Firebase
		if update_time == date_today and update_time != 'None':

			url = 'https://stock-price-predictor-af4ea-default-rtdb.firebaseio.com/'
			ticker_get_url = url + ticker + '.json'
			response = requests.get( ticker_get_url )

			stock_dict = dict(response.json())

		else:
			yahoo_flag = "Yes"
			stock_dict = getStockInfo(ticker)
			update_time = date_today

		pred_results, rmse = predictStockPrice(stock_dict)

		send_all = sendDict(pred_results, stock_dict, ticker, yahoo_flag, update_time)

		# direct to new page
		return render_template('analysis.html', **send_all)

	else:
	    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=False,threaded=False)






