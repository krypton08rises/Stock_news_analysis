import gradio as gr
import yfinance as yf

from pytickersymbols import PyTickerSymbols


index_options = ['FTSE 100(UK)', 'NASDAQ(USA)', 'CAC 40(FRANCE)']
list_of_stocks = []
ticker_dict = {'FTSE 100(UK)': 'FTSE 100', 'NASDAQ(USA)': 'NASDAQ 100', 'CAC 40(FRANCE)': 'CAC 40'}


def get_stocks_from_index(dropdown_security):
    stock_data = PyTickerSymbols()
    indices = stock_data.get_all_indices()
    index = ticker_dict[dropdown_security]

    stock_data = PyTickerSymbols()
    # returns 2d list with the following information
    # 'name', 'symbol', 'country', 'indices', 'industries', 'symbols', 'metadata', 'isins', 'akas'

    stocks = list(stock_data.get_stocks_by_index(index)) ##converting filter object to list

    printable_stock_names = []
    for stock in stocks:
      printable_stock_names.append(stock['name']+'"' + stock['symbol'] +'"')
    return printable_stock_names



def get_stock_news(stock):
    text = "Your stock is:" + stock
    return text


# dropdown_stocks = gr.Dropdown(, label='Stocks')

news = ""
demo = gr.Blocks()
with demo:
  dropdown_index = gr.Dropdown(index_options, label='Please select Index...', info='Will be adding more indices later on')
  button_index = gr.Button("Get Stocks of Index")

  dropdown_stocks = gr.Dropdown(label='Please Select Stock from your selected index')
  button_stocks = gr.Button("Get News about Stocks")
  out = gr.Textbox()

  button_index.click(get_stocks_from_index, inputs=dropdown_index, outputs=dropdown_stocks)
  button_stocks.click(get_stock_news, inputs=dropdown_stocks, outputs=out)

demo.launch()