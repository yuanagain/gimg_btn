""" Adjusts weights of analysts according to past performance, with parameters for learning """

import pyalgotrade
import numpy as np
## import sklearn

from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance

## trader object

class analyst(object):
    def __init__(self, name, confidence = 5):
        self.name = name
        self.weights = dict()
        self.total = 0.0
        if (confidence > 10 or confidence < 0):
            self.confidence = 5

    def assign_weight(self, instrument, weight):
        """
        Assigns weights to security. Overwrites as necessary
        
        Parameters
        ----------
        security : Name of instrument whose weight you would like to assign. 
        
        weight : Weight of the instrument, between 0.0 and 1.0     
        """
        if (self.total + weight > 1.0):
            print "sum of weights cannot exceed 1.0, please try again or reset"
        else:
            self.weights[instrument] = weight
            self.total += weight
            print self.name + " weights " + instrument + " at " + weight
            
    def status(self):
        """Returns status of analyst """
        print "printing current status for " + self.name
        print "confidence: " + self.confidence
        for instr in weights:
            weight = weights[instr]
            print self.name + " weights " + security + " at " + weight 
        print "Unassigned Weight: " + str(1.0 - self.total)
    
    def reset_weights(self):
        """ Resets weights """
        self.weights = dict()
        self.total = 0.0


        
        
    