#!/usr/bin/env python
# coding: utf-8

"""
This class implements the 'SimpleAverageForecast' class 
to compute the average interval difference of the 
complete dataset and uses it to predict the time left 
until the next immediate call.
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

class SimpleAverageForecast:
    '''
    This class implements algorithm to compute the average interval 
    difference of the complete dataset and uses it to predict the 
    time left until the next immediate call
    '''
    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData):
        '''
        Fits the training model using simple average forecast

        @param {DataFrame} trainData - Training data
        @returns {SimpleAverageForecast} - self
        '''

        try:
            self.trainData = trainData
            self.model = self.trainData['CallDifferenceInterval'].mean()

            return self
        except:
            logger.Logger.LOGERROR("simple_average_forecast.py", "SimpleAverageForecast::fit", "Unable to train model")
            return None

    def predict(self, testData):
        '''
        Predicts using the training model for simple average forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        try:
            self.testData = testData
            self.forecastData = self.testData.copy()
            self.forecastData['CallDifferenceInterval'] = self.model
            return self.forecastData
        except:
            logger.Logger.LOGERROR("simple_average_forecast.py", "SimpleAverageForecast::predict", "Unable to predict forecast")
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