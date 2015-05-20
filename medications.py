#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request, json
from dateutil import parser
import datetime
from pprint import pprint

class MedicationEntry(object):
    '''This class ...'''

    def __init__(self, name, start, status, prescriber, dose, admMethod, end):
        try:
            # This gives the display name of the medication:
            self.name =  name
            # Date written:
            self.start = start
            # Status:
            self.status = status
            # Prescriber (right now it is a URL. need to deal with that): 
            self.prescriber = prescriber
            # Dose: Another way to get this could be parsing the name field. Talk to group about this option
            self.dose = dose
            # AdministrationMethod: 
            self.admMethod = admMethod
            # End Date: 
            self.end = end
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
        result += "Start Date:" + str(self.start) + "\n"
        result += "Status: " + self.status + "\n"
        result += "Prescriber: " + self.prescriber + "\n"
        result += "Dose: " + str(self.dose) + "\n"
        result += "Admin Method: " + self.admMethod + "\n"
        result += "End Date: " + str(self.end)
        return result

    def to_dict(self):
        return {'name': self.name, 'start': self.start, 'status': self.status, 'prescriber': self.prescriber, 'dose': self.dose, 'administrationMethod': self.admMethod, 'end': self.end}


class MedicationHistory(object):
    def __init__(self):
        self.meds = []
        self.minDate = datetime.datetime.now()

    def add_meds(self, med_array):
        med_array_set = set(med_array);
        med_array = list(med_array_set);
        for med in med_array:
            if type(med) is MedicationEntry:
                self.meds.append(med.to_dict())
                if med.start < self.minDate and med.start != "n/a":
                    self.minDate = med.start
        self.minDate = self.minDate - datetime.timedelta(days=30)
                
def initialize_epic(data):
    try:
        name =  data["content"]["medication"]["display"]
        start = data["content"]["dateWritten"]
        status = data["content"]["status"]
        prescriber = data["content"]["prescriber"]["reference"]
        dose = data["content"]["dosageInstruction"][0]["doseQuantity"]["value"] 
        admMethod = data["content"]["dosageInstruction"][0]["route"]["text"]
        end = data["content"]["dosageInstruction"][0]["timingSchedule"]["repeat"]["end"]
        return MedicationEntry(name, start, status, prescriber, dose, admMethod, end)
    except: 
        print "Malformed data for object initialization"
        return None

# with open('static/SMART_Sandbox/medications.json') as data_file:    
#     data = json.load(data_file)
#     #pprint(data)
#     #need to split the query results into individual entries
#     entryList = data["entry"]
#     for entry in entryList:
#         drug = MedicationEntry(entry)
#         print str(drug)
#         print "-------------------------------------------------------------------------------------------"

def intialize_hapi(entry):
    try:
        start = entry["resource"]["dateWritten"]
        start = parser.parse(start)
        name = entry["resource"]["medication"]["display"]
        duration = datetime.timedelta(days=1)
        timeUnit = entry["resource"]["dispense"]["expectedSupplyDuration"]["units"]
        if timeUnit == "months":
            duration *= 30
        elif timeUnit == "weeks":
            duration *= 7
        numUnits = entry["resource"]["dispense"]["expectedSupplyDuration"]["value"]
        duration *= int(numUnits)
        end = start + duration
        dose = entry["resource"]["dispense"]["quantity"]["value"]
        if "units" in entry["resource"]["dispense"]["quantity"]:
            dose += " " + entry["resource"]["dispense"]["quantity"]["units"]
        drug = MedicationEntry(name, start, "n/a", "n/a", dose, "n/a", end)
        return drug
    except:
        return None

def load_patient1_meds():
    with open('static/FHIR_Sandbox/patient1_medications.json') as medication_json:
        entryList = json.load(medication_json)
        returnList = []
        for entry in entryList:
            returnList.append(intialize_hapi(entry))
        history = MedicationHistory();
        history.add_meds(returnList)
        return history


        
    
