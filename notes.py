#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request, json
from dateutil import parser
import datetime 
from pprint import pprint



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
        return {'service':self.service, 'preview':self.preview,'time':self.time,         
                'type':self._type, 'inpatient': self.inpatient, 'id':self._id, 'heightcount':self.heightcount}

class NoteHistory(object):

    services = ["Medicine", "Emergency Medicine", "Critical Care", "Other"]
    serv2color = {services[0]:'#ee2222',services[1]:'#2222dd',services[2]:'#ee22cc',services[-1]:'#222222'}


    def __init__(self):
        self.notes = {}
        self.notesByDate = {}
        self.notesByID = {}
        self.minDate = datetime.datetime.now().date()      # as late as any possible dates
        self.maxDate = datetime.datetime(1900,1,1).date()  # earlier than all reasonable dates
        self.series = {}
        self.hospitalizations = []

    def __str__(self):
        result = ""
        for i,note in enumerate(self.notes):
            result += "Note " + str(i) + " preview:" + note["preview"] + "\n"
        return result

    def standard_service(self,service):
        if service == "Medicine":
            return self.services[0]
        elif service == "General Medicine":
            return self.services[0]
        elif service == "Internal Medicine":
            return self.services[0]
        elif service == "Emergency Medicine":
            return self.services[1]
        elif service == "Critical Care":
            return self.services[2]
        elif service == "General Surgery":
            return self.services[-1]
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

            while idx < max_-1:
                idx+=1


                # look for next inpatient note. this defines the start date of the hospitalization
                if self.notes[ks[idx]].inpatient:
                    hosp = [str(self.notes[ks[idx]].time.date())]

                    while idx < max_:
                        # look for next outpatient note. this defines the end date of the hospitalization
                        idx += 1 
                        if idx == max_:
                            # if reach end of notes without reverting to outpatient, put today's date as end date
                            hosp.append(str(datetime.datetime.now().date()))



                            # append current hospitalization to hospitalization list
                            self.hospitalizations.append(hosp)

                            # exit while loop 
                            break  


                        if not self.notes[ks[idx]].inpatient:
                            # append time from PREVIOUS note to "hosp" as end date
                            hosp.append(str(self.notes[ks[idx-1]].time.date()))

                            # append current hospitalization to hospitalization list
                            self.hospitalizations.append(hosp)

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

                    # maintain a dictionary of notes: key = ID, value = note
                    # ------------------------------------------------------
                    self.notesByID[note._id]=note

                    # maintain an array of notes for each active calendar day
                    # -------------------------------------------------------

                    # 1. get note date
                    t = note.time.date()

                    # 2. make dict entry for date if doesn't exist yet, key = date, value = array of notes 
                    if str(t) not in self.notesByDate:
                        self.notesByDate[str(t)]=[]

                    # 3. associate note count (by day) information with note
                    # this is the ith (i=current array length) note of the day; we will plot note at height proportional to i
                    note.heightcount = len(self.notesByDate[str(t)])+1

                    # 4. add note to corresponding calendar day
                    self.notesByDate[str(t)].append(note.to_dict())



                    # 5. compare to latest and earliest dates, modify either if superseded
                    if t != "n/a":
                        if t < self.minDate:
                            self.minDate = t
                        if t > self.maxDate:
                            self.maxDate = t


                    # add to [time,height] pair to corresponding dataseries (by service)
                    # ------------------------------------------------------------------

                    # 1. get service
                    s = self.standard_service(note.service)

                    # 2. make dict entry for service if doesn't exist, key = service, value = plot data and color
                    if s not in self.series:
                        self.series[s]={'color':self.serv2color[s],'data':[]}

                    # 3. append [time,height] pair to relevant data series
                    self.series[s]['data'].append([str(t),note.heightcount])


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
        start = parser.parse(start)
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
        time = parser.parse(time)
        _type = entry["type"]
        inpatient = entry["inpatient"]=="true" or entry["inpatient"]=="True" 
        return NoteEntry(service,preview,fulltext,_id,time,_type,inpatient)
    except:
        print "Malformed data for NoteEntry object population"
        return None    

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








