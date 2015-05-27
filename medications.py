#!/usr/bin/env python
# The classes and methods in this file are used to parse and organize medication information from the Ajax queries made in app.py

from flask import Flask, request, json
from dateutil import parser
import datetime
from pprint import pprint
import urllib2
from sortedcontainers import SortedListWithKey, SortedList
from dateutil.parser import *
from operator import itemgetter

class MedicationEntry(object):
    '''This class represents a single medication entry in a patient's record. Its attributes consist of basic information about the drug originally
       obtained from a JSON-formatted query result. '''

    def __init__(self, name, start, status, dose, doseUnits, admMethod, end):
        try:
            # This gives the display name of the medication. Generally includes a dose:
            self.name = name
            # Date written:
            self.start = start
            # Status:
            self.status = status
            # Dose: 
            self.dose = float(dose)
            # Dose units
            self.doseUnits = doseUnits
            # AdministrationMethod: 
            self.admMethod = admMethod
            # End Date: 
            self.end = end
            # Class: ATC drug classification obtained using the RxNorm API. For now, if a medication belongs to multiple subgroups, we will use the first one.
            self.classification = getClassification(self.name)
            # Display group
            self.display_group = 0
            # Tuple containing the start date, end date, and dose of the MedicationEntry
            self.triple = (start, end, dose)
        except: 
            print "Malformed data for MedicationEntry object initialization"
 
    def __str__(self):
        '''Function: str 
        Prints out the string representation of the drug (for debugging/information purposes)'''
        result = ""
        result += "Name: " + self.name + "\n"
        result += "Start Date:" + str(self.start) + "\n"
        result += "Status: " + self.status + "\n"
        result += "Dose: " + str(self.dose) + "\n"
        result += "Dose Units: " + str(self.doseUnits) + "\n"
        result += "Admin Method: " + self.admMethod + "\n"
        result += "End Date: " + str(self.end) + "\n"
        if (self.classification is None):
            result += "Classification: " + "n/a" + "\n"
        else: 
            result += "Classification: " + str(self.classification) + "\n"
        result += "Display Group:" + str(self.display_group) + "\n" 
        return result

    def to_dict(self):
        return {'name': self.name, 'start': self.start, 'status': self.status, 'dose': self.dose, 'doseUnits': self.doseUnits, 'administrationMethod': self.admMethod, 'end': self.end, 'classification': self.classification, 'display_group': self.display_group}

class MedicationTrack(object):
    ''' This is a container for MedicationEvents related to a single drug. Intervals in self.intervals are not sorted, but are sorted in self.mergedIntervals'''

    def __init__(self, triple, name, dose, doseUnits, admMethod, classification, end, start):
        try:
            self.name = name
            self.maxDose = dose
            self.doseUnits = doseUnits
            self.admMethod = admMethod
            self.classification = classification
            self.lastEnd = end
            self.lastStart = start
            self.intervals = []
            self.mergedIntervals = []
            # Add the initializing MedicationEntry to the track's intervals
            self.intervals.append(triple)
         
        except:
            print "Malformed data for MedicationTrack object initialization"

    def __str__(self):
        '''For debugging'''
        result = ""
        result += "Drug Name: " + str(self.name) + "\n"
        result += "Intervals:" + "\n"
        for block in self.intervals:
            result += "\t" + str(block[2]) + " " + str(block[0]) + " to " + str(block[1]) + "\n"
        return result

    def getDict(self):
        ''' This function packages the MedicationTrack as a dict, which is processed by the app front end to display the medication track.'''
        plotData = []
        if self.mergedIntervals is None:
            print self.name
            return None
        for entry in self.mergedIntervals:
            plotData.append([entry[0], entry[2]])
            plotData.append([entry[1], entry[2]])
            plotData.append(None) #spacer
        #print (self.mergedIntervals[-1])[0]
        #exit()
        return { 'plotData': plotData, 'lastEnd': self.lastEnd, 'lastStart': self.lastStart, 'drugName': self.name, 'maxDose': self.maxDose, 'doseUnits': self.doseUnits, 'admMethod': self.admMethod, 
               'classification': self.classification, 'trackStart': self.lastStart, 'trackEnd': self.lastEnd }  
        
    def addEvent(self, triple):
        ''' This function adds a medication event to the medication track '''
        # Add MedicationEntry to the track. It will be sorted by end date in ascending order, and then by start date in ascending order
        self.intervals.append(triple)

        currStart = triple[0]
        currEnd = triple[1]
        currDose = triple[2]
        # Adjust lastStart and lastEnd if necessary
        if(currEnd > self.lastEnd):
            self.lastEnd = currEnd
        if(currStart > self.lastStart):
            self.lastStart = currStart
        # Update maximum dose if the current event has a higher dose than the previous maximum
        if(currDose > self.maxDose):
            self.maxDose = currDose
        return

    def consolidateTrack(self):
        '''This function takes in a series of start-end-dose tuples from a MedicationTrack and merges overlapping ranges. If the doses of conflicting ranges are different, the higher dose is prioritized.'''
        result = []
        sortedTrack = sorted(self.intervals, key=lambda x:(x[1], x[0]))

        if len(sortedTrack) == 1:
            return sortedTrack

        initInterval = sortedTrack[0]
        result.append(initInterval)
        currStart = initInterval[0]
        currEnd =  initInterval[1]
        currDose =  initInterval[2]

        for start, end, dose in sortedTrack[1:]:
            if start > currEnd:
                # This interval starts after its predecessor stops, so just add it to results
                result.append([start, end, dose])
                currStart, currEnd, currDose = start, end, dose
            else: 
                # There is overlap, so we need to merge
                if currDose == dose:
                    # Since the dose is the same, we can consolidate these into one big interval
                    result[-1] = [currStart, end, dose]
                else:
                    result[-1] = [currStart, start, currDose]
                    result.append([start, max(currEnd, end), dose])
                    currStart = start
                    currDose = dose
                currEnd = max(currEnd, end)
        self.mergedIntervals = result
        return


