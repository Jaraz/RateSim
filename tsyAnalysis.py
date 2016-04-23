# -*- coding: utf-8 -*-
"""
Created on Mon Feb 01 20:56:10 2016

@author: jaycw_000
"""

from __future__ import division
from fredapi import Fred
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import optimize
import statsmodels.formula.api as smf
import statsmodels.api as sm
import sklearn

fred = Fred(api_key='ba6be791f155502772efcac065904210')

localDir = 'C:\Users\jaycw_000\Documents\GitHub\EDAnalysis\srvixclose.csv'
localDir2 = 'C:\Users\jaycw_000\Documents\GitHub\EDAnalysis\sp500.xls'
fred = Fred(api_key='ba6be791f155502772efcac065904210')

startDate = '2010-01-01'
endDate = '2016-03-25'

def pullData(startDate, endDate):
    
    df = {}
    df["cmt1m"] = fred.get_series('DGS1MO', observation_start = startDate, observation_end = endDate)
    df["cmt3m"] = fred.get_series('DGS3MO', observation_start = startDate, observation_end = endDate)
    df["cmt6m"] = fred.get_series('DGS6MO', observation_start = startDate, observation_end = endDate)
    df["cmt1"] = fred.get_series('DGS1', observation_start = startDate, observation_end = endDate)
    df["cmt2"] = fred.get_series('DGS2', observation_start = startDate, observation_end = endDate)
    df["cmt3"] = fred.get_series('DGS3', observation_start = startDate, observation_end = endDate)
    df["cmt5"] = fred.get_series('DGS5', observation_start = startDate, observation_end = endDate)
    df["cmt7"] = fred.get_series('DGS7', observation_start = startDate, observation_end = endDate)
    df["cmt10"] = fred.get_series('DGS10', observation_start = startDate, observation_end = endDate)    
    df["cmt20"] = fred.get_series('DGS20', observation_start = startDate, observation_end = endDate)
    df["cmt30"] = fred.get_series('DGS30', observation_start = startDate, observation_end = endDate)
    
    df = pd.DataFrame(df)
    
    df = df[['cmt1m', 'cmt3m', 'cmt6m', 'cmt1', 'cmt2', 'cmt3', 'cmt5', 'cmt7', 'cmt10', 'cmt20', 'cmt30']]    
    
    df.dropna()    
    
    return df

def plotDate(tVec, df):
    x = [0.0833333, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    ax = plt.figure()
    ax = plt.subplot(111)
    for i in tVec:    
        ax.plot(x, df.loc[i].values, label=i)

    ax.legend(loc='upper left')
    plt.show()

def plotGFly(sDate, eDate, first, second, third, df):
    test = -df[first] + 2 * df[second] - df[third]
    plot(test[test.notnull()][sDate:eDate])

    #first minus second
def plotSpread(sDate, eDate, first, second, df):
    test = df[first] - df[second]
    plot(test[test.notnull()][sDate:eDate])

def plotRate(sDate, eDate, first, df):
    test = df[first]
    plot(test[test.notnull()][sDate:eDate])

#plot & return rolling realized vol
def realizedVol(sDate, eDate, product, days, df):
    df = df.dropna()
    test = df[df.notnull()][sDate:eDate][product]
    answer = myrolling_apply(test, days, realFunc)
    plot(answer)
    return answer

def realFunc(df, days):
    ret = df[1:] - df.shift(1)[1:]
    ret2 = np.power(ret,2)
    return np.sqrt(252 * np.sum(ret2)/(days-2)) * 100
    
def myrolling_apply(df, N, f, nn=1):
    ii = [int(x) for x in arange(0, df.shape[0] - N + 1, nn)]
    out = [f(df.iloc[i:(i + N)],N) for i in ii]
    out = pd.Series(out)
    out.index = df.index[N-1::nn]
    return(out)
    
#df = pullData(startDate,endDate)
#date = ['2010-01-05', '2011-01-03', '2012-01-03', '2013-01-03', '2014-01-02', '2015-01-05', '2016-01-29', '2016-02-25']
#date = ['2015-01-05', '2016-01-29', '2016-02-25', '2016-03-07']
#plotDate(date, df)
#plotGFly('2015-01-05','2016-03-10', 'cmt2', 'cmt10', 'cmt30', df)