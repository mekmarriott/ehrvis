#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request

class MedicationEvent():
    '''This class ...Type of information represented here is a point, not a block.'''

    def __init__(self, queryResult):
        self.name = request.args.get('queryResult[subobj][foo]',0,type=int) #This is not correct yet
        pass

class MedicationTrack():
    '''This class represents a specific medication that a patient is taking over time. This encompasses MedicationEvents such as changing the dose or 
       changing to another brand/generic version of the same compound. I need to think about how to most effectively store MedicationEvents associated with this. '''

    def __init__(self):
        pass

class ClinicalNote():
    '''This class represents...'''
    def__init__(self):
        pass
