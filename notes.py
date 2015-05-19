#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request
import json
from pprint import pprint

class NoteEntry():
    '''This class ...'''

    def __init__(self, data):
        try:
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
        except: 
            print "Malformed data for object initialization"
    '''Function: str 
        Prints out the string representation of the drug (for debugging/information purposes)'''
    def __str__(self):
        result = ""
        result += "Name: " + self.name + "\n"
        result += "Start Date:" + self.start + "\n"
        result += "Status: " + self.status + "\n"
        result += "Prescriber: " + self.prescriber + "\n"
        result += "Dose: " + self.dose + "\n"
        result += "Admin Method: " + self.admMethod + "\n"
        result += "End Date: " + self.end
        return result

#class MedicationTrack():
#    '''This class represents a specific medication that a patient is taking over time. This encompasses MedicationEvents such as changing the dose or 
#       changing to another brand/generic version of the same compound. I need to think about how to most effectively store MedicationEvents associated with this. '''

#    def __init__(self):
#        pass


with open('static/Note_Sandbox/notes.json') as data_file:    
    data = json.load(data_file)
    #pprint(data)
    #need to split the query results into individual entries
    entryList = data["entry"]
    for entry in entryList:
        drug = MedicationEntry(entry)
        print str(drug)
        print "-------------------------------------------------------------------------------------------"