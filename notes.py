#!/usr/bin/env python

# Author: Baris Ungun
# Description: Defines Note & NoteHistory object classes and auxiliary methods for populating them from JSON data


from flask import json
from datetime import datetime, timedelta
from ehrvisutil import date2utc

class NoteEntry(object):

    def __init__(self, service, preview, fulltext, _id, time, _type = "Other/Unknown", inpatient=False):
        try:
            self._type = _type
            self.service = service
            self.time = time
            self.preview = preview
            self.fulltext = fulltext
            self._id = _id
            self.inpatient = inpatient
            self.heightcount = 0
        except: 
            print "Malformed data for object initialization"


    def __str__(self):
        result = ""
        result += "Type: " + self._type + "\n"
        result += "Service: " + self.service + "\n"
        result += "Date: " + str(self.time) + "\n"
        result += "Preview: " + self.preview + "\n"
        return result


    def to_dict(self):
        # omit "fulltext" for faster loading
        return {'service':self.service, 'preview':self.preview,'time':self.time.strftime('%A %d %B %Y, %-I:%M %p'),         
                'type':self._type, 'inpatient': self.inpatient, 'id':self._id, 'heightcount':self.heightcount}

class NoteHistory(object):

    services = ["Medicine", "Emergency Medicine", "Critical Care", "Imaging Studies", "Laboratory Studies", "Procedures", "Other"]
    serv2color = {services[0]:'#2244dd',services[1]:'#dd2222',services[2]:'#dd9933',services[3]:'green',services[4]:'purple',services[5]:'brown',services[-1]:'#222222'}
    serv2icon = {services[0]:'circle',services[1]:'circle',services[2]:'circle',services[3]:'diamond',services[4]:'diamond',services[5]:'cross',services[-1]:'circle'}

    def __init__(self):
        self.notes = {}
        self.notesByDate = {}
        self.notesByService = {}
        self.previewsByService = {}
        self.minDate = datetime.now()      # as late as any possible dates
        self.maxDate = datetime(1900,1,1)  # earlier than all reasonable dates
        self.series = {}
        self.hospitalizations = []

    def __str__(self):
        result = ""
        for i,k in enumerate(self.notes):
            result += "Note " + str(i) + " preview:" + self.notes[k].preview + "\n"
        return result

    def standard_service(self,service, _type):
        if "Emergency" in service:
            return self.services[1]
        elif "Critical Care" in service:
            return self.services[2]
        elif "CCU" in service:
            return self.services[2]
        elif "General Surgery" in service:
            return self.services[-1]
        elif "Radiology" in service:
            return self.services[3]
        elif "Sonography" in service:
            return self.services[3]
        elif "Laboratory" in service:
            return self.services[4]
        elif "Colonoscopy" in _type:
            return self.services[5]
        elif "Medicine" in service:
            return self.services[0]
        else:
            return self.services[-1]



    def compile_hospitalizations(self):
        try:
            if not self.notes:
                print "cannot compile hospitalizations from empty note list \n"
                return

            ks = self.notes.keys()
            ks.sort()


            # current key index
            idx = -1
            
            # number of keys
            max_ = len(ks)

            hosp = []

            while idx < max_-1:
                idx+=1

                # look for next inpatient note. this defines the start date of the hospitalization
                if self.notes[ks[idx]].inpatient or "H&P" in self.notes[ks[idx]]._type:
                    hosp.append(date2utc(self.notes[ks[idx]].time))
                    print hosp

                    while idx < max_:
                        # look for next outpatient note. this defines the end date of the hospitalization
                        idx += 1 
                        if idx == max_:
                            # if reach end of notes without reverting to outpatient, put today's date as end date
                            hosp.append(date2utc(self.maxDate))
                            print hosp

                            # append current hospitalization to hospitalization list
                            self.hospitalizations.append(hosp)

                            hosp = []

                            # exit while loop 
                            break  

                        if "Discharge" in self.notes[ks[idx]]._type:
                            # append time from CURRENT note to "hosp" as end date
                            hosp.append(date2utc(self.notes[ks[idx]].time))

                            print hosp

                            # append current hospitalization to hospitalization list
                            self.hospitalizations.append(hosp)

                            hosp = []

                            # exit while loop 
                            break

                        if not self.notes[ks[idx]].inpatient:

                            # append time from PREVIOUS note to "hosp" as end date
                            hosp.append(date2utc(self.notes[ks[idx-1]].time))

                            print hosp

                            # append current hospitalization to hospitalization list
                            self.hospitalizations.append(hosp)

                            hosp = []

                            # exit while loop 
                            break


 
            return
        except:
            print "error while attempting to compile hospitalizations from note list \n"
            return                                             



    def add_notes(self, note_array):
        try:
            for note in note_array:
                if type(note) is NoteEntry:



                    # maintain a dictionary of notes: key = timestamp, value = note
                    # -------------------------------------------------------------
                    self.notes[str(note.time)]=note


                    # maintain a earliest and latest dates in note history
                    # ----------------------------------------------------

                    # 1. get note timestamp
                    t = note.time

                    # 2. compare to latest and earliest dates, modify either if superseded
                    if t != "n/a":
                        if t < self.minDate:
                            self.minDate = t
                        if t > self.maxDate:
                            self.maxDate = t                    

                    # maintain a dictionary of events on each day: key = active calendar day, value = count
                    # -------------------------------------------------------------------------------------


                    # 1. make dict entry for date if doesn't exist yet, key = date, initial value = 0
                    if str(t.date()) not in self.notesByDate:
                        self.notesByDate[str(t.date())]=0

                    # 2. increment count 
                    self.notesByDate[str(t.date())]+=1

                    # 3. associate note count (by day) information with note
                    # this is the ith (i=current array length) note of the day; we will plot note at height proportional to i
                    note.heightcount = self.notesByDate[str(t.date())]

     


                    # add to [time,height] pair to corresponding dataseries (by service)
                    # ------------------------------------------------------------------

                    # 1. get service
                    s = self.standard_service(note.service, note._type)

                    # 2. make dict entry for service if doesn't exist, key = service, value = plot data and color
                    if s not in self.series:
                        self.series[s]={'label':s,'color':self.serv2color[s],'symbol':self.serv2icon[s], 'data':[]}

                    # 3. append [time,height] pair to relevant data series
                    self.series[s]['data'].append([date2utc(t),note.heightcount])

                    # 4. assign note ID by its position within the note series (use 0-based indexing)
                    _id = len(self.series[s]['data'])-1

                    note._id = _id   


                    # maintain dictionaries of notes and note previews by service
                    # ---------------------------------------

                    # 1. make dict entry for service if doesn't exist, key = service, value = note dict by ID
                    if s not in self.notesByService:
                        self.notesByService[s]={}
                        self.previewsByService[s]={}

                    # 2. add current note to corresponding dictionary position
                    self.notesByService[s][_id]=note
                    
                    # 3. add preview of current note to corresponding dictionary position
                    self.previewsByService[s][_id]=note.to_dict()

            # add viewing buffer to latest and earliest times
            self.minDate = self.minDate - datetime.timedelta(days=1)
            self.maxDate = self.minDate + datetime.timedelta(days=1)

            return 
        except:
            print "Malformed data for NoteHistory object population"
            return 



