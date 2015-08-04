"""Provides Analyst and Organization helper classes"""

import pyalgotrade
import numpy as np
from time import gmtime, strftime

class Analyst(object):
    def __init__(self, name, confidence = 0.1, group = 'EMORY_GIMG'):
        self.name = name.upper()
        self.weights = dict()
        self.total = 0.0
        self.group = group
        if (confidence > 1.0 or confidence < 0):
            self.confidence = 0.1
        else: self.confidence = confidence

    def assign_weight(self, instrument, weight):
        """
        Assigns weights to security. Overwrites as necessary
        
        Parameters
        ----------
        security : String
        Name of instrument whose weight you would like to assign. 
        
        weight : float
        Weight of the instrument, between 0.0 and 1.0     
        """
        if (weight > 1.0 or weight < 0.0):
            raise ValueError('Weight must be between 0.0 and 1.0')
        if self.weights.has_key(instrument):
            old_weight = self.weights[instrument]
            for instr in self.weights:
                self.weights[instr] *= (1 - weight) / (1 - old_weight)
        else:
            for instr in self.weights:
                self.weights[instr] *= (1 - weight)  

        self.weights[instrument] = weight  
        if len(self.weights) == 1: 
            self.weights[instrument] = 1.0
            
    def status(self):
        """Returns status of analyst """
        print "Printing current status for " + self.name
        print "--------------------------------------------"
        print "BEGIN ANALYST STATUS"
        print "Time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        print "Organization: " + self.group
        print "Analyst: " + self.name
        print "Confidence: " + str(self.confidence)
        for instr in self.weights:
            weight = self.weights[instr]
            print self.name + " weights [ " + instr.upper() + " ] at " + str(weight)
        print "END ANALYST STATUS"
        print "--------------------------------------------"
    
    def reset_weights(self):
        """ Resets weights """
        self.weights = dict()
        self.total = 0.0

    def debug_print_cumulative_weight(self):
        summ = 0.0
        for instr in self.weights:
            summ += self.weights[instr]
        print "TOTAL WEIGHTS FOR ANALYST: " + str(summ)

class Organization(object):
    def __init__(self, name = 'EMORY_GIMG'):
        self.name = name
        self.analysts = dict()
        self.cumul_confidence = 0.0
        self.weights = dict()

    def add_analyst(self, analyst, conf = None):
        """"
        Adds analyst of a given name

        Parameters
        ---------
        analyst : Analyst object
        Analyst to be added to Organization
 
        conf : Str (default = None)
        Determines how analyst confidence in organization is initialized

            None        :   Analyst begins with mean confidence
            'given'     :   Analyst begins with confidence as given
        """
        # base case

        if (self.analysts.has_key(analyst.name) == False):
            self.analysts[analyst.name] = analyst

            if (conf == None): 
                if (len(self.analysts) > 1):
                    av_confidence = self.cumul_confidence / len(self.analysts)
                    analyst.confidence = av_confidence

            self.cumul_confidence += analyst.confidence
        else: 
            print "FAILED: Analyst under name " + analyst.name + " already exists"
        self.normalize_confidence()

    def remove_analyst(self, analyst_name):
        """
        Removes analyst of a given name

        Parameters
        -----------
        analyst_name : String
        Name of analyst to be removed

        """
        analyst_name = analyst_name.upper()
        if (self.analysts.has_key(analyst_name)):
            self.cumul_confidence -= self.analysts[analyst_name].confidence
            del self.analysts[analyst_name]
            print "Analyst " + analyst_name + " removed"
        else:
            print "Analyst under name " + analyst.name + " does not exist"
        self.normalize_confidence()

    def status(self):
        """Provides summary of organization """
        print "Begin status report for " + self.name
        print "================================================="
        self.print_weights()
        self.print_confidence()
        for name in self.analysts:
            analyst = self.analysts[name]
            analyst.status()

        print "End report"
        print "================================================="

    def print_confidence(self):
        """Prints summary of analyst confidence """
        print "Confidences for analysts are as follows:"
        print "============================"
        for name in self.analysts:
            analyst = self.analysts[name]
            print analyst.name + ": " + str(analyst.confidence)

    def reset_confidence(self):
        """Establishes equality for all analyst confidences """
        if (len(self.analysts)== 0): return
        for name in self.analysts:
            analyst = self.analysts[name]
            analyst.confidence = 1.0 / len(self.analysts)


    def normalize_confidence(self):
        """Normalizes confidence ratings across analyst set"""
        if (self.cumul_confidence == 0.0 and len(self.analysts) > 0):
            print "WARNING: ZERO cumulative confidence"
            return
        for name in self.analysts:
            analyst = self.analysts[name]
            analyst.confidence /= self.cumul_confidence
        self.cumul_confidence = 1.0

    def get_weights(self):
        """Updates weights and returns organization's weightings"""
        self.weights = dict()
        for name in self.analysts:
            analyst = self.analysts[name]
            for instrument in analyst.weights:
                if (self.weights.has_key(instrument)):
                    self.weights[instrument] += analyst.weights[instrument] * analyst.confidence
                else:
                    self.weights[instrument] = analyst.weights[instrument] * analyst.confidence
        return self.weights

    def print_weights(self):
        """Prints weights on each instrument held by organization """
        self.get_weights()
        for instrument in self.weights:
            print self.name + " weights " + instrument + " at " + str(self.weights[instrument])

    def print_weights_debug(self):
        """Prints weights on each instrument held by organization """
        self.get_weights()
        sumup = 0.0
        for instrument in self.weights:
            print self.name + " weights " + instrument + " at " + str(self.weights[instrument])
            sumup += self.weights[instrument]
        print "======== Printing Data =========="
        print "total weight = " + str(sumup)
        print "==== Printing Analyst Weights ===="
        for name in self.analysts:
            analyst = self.analysts[name]
            analyst.debug_print_cumulative_weight()
            print analyst.weights
        print self.weights
        print '============ END DEBUG ============'

def main():
    """Tests functionalities of helper classes and methods """
    testing = True
    excessive = False
    if (testing):
        al1 = Analyst('Ivy Kang')
        al1.assign_weight('cmg', 0.673)
        al1.assign_weight('aapl', 0.215)

        al2 = Analyst('Charlie Brown')
        al2.assign_weight('cmg', 0.420)
        al2.assign_weight('orcl', 0.130)
        al2.assign_weight('bk', 0.32)
        al2.assign_weight('bk', 0.40)
        al2.assign_weight('cmg', 0.30)
        al2.assign_weight('aapl', 0.02)
        al2.assign_weight('aapl', 0.04)

        al3 = Analyst('Snoopy')
        al4 = Analyst('Mick Jagger')
        al5 = Analyst('Beavis and Butthead')
        # al.assign_weight('orcl', 0.4)
        # al.status()
        # al.reset_weights()
        # al.status()
        org = Organization()
        org.add_analyst(al1)
        org.add_analyst(al2)

        
        if (excessive):
            org.add_analyst(al3)
            org.add_analyst(al4)
            org.add_analyst(al5)

        #org.reset_confidence()
        org.print_confidence()
        org.print_weights_debug()

        ##org.status()

if __name__ == "__main__":
    main()

        
        
    