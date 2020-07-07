#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'DataTank' module to manipulate data which 
is used by other modules for prediction purposes.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
import pandas as pd
import datetime as dt

# Owned
from PCATR.Logger import logger

class DataTank:
    '''
    This module implements algorithms to manipulate data which 
    is used by other modules for prediction purposes.
    '''

    def __init__(self):
        self.fullData = None
        self.trainData = None
        self.testData = None

    def loadData(self, filename):
        '''
        Loads the data in CSV file using Python's pandas module

        @param {string} filename - Name of CSV file
        @returns {DataFrame} - Loaded data wrapped in pandas' DataFrame object 
        '''

        try:
            self.fullData = pd.read_csv(filename)
        except FileNotFoundError as e:
            logger.Logger.LOGERROR("data_tank.py", "DataTank::loadData", "Unable to load file")
        return self.fullData

    def getProcessedData(self):
        '''
        Processes the data and adds a new column 'CallDifferenceInterval' to DataFrame object 

        @returns {DataFrame} - Processed data wrapped in pandas' DataFrame object 
        '''

        try:
            # Introducing new column 'CallDifferenceInterval' for analysis
            self.fullData['CallDifferenceInterval'] = self.fullData.groupby(['CallArrivalDate'])['DialerCallArrivalTime'] \
                .diff().fillna(self.fullData['DialerCallArrivalTime'])

            # Splitting time entry from datetime into a new column 'TimeOfCall'
            datetimeObj = self.fullData["CallArrivalTime"].str.split(" ", n=1, expand=True)
            self.fullData["TimeOfCall"] = datetimeObj[1]
            
            # Generating new columns 'Hour', 'Minutes', 'Seconds' for hour, minutes and seconds entries respectively
            self.fullData['Hour'] = self.fullData.TimeOfCall.str[:2]
            self.fullData['Minutes'] = self.fullData.TimeOfCall.str[3:5]
            self.fullData['Seconds'] = self.fullData.TimeOfCall.str[6:]
            # self.fullData['Hour'] = pd.to_numeric(self.fullData['Hour'])
            # self.fullData['Minutes'] = pd.to_numeric(self.fullData['Minutes'])
            # self.fullData['Seconds'] = pd.to_numeric(self.fullData['Seconds'])

            # Generating new columns 'Year', 'Month', 'DayDate' for year, month and day entries respectively
            dateObj = self.fullData["CallArrivalDate"].str.split('/', n=2, expand=True)   
            self.fullData['Year'] = dateObj[0]
            self.fullData['Month'] = dateObj[1]
            self.fullData['DayDate'] = dateObj[2]
            self.fullData['Year'] = pd.to_numeric(self.fullData['Year'])
            self.fullData['Month'] = pd.to_numeric(self.fullData['Month'])
            self.fullData['DayDate'] = pd.to_numeric(self.fullData['DayDate'])

            # Generating new column similar to 'DialerStartTime' but without the 'Seconds' entry
            self.fullData['DialerStartTimeMinusSeconds'] = self.fullData['CallArrivalDate'] + ' ' + self.fullData.TimeOfCall.str[:5]

            # Converting date and time dependent columns to DateTime objects
            self.fullData['CallArrivalTime'] = pd.to_datetime(self.fullData['CallArrivalTime'])
            self.fullData['CallArrivalDate'] = pd.to_datetime(self.fullData['CallArrivalDate'])
            self.fullData['DialerStartTime'] = pd.to_datetime(self.fullData['DialerStartTime'])
            
            # Introducing new columns for 'IntervalOfDay' day intervals - morning, afternoon, evening, night
            morning = (self.fullData['CallArrivalTime'].dt.time \
                >= dt.time(hour=7,minute=0))&(self.fullData['CallArrivalTime'].dt.time \
                    <= dt.time(hour=12,minute=0))

            afternoon = (self.fullData['CallArrivalTime'].dt.time \
                >= dt.time(hour=12,minute=0))&(self.fullData['CallArrivalTime'].dt.time \
                    <= dt.time(hour=16,minute=0))        
            
            evening = (self.fullData['CallArrivalTime'].dt.time \
                >= dt.time(hour=16,minute=0))&(self.fullData['CallArrivalTime'].dt.time \
                    <= dt.time(hour=19,minute=0))
            
            night = (self.fullData['CallArrivalTime'].dt.time \
                >= dt.time(hour=19,minute=0))&(self.fullData['CallArrivalTime'].dt.time \
                    <= dt.time(hour=23,minute=59))

            self.fullData.loc[morning,'IntervalOfDay'] = 'morning'
            self.fullData.loc[afternoon,'IntervalOfDay'] = 'afternoon'
            self.fullData.loc[evening,'IntervalOfDay'] = 'evening'
            self.fullData.loc[night,'IntervalOfDay'] = 'night'
            
        except:
            logger.Logger.LOGERROR("data_tank.py", "DataTank::getProcessedData", "Unable to process data")
        return self.fullData

    def trainTestSplit(self, splitRatio=0.66):
        '''
        Splits the data in DataFrame object into train and test

        @param {int} splitRatio - ratio of the train test split
        @returns {DataFrame} - DataFrame objects of train and test split 
        '''

        try:
            _tSize = int(len(self.fullData) * splitRatio)
            self.trainData = self.fullData[:_tSize]
            self.testData = self.fullData[_tSize:]
        except:
            logger.Logger.LOGERROR("data_tank.py", "DataTank::trainTestSplit", "Unable to create train-test split")
        return self.trainData, self.testData