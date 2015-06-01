
import sys
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

def main():
    infile = sys.argv[1]
    standardSUS, ehrvisSUS, adlEhrvis = process(infile)
    #calcSUscore(standardSUS)
    #calcSUscore(ehrvisSUS)
    medStudents, physicians = splitByProfession(ehrvisSUS)
    zeroToOne, twoToFive, fiveToTen, tenUp = splitByEHRYears(ehrvisSUS)

    # For plotting med students and physician scores in a histogram: Interesting way of seeing whether a particular group was more harsh or lenient in general
    #avgSU, medSU, sd, medStudentIndivScores = calcSUscore(medStudents)
    #avgSU, medSU, sd, physicianIndivScores = calcSUscore(physicians)
    #plotSUscores(medStudentIndivScores, physicianIndivScores)

    # Plot standard EHR and EHRVis scores in a histogram. No separation by profession- this is across all users
    #overallAnalysis(standardSUS, ehrvisSUS)

    # Plot all users' answers to the 5 extra EHRVis questions
    analyzeExtraQuestions(adlEhrvis)


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


def overallAnalysis(standardSUS, ehrvisSUS):
    '''This function plots standard EHR and EHRVis scores in a histogram. No separation by profession- this is across all users'''
    avgSU, medSU, sd, standard = calcSUscore(standardSUS)
    avgSU, medSU, sd, ehrvis = calcSUscore(ehrvisSUS)

    plt.figure()
    plt.hist([standard, ehrvis], bins = 7, histtype='barstacked', color = ["steelblue", "lightskyblue"])
    plt.ylim([0,10]) # Raise y range to make plot look cleaner
    plt.legend(["Standard EHR System", "EHRVis Interface"])
    plt.title("Distribution of Standard Usability Scores Across All Participants")
    plt.xlabel('Standard Usability Score')
    plt.ylabel('Number of scores')
    plt.show()

def analyzeExtraQuestions(t):
    '''This function creates a multi-window histogram of user answers to the medical questions about EHRVis'''

    # Remove background info since we only want scores
    t = [ row[3:] for row in t ]

    #x = [0, 0, 0, 0]
    responses = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    # Process all responses
    for i in range(0,len(t)):
        for j in range(0, len(t[0])-1):
            ans = t[i][j]
            if ans == "Yes":
                responses[j][0] += 1
            if ans == "Somewhat":
                responses[j][1] += 1
            if ans == "Unsure":
                responses[j][2] += 1
            if ans == "No":
                responses[j][3] += 1
    print responses

    Q1 = responses[0]
    Q2 = responses[1]
    Q3 = responses[2]
    Q4 = responses[3]
    Q5 = responses[4]

    #plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=2, ncols=3)
    ax1, ax2, ax3, ax4, ax5, ax6 = axes.ravel()
    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.0)
    x = np.arange(4)
    width = 0.25

    # Question 1 plot
    ax1.bar(x, Q1, width, align='center')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])
    ax1.set_xlabel('x-label')
    ax1.set_ylabel('y-label')
    #ax1.set_title("Did EHRVis help you see patterns of patient interaction with medical system?", fontsize = 12)
    ax1.set_title("\n".join(wrap("Did EHRVis help you see patterns of patient interaction with medical system?", 12)))

    # Question 2 plot
    ax2.bar(x, Q2, width, align='center')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])
  
    # Question 3 plot
    ax3.bar(x, Q3, width, align='center')
    ax3.set_xticks(x)
    ax3.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])

    # Question 4 plot
    ax4.bar(x, Q4, width, align='center')
    ax4.set_xticks(x)
    ax4.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])

    # Question 5 plot
    ax5.bar(x, Q5, width, align='center')
    ax5.set_xticks(x)
    ax5.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])



    #f = plt.figure()
    #ax = f.add_axes([0.1, 0.1, 0.8, 0.8])
    #axes[0, 0].ax.bar(x, Q1, align='center')
    #ax.set_xticks(x)
    #ax.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'])
    plt.show()
    # add some text for labels, title and axes ticks
    #ax.set_ylabel('Scores')
    #ax.set_title('Scores by group and gender')
    #ax.set_xticks(ind+width)
    #ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
#    Plot scores for one system at a time for doctors and med students
#    physicians = np.array(physicians)
#    medStudents = np.array(medStudents)

#    plt.figure()
#    plt.hist([medStudents,physicians], 7, histtype='barstacked')
#    plt.show()

 
main()
