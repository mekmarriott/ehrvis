#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request
import json
from pprint import pprint

class MedicationEvent():
    '''This class ...Type of information represented here is a point, not a block.'''

    def __init__(self, data):
        # This gives the display name of the medication: print data["content"]["medication"]["display"]
        # Date written: print data["content"]["dateWritten"]
        # Status: print data["content"]["status"]
        # Prescriber (right now it is a URL. need to deal with thati): print data["content"]["prescriber"]["reference"]
        # Dose: print data["content"]["prescriber"]["reference"] 
        # Duration:
        # Reason: 
        # Class: 

#class MedicationTrack():
#    '''This class represents a specific medication that a patient is taking over time. This encompasses MedicationEvents such as changing the dose or 
#       changing to another brand/generic version of the same compound. I need to think about how to most effectively store MedicationEvents associated with this. '''

#    def __init__(self):
#        pass


with open('static/FHIR_Sandbox/medications.json') as data_file:    
    data = json.load(data_file)
    #pprint(data)
    #need to split the query results into individual entries
    entryList = data["entry"]
    for entry in entryList:
        drug = MedicationEvent(entry)
        
        print "-------------------------------------------------------------------------------------------"
        #x=x.encode("ascii")

    #x = request.args.get('data[medication][display]',"",type=string) 
    #x = data["display"]
    #
    #x = data["entry"][0]["title"]
        
    #drug = MedicationEvent(data)
    #print drug.name();
    
