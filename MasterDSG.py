#import necessary libraries.
import os
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from matplotlib import dates
from matplotlib.finance import candlestick_ohlc
import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import scipy as scipy
from scipy.stats import iqr
import re


def get_name(): #function is used to set global variable ticker. Will be called later on when fetching company data.
    global ticker
    while True:
        try: #check to see if that ticker exists on the Nasdaq. Error message and repeat until it does.
            ticker = input("Enter Ticker: ")
            path="http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download"
            load_csv = pd.read_csv(path, usecols = [0])
            match = load_csv["Symbol"].str.match((re.escape(ticker)), case = False)
            search = load_csv.loc[match]
            if search.empty:
                print("That Ticker Does Not Exist on The Nasdaq")
            else:
                print(search)
                break
        except:
            print("\nIncorrect selection, please choose a valid option\n\n")
            break
    return ticker

def day(days): #function built to be used when user wants use set date ranges for examining stock.
    global start #global start and end will be combined with global ticke to fetch data.
    global end
    end = dt.date.today()
    start = end - dt.timedelta(days = days)
    return start, end

def custom_range(): #function for when user wants to define their own range for examining data.
    global start, end
    while True:
        try: #while loop for catching errors. Will constantly loop until format and other rules satisfied.
            start_date = input("Start Date (YYYY, MM, DD): ")
            end_date = input("End Date (YYYY, MM, DD): ") #takes input from user.
            start = dt.datetime.strptime(start_date, '%Y, %m, %d') #uses strptime to change from string into dt format to be used later
            end = dt.datetime.strptime(end_date, '%Y, %m, %d' )
            start = start.date() #changes to just date, not datetime
            end = end.date()
            if start > end:
                print("Start Date Must Be Before End Date. Please Re-Enter")
                custom_range()
            break
        except ValueError:
            print("Incorrect Date Format. Please enter again")
    return start, end

def day_train(days): #same as above, but for training data in regression.
    global start_train
    global end_train
    end_train = dt.date.today()
    start_train = end_train - dt.timedelta(days = days)
    return start_train, end_train

def custom_range_train(): #same as above but for teraining data in regression.
    global start_train, end_train
    while True:
        try:
            start_train_date = input("Start Date (YYYY, MM, DD): ")
            end_train_date = input("End Date (YYYY, MM, DD): ")
            start_train = dt.datetime.strptime(start_train_date, '%Y, %m, %d')
            end_train = dt.datetime.strptime(end_train_date, '%Y, %m, %d' )
            start_train = start_train.date()
            end_train = end_train.date()
            break
        except ValueError:
            print("Incorrect date format. Please enter again")
    return start_train, end_train

def reg_day(days): #same idea as above but for setting pre-set future dates for regression
    global start_train
    global end_pred
    start_reg = dt.date.today()
    end_pred = start_reg + dt.timedelta(days = days)
    return end_pred

def custom_range_pred(): #custom future dates for regression prediciton.
    global end_pred
    while True:
        try:
            end_date = input("Prediction Date (YYYY, MM, DD): ")
            end_reg = dt.datetime.strptime(end_date, '%Y, %m, %d' )
            end_pred = end_reg.date()
            break
        except ValueError:
            print("Incorrect Date Format. Please Enter Again")
    return end_pred

def get_data(): #this function is used to bring global ticker and global start and end dates together.
    global stock, date, open_, high, low, close, volume, start, end #make all variables global as will be called throughout the programme.
    stock = web.DataReader(ticker, 'yahoo', start, end) #use DataReader and ticker and dates defined earlier to fetch company data from web.
    #Make columns variables for easier reference going forward.
    date = stock.index
    open_ = stock['Open']
    high = stock['High']
    low = stock['Low']
    close = stock['Close']
    volume = stock['Volume']
    return stock, date, open_, high, low, close, volume

#Define Descriptive Functions - Self Explanatory
def mean(data):
    mean = np.mean(data)
    print("Mean Price: ${:.2f}\n".format(mean))
def range_(data):
    print("Range: ${:.2f}\n".format((max(data)) - min(data)))
def std_dev(data):
    std_dev = np.std(data)
    print("Standard Deviation: ${:.2f}\n".format(std_dev))
def co_v(data):
    co_v = scipy.stats.variation(data)
    print("Coefficient of Variation: {:.4f}\n".format(co_v))
