#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request
import json
from pprint import pprint

class MedicationEntry():
    '''This class ...'''

    def __init__(self, data):
        # This gives the display name of the medication:
        self.name =  data["content"]["medication"]["display"]
        # Date written:
        self.start = data["content"]["dateWritten"]
        # Status:
        self.status = data["content"]["status"]
        # Prescriber (right now it is a URL. need to deal with that): 
        self.prescriber = data["content"]["prescriber"]["reference"]
        # Dose: Another way to get this could be parsing the name field. Talk to group about this option
        self.dose = data["content"]["dosageInstruction"][0]["doseQuantity"]["value"] 
        # AdministrationMethod: 
        self.admMethod = data["content"]["dosageInstruction"][0]["route"]["text"]
        # End Date: 
        self.end = data["content"]["dosageInstruction"][0]["timingSchedule"]["repeat"]["end"]
        # Duration: 
        # Reason: I haven't figured out how to get this yet
        # Class: I haven't figured out how to get this yet

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
        drug = MedicationEntry(entry)
        print drug.name 
        print "-------------------------------------------------------------------------------------------"

        
    
