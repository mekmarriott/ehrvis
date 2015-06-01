
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

    #Output comprehensive summary statistics
    printSummaryStatistics(standardSUS, ehrvisSUS)

    # For plotting med students and physician scores in a histogram: Interesting way of seeing whether a particular group was more harsh or lenient in general
    #mavgSU, mmedSU, msd, medStudentIndivScores = calcSUscore(medStudents)
    #pavgSU, pmedSU, psd, physicianIndivScores = calcSUscore(physicians)
    #print "Med Students (" + str(len(medStudentIndivScores)) + "): " + str(msd) + " Doctors (" + str(len(physicianIndivScores)) + "): " + str(psd)
    #plotSUscores(medStudentIndivScores, physicianIndivScores)

    # Plot standard EHR and EHRVis scores in a histogram. No separation by profession- this is across all users. For presentation
    #overallAnalysis(standardSUS, ehrvisSUS)

    # Plot all users' answers to the 5 extra EHRVis questions. For presentation
    #analyzeExtraQuestions(adlEhrvis)


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
  
def printSummaryStatistics(standard, ehrvis):
    '''This function calculates SU scores for the standard and EHRVis systems and then prints a summary of their statistics, including:
       -Overall (all participants): Mean, Median, Standard Deviation
       -Split between physicians and med students: Mean, Median, SD
       -Split by years of EHR experiance: Mean, Median, Standard Deviation
    Also, print specifications for a Latex table to file.
    '''
    # Get overall results for standard system
    oSAvg, oSMed, oSSD, oSIndivScores = calcSUscore(standard)
    # Get overall results for EHRVis
    oEAvg, oEMed, oESD, oEIndivScores = calcSUscore(ehrvis)

    # Get physician results for standard system
    medStudentsStandard, physiciansStandard = splitByProfession(standard)
    nDoctors = len(physiciansStandard)
    nStudents = len(medStudentsStandard)
    pSAvg, pSMed, pSSD, pSIndivScores = calcSUscore(physiciansStandard)
    # Get med student results for standard system
    mSAvg, mSMed, mSSD, mSIndivScores = calcSUscore(medStudentsStandard)
     # Get physician results for EHRVis system
    medStudentsEhrvis, physiciansEhrvis = splitByProfession(ehrvis)
    pEAvg, pEMed, pESD, pEIndivScores = calcSUscore(physiciansEhrvis)
    # Get med student results for EHRVis system
    mEAvg, mEMed, mESD, mEIndivScores = calcSUscore(medStudentsEhrvis)

    sZeroToOne, sTwoToFive, sFiveToTen, sTenUp = splitByEHRYears(standard)
    eZeroToOne, eTwoToFive, eFiveToTen, eTenUp = splitByEHRYears(ehrvis)

    # Get results for standard system by years of EHR Use (in same order as above)
    zoSAvg, zoSMed, zoSSD, zoSIndivScores = calcSUscore(sZeroToOne)
    tfSAvg, tfSMed, tfSSD, tfSIndivScores = calcSUscore(sTwoToFive)
    ftSAvg, ftSMed, ftSSD, ftSIndivScores = calcSUscore(sFiveToTen)
    tSAvg, tSMed, tSSD, tSIndivScores = calcSUscore(sTenUp) 
    # Get results for EHRVis system by years of EHR Use (in same order as above)
    zoEAvg, zoEMed, zoESD, zoEIndivScores = calcSUscore(eZeroToOne)
    tfEAvg, tfEMed, tfESD, tfEIndivScores = calcSUscore(eTwoToFive)
    ftEAvg, ftEMed, ftESD, ftEIndivScores = calcSUscore(eFiveToTen)
    tEAvg, tEMed, tESD, tEIndivScores = calcSUscore(eTenUp)
    # Get size of each group
    nZO = len(zoSIndivScores)
    nTF = len(tfSIndivScores)
    nFT = len(ftSIndivScores)
    nT = len(tSIndivScores)

    print "Standard System: Mean, Median, and Standard Deviation"
    print "\t Overall: " + str(oSAvg) + "\t" + str(oSMed) + "\t" + str(oSSD)
    print "\t Med Students (" + str(nStudents) + "): " + str(mSAvg) + "\t" + str(mSMed) + "\t" + str(mSSD) 
    print "\t Doctors (" + str(nDoctors) + "): " + str(pSAvg) + "\t" + str(pSMed) + "\t" + str(pSSD) 
    print "\t 0-1 Years Experience (" + str(nZO) + "): " + str(zoSAvg) + "\t" + str(zoSMed) + "\t" + str(zoSSD) 
    print "\t 2-5 Years Experience (" + str(nTF) + "): " + str(tfSAvg) + "\t" + str(tfSMed) + "\t" + str(tfSSD) 
    print "\t 5-10 Years Experience (" + str(nFT) + "): " + str(ftSAvg) + "\t" + str(ftSMed) + "\t" + str(ftSSD) 
    print "\t 10+ Years Experience (" + str(nT) + "): " + str(tSAvg) + "\t" + str(tSMed) + "\t" + str(tSSD) 

    print "EHRVis Interface: Mean, Median, and Standard Deviation"
    print "\t Overall: " + str(oEAvg) + "\t" + str(oEMed) + "\t" + str(oESD)
    print "\t Med Students (" + str(nStudents) + "): " + str(mEAvg) + "\t" + str(mEMed) + "\t" + str(mESD) 
    print "\t Doctors (" + str(nDoctors) + "): " + str(pEAvg) + "\t" + str(pEMed) + "\t" + str(pESD) 
    print "\t 0-1 Years Experience (" + str(nZO) + "): " + str(zoEAvg) + "\t" + str(zoEMed) + "\t" + str(zoESD) 
    print "\t 2-5 Years Experience (" + str(nTF) + "): " + str(tfEAvg) + "\t" + str(tfEMed) + "\t" + str(tfESD) 
    print "\t 5-10 Years Experience (" + str(nFT) + "): " + str(ftEAvg) + "\t" + str(ftEMed) + "\t" + str(ftESD) 
    print "\t 10+ Years Experience (" + str(nT) + "): " + str(tEAvg) + "\t" + str(tEMed) + "\t" + str(tESD) 

    # LATEX File Section: Standard EHR
    o = open("standard_summary_table_20.tex", 'w')
    o.write('% Please add the following required packages to your document preamble:' + "\n")
    o.write('\usepackage[table,xcdraw]{xcolor}' + "\n")
    o.write(str('\\') + "begin{table}[h]" + "\n")
    o.write(str('\\') + "begin{tabular}{|l|l|l|l|}" + "\n")
    o.write(str('\\') + 'hline' + "\n")
    o.write(str('\\') + 'rowcolor[HTML]{191870}' + "\n") 
    o.write(str('\\') + 'multicolumn{1}{|c|}{\cellcolor[HTML]{191870}{\color[HTML]{FFFFFF} {\\bf Group}}} & {\color[HTML]{FFFFFF}{\\bf Mean}} & {\color[HTML]{FFFFFF} {\\bf Median}} & {\color[HTML]{FFFFFF} {\\bf Std. Dev.}} \\\\ \hline' + "\n")
    o.write('All Participants                                                           & ' + str(oSAvg) + '                       & ' + str(oSMed) + '                          & ' + str(oSSD) + '                              \\\\ \hline' + "\n")
    o.write('Medical Students (' + str(nStudents) + ')' + '                                                           & '+ str(mSAvg) + '                       & ' + str(mSMed) + '                          & ' + str(mSSD) + '                              \\\\ \hline' + "\n")
    o.write('Physicians (' + str(nDoctors) + ')' + '                                                                 & ' + str(pSAvg) + '                       & ' + str(pSMed) + '                          & ' + str(pSSD) + '                              \\\\ \hline' + "\n")
    o.write('0-1 Years Experience (' + str(nZO) + ')' + '                                                       & ' + str(zoSAvg) + '                        & ' + str(zoSMed) + '                           & ' + str(zoSSD) + '                               \\\\ \hline' + "\n")
    o.write('2-5 Years Experience (' + str(nTF) + ')' + '                                                       & ' + str(tfSAvg) + '                        & ' + str(tfSMed) + '                           & ' + str(tfSSD) + '                               \\\\ \hline' + "\n")
    o.write('5-10 Years Experience (' + str(nFT) + ')' + '                                                      & ' + str(ftSAvg) + '                        & ' + str(ftSMed) + '                           & ' + str(ftSSD) + '                               \\\\ \hline' + "\n")
    o.write('10+ Years Experience(' + str(nT) + ')' + '                                                       & ' + str(tSAvg) + '                        & ' + str(tSMed) + '                           & ' + str(tSSD) + '                               \\\\ \hline' + "\n")
    o.write("\end{tabular}" + "\n")
    o.write("\end{table}" + "\n")
    o.close()

   # LATEX File Section: EHRVis
    o = open("ehrvis_summary_table_20.tex", 'w')
    o.write('% Please add the following required packages to your document preamble:' + "\n")
    o.write('\usepackage[table,xcdraw]{xcolor}' + "\n")
    o.write(str('\\') + "begin{table}[h]" + "\n")
    o.write(str('\\') + "begin{tabular}{|l|l|l|l|}" + "\n")
    o.write(str('\\') + 'hline' + "\n")
    o.write(str('\\') + 'rowcolor[HTML]{191870}' + "\n") 
    o.write(str('\\') + 'multicolumn{1}{|c|}{\cellcolor[HTML]{191870}{\color[HTML]{FFFFFF} {\\bf Group}}} & {\color[HTML]{FFFFFF}{\\bf Mean}} & {\color[HTML]{FFFFFF} {\\bf Median}} & {\color[HTML]{FFFFFF} {\\bf Std. Dev.}} \\\\ \hline' + "\n")
    o.write('All Participants                                                           & ' + str(oEAvg) + '                       & ' + str(oEMed) + '                          & ' + str(oESD) + '                              \\\\ \hline' + "\n")
    o.write('Medical Students (' + str(nStudents) + ')' + '                                                            & '+ str(mEAvg) + '                       & ' + str(mEMed) + '                          & ' + str(mESD) + '                              \\\\ \hline' + "\n")
    o.write('Physicians (' + str(nDoctors) + ')' + '                                                                 & ' + str(pEAvg) + '                       & ' + str(pEMed) + '                          & ' + str(pESD) + '                              \\\\ \hline' + "\n")
    o.write('0-1 Years Experience (' + str(nZO) + ')' + '                                                       & ' + str(zoEAvg) + '                        & ' + str(zoEMed) + '                           & ' + str(zoESD) + '                               \\\\ \hline' + "\n")
    o.write('2-5 Years Experience (' + str(nTF) + ')' + '                                                       & ' + str(tfEAvg) + '                        & ' + str(tfEMed) + '                           & ' + str(tfESD) + '                               \\\\ \hline' + "\n")
    o.write('5-10 Years Experience (' + str(nFT) + ')' + '                                                      & ' + str(ftEAvg) + '                        & ' + str(ftEMed) + '                           & ' + str(ftESD) + '                               \\\\ \hline' + "\n")
    o.write('10+ Years Experience (' + str(nT) + ')' + '                                                       & ' + str(tEAvg) + '                        & ' + str(tEMed) + '                           & ' + str(tESD) + '                               \\\\ \hline' + "\n")
    o.write("\end{tabular}" + "\n")
    o.write("\end{table}" + "\n")
    o.close()



 
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
    avgSU = round(np.mean(indivScores), 2) 
    medSU = round(np.median(indivScores), 2)
    sd = round(np.std(indivScores), 2)
    #print medSU
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
    eavgSU, medSU, sd, ehrvis = calcSUscore(ehrvisSUS)
    print "Standard: " + str(avgSU) + " EHRVis: " + str(eavgSU)

    plt.figure()
    plt.hist([standard, ehrvis], bins = 6, histtype='barstacked', color = ["steelblue", "lightskyblue"])
    plt.ylim([0,16]) # Raise y range to make plot look cleaner
    plt.legend(["Standard EHR System", "EHRVis Interface"])
    plt.title("Distribution of Standard Usability Scores Across All Participants")
    plt.xlabel('Standard Usability Score', fontsize=13)
    plt.ylabel('Number of scores', fontsize=13)
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
    Q1 = responses[0]
    Q2 = responses[1]
    Q3 = responses[2]
    Q4 = responses[3]
    Q5 = responses[4]

    fig = plt.figure(figsize=(10,5))

    ax1 = plt.subplot2grid((2, 3), (0, 0))
    ax2 = plt.subplot2grid((2, 3), (0, 1))
    ax3 = plt.subplot2grid((2, 3), (0, 2))#, colspan=1, rowspan=1)
    ax4 = plt.subplot2grid((2, 3), (1, 0))#, rowspan=1)
    ax5 = plt.subplot2grid((2, 3), (1, 1), rowspan=1)

    plt.tight_layout(pad=0.5, w_pad=2, h_pad=4.0)
    x = np.arange(4)
    width = 0.35

    # Question 1 plot
    ax1.bar(x, Q1, width, align='center', color = "navy")
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'], fontsize=11)
    ax1.set_ylabel('Responses')
    ax1.set_title("Did EHRVis Notes help you see patterns of \n patient interaction with medical system? \n", fontsize=11)
    ax1.set_ylim([0, 14])

    # Question 2 plot
    ax2.bar(x, Q2, width, align='center', color = "navy")
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'], fontsize=11)
    ax2.set_title("Did EHRVis help you see changes to the \n patient's medications more easily?", fontsize=11)
    ax2.set_ylim([0, 14])
  
    # Question 3 plot
    ax3.bar(x, Q3, width, align='center', color = "navy")
    ax3.set_xticks(x)
    ax3.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'], fontsize=11)
    ax3.set_title("Was EHRVis helpful for visualizing \n trends in the patient case?", fontsize=11)
    ax3.set_ylim([0, 14])

    # Question 4 plot
    ax4.bar(x, Q4, width, align='center', color = "navy")
    ax4.set_xticks(x)
    ax4.set_ylabel('Responses')
    ax4.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'], fontsize=11)
    ax4.set_title("Would EHRVis help you make \n clinical decisions faster?", fontsize=11)
    ax4.set_ylim([0, 14])

    # Question 5 plot
    ax5.bar(x, Q5, width, align='center', color = "navy")
    ax5.set_xticks(x)
    ax5.set_xticklabels(['Yes', 'Somewhat', 'Unsure', 'No'], fontsize=11)
    ax5.set_title("Would EHRVis help you make \n clinical decisions more easily?", fontsize=11)
    ax5.set_ylim([0, 14])

    plt.subplots_adjust(top=0.85, left=0.05)
    plt.show()

main()
