#!/usr/bin/env python
# The classes and methods in this file are used to parse and organize medication information from the Ajax queries made in app.py

from flask import Flask, request, json
from datetime import datetime, timedelta
from pprint import pprint
import urllib2
from sortedcontainers import SortedListWithKey, SortedList
from operator import itemgetter
from ehrvisutil import date2utc

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
            self.classification = ""#getClassification(self.name)
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


class MedicationTrack(object):
    ''' This is a container for MedicationEvents related to a single drug. Intervals in self.intervals are not sorted, but are sorted in self.mergedIntervals'''

    def __init__(self, triple, name, dose, doseUnits, admMethod, classification, end, start):
        try:
            # name: Name of the drug that the track is for (string)
            self.name = name
            # maxDose: Largest dose currently in the track
            self.maxDose = dose
            # doseUnits: Units of doses (ie mg)
            self.doseUnits = doseUnits
            # admMethod: How the drug is taken (ie oral)
            self.admMethod = admMethod
            # classification: ATC classification of the drug obtained through RxNorm
            self.classification = classification
            # lastEnd: the end date of the last interval on the track
            self.lastEnd = end
            # lastStart: the start date of the last interval on the track
            self.lastStart = start
            # intervals: a list containing each recorded time period where the patient was prescribed the drug. Consists of [start, end, dose] triples
            self.intervals = []
            # mergedIntervals: a list generated by calling consolidateTrack. It sorts the intervals and merges those that overlap.
            self.mergedIntervals = []
     
            # Upon initialization, add the initializing MedicationEntry to the track's intervals
            self.intervals.append(triple)
            self.active=False;
        except:
            print "Malformed data for MedicationTrack object initialization"

    def __str__(self):
        ''' String representaion for debugging'''
        result = ""
        result += "Drug Name: " + str(self.name) + "\n"
        result += "Intervals:" + "\n"
        for block in self.intervals:
            result += "\t" + str(block[2]) + " " + str(block[0]) + " to " + str(block[1]) + "\n"
        return result


    def getDict(self):
        ''' This function packages the MedicationTrack as a dict, which is processed by the app front end to display the medication track. 

            Keys/Values
            plotData: a list of lists with the following structure: [ [range1_start, dose], [range1_end, dose], None, [range2_start, dose], [range2_end, dose] ...]
            lastEnd: is the end point of the track.
            lastStart: the start date of the final range in the track
            drugName: the name of the drug represented by the track
            maxDose: the maximum dose in the track
            doseUnits: the units of the doses
            admMethod: how the drug is administered
            classification: ATC classification of the drug obtained through RxNorm
        '''
        plotData = []
        if self.mergedIntervals is None:
            return None
        for entry in self.mergedIntervals:
            plotData.append([date2utc(entry[0]), entry[2]])
            plotData.append([date2utc(entry[1]), entry[2]])
            plotData.append(None) #spacer
        return { 'plotData': plotData, 'lastEnd': date2utc(self.lastEnd), 'lastStart': date2utc(self.lastStart), 'drugName': self.name, 'maxDose': self.maxDose, 
                    'doseUnits': self.doseUnits, 'admMethod': self.admMethod, 'classification': self.classification, 'active':self.lastEnd > datetime.now() }  

        
    def addEvent(self, triple):
        ''' This function adds a medication event to the medication track '''
        # Add MedicationEntry to the track.
        self.intervals.append(triple)

        print triple
        currStart = triple[0]
        currEnd = triple[1]
        currDose = triple[2]

        # Adjust lastStart and lastEnd if necessary
        if currEnd > self.lastEnd:
            self.lastEnd = currEnd
        if currStart > self.lastStart:
            self.lastStart = currStart

        # Update maximum dose if the current event has a higher dose than the previous maximum
        if currDose > self.maxDose:
            self.maxDose = currDose
        return

    def consolidateTrack(self):
        '''This function takes in a series of start-end-dose tuples from a MedicationTrack and merges overlapping ranges. If the doses of conflicting ranges are different, the higher dose is prioritized.'''
        result = []
        sortedTrack = sorted(self.intervals, key=lambda x:(x[1], x[0]))

        if len(sortedTrack) == 1:
            entry = list(sortedTrack[0])
            self.mergedIntervals = [entry]
            return

        initInterval = sortedTrack[0]
        currStart = initInterval[0]
        currEnd =  initInterval[1]
        currDose =  initInterval[2]
        result.append(list(initInterval))

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

def initialize_epic(data):
    try:
        defaultEnd = date.today()
        name =  data["content"]["medication"]["display"]

        start = data["content"]["dosageInstruction"][0]["timingSchedule"]["event"][0]["start"]
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")

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
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        return MedicationEntry(name, start, status, dose, doseUnits, admMethod, end)
    except: 
        print "Malformed data for object initialization"
        return None



def initialize_hapi(entry):
    '''For use with HAPI medication data. Creates a medicationEntry object by parsing data from the provided JSON entry'''
    try:
        start = entry["resource"]["dateWritten"]
        start = datetime.strptime(start, "%Y-%m-%d")
        name = entry["resource"]["medication"]["display"].strip()
        duration = timedelta(days=1)
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

def load_playground_meds():
    '''For use with manually entered Epic Playground medication data'''

    defaultEnd = datetime.today() 
    infile = "static/epic_playground/epic_medications.txt"
    returnList = []
    tracks = {}
    outputTracks = []

    with open(infile, 'r') as f:
        for line in f:
            line = line.strip()
            info = line.split("\t")
            name = info[0]
            start = datetime.strptime(info[1], '%Y-%m-%d')
            if info[2] == "n/a": 
                end = defaultEnd
            else:
                end =  datetime.strptime(info[2], '%Y-%m-%d')
            dose = float(info[3])
            doseUnits = info[4]
            admMethod = info[5]
 
            entry = MedicationEntry(name, start, "n/a", dose, doseUnits, "n/a", end)
            addToTrack(entry, tracks)
    for key, track in tracks.items():
        track.consolidateTrack()
        d = track.getDict()
        outputTracks.append(d)
    output = sorted(outputTracks, key=lambda x:(x.get('lastEnd'), x.get('lastStart')), reverse = True)
    return output
            

def load_patient1_meds():
    entryList = json.load(open('static/FHIR_Sandbox/patient1_medications.json'))
    returnList = []
    tracks = {}
    outputTracks = []
    for entry in entryList:
        medEntry = initialize_hapi(entry)
        if medEntry:
            addToTrack(medEntry, tracks)
        else:
            print "EMPTY"
            print entry["resource"]["medication"]["display"].strip()
            print 
    for key, track in tracks.items():
        track.consolidateTrack()
        d = track.getDict()
        outputTracks.append(d)
    output = sorted(outputTracks, key=lambda x:(x.get('lastEnd'), x.get('lastStart')), reverse = False)
    for idx,track_dict in enumerate(output):
        track_dict['rank']=idx+1
    return output

def getClassification(name):
    # Get ATC classification of a drug using the RxNorm API.
    drug = name.replace (" ", "+")
    classURL = 'http://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json?drugName=' + drug + '&relaSource=ATC'
    classReq = urllib2.urlopen(classURL)
    rxclass = json.loads(classReq.read())
    try:
        classification = rxclass["rxclassDrugInfoList"]["rxclassDrugInfo"][0]["rxclassMinConceptItem"]["className"]
        return classification
    except:
        return None


