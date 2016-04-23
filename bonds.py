# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 15:35:26 2015

@author: jaycw_000
"""

from __future__ import division
from fredapi import Fred
import numpy
import scipy
import matplotlib
from matplotlib import pyplot
from scipy import interpolate
from scipy import optimize
import numpy as np
import datetime
fred = Fred(api_key='ba6be791f155502772efcac065904210')

#date frame should have CMT dates for now and CMT yield - par 100
#compouning should be 1 for annual, 2 for semi, 4 for quarterly
#interp flag unused right now
class bondCurve:
    def __init__(self, df, compounding, interp="Linear"):
        self.data = df/100     
        self.compounding = compounding
        self.interp = interp
        self.dates = [0, 0.0833333, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
        self.curve = [0.0025, 0.0025, 0.0035, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.0225, 0.025, 0.03]
        self.spotRefresh()
        self.buildCurve()

    def spotRefresh(self):
        self.spotCurve = interpolate.interp1d(self.dates, self.curve)
        
    def bp(self,t1,t2,coupon):
        mat = (datestr2num(t2)-datestr2num(t1))/365
        price = self.dfBondPricer(mat,coupon)
        yiel  = ytm(mat, coupon, self.compounding, price)
        delta = dv01(mat, coupon, self.compounding, yiel)
        dur   = duration(int(round(mat)), coupon, self.compounding, yiel)
        return price, yiel, delta, dur
        
    #Clean Price
    def dfBondPricer(self, maturity, coupon):
        price = 0

        periods = int(maturity//(1./self.compounding))
        remainder = (maturity - periods * (1./self.compounding))
        periods+=1
        ai = 1 - remainder/(1./self.compounding)
        if remainder==0:
            periods-=1
            ai = 0
            remainder=1./self.compounding
            
        if maturity < 0.5:
            df = self.discFact(maturity)            
            price = coupon * maturity * df * 100
        else:
            for i in xrange(0, periods): 
                t = remainder + 1.0 / self.compounding * i
                df = self.discFact(t)
                price += (coupon/self.compounding) * df * 100
                #print maturity,periods,remainder,t,df,price,ai
            price+= -ai * coupon/self.compounding * 100

        df = self.discFact(maturity)
        price += 100 * df
        return price 
        
    def bondOptim(self, x, i):
        self.curve[i] = x
        self.spotRefresh()
        answer = self.dfBondPricer(self.dates[i], self.data[i-1]) - 100
        #print x, answer
        return answer
        
    def buildCurve(self):
        for i in xrange(1, len(self.curve)):
            self.curve[i] = scipy.optimize.brentq(self.bondOptim, a = 0.00011, b = 0.0999, args = (i))
        self.curve[0] = self.curve[1]
        self.spotRefresh()

    def discFact(self, t):
        return 1 / (1 + self.spotCurve(t) / self.compounding)**(self.compounding*t)
        
    def plotSpot(self):
        x = np.linspace(0,30)
        plot(x, self.spotCurve(x))
        
    def plotFwd(self):
        x = np.linspace(0.5,30)
        y = self.fwdRate(x)
        plot(x, y)

    def fwdRate(self, t):
        df1 = self.discFact(t-0.5)
        df2 = self.discFact(t)
        return (df1/df2-1)*2
        
    

#compounding = 1 - annual, 2 - semi
def bondPrice(maturity, coupon, compounding, YTM):
    #period calc
    periods = int(maturity//(1./compounding))
    remainder = (maturity - periods * (1./compounding))/(1./compounding)
    periods+=1
    if remainder==0:
        remainder=1
        periods-=1
        
    ai = 1 - remainder

    price = 0
    for i in xrange(0, periods): 
        price += (coupon/compounding) / (1 + YTM / compounding)**(remainder+i) * 100

    price += 100 / (1 + YTM / compounding)**(remainder + periods-1)
    
    return price - ai * coupon/compounding * 100

def plotBond(maturity, coupon, compounding):
    ytmVec = numpy.array(range(0,10))/100

    answer = bondPrice(maturity, coupon, compounding, ytmVec)
    plot(ytmVec, answer)
    
    
def ytm(maturity, coupon, compounding, price):
    func = lambda x: bondPrice(maturity, coupon, compounding, x) - price
    answer = scipy.optimize.brentq(func, a = 0.0000001, b = 10)
    return answer    

def duration(maturity, coupon, compounding, YTM):
    price = bondPrice(maturity, coupon, compounding, YTM)
    numer = 0
    for i in xrange(1, maturity * compounding+1):
        numer += (i/compounding * coupon/compounding) / (1 + YTM / compounding)**i * 100
    numer += (maturity * 100) / (1 + YTM / compounding)**(maturity*compounding)

    return numer / price

def modDuration(maturity, coupon, compounding, YTM):
    return duration(maturity, coupon, compounding, YTM) / (1 + YTM/compounding)
    
def dv01(maturity, coupon, compounding, YTM):
    delta = 0.0001
    return (bondPrice(maturity, coupon, compounding, YTM+delta/2.0)-bondPrice(maturity, coupon, compounding, YTM-delta/2.0))/2.0

def bond(maturity, coupon, compounding, YTM):
    print "Price    = ", bondPrice(maturity, coupon, compounding, YTM)
    #print "Duration = ", duration(maturity, coupon, compounding, YTM)
    print "ModDur   = ", modDuration(maturity, coupon, compounding, YTM)
    print "bpv      = ", -modDuration(maturity, coupon, compounding, YTM) * 0.0001 * bondPrice(maturity, coupon, compounding, YTM)
    #print "act bpv  = ", bondPrice(maturity, coupon, compounding, YTM+0.0001) - bondPrice(maturity, coupon, compounding, YTM)


curveMar2 = bondCurve(df.loc['2016-03-02'].values,2)
price10s  = curveMar2.bp('2016-03-02','2025-11-15',0.0225)
price30s  = curveMar2.bp('2016-03-02','2046-02-15',0.025)

print "nov 25s: ", price10s
print "feb 46s: ", price30s

print price30s[3]/price10s[3]

#print bondPrice(9.712,0.0225,2,0.01865)
#print bondPrice(29.9781,0.025,2,0.0269)
#print ""
#x10 = dv01(9.712,0.0225,2,0.01865)
#x30 = dv01(29.9781,0.025,2,0.0269)