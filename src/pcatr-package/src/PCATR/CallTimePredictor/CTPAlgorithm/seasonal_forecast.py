#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'SeasonalForecast' class 
to compute forecasts upon calculating 
weighted averages of past individual observations and 
a weighted average of the estimated trend at a respective 
time by additionally capturing seasonality components.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.2'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
import pandas as pd
import numpy as np
import statistics
import datetime
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing

# Owned
from PCATR.Logger import logger

# This needs to be modified
class SeasonalForecast:
    '''
    This class implements algorithms 
    to compute forecasts upon calculating 
    weighted averages of past individual observations and 
    a weighted average of the estimated trend at a respective 
    time by additionally capturing seasonality components.
    '''
    def __init__(self, fullData, numTrainWeeks):
        '''
        Fits the training model using seasonal forecast

        @param {DataFrame} fullData - Full data without train test split
        @param {int} numTrainWeeks - Split ratio for train test split
        '''

        self.model = None
        self.fullData = fullData
        self.trainData = None
        self.testData = None
        self.forecastData = None
        self.index = None
        self.trainTestData = None

        # Prepares the train test split from 'fullData' based on the 'numTrainWeeks'
        def _prepareTrainTestSplit():
            firstCallArrivalDate = self.fullData.CallArrivalDate.iloc[0]
            lastCallArrivalDate = self.fullData.CallArrivalDate.iloc[-1]
            
            weeks = pd.date_range(start=firstCallArrivalDate, end=lastCallArrivalDate, freq='7D')
            
            return weeks[0], weeks[int(numTrainWeeks)], weeks, numTrainWeeks

        trainTestData = _prepareTrainTestSplit()
        
        
        dataV2 = self.fullData.groupby('DialerStartTimeMinusSeconds').median()
        
        # Preparing train data
        index = pd.date_range(start=trainTestData[0], end=trainTestData[1], freq='1min')
        self.index = index
        
        indexDFTrain = pd.DataFrame(self.index, columns=['DialerStartTimeMinusSeconds'])
        indexDFTrain['DialerStartTimeMinusSeconds'] = indexDFTrain['DialerStartTimeMinusSeconds'].astype(str)
        indexDFTrain['DialerStartTimeMinusSeconds'] = indexDFTrain.DialerStartTimeMinusSeconds.apply(lambda x: x[:16])

        self.trainData = pd.merge(indexDFTrain, dataV2, on='DialerStartTimeMinusSeconds', how='left')
        self.trainData.CallDifferenceInterval.fillna(1, inplace=True)
        self.trainData.DialerCallArrivalTime.fillna(method='ffill', inplace=True)
        self.trainData.DialerCallArrivalTime.fillna(1, inplace=True)

        # Preparing test data
        testDate = trainTestData[2]
        testDateStart = str(testDate[int(trainTestData[3])])[:10]
        testDateEnd = str(testDate[int(trainTestData[3])+1])[:10]
        test = self.fullData[self.fullData.DialerStartTimeMinusSeconds.str[:10] >= testDateStart ] 
        test = test[test.DialerStartTimeMinusSeconds.str[:10] < testDateEnd] 

        testIndex = pd.date_range(start=testDateStart, end=testDateEnd, freq='1min')
        indexDFTest = pd.DataFrame(testIndex, columns=['DialerStartTimeMinusSeconds'])
        indexDFTest['DialerStartTimeMinusSeconds'] = indexDFTest['DialerStartTimeMinusSeconds'].astype(str)
        indexDFTest['DialerStartTimeMinusSeconds'] = indexDFTest.DialerStartTimeMinusSeconds.apply(lambda x: x[:16])

        self.testData = pd.merge(indexDFTest, dataV2, on='DialerStartTimeMinusSeconds', how='left')
        self.testData.CallDifferenceInterval.fillna(1, inplace=True)
        self.testData.DialerCallArrivalTime.fillna(method='ffill', inplace=True)
        self.testData.DialerCallArrivalTime.fillna(1, inplace=True)

    def fit(self):
        '''
        Fits the training model using seasonal forecast

        @returns {SeasonalForecast} - self
        '''

        try:
            trainSeries = pd.Series(self.trainData.CallDifferenceInterval.tolist(), self.index)
            
            self.model = ExponentialSmoothing(trainSeries, seasonal_periods=10080, trend=None, seasonal='add').fit(smoothing_level=0.1,use_boxcox=True)
            
            return self
        except:
            logger.Logger.LOGERROR("seasonal_forecast.py", "SeasonalForecast::fit", "Unable to train model")
            return None

    def predict(self):
        '''
        Predicts using the training model for seasonal forecast

        @returns {DataFrame} - Predicted values
        '''

        try:
            trainSeries = pd.Series(self.trainData.CallDifferenceInterval.tolist(), self.index)
            
            ax = trainSeries.plot()
        
            self.model.forecast(10080).rename('Holt-Winters (add-add-seasonal)').plot(ax=ax, style='--', marker='o', color='red', legend=True)
            self.forecastData = self.model.forecast(10080)
        
            return self.forecastData

        except:
            logger.Logger.LOGERROR("seasonal_forecast.py", "SeasonalForecast::predict", "Unable to predict forecast")
            return None
            
    def showPlot(self):
        '''
        Displays the plot of train data, test data and predicted results

        @returns {None}
        '''
    
        plt.figure(figsize=(12,8))
        
        trainSeries = pd.Series(self.trainData.CallDifferenceInterval.tolist(), self.index)

        # Interval Difference vs. Actual Time of Call
        ax = trainSeries.plot()
        ax.set_xlabel("Time")
        ax.set_ylabel("Interval Difference")
        plt.show()

        ax = trainSeries.plot(figsize=(10,6), marker='o', color='black', title="Forecasts from Holt-Winters' multiplicative method" )
        ax.set_ylabel("Interval Difference")
        ax.set_xlabel("Time")
        self.model.fittedvalues.plot(ax=ax, style='--', color='red')

        self.model.forecast(10080).rename('Holt-Winters (add-add-seasonal)').plot(ax=ax, style='--', marker='o', color='red', legend=True)
        plt.show()