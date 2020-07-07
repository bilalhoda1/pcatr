#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'SmoothingForecast' class 
to compute future values using weighted averages, 
where the weights decrease exponentially as observations 
come from further in the past – the smallest weights are 
associated with the oldest observations.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing #, ExponentialSmoothing

# Owned
from PCATR.Logger import logger

class SmoothingForecast:
    '''
    This class implements algorithm to compute future 
    values using weighted averages, where the weights 
    decrease exponentially as observations come from 
    further in the past – the smallest weights are 
    associated with the oldest observations.
    '''
    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData):
        '''
        Fits the training model using smoothing forecast

        @param {DataFrame} trainData - Training data
        @returns {SmoothingForecast} - self
        '''

        try:
            self.trainData = trainData
            
            self.model = SimpleExpSmoothing(np.asarray(self.trainData['CallDifferenceInterval']))\
                .fit(smoothing_level=0.6, optimized=False)

            return self
        except:
            logger.Logger.LOGERROR("smoothing_forecast.py", "SmoothingForecast::fit", "Unable to train model")
            return None

    def predict(self, testData):
        '''
        Predicts using the training model for smoothing forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        try:
            self.testData = testData
            self.forecastData = self.testData.copy()
            self.forecastData['CallDifferenceInterval'] = self.model.forecast(len(self.testData))
            return self.forecastData
        except:
            logger.Logger.LOGERROR("smoothing_forecast.py", "SmoothingForecast::predict", "Unable to predict forecast")
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