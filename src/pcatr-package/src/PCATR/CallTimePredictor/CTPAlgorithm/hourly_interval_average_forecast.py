#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'HourlyIntervalAverageForecast' class 
to compute a set of average values and each value is associated 
with a specific day and a specific hour gap. It distinguishes 
between hours and determines associated average value and predicts 
the time until the next call.
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

# Owned
from PCATR.Logger import logger

class HourlyIntervalAverageForecast:
    '''
    This class implements algorithms to compute a set of 
    average values and each value is associated with a 
    specific day and a specific hour gap. It distinguishes 
    between hours and determines associated average value 
    and predicts the time until the next call
    '''

    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData):
        '''
        Fits the training model using hourly interval average forecast

        @param {DataFrame} trainData - Training data
        @returns {HourlyIntervalAverageForecast} - self
        '''
        try:
            self.trainData = trainData
            self.model = pd.DataFrame(self.trainData.groupby(['DayOfWeek'])['CallDifferenceInterval'].mean())

            return self
        except:
            logger.Logger.LOGERROR("hourly_interval_average_forecast.py", "HourlyIntervalAverageForecast::fit", "Unable to train model")
            return None 

    def predict(self, testData):
        '''
        Predicts using the training model for hourly interval average forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        try:
            self.testData = testData
            self.forecastData = self.testData.copy()

            monday = self.forecastData['DayOfWeek'] == 'Monday'
            self.forecastData.loc[monday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[1]

            tuesday = self.forecastData['DayOfWeek'] == 'Tuesday'
            self.forecastData.loc[tuesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[5]

            wednesday = self.forecastData['DayOfWeek'] == 'Wednesday'
            self.forecastData.loc[wednesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[6]

            thursday = self.forecastData['DayOfWeek'] == 'Thursday'
            self.forecastData.loc[thursday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[4]

            friday = self.forecastData['DayOfWeek'] == 'Friday'
            self.forecastData.loc[friday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[0]

            saturday = self.forecastData['DayOfWeek'] == 'Saturday'
            self.forecastData.loc[saturday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[2]

            sunday = self.forecastData['DayOfWeek'] == 'Sunday'
            self.forecastData.loc[sunday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[3]

            return self.forecastData
        except:
            logger.Logger.LOGERROR("hourly_interval_average_forecast.py", "HourlyIntervalAverageForecast::predict", "Unable to predict forecast")
            return None
    
    def showPlot(self):
        '''
        Displays the plot of train data, test data and predicted results

        @returns {None}
        '''

        plt.figure(figsize=(12,8))
        plt.plot(self.trainData['CallDifferenceInterval'], label='Train')
        plt.plot(self.testData['CallDifferenceInterval'], label='Test')
        plt.plot(self.forecastData['CallDifferenceInterval'], label='Forecast')
        plt.legend(loc='best')
        plt.show()