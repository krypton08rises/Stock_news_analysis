import gradio as gr
import yfinance as yf

from pytickersymbols import PyTickerSymbols

index_options = ['FTSE 100(UK)', 'NASDAQ(USA)', 'CAC 40(FRANCE)']
ticker_dict = {'FTSE 100(UK)': 'FTSE 100', 'NASDAQ(USA)': 'NASDAQ 100', 'CAC 40(FRANCE)': 'CAC 40'}

demo = gr.Blocks()
stock_names = []
with demo:
    d1 = gr.Dropdown(index_options, label='Please select Index...',
                     info='Will be adding more indices later on',
                     interactive=True)

    d2 = gr.Dropdown([])  # for specific stocks
    d3 = gr.Dropdown([])


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
            stock_names.append(stock['name'] + '"' + stock['symbol'] + '"')
        d2 = gr.Dropdown(choices=stock_names, label='Please Select Stock from your selected index', interactive=True)
        return d2


    d1.input(get_stocks_from_index, d1, d2)
    out = gr.Textbox()


    def get_stock_news(stocks):
        for stock in stocks:
            text = "Your stock is:" + stock
        return text


    d2.input(get_stock_news, d2, out)
    # button_index.click(get_stocks_from_index, inputs=[dropdown_index], outputs=[dropdown_stocks])
    # button_stocks.click(get_stock_news, inputs=[dropdown_stocks], outputs=out)

demo.launch()
