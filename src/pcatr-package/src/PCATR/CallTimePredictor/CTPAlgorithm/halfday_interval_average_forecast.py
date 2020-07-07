#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'HalfdayIntervalAverageForecast' class 
to compute a set of average values where each value is 
associated with a specific day and the first or second 
half of the day. It distinguishes between the two halves 
of the day and determines the time until the next call.
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

# Owned
from PCATR.Logger import logger

class HalfdayIntervalAverageForecast:
    '''
    This class implements algorithm  to compute a 
    set of average values where each value is associated 
    with a specific day and the first or second 
    half of the day. It distinguishes between the two halves 
    of the day and determines the time until the next call
    '''
    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData):
        '''
        Fits the training model using halfday interval average forecast

        @param {DataFrame} trainData - Training data
        @returns {HalfdayIntervalAverageForecast} - self
        '''

        try:
            self.trainData = trainData
            self.model = pd.DataFrame(self.trainData.groupby(['DayOfWeek', 'IntervalOfDay'])['CallDifferenceInterval'].mean())

            return self
        except:
            logger.Logger.LOGERROR("halfday_interval_average_forecast.py", "HalfdayIntervalAverageForecast::fit", "Unable to train model")
            return None 

    def predict(self, testData):
        '''
        Predicts using the training model for halfday interval average forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        try:
            self.testData = testData
            self.forecastData = self.testData.copy()

            # Monday
            monday = (self.forecastData['DayOfWeek'] == 'Monday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[monday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[6]

            monday = (self.forecastData['DayOfWeek'] == 'Monday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[monday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[4]

            monday = (self.forecastData['DayOfWeek'] == 'Monday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[monday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[5]

            monday = (self.forecastData['DayOfWeek'] == 'Monday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[monday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[7]

            # Tuesday
            tuesday = (self.forecastData['DayOfWeek'] == 'Tuesday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[tuesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[22]

            tuesday = (self.forecastData['DayOfWeek'] == 'Tuesday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[tuesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[20]

            tuesday = (self.forecastData['DayOfWeek'] == 'Tuesday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[tuesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[21]

            tuesday = (self.forecastData['DayOfWeek'] == 'Tuesday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[tuesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[23]
            
            # Wednesday
            wednesday = (self.forecastData['DayOfWeek'] == 'Wednesday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[wednesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[26]

            wednesday = (self.forecastData['DayOfWeek'] == 'Wednesday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[wednesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[24]

            wednesday = (self.forecastData['DayOfWeek'] == 'Wednesday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[wednesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[25]

            wednesday = (self.forecastData['DayOfWeek'] == 'Wednesday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[wednesday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[27]

            # Thursday
            thursday = (self.forecastData['DayOfWeek'] == 'Thursday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[thursday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[18]

            thursday = (self.forecastData['DayOfWeek'] == 'Thursday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[thursday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[16]

            thursday = (self.forecastData['DayOfWeek'] == 'Thursday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[thursday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[17]

            thursday = (self.forecastData['DayOfWeek'] == 'Thursday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[thursday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[19]

            # Friday
            friday = (self.forecastData['DayOfWeek'] == 'Friday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[friday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[2]

            friday = (self.forecastData['DayOfWeek'] == 'Friday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[friday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[0]

            friday = (self.forecastData['DayOfWeek'] == 'Friday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[friday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[1]

            friday = (self.forecastData['DayOfWeek'] == 'Friday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[friday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[3]

            # Saturday
            saturday = (self.forecastData['DayOfWeek'] == 'Saturday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[saturday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[10]

            saturday = (self.forecastData['DayOfWeek'] == 'Saturday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[saturday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[8]

            saturday = (self.forecastData['DayOfWeek'] == 'Saturday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[saturday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[9]

            saturday = (self.forecastData['DayOfWeek'] == 'Saturday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[saturday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[11]

            # Sunday
            sunday = (self.forecastData['DayOfWeek'] == 'Sunday')&(self.forecastData['IntervalOfDay'] == 'morning')
            self.forecastData.loc[sunday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[10]

            sunday = (self.forecastData['DayOfWeek'] == 'Sunday')&(self.forecastData['IntervalOfDay'] == 'afternoon')
            self.forecastData.loc[sunday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[8]

            sunday = (self.forecastData['DayOfWeek'] == 'Sunday')&(self.forecastData['IntervalOfDay'] == 'evening')
            self.forecastData.loc[sunday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[9]

            sunday = (self.forecastData['DayOfWeek'] == 'Sunday')&(self.forecastData['IntervalOfDay'] == 'night')
            self.forecastData.loc[sunday,'CallDifferenceInterval'] = \
                self.model['CallDifferenceInterval'].iloc[11]

            return self.forecastData
        except:
            logger.Logger.LOGERROR("halfday_interval_average_forecast.py", "HalfdayIntervalAverageForecast::predict", "Unable to predict forecast")
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