# Obtain the stock closing price data for a certain stock for the past year
import os

import discord
import yfinance as yf
import matplotlib.pyplot as plt


async def plot_stock(message, ticker):
    # Define the ticker
    tick = yf.Ticker(ticker)
    # # Get stock info
    print(tick.info)

    # Get historical market data
    hist = tick.history(period="1d", interval='1m')
    closing = hist['Close']
    print(hist)
    # Graph the data
    closing.plot(figsize=(16, 9))
    plt.title(f'{tick.info["longName"]} Graph Over Past Day')
    plt.savefig(fname='plot')
    await message.channel.send(file=discord.File('plot.png'))
    os.remove('plot.png')
    await message.channel.send(f'Current Price: ${format(hist["Open"][-1], ".2f")}, Market Open:'
                               f' ${tick.info["regularMarketOpen"]}, Previous Close: ${tick.info["previousClose"]}, ')
