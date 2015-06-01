
import sys
import numpy as np

def main():
    infile = sys.argv[1]
    standardSUS, ehrvisSUS, adlEhrvis = process(infile)
    #calcSUscore(standardSUS)
    #calcSUscore(ehrvisSUS)
    medStudents, physicians = splitByProfession(ehrvisSUS)
    zeroToOne, twoToFive, fiveToTen, tenUp = splitByEHRYears(ehrvisSUS)


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
    # Remove background info since we only want scores
    t = [ row[3:] for row in t ]

    indivScores = []
    avgSU = 0

    for i in range(0,len(t)):	#Loop over rows
        currSU = 0
        for j in range(0,len(t[0])):	#Loop over cols
            numQ = j + 1
            if numQ % 2 == 0:	
                # If the question number is even, the score contribution is 5 minus the answer
                ans = int(t[i][j])
                ans = 5 - ans
                currSU = currSU + ans
            else:
                # If the question number is odd, the score contribution is the answer - 1
                ans = int(t[i][j])
                ans = ans - 1 
                currSU = currSU + ans
        indivScores.append(2.5*currSU)    
    print indivScores
    avgSU = np.mean(indivScores) 
    medSU = np.median(indivScores)
    sd = np.std(indivScores)
    #print medSU
    print avgSU
    #print sd
    return avgSU, medSU, sd, indivScores


def splitByProfession(t):
    '''This function splits the table by profession (med student or physician) and returns the two groups. Only accomodates those groups right now'''
    medStudents = []# row[0]=="Medical Student") row for row in t ]
    physicians = []
    for row in t:
        if row[0] == "Medical Student":
            medStudents.append(row)
        else:
            physicians.append(row)
    
    return medStudents, physicians
    #calcSUscore(medStudents)
    #calcSUscore(physicians)

def splitByEHRYears(t):
    '''This function splits the table by years of experience with EHRs and returns the groups separately. '''
    zeroToOne = []
    twoToFive = []
    fiveToTen = []
    tenUp = []
    for row in t:
        if row[1] == "0-1":
            zeroToOne.append(row)
        elif row[1] == "2-5":
            twoToFive.append(row)
        elif row[1] == "5-10":
            fiveToTen.append(row)
        else:
            tenUp.append(row)
    #print "0 to 1 years:"
    #calcSUscore(zeroToOne)
    #print "2 to 5 years:"
    #calcSUscore(twoToFive)
    #print "5 to 10 years:"
    #calcSUscore(fiveToTen)
    #print "10+ years:"
    #calcSUscore(tenUp)
    return zeroToOne, twoToFive, fiveToTen, tenUp 



 
main()