def max_(data):
    print("Maximum Value: ${:.2f}\n".format(max(data)))
def min_(data):
    print("Minimum Value: ${:.2f}\n".format(min(data)))
def box_whisker(data): #gives user the option to see the information graphically if they wish
    fig = plt.figure(figsize = (8,8))
    plt.boxplot(data)
    plt.title('Boxplot of Prices')
    plt.ylabel('Price')
    plt.show()
def all_(data):
    mean(data)
    range_(data)
    std_dev(data)
    co_v(data)
    max_(data)
    min_(data)

#Graphs

def closing(data): #plots raw time series
    fig = plt.figure(figsize = (15, 10)) #make plot bigger, used in all graphs
    data.plot(label = 'Closing Price')
    plt.legend(loc = 'best') #legend used in all graphs
    plt.ylabel('Closing Price')
    plt.xlabel('Date')
    plt.title('Raw Time Series Graph')
    plt.show()

def close_trend(): #plots raw time series with trendline.
    stock['Date'] = stock.index.map(mdates.date2num) #convert dates into integers so trend can be established.
    x = stock['Date']
    y = stock['Close']
    fig = plt.figure(figsize = (15, 10))
    fig = plt.plot(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z) #establish trendline between close and dates
    plt.plot(x, p(x), 'b--') #plot trendline
    plt.xlabel('Date')
    plt.ylabel('Prices')
    plt.xticks(rotation = 45) #makes dates visible on x ais
    plt.title('Closing Prices With Trendline ')
    formatter = dates.DateFormatter('%d-%m-%Y') #brings dates back from integers to dates. Looks better on x axis.
    ax = plt.gcf().axes[0]
    ax.xaxis.set_major_formatter(formatter)
    plt.show()


def moving_avg(data): #plots moving avergae
    while True: #while loop set up to catch common errors when asking for input from user.
        try:
            days = int(input("Number of Days For Moving Average: "))
            if days <= 0 or isinstance(days, int) != True: #checks positive integer.
                print("Number of Days Must Be a Positive Number. Please Re-Enter.")
                moving_avg(data)
            else:
                stock['Moving Average'] = stock['Close'].rolling(window = days, min_periods = 0).mean() #creates moving average column.
                print("Please Close Graph to Proceed.") #need to remind user to close before proceeding.
                fig = plt.figure(figsize = (15, 10))
                ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
                ax1.plot(date, stock['Moving Average'], label = 'Moving Average')
                plt.legend(loc = 'best')
                plt.ylabel('Price')
                plt.xlabel('Date')
                plt.title('Moving Average Graph')
                plt.show()
                break
            break
        except ValueError:
            print("Number of Days Must Be a Positive Integer. Please Re-Enter.")
        except OverflowError:
            print("Window Size Too Large For Moving Average. Please Re-Enter.")
        except AttributeError:
            print("Number of Days must be a number. Please Re-Enter.")



def moving_avg_close(data): #same as above but includes raw close for comparison
    while True:
        try:
            days = int(input("Number of Days For Moving Average: "))
            stock['Moving Average'] = stock['Close'].rolling(window = days, min_periods = 0).mean()
            break
        except ValueError:
            print("Number of Days Must Be a Positive Integer. Please Re-Enter.")
        except OverflowError:
            print("Window Size Too Large For Moving Average. Please Re-Enter.")
    print("Please Close Graph to Proceed")
    #Plot closing price and moving average
    fig = plt.figure(figsize = (15, 10))
    ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
    ax1.plot(date, data)
    ax1.plot(date, stock['Moving Average'], label = 'Moving Average')
    plt.legend(loc = 'best')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.title('Moving Average Graph')
    plt.show()

def moving_avg_vol(data): #same as above but with a subplot to show volume
    while True:
        try:
            days = int(input("Number of Days For Moving Average: "))
            stock['Moving Average'] = stock['Close'].rolling(window = days, min_periods = 0).mean()
            break
        except ValueError:
            print("Number of Days Must Be an Integer. Please Re-Enter.")
        except OverflowError:
            print("Window Size Too Large for Moving Average. Please Re-Enter")
    print("Please Close Graph to Proceed.")
    #Plot closing price and moving average
    fig = plt.figure(figsize = (15, 10))
    ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((6, 1), (5,0), rowspan = 1, colspan = 1, sharex = ax1) #add a subplot showing volume
    ax1.plot(date, data)
    ax1.plot(date, stock['Moving Average'], label = 'Moving Average')
    ax1.title.set_text('Moving Average Graph')
    ax1.set_ylabel('Price')
    ax2.bar(date, volume) #shows the volume
    plt.legend(loc = 'best')
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.show()

