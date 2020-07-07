#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'EDA' module to deal with exploratory
data analysis techniques for PCATR.CallTimePredictor
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
import seaborn as sns
import statistics

class EDA:
    '''
    This module implements the algorithms/functions to deal with exploratory
    data analysis techniques for PCATR.CallTimePredictor

    @param {DataFrame} dataframe - The dataset on which the analysis needs to be done
    '''

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def callDays(self):
        '''
        Gives the names of days at which the full dataset is spread

        @returns {array<string>} - Array containing unique days in the dataset
        '''

        return self.dataframe['DayOfWeek'].unique()

    def callTimeAndCallDifferenceInterval(self, showPlot=False):
        '''
        Gives the arrival differences between two consecutive calls

        @returns {array<string>} - Array containing arrival differences between two consecutive calls
        '''

        if showPlot:
            plt.xlabel("Arrival Differences")
            plt.ylabel("Total Count")
            plt.hist(self.dataframe['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

        return self.dataframe['CallDifferenceInterval']

    def eachDayCallCount(self, showPlot=False):
        '''
        Gives the count of calls for each individual day in the dataset

        @returns {DataFrame} - A DataFrame object consisting the count of calls for each individual day in the dataset
        '''

        callsEachDay = self.dataframe.groupby(["CallArrivalDate","DayOfWeek"]).size()
        if showPlot:
            # Histogram
            plt.figure(figsize=(12,8))
            plt.hist(callsEachDay)
            plt.show()

            # Line plot
            dayCount = len(list(self.dataframe['CallArrivalDate'].unique()))

            daySerialNumber = [i for i in range(1, dayCount + 1)]
            plt.xlabel('Days')
            plt.ylabel("Call Count")

            callsEachDayPerDate = self.dataframe.groupby(["CallArrivalDate"]).size()

            plt.plot(daySerialNumber, callsEachDayPerDate)
            plt.show()

            # Scatter plot
            _ = pd.DataFrame(callsEachDay)
            _.reset_index(inplace=True)

            plt.figure(figsize=(12,8))
            plt.scatter(_['DayOfWeek'], _[0])
            plt.show()

            # Swarm plot
            sns.swarmplot(_['DayOfWeek'], _[0])
            plt.show()

        return callsEachDay

    def eachDayCallCountDescription(self):
        '''
        Gives the description of count of calls for each
        individual day in the dataset

        @returns {DataFrame} - A DataFrame object consisting of description of the count of calls for each individual day in the dataset
        '''

        return self.eachDayCallCount().describe()

    def eachDayIntervalsCallCount(self, showPlot=False):
        '''
        Gives the count of calls for morning, afternoon, evening, 
        night intervals for each individual day in the dataset
        
        @returns {DataFrame} - DataFrame object with 'CallArrivalDate', 'IntervalOfDay' and column of count
        '''
        
        countByInterval = self.dataframe.groupby(['CallArrivalDate','IntervalOfDay']).size()
        countByInterval = pd.DataFrame(countByInterval)
        countByInterval.reset_index(inplace=True)

        if showPlot:
            sns.swarmplot(countByInterval['IntervalOfDay'], countByInterval[0])
            plt.show()
        
        return countByInterval

    def interdayCallCount(self):
        '''
        Gives the count of calls for each weekday grouped 
        over full dataset
        
        @returns {DataFrame} - DataFrame object with 'DayOfWeek' and column of count
        '''

        return self.dataframe.groupby(["DayOfWeek"]).size()

    def maxCallDifferenceInterval(self):
        '''
        Gives the maximum value of 'CallDifferenceInterval'
        
        @returns {int} - max value in dataframe['CallDifferenceInterval']
        '''

        return max(self.callTimeAndCallDifferenceInterval())

    def maxCallTime(self):
        '''
        Gives the maximum call arrival time for each day 
        from full dataset
        
        @returns {DataFrame} - DataFrame object with 'CallArrivalDate' and max call arrival time
        '''

        return self.dataframe.groupby(['CallArrivalDate'])['CallArrivalTime'].max()

    def meanCallCount(self):
        '''
        Gives the mean of call count on full dataset
        
        @returns {int} - mean of call count on full dataset
        '''

        return statistics.mean(self.eachDayCallCount())

    def minCallDifferenceInterval(self):
        '''
        Gives the minimum value of 'CallDifferenceInterval'
        
        @returns {int} - min value in dataframe['CallDifferenceInterval']
        '''

        return min(self.callTimeAndCallDifferenceInterval())

    def minCallTime(self):
        '''
        Gives the minimum call arrival time for each day 
        from full dataset
        
        @returns {DataFrame} - DataFrame object with 'CallArrivalDate' and min call arrival time
        '''

        return self.dataframe.groupby(['CallArrivalDate'])['CallArrivalTime'].min()

    def arrivalDifferencesPerDay(self, showPlot=False):
        '''
        Gives the arrival differences against each day
        
        @returns {List<DataFrame>} - List of dataframe columns for the arrival differences against each day
        '''

        monday = self.dataframe[self.dataframe['DayOfWeek'] =='Monday']
        tuesday = self.dataframe[self.dataframe['DayOfWeek'] =='Tuesday']
        wednesday = self.dataframe[self.dataframe['DayOfWeek'] =='Wednesday']
        thursday = self.dataframe[self.dataframe['DayOfWeek'] =='Thursday']
        friday = self.dataframe[self.dataframe['DayOfWeek'] =='Friday']
        saturday = self.dataframe[self.dataframe['DayOfWeek'] =='Saturday']
        sunday = self.dataframe[self.dataframe['DayOfWeek'] =='Sunday']

        if showPlot:
            # Monday    
            plt.xlabel("Arrival Differences for Monday")
            plt.ylabel("Total Count")
            plt.hist(monday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Tuesday    
            plt.xlabel("Arrival Differences for Tuesday")
            plt.ylabel("Total Count")
            plt.hist(tuesday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Wednesday
            wednesday = self.dataframe[self.dataframe['DayOfWeek'] =='Wednesday']
            plt.xlabel("Arrival Differences for Wednesday")
            plt.ylabel("Total Count")
            plt.hist(wednesday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Thursday   
            thursday = self.dataframe[self.dataframe['DayOfWeek'] =='Thursday']
            plt.xlabel("Arrival Differences for Thursday")
            plt.ylabel("Total Count")
            plt.hist(thursday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Friday  
            friday = self.dataframe[self.dataframe['DayOfWeek'] =='Friday']
            plt.xlabel("Arrival Differences for Friday")
            plt.ylabel("Total Count")
            plt.hist(friday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Saturday
            saturday = self.dataframe[self.dataframe['DayOfWeek'] =='Saturday']
            plt.xlabel("Arrival Differences for Saturday")
            plt.ylabel("Total Count")
            plt.hist(saturday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

            # Sunday  
            sunday = self.dataframe[self.dataframe['DayOfWeek'] =='Sunday']
            plt.xlabel("Arrival Differences for Sunday")
            plt.ylabel("Total Count")
            plt.hist(sunday['CallDifferenceInterval'], bins=100, edgecolor='black')
            plt.show()

        return [monday, tuesday, wednesday, thursday, friday, saturday, sunday]