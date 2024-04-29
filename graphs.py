import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datetime import date
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots

# Solid or Hollow
#     Solid candle if the current closing price is lower than the current opening price.
#     Hollow candle if the current closing price is higher than the current opening price
# Green or red
#     Green candle if the current closing price is higher than the previous closing price.
#     Red candle if the current closing price is lower than the previous closing price.



def line_graph(df, start_date=pd.to_datetime('2020-4-1'), end_date=pd.to_datetime('2020-9-30')):

    """
    Line Graph for the adjusted closing price of a stock
    """
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    new_df = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    df1 = df.loc[new_df]
    stock_data = df1.set_index('Date')
    top_plt = plt.subplot2grid((5, 4), (0, 0), rowspan=3, colspan=4)
    top_plt.plot(stock_data.index, stock_data["Close"])
    plt.title('Historical stock prices of Alphabet Inc. [01-04-2020 to 30-09-2020]')
    bottom_plt = plt.subplot2grid((5, 4), (3, 0), rowspan=1, colspan=4)
    bottom_plt.bar(stock_data.index, stock_data['Volume'])
    plt.title('\nAlphabet Inc. Trading Volume', y=-0.60)
    plt.gcf().set_size_inches(12, 8)

    return plt.figure()


def candlestick_graph():

# Initialize empty plot with marginal subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        shared_xaxes="columns",
        shared_yaxes="rows",
        column_width=[0.8, 0.2],
        row_heights=[0.8, 0.2],
        horizontal_spacing=0,
        vertical_spacing=0,
        subplot_titles=["Candlestick", "Price Bins", "Volume", ""]
    )

    ohlc["previousClose"] = ohlc["Close"].shift(1)
    # Define color based on close and previous close
    ohlc["color"] = np.where(ohlc["Close"] > ohlc["previousClose"], "green", "red")
    # Set fill to transparent if close > open and the previously defined color otherwise
    ohlc["fill"] = np.where(ohlc["Close"] > ohlc["Open"], "rgba(255, 0, 0, 0)", ohlc["color"])

    showlegend = True
    for index, row in ohlc.iterrows():
        color = dict(fillcolor=row["fill"], line=dict(color=row["color"]))
        fig.add_trace(
            go.Candlestick(
                x=[index],
                open=[row["Open"]],
                high=[row["High"]],
                low=[row["Low"]],
                close=[row["Close"]],
                increasing=color,
                decreasing=color,
                showlegend=showlegend,
                name="GE",
                legendgroup="Hollow Candlesticks"
            ),
            row=1,
            col=1
        )
        showlegend = False


    ohlc["Percentage"] = ohlc["Volume"]*100/ohlc["Volume"].sum()

    fig.add_trace(
        go.Bar(
            x=ohlc.index,
            y=ohlc["Volume"],
            text=ohlc["Percentage"],
            marker_line_color=ohlc["color"],
            marker_color=ohlc["fill"],
            name="Volume",
            texttemplate="%{text:.2f}%",
            hoverinfo="x+y",
            textfont=dict(color="white")
        ),
        col=1,
        row=2,
    )

    ohlc["Percentage"] = ohlc["Volume"]*100/ohlc["Volume"].sum()

    fig.add_trace(
        go.Bar(
            x=ohlc.index,
            y=ohlc["Volume"],
            text=ohlc["Percentage"],
            marker_line_color=ohlc["color"],
            marker_color=ohlc["fill"],
            name="Volume",
            texttemplate="%{text:.2f}%",
            hoverinfo="x+y",
            textfont=dict(color="white")
        ),
        col=1,
        row=2,
    )
    fig.show()


if __name__=='__main__':
    stock = "GE"
    END_DATE = date.today()
    START_DATE = END_DATE - relativedelta(years=5)

    ochlv = yf.download(stock, start=START_DATE,end=END_DATE)
    print(ochlv.columns)
    plot = line_graph(ochlv)
    plt.show()
