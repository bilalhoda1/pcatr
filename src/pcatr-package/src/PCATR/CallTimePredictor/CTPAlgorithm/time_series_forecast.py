#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'TimeSeriesForecast' class 
to compute future values using ARIMA modeling. Past 
time points of time series data can impact current 
and future time points. ARIMA models take this concept 
into account when forecasting current and future values. 
ARIMA uses a number of lagged observations of time series 
to forecast observations.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Owned
from PCATR.Logger import logger

class TimeSeriesForecast:
    '''
    This class implements algorithms
    to compute future values using ARIMA modeling. Past 
    time points of time series data can impact current 
    and future time points. ARIMA models take this concept 
    into account when forecasting current and future values. 
    ARIMA uses a number of lagged observations of time series 
    to forecast observations.
    '''
    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData, testData):
        '''
        Fits the training model using time series forecast

        @param {DataFrame} trainData - Training data
        @param {DataFrame} testData - Test data
        @returns {TimeSeriesForecast} - self
        '''

        try:
            self.trainData = trainData
            self.testData = testData
            fullData = pd.concat([self.trainData, self.testData])

            model = sm.tsa.statespace.SARIMAX(fullData['CallDifferenceInterval'],
                                            order=(1, 0, 1),
                                            seasonal_order=(0, 0, 0, 0),
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            self.model = model.fit()
            
            return self
        except:
            logger.Logger.LOGERROR("time_series_forecast.py", "TimeSeriesForecast::fit", "Unable to train model")
            return None

    def predict(self, testData):
        '''
        Predicts using the training model for time series forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        try:
            self.testData = testData

            pred = self.model.get_prediction(dynamic=False)

            self.forecastData = pred
            return self.forecastData
        except:
            logger.Logger.LOGERROR("time_series_forecast.py", "TimeSeriesForecast::predict", "Unable to predict forecast")
            return None
            
    def showPlot(self):
        '''
        Displays the plot of train data, test data and predicted results

        @returns {None}
        '''

        plt.figure(figsize=(12, 8))

        self.model.plot_diagnostics(figsize=(12, 8))
        plt.show()

        pred_ci = self.forecastData.conf_int()

        y = self.trainData['CallDifferenceInterval']

        plt.plot(self.testData['CallDifferenceInterval'], label='Test')

        ax = y[:].plot(label='Train')
        self.forecastData.predicted_mean.plot(ax=ax, label='Forecast', alpha=.7, figsize=(12, 8))
        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.5)
        ax.set_xlabel('Date')
        ax.set_ylabel('Next Call')
        ax.set_ylim(0, max(self.trainData['CallDifferenceInterval'].max(),
            self.testData['CallDifferenceInterval'].max()))
        plt.legend()
        plt.show()