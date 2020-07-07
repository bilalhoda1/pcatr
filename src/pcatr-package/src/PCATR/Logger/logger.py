#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'Logger' module to deal with efficient
logging mechanisms in PCATR where necessary.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

class Logger:
    '''
    This module implements function  to deal with efficient
    logging mechanisms in PCATR where necessary.
    '''

    def __init__(self):
        pass

    @staticmethod
    def LOGERROR(filename, functionName, errorSummary, errorObject=None):
        '''
        Logs the error occurrences for PCATR

        @param {string} filename - Name of file in which the function is called
        @param {string} functionName - Name of function in which the function is called
        @param {string} errorSummary - A short error description
        @param {string} errorObject - Full error with stack trace
        @returns {None} 
        '''

        if errorObject != None:
            print("[-]ERROR:\t {}\t {}\t {}".format(filename, functionName, errorSummary))
        else:
            print("[-]ERROR:\t {}\t {}\t {}\n{}".format(filename, functionName, errorSummary, errorObject))
    
    @staticmethod
    def LOGDEBUG(filename, functionName, debugSummary):
        '''
        Logs the success/debug/analytical occurrences for PCATR

        @param {string} filename - Name of file in which the function is called
        @param {string} functionName - Name of function in which the function is called
        @param {string} debugSummary - A short debug description
        @returns {None} 
        '''

        print("[+]DEBUG:\t {}\t {}\t {}".format(filename, functionName, debugSummary))
        
    @staticmethod
    def LOGINFO(filename, functionName, infoSummary):
        '''
        Logs the general information occurrences for PCATR

        @param {string} filename - Name of file in which the function is called
        @param {string} functionName - Name of function in which the function is called
        @param {string} infoSummary - A short info description
        @returns {None} 
        '''

        print("[!]INFO:\t {}\t {}\t {}".format(filename, functionName, infoSummary))