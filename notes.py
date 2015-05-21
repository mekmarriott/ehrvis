#!/usr/bin/env python
# Need to parse query output to store information of interest

from flask import Flask, request, json
from dateutil import parser
import datetime 
from pprint import pprint

# note JSON format:
# // var note  = 
# // {
# // service: foo
# // preview: 
# // fulltext: 
# // visObject: 
# //  {
# //  id:-
# //  start: 'yyyy-mm-dd'
# //  group: Enum
# //  }
# // }

# group enumeration:
# // 1 - Note
# // 2 - Consult
# // 3 - Radiology Report 
# // 4 - Nursing Note


class NoteEntry(object):

    groupList = {1:"Note", 2:"Consult", 3:"Radiology Report", 4:"Nursing Note"}  

    def __init__(self, service, preview, fulltext, _id, start, group):
        try:
            self.service = service
            self.preview = preview
            self.fulltext = fulltext
            self.visObject = {'id': _id,'start': start,'group':group}
        except: 
            print "Malformed data for object initialization"


    def __str__(self):
        result = ""
        result += "Group: " + self.visObject["group"] + "\n"
        result += "Service: " + self.service + "\n"
        result += "Date: " + str(self.visObject["start"]) + "\n"
        result += "Preview: " + self.preview + "\n"
        return result

    def get_start(self):
        return self.visObject['start']

    def to_dict(self):
        return {'service':self.service, 'preview':self.preview,'fulltext':self.fulltext,'visObject':self.visObject}

class NoteHistory(object):
    def __init__(self):
        self.notes = []
        self.minDate = datetime.datetime.now()

    def __str__(self):
        result = ""
        for i,note in enumerate(self.notes):
            result += "Note " + str(i) + " preview:" + note["preview"] + "\n"
        return result

    def add_notes(self, note_array):
        for note in note_array:
            if type(note) is NoteEntry:
                self.notes.append(note.to_dict())
                start = note.get_start()
                if start != "n/a" and start < self.minDate:
                    self.minDate = start
        self.minDate = self.minDate - datetime.timedelta(days=30)


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
        return None

def load_mimic_notes():
    entryList = json.load(open('static/Note_Sandbox/mimic_notes.json'))
    returnList = []
    for i,entry in enumerate(entryList):
        returnList.append(initialize_mimic(entry))
        returnList[-1].visObject["id"]=i
    history = NoteHistory();
    history.add_notes(returnList)
    return history







