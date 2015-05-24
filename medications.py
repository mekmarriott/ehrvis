#!/usr/bin/env python
# The classes and methods in this file are used to parse and organize medication information from the Ajax queries made in app.py

from flask import Flask, request, json
from dateutil import parser
import datetime
from pprint import pprint
import urllib2

class MedicationEntry(object):
    '''This class represents a single medication entry in a patient's record. Its attributes consist of basic information about the drug originally
       obtained from a JSON-formatted query result. '''

    def __init__(self, name, start, status, dose, admMethod, end):
        try:
            # This gives the display name of the medication. Generally includes a dose:
            self.name =  name
            # Date written:
            self.start = start
            # Status:
            self.status = status
            # Dose: Another way to get this could be parsing the name field. Talk to group about this option. Also, may need variable for dose units.
            self.dose = dose
            # AdministrationMethod: 
            self.admMethod = admMethod
            # End Date: 
            self.end = end
            # Class: ATC drug classification obtained using the RxNorm API. For now, if a medication belongs to multiple subgroups, we will use the first one.
            self.classification = getClassification(self.name)
            # Display group
            self.display_group = 0
        except: 
            print "Malformed data for object initialization"
    '''Function: str 
        Prints out the string representation of the drug (for debugging/information purposes)'''
    def __str__(self):
        result = ""
        result += "Name: " + self.name + "\n"
        result += "Start Date:" + str(self.start) + "\n"
        result += "Status: " + self.status + "\n"
        result += "Dose: " + str(self.dose) + "\n"
        result += "Admin Method: " + self.admMethod + "\n"
        result += "End Date: " + str(self.end) + "\n"
        result += "Classification: " + str(self.classification) + "\n"
        result += "Display Group:" + str(self.display_group) + "\n" 
        return result

    def to_dict(self):
        return {'name': self.name, 'start': self.start, 'status': self.status, 'dose': self.dose, 'administrationMethod': self.admMethod, 'end': self.end, 'classification': self.classification, 'display_group': self.display_group}


class MedicationHistory(object):
    '''This class '''
    def __init__(self):
        self.meds = []
        self.minDate = datetime.datetime.now()
        self.medNames = []
        self.med2idx = {}
        self.idx2med = {}

    def add_meds(self, med_array):
        # make list of (unique) medication names
        self.medNames = list(set([med.name for med in med_array]))

        # map medication names to display groups (for tracked display)
        for i,name in enumerate(self.medNames):
            self.idx2med[i]=name
            self.med2idx[name]=i

        # add each MedicationEvent from the input array to the MedicationHistory
        for med in med_array:
            if type(med) is MedicationEntry:
                # set display group for current medication using the mapping generated above
                med.display_group = self.med2idx[med.name]

                # add MedicationEvent to history
                self.meds.append(med.to_dict())

                # update earliest time in history, if relevant
                if med.start != "n/a" and med.start < self.minDate:
                    self.minDate = med.start


        # viewing buffer for time window
        self.minDate = self.minDate - datetime.timedelta(days=30)
                
def initialize_epic(data):
    try:
        name =  data["content"]["medication"]["display"]
        start = data["content"]["dateWritten"]
        status = data["content"]["status"]
        dose = data["content"]["dosageInstruction"][0]["doseQuantity"]["value"] 
        admMethod = data["content"]["dosageInstruction"][0]["route"]["text"]
        end = data["content"]["dosageInstruction"][0]["timingSchedule"]["repeat"]["end"]
        return MedicationEntry(name, start, status, dose, admMethod, end)
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
        drug = MedicationEntry(name, start, "n/a", dose, "n/a", end)
        return drug
    except:
        return None

def load_patient1_meds():
    entryList = json.load(open('static/FHIR_Sandbox/patient1_medications.json'))
    returnList = []
    for entry in entryList:
        returnList.append(intialize_hapi(entry))
    history = MedicationHistory();
    history.add_meds(returnList)
    return history

def getClassification(name):
    # Get ATC classification of a drug using the RxNorm API.
    drug = name.split(' ')[0]
    classURL = 'http://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json?drugName=' + drug + '&relaSource=ATC'
    classReq = urllib2.urlopen(classURL)
    rxclass = json.loads(classReq.read())
    try:
        classification = rxclass["rxclassDrugInfoList"]["rxclassDrugInfo"][0]["rxclassMinConceptItem"]["className"]
        return classification
    except:
        return None

