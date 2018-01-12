import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from pandas import Series, DataFrame as df
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tools as smt
import MasterDSG as dsg
from matplotlib import style
import sys
import os
from pandas_datareader._utils import RemoteDataError
style.use('ggplot')


def LinRegress(x):
    try:                                                        # This try clause is in place to ensure the user
        stock_reg = web.DataReader(x, 'yahoo', dsg.start_train, dsg.end_train)                                          # has selected a company to examine
                                                          # if not, the user is sent to the ticker menu

    except RemoteDataError:                                     # if remote data error occurs
        print("Connection Failure - Reconnecting..")            # Prints error message while returning to menu

    stock_reg = web.DataReader(x, 'yahoo', dsg.start_train, dsg.end_train)
    trading_days = []
    for i in range(len(stock_reg['Close'].values)):
        x=stock_reg.index[i] - stock_reg.index[0]
        x_days = x.days
        trading_days.append(x_days)
    days = trading_days
    days = sm.add_constant(days)
    days.shape = (len(trading_days), 2)
    Close_price = stock_reg['Close'].values
    Close_price.shape = (len(trading_days), 1)

    #Build a Model for closing price
    regr = smf.OLS(Close_price, days).fit()

    print("\n", 96 * ("="), "\n\nRegression Model Summary\ny = stock_reg Price\nx1 = Number of days\n\n","\n", regr.summary(), "\n", 96 * ("="))

    #Prediction Section
    predict_date_int = (dsg.end_pred - dsg.start_train)# stock_reg.index[0])
    predict_date_int_days = predict_date_int.days

    predict_dt_int_days = np.array([1, predict_date_int_days])
    predict_dt_int_days.shape = (1, 2)
###############################################################################################################################################################################################
    stock_reg_price_predict = regr.predict(predict_dt_int_days)
    if float(stock_reg_price_predict) > 0:
        print("\n\nPrediction Section\n\nPredicted CLosing Stock Price on {}: ".format(dsg.end_pred), float(stock_reg_price_predict),
        "\nPredicted CLosing Stock Price (in dollars) on {}: ".format(dsg.end_pred),
        "$", round(float(stock_reg_price_predict), 2), "\n\n", 80 * ("="))
    else:
        print("WARNING!\nThe Predicted CLosing Stock Price (in Dollars) on {} is Negative\nPredicted Stock Price: ".format(dsg.end_pred), "$", round(float(stock_reg_price_predict), 2))
###############################################################################################################################################################################################


    #Plot Regression
    fig = plt.figure(figsize = (15, 9))
    plt.scatter(trading_days, Close_price, s=0.05)  # Plot the raw data
    plt.xticks(rotation=45)
    plt.title("Company: {} \nStart Date: {} \nEnd Date: {}".format(dsg.ticker.upper(), dsg.start_train, dsg.end_train))
    plt.xlabel("Training Data: Days")
    plt.ylabel("Closing Stock Price")
    plt.plot(trading_days, Close_price, 'r', linewidth = 0.5, label = "Closing Stock Price")# Add the regression line, colored in red

    #Trendline
    trend_x = np.array(trading_days)
    trend_x.shape = (len(trading_days), 1)
    trend_x_array = sm.add_constant(trend_x)
    trend_x_array.shape = (len(trading_days), 2)
    trend_y = np.array([regr.predict(trend_x_array)])
    trend_y.shape = (len(trading_days), 1)
    xlim = trend_x[-1] * 1.05

    #plot trendline
    plt.plot(trend_x, trend_y, 'g', linewidth = 1, label = 'Trend Line')
    plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.xlim(0, xlim)
    plt.legend(loc='best')

    #Evaluation of model: R squared, RMSE
    r_squared = round(float(regr.rsquared), 4)
    print('\nEvaluation of Model\nR-squared value: ', r_squared,  "\n\n", 80 * ("="))
    print("\nPlease Close Graph to Proceed")
    # RMSE = smt.eval_measures.rmse(trend_y, Close_price, axis=0)
    # print("RMSE: ", round(float(RMSE), 4), "\n", 96 * ("="))


    plt.show()




#################################################################################
