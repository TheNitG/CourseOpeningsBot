# Obtain the stock closing price data for a certain stock for the past year
import os

import discord
import yfinance as yf
import mplfinance as mpf


# Plot the stock price data for a certain stock
async def plot_stock(message, ticker):
    # Define the ticker
    tick = yf.Ticker(ticker)
    # # Get stock info
    print(tick.info)
    # Download stock data with 1 minute intervals
    data = yf.download(ticker, period='1d', interval='1m')
    mpf.plot(data, type='candle', style='charles', savefig='plot.png', title=f'{tick.info["longName"]} Stock Value '
                                                                             f'Over Past Day')
    await message.channel.send(file=discord.File('plot.png'))
    os.remove('plot.png')

    # # Get historical market data
    hist = tick.history(period="1d", interval='1m')
    await message.channel.send(f'Current Price: ${format(hist["Open"][-1], ".2f")}, Market Open:'
                               f' ${tick.info["regularMarketOpen"]}, Previous Close: ${tick.info["previousClose"]}.')
