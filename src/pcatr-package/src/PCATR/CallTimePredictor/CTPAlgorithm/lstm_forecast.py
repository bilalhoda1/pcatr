#!/usr/bin/env python
# coding: utf-8

"""
This file implements the 'LstmForecast' class 
to compute the prediction results using a deep 
learning technique. It uses LSTM network 
(special kind of recurrent neural network) with 
sequence length of over 100.
"""

__author__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__copyright__ = 'Copyright 2019, Prediction of Call Arrival Times and Rates'
__credits__ = ['Afiniti Software Solutions (Pvt.) Ltd.']
__version__ = '0.0.1'
__maintainer__ = 'Emad Bin Abid, Ateeb Ahmed, Syed Bilal Hoda'
__status__ = 'dev'

# Libs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable

# Owned
from PCATR.Logger import logger


def slidingWindows(data, seq_length):
    x = []
    y = []

    for i in range(len(data)-seq_length-1):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)

class LSTM(nn.Module):

    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        super(LSTM, self).__init__()
        
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True)
        
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))
        
        c_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))
        
        # Propagate input through LSTM
        ula, (h_out, _) = self.lstm(x, (h_0, c_0))
        h_out = h_out.view(-1, self.hidden_size)
        out = self.fc(h_out)
        
        return out

class LstmForecast:
    '''
    This class implements algorithm 
    to compute the prediction results using a deep 
    learning technique. It uses LSTM network 
    (special kind of recurrent neural network) with 
    sequence length of over 100.
    '''
    def __init__(self):
        self.model = None
        self.trainData = None
        self.testData = None
        self.forecastData = None

    def fit(self, trainData):
        '''
        Fits the training model using lstm forecast

        @param {DataFrame} trainData - Training data
        @returns {LstmForecast} - self
        '''

        try:
            # pass
            self.trainData = trainData

            training_data = self.trainData.iloc[:,6:7].values
            seq_length = 2
            self.x, self.y = slidingWindows(training_data, seq_length)

            dataX = Variable(torch.Tensor(np.array(self.x)))
            dataY = Variable(torch.Tensor(np.array(self.y)))

            trainX = Variable(torch.Tensor(np.array(self.x[0:len(self.trainData)])))
            trainY = Variable(torch.Tensor(np.array(self.y[0:len(self.trainData)])))

            testX = Variable(torch.Tensor(np.array(self.x[len(self.trainData):len(self.x)])))
            testY = Variable(torch.Tensor(np.array(self.y[len(self.trainData):len(self.y)])))

            num_epochs = 1000
            learning_rate = 0.01

            input_size = 1
            hidden_size = 2
            num_layers = 1

            num_classes = 1

            lstm = LSTM(num_classes, input_size, hidden_size, num_layers)

            criterion = torch.nn.MSELoss()    # mean-squared error for regression
            optimizer = torch.optim.Adam(lstm.parameters(), lr=learning_rate)
            #optimizer = torch.optim.SGD(lstm.parameters(), lr=learning_rate)

            # Train the model
            for epoch in range(num_epochs + 1):
                outputs = lstm(trainX)
                optimizer.zero_grad()
                
                # obtain the loss function
                loss = criterion(outputs, trainY)
                
                loss.backward()
                
                optimizer.step()
                if epoch % 100 == 0:
                    print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))
            
            self.model = lstm
            return self

        except:
            logger.Logger.LOGERROR("lstm_forecast.py", "LstmForecast::fit", "Unable to train model")
            return None

    def predict(self, testData):
        '''
        Predicts using the training model for lstm forecast

        @param {DataFrame} testData - Testing data
        @returns {DataFrame} - Predicted values
        '''

        # try:
        if True:
            self.testData = testData
            
            testX = Variable(torch.Tensor(np.array(self.x[len(self.trainData):len(self.x)])))
            testY = Variable(torch.Tensor(np.array(self.y[len(self.trainData):len(self.y)])))

            lstm = self.model
            lstm.eval()
            train_predict = lstm(testX)

            self.forecastData = train_predict.data.cpu().numpy()
            return self.forecastData
        # except:
        #     logger.Logger.LOGERROR("lstm_forecast.py", "LstmForecast::predict", "Unable to predict forecast")
        #     return None
            
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