def w_moving_avg(data): #weighted moving average graph
    while True:
        try:
            days = int(input("Number of Days for Weighted Moving Average: "))
            weights = np.exp(np.linspace(-1., 0., days))
            weights /= weights.sum()
            weighted_moving = np.convolve(data, weights, mode = 'full')[:len(data)]
            weighted_moving[:days] = weighted_moving[days]
            break
        except IndexError:
            print("Window Size Cannot Be Greater Than Date Range. Please Re-Enter.")
        except ValueError:
            print("Number of Days Must Be a Positive Integer. Please Re-Enter.")
        except MemoryError:
            print("Window Size Too Large. Please Try Again Using a Suitable Number")
    print("Please Close Graph to Proceed.")
    fig = plt.figure(figsize = (15, 10))
    ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
    ax1.plot(date, data)
    ax1.plot(date, weighted_moving, label = 'Weighted Moving Average')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.title('Weighted Moving Average Graph')
    plt.legend(loc = 'best')
    plt.show()



def bbands(data):#bollinger bands are a popular technical analysis technique to get an idea of overbought and oversold.
    while True: #idea is to create an upper and low band by adding and subtracting standard deviations.
        try:
            days = int(input("Number of days: "))
            MA = data['Close'].rolling(days).mean()
            SD = data['Close'].rolling(days).std()
            data['UpperBB'] = MA + (2 * SD)
            data['LowerBB'] = MA - (2 * SD)
            break
        except ValueError:
            print("Invalid Input. Please try again using a suitable positive number.")
        except ZeroDivisionError:
            print("Cannot Use Zero Number of Days. Please Try Again Using a Suitable Positive Number.")
        except OverflowError:
            print("Number of Days Entered is Too Large. Please Try Again Using a Suitable Positive Number.")
    print("Please Close Graph to Proceed.")
    fig = plt.figure(figsize = (15, 10))
    ax1 = plt.subplot2grid((6, 4), (0, 0), rowspan = 10, colspan = 10)
    ax1.plot(date, close)
    ax1.plot(date, data['UpperBB'], label = 'Upper Bollinger Band')
    ax1.plot(date, data['LowerBB'], label = 'Lower Bollinger Band')
    plt.legend(loc = 'best')
    plt.xlabel('Dates')
    plt.ylabel('Price')
    plt.title('Bollinger Bands Graph')
    plt.show()



def macd_1(): #moving average convergence divergence.
    stock['26ema'] = close.ewm(ignore_na = False, adjust = True, min_periods = 0, span = 26).mean() #create fast and slow moving averages
    stock['12ema'] = close.ewm(ignore_na = False, adjust = True, min_periods = 0, span = 12).mean()
    stock['MACD'] = (stock['12ema'] - stock['26ema']) #subtract one from the other.
    stock['Signal'] = stock['MACD'].ewm(ignore_na = False, adjust = True, min_periods = 0, span = 9).mean() #build a signal line to plot as well.
    stock.plot(y = ['MACD', 'Signal'], title = 'MACD & Signal', figsize = (15, 10))
    plt.show()


def candlestick(): #way of visualizing open, high, low and close all on one.
    stock_ohlc = stock['Adj Close'].resample('10D').ohlc() #need to take just a sample of 10days as 1 day would be overkill on the screen.
    stock_volume = stock['Volume'].resample('10D').sum()
    stock_ohlc.reset_index(inplace = True)
    stock_ohlc['Date'] = stock_ohlc['Date'].map(mdates.date2num)
    fig = plt.figure(figsize = (15, 10))
    fig = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
    fig.xaxis_date()
    plt.xlabel('Date')
    plt.ylabel('Prices')
    plt.legend(loc = 'best')
    plt.title('Candlestick Graph')
    candlestick_ohlc(fig, stock_ohlc.values, width = 5, colorup = 'g', colordown = 'r') #change up and down colours to standard red and green.
    plt.show()
