#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request
import json
from pprint import pprint

class MedicationEvent():
    '''This class ...Type of information represented here is a point, not a block.'''

    def __init__(self, data):
        self.name = request.args.get('data[medication][display]',"",type=string) #This may not be correct yet


#class MedicationTrack():
#    '''This class represents a specific medication that a patient is taking over time. This encompasses MedicationEvents such as changing the dose or 
#       changing to another brand/generic version of the same compound. I need to think about how to most effectively store MedicationEvents associated with this. '''

#    def __init__(self):
#        pass

#class ClinicalNote():
#    '''This class represents...'''
#    def__init__(self):
#        pass


with open('static/FHIR_Sandbox/medications.json') as data_file:    
    data = json.load(data_file)
    #pprint(data)
    #x = request.args.get('data[medication][display]',"",type=string) 
    #x = data["display"]
    #
    x = data["entry"][0]["title"]
    #y = data.get("title")i
    print data.values()
    for k, v in data.items():
        print k, v, "\n"
        
    #drug = MedicationEvent(data)
    #print drug.name();