class MedicationHistory(object):
    '''This class looks at all medications a patient is on and keeps track of unique medication names and the minimum date among them.'''
    def __init__(self):
        self.meds = []
        self.minDate = date.today()
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
        defaultEnd = date.today()
        name =  data["content"]["medication"]["display"]
        start = parse(data["content"]["dosageInstruction"][0]["timingSchedule"]["event"][0]["start"])
        status = data["content"]["status"]
        dose = int(data["content"]["dosageInstruction"][0]["doseQuantity"]["value"]) 
        doseUnits = None
        frequency = int(data["content"]["dosageInstruction"][0]["timingSchedule"]["repeat"]["frequency"])
        dose = dose*frequency
        admMethod = data["content"]["dosageInstruction"][0]["route"]["text"]
        end = data["content"]["dosageInstruction"][0]["timingSchedule"]["repeat"]["end"]
        if (end == "0001-01-01T00:00:00"):
            end = defaultEnd
        else:
            end = parse(end)
        return MedicationEntry(name, start, status, dose, doseUnits, admMethod, end)
    except: 
        print "Malformed data for object initialization"
        return None

def addToTrack(entry, tracks):
    ''' Given a MedicationEntry object, this function adds it to a MedicationTrack, creating a new track if none exists for that drug.'''
    name = entry.name
    if name in tracks:
        currTrack = tracks.get(name)
        currTrack.addEvent(entry.triple)
    else:
        newTrack = MedicationTrack(entry.triple, entry.name, entry.dose, entry.doseUnits, entry.admMethod, entry.classification, entry.end, entry.start)
        tracks[name] = newTrack
    return



def initialize_hapi(entry):
    try:
        start = parse(entry["resource"]["dateWritten"]).date()
        name = entry["resource"]["medication"]["display"].strip()
        duration = datetime.timedelta(days=1)
        timeUnit = entry["resource"]["dispense"]["expectedSupplyDuration"]["units"]
        if timeUnit == "months":
            duration *= 30
        elif timeUnit == "weeks":
            duration *= 7
        numUnits = entry["resource"]["dispense"]["expectedSupplyDuration"]["value"]
        duration *= int(numUnits)
        end = start + duration
        doseUnits = None
        dose = entry["resource"]["dispense"]["quantity"]["value"]
        if "units" in entry["resource"]["dispense"]["quantity"]:
            doseUnits = entry["resource"]["dispense"]["quantity"]["units"]
        drug = MedicationEntry(name, start, "n/a", dose, doseUnits, "n/a", end)
        return drug
    except:
        return None

def load_patient1_meds():
    entryList = json.load(open('static/FHIR_Sandbox/patient1_medications.json'))
    returnList = []
    tracks = {}
    outputTracks = []
    for entry in entryList:
        medEntry = initialize_hapi(entry)
        addToTrack(medEntry, tracks)
    for key, track in tracks.items():
        track.consolidateTrack()
        d = track.getDict()
        outputTracks.append(d)
    output = sorted(outputTracks, key=lambda x:(x.get('lastEnd'), x.get('lastStart')), reverse = True)
    for t in output:
        print str(t.get('lastStart')) + " " + str(t.get('lastEnd'))
    return output

def getClassification(name):
    # Get ATC classification of a drug using the RxNorm API.
    #drug = name.split(' ')[0]
    drug = name.replace (" ", "+")
    classURL = 'http://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json?drugName=' + drug + '&relaSource=ATC'
    classReq = urllib2.urlopen(classURL)
    rxclass = json.loads(classReq.read())
    try:
        classification = rxclass["rxclassDrugInfoList"]["rxclassDrugInfo"][0]["rxclassMinConceptItem"]["className"]
        return classification
    except:
        return None

load_patient1_meds()
