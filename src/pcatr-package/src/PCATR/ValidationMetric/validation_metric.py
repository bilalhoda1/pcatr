#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'ValidationMetric' class 
to compute validation results of trained models on
test samples.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
from sklearn.metrics import mean_squared_error
from math import sqrt

class ValidationMetric:
    '''
    This class implements algorithms to compute 
    validation results of trained models on
    test samples.
    '''
    def __init__(self):
        pass

    def meanSquaredError(self, actual, predicted):
        '''
        Finds the mean square error between actual
        and predicted values

        @param {DataFrame column} actual  - Actual values
        @param {DataFrame column} predicted - Predicted values
        @returns {int} mean squared error value  
        '''

        mse = mean_squared_error(actual, predicted)
        return mse

    def rootMeanSquaredError(self, actual, predicted):
        '''
        Finds the root mean square error between actual
        and predicted values

        @param {DataFrame column} actual  - Actual values
        @param {DataFrame column} predicted - Predicted values
        @returns {int} mean squared error value  
        '''

        mse = sqrt(mean_squared_error(actual, predicted))
        return mse