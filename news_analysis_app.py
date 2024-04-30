import datetime
import gradio as gr
import pandas as pd
import yfinance as yf
import seaborn as sns;

sns.set()
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datetime import date, timedelta
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
from pytickersymbols import PyTickerSymbols
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import autocorrelation_plot
from dateutil.relativedelta import relativedelta

index_options = ['FTSE 100(UK)', 'NASDAQ(USA)', 'CAC 40(FRANCE)']
ticker_dict = {'FTSE 100(UK)': 'FTSE 100', 'NASDAQ(USA)': 'NASDAQ 100', 'CAC 40(FRANCE)': 'CAC 40'}

global START_DATE, END_DATE

END_DATE = date.today()
START_DATE = END_DATE - relativedelta(years=1)
FORECAST_PERIOD = 7
demo = gr.Blocks()
stock_names = []

with demo:
    d1 = gr.Dropdown(index_options, label='Please select Index...',
                     info='Will be adding more indices later on',
                     interactive=True)

    d2 = gr.Dropdown([])  # for specific stocks


    # d3 = gr.Dropdown(['General News'])

    def forecast_series(series, model="ARIMA", forecast_period=7):

        predictions = list()
        if series.shape[1] > 1:
            series = series['Close'].values.tolist()
        plt.show()
        if model == "ARIMA":
            ## Do grid search here --> Custom for all stocks
            for i in range(forecast_period):
                model = ARIMA(series, order=(5, 1, 0))
                model_fit = model.fit()
                output = model_fit.forecast()
                yhat = output[0]
                predictions.append(yhat)
                series.append(yhat)

        return predictions


    def is_business_day(a_date):
        return a_date.weekday() < 5


    def get_stocks_from_index(idx):
        stock_data = PyTickerSymbols()
        # indices = stock_data.get_all_indices()
        index = ticker_dict[idx]
        stock_data = PyTickerSymbols()

        # returns 2d list with the following information
        # 'name', 'symbol', 'country', 'indices', 'industries', 'symbols', 'metadata', 'isins', 'akas'
        stocks = list(stock_data.get_stocks_by_index(index))  ##converting filter object to list
        stock_names = []
        for stock in stocks:
            stock_names.append(stock['name'] + ':' + stock['symbol'])
        d2 = gr.Dropdown(choices=stock_names, label='Please Select Stock from your selected index', interactive=True)
        return d2


    d1.input(get_stocks_from_index, d1, d2)
    out = gr.Plot(every=10)


    def get_stock_graph(idx, stock):

        stock_name = stock.split(":")[0]
        ticker_name = stock.split(":")[1]

        if ticker_dict[idx] == 'FTSE 100':
            if ticker_name[-1] == '.':
                ticker_name += 'L'
            else:
                ticker_name += '.L'
        elif ticker_dict[idx] == 'CAC 40':
            ticker_name += '.PA'

        ## Can also download lower interval data apparently using line below
        # data = yf.download(tickers="MSFT", period="5d", interval="1m")
        series = yf.download(tickers=ticker_name, start=START_DATE, end=END_DATE)  # stock.split(":")[1]
        series = series.reset_index()

        predictions = forecast_series(series)

        last_date = pd.to_datetime(series['Date'].values[-1])
        forecast_week = []

        while len(forecast_week) != FORECAST_PERIOD:
            if is_business_day(last_date):
                forecast_week.append(last_date)
            last_date += timedelta(days=1)

        forecast = pd.DataFrame({"Date": forecast_week, "Forecast": predictions})

        fig = plt.figure(figsize=(14, 5))
        sns.set_style("ticks")
        sns.lineplot(data=series, x="Date", y="Close", color="firebrick")
        sns.lineplot(data=forecast, x="Date", y="Forecast", color="blue")
        sns.despine()

        plt.title("Stock Price of {}".format(stock_name), size='x-large', color='blue')  # stock.split(":")[0]
        text = "Your stock is:" + str(stock)
        return fig


    d2.input(get_stock_graph, [d1, d2], out)
    # button_index.click(get_stocks_from_index, inputs=[dropdown_index], outputs=[dropdown_stocks])
    # button_stocks.click(get_stock_news, inputs=[dropdown_stocks], outputs=out)

demo.launch()