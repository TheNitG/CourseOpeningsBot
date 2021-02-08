# Obtain the stock closing price data for a certain stock for the past year
import os

import discord
import yfinance as yf
import matplotlib.pyplot as plt


async def plot_stock(message, ticker):
    # Define the ticker
    tick = yf.Ticker(ticker)

    # # Get stock info
    # print(tick.info)

    # Get historical market data
    hist = tick.history(period="1y")
    closing = hist['Close']

    # Graph the data
    closing.plot(figsize=(16, 9))
    plt.title(f'{tick.info["longName"]} Graph Over Past Year')
    plt.savefig(fname='plot')
    await message.channel.send(file=discord.File('plot.png'))
    os.remove('plot.png')
