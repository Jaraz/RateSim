# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 09:47:36 2015

@author: jaycw_000
"""

import numpy as np

#Portfolio
class portfolio:
    def __init__(self, secs):
        self.secList = []
        self.secLIst = secs

    def returnSec(self):
        return self.opt
        
    def addSec(self, addList):
        self.secList += addList
    
    def removeLast(self):
        self.secList = self.secList[0:len(self.opt)-1]


#Option Classes
class security:
    desc = ""    
    
    #Freq is how many times per year the daily sim needs to run
    def __init__(self, paymentVec, notional):
        self.paymentVec = paymentVec
        self.notional = notional

    def returnDesc(self):
        return self.desc
    
    def returnNotional(self):
        return self.notional
        
            
class cash(security):
    desc = "cash payment"
    
    def payoff(self):
        return self.notional
        
class fra(security):
    desc = "FRA"
    
    def payoff(self):
        return 10
        