def initialize_mimic(entry):
    try:
        service = entry["service"]
        preview = entry["preview"]
        fulltext = entry["fulltext"]
        _id = entry["visObject"]["id"]
        start = entry["visObject"]["start"]
        # start = parser.parse(start)
        start = datetime.strptime(start, "%Y-%m-%d %H:%M" ) #2012-01-13 10:00
        group = entry["visObject"]["group"]
        
        return NoteEntry(service, preview, fulltext, _id, start, group)
    except:
        print "Malformed data for NoteEntry object population"
        return None

def initialize_epic(entry):
    try:
        service = entry["service"]
        preview = entry["preview"]
        fulltext = entry["fulltext"]
        _id = entry["visObject"]["id"]
        time = entry["visObject"]["start"]
        time = datetime.strptime(time, "%Y-%m-%d %H:%M" ) #2012-01-13 10:00
        _type = entry["type"]
        inpatient = entry["inpatient"]=="true" or entry["inpatient"]=="True" 
        return NoteEntry(service,preview,fulltext,_id,time,_type,inpatient)
    except:
        print "Malformed data for NoteEntry object population"
        return None    


def load_playground_notes():
    entryList = json.load(open('static/Note_Sandbox/playground.json'))
    returnList = []
    for i,entry in enumerate(entryList):
        returnList.append(initialize_epic(entry))
        returnList[-1]._id=i
    history = NoteHistory();
    history.add_notes(returnList)
    history.compile_hospitalizations()
    return history    

def load_epic_notes():
    entryList = json.load(open('static/Note_Sandbox/notes.json'))
    returnList = []
    for i,entry in enumerate(entryList):
        returnList.append(initialize_epic(entry))
        returnList[-1]._id=i
    history = NoteHistory();
    history.add_notes(returnList)
    history.compile_hospitalizations()
    return history    

def load_mimic_notes():
    entryList = json.load(open('static/Note_Sandbox/mimic_notes.json'))
    returnList = []
    for i,entry in enumerate(entryList):
        returnList.append(initialize_mimic(entry))
        returnList[-1].visObject["id"]=i
    history = NoteHistory();
    history.add_notes(returnList)
    return history








