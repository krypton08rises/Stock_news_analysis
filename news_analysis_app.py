import gradio as gr
import yfinance as yf
import seaborn as sns;

sns.set()
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datetime import date, timedelta
from plotly.subplots import make_subplots
from pytickersymbols import PyTickerSymbols
from dateutil.relativedelta import relativedelta

index_options = ['FTSE 100(UK)', 'NASDAQ(USA)', 'CAC 40(FRANCE)']
ticker_dict = {'FTSE 100(UK)': 'FTSE 100', 'NASDAQ(USA)': 'NASDAQ 100', 'CAC 40(FRANCE)': 'CAC 40'}

global START_DATE, END_DATE

END_DATE = date.today()
START_DATE = END_DATE - relativedelta(years=5)
demo = gr.Blocks()
stock_names = []
with demo:
    d1 = gr.Dropdown(index_options, label='Please select Index...',
                     info='Will be adding more indices later on',
                     interactive=True)

    d2 = gr.Dropdown([])  # for specific stocks


    # d3 = gr.Dropdown(['General News'])

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

        ## Can also download lower interval data apparently using line below
        # data = yf.download(tickers="MSFT", period="5d", interval="1m")
        time_series = yf.download(tickers=ticker_name, start=START_DATE, end=END_DATE)  # stock.split(":")[1]
        time_series.reset_index(inplace=True)

        fig = plt.figure(figsize=(14, 5))
        sns.set_style("ticks")
        sns.lineplot(data=time_series, x="Date", y='Close', color='firebrick')
        sns.despine()

        plt.title("Stock Price of {}".format(stock_name), size='x-large', color='blue')  # stock.split(":")[0]
        text = "Your stock is:" + str(stock)
        return fig


    d2.input(get_stock_graph, [d1, d2], out)
    # button_index.click(get_stocks_from_index, inputs=[dropdown_index], outputs=[dropdown_stocks])
    # button_stocks.click(get_stock_news, inputs=[dropdown_stocks], outputs=out)

demo.launch()
