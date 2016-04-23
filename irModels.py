# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 21:50:49 2015

@author: jaycw_000
"""

from __future__ import division
import numpy as np
import scipy
import yieldCurve
import Random
import matplotlib
from matplotlib import pyplot

class irEngine:
    def __init__(self, model, portfolio):
        self.model = model        
        self.port = portfolio

class hoLee:
    def __init__(self, rate, sigma):
        self.sigma = sigma
        self.r0 = rate
        self.rnd = Random.randMC(False, False)
        
    def plotSpotCurve(self):
        numPer = 120

        dates = np.linspace(0,numPer*0.25,numPer+1)
        bonds = np.exp(-self.r0 * dates + 1./6 * self.sigma**2 * dates**3)
        fwds = (bonds[:-1]/bonds[1:] - 1) / 0.25

        pyplot.plot(dates[0:120], fwds)
        
    def bondPricer(self, r, t, T):
        dt = T-t
        return numpy.exp(-r * dt + 1./6 * self.sigma**2 * dt**3)        
        
    #DF to T0, not future df
    def analyticDF(self, t):
        return numpy.exp(-self.r0 * t + 1/6 * self.sigma**2 * t**3)
    
    def euler(self, evoTime, paths, steps):
        dt = evoTime / steps
        rndNumbers = self.rnd.genNormalMatrix(paths, steps)
        r_last = self.r0        
        
        discount = 0
        for i in xrange(steps):
            r_next = r_last + self.sigma * numpy.sqrt(dt) * rndNumbers[i]
            discount += r_last
            r_last = r_next

        return numpy.mean(numpy.exp(-discount*dt)) #* self.bondPrice(r_next,5,5)
    
modelHoLee = hoLee(200/10000, 100/10000)
testTime = 2
print "Analytic DF: ", modelHoLee.analyticDF(testTime)
print "Euler DF: ", modelHoLee.euler(testTime,10000,testTime*12)