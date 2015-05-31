
import sys

def main():
    infile = sys.argv[1]
    standardSUS, ehrvisSUS, adlEhrvis = process(infile)
    print standardSUS


def process(infile):
    '''Read in results file and create 3 tables based on question type:
       1) SUS questions about standard EHRs
       2) SUS questions about EHRVis
       3) Additional questions about EHRVis
       In each table, retain background info about participants. '''
    standardSUS = []
    ehrvisSUS = []
    adlEhrvis = []
    with open(infile, 'r') as f:
        lines = f.readlines()
        nLines = len(lines)
        for i in range(1,nLines):
            response = lines[i].strip()

            # Parse sections
            answers = response.split("\t")
            background = answers[1:4]
            standardQs = answers[4:14] 
            ehrvisQs = answers[14:24]
            adlQs = answers[24:]

            # Add data from this particular response to the tables
            standardSUS.append(background + standardQs)
            ehrvisSUS.append(background + ehrvisQs)
            adlEhrvis.append(background + adlQs)
    return standardSUS, ehrvisSUS, adlEhrvis
   
def calcSUscore(t):
    '''Reads in a table of SUS question answers and calculates the System Usability Score'''
    

main()
