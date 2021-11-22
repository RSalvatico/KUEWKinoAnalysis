import sys
import csv
import copy

arr = []
l_mass_points = []
replace_index = 6
replace_char = '-'
row = []
bad_matching = False
mass_point_counter1 = 0
mass_point_counter2 = 0

#with open("/home/t3-ku/rsalvatico/KU_SUSY_latest/CMSSW_10_6_5/src/KUEWKinoAnalysis/BF_bkg_Signals_yearSeparated/AsymptoticLimits/" + str(sys.argv[1]) + "/limits.json","r") as f1, open("../BF_bkg_Signals/AsymptoticLimits/" + str(sys.argv[1]) + "/limits.json","r") as f2:

with open("/home/t3-ku/rsalvatico/KU_SUSY_ultimate/CMSSW_10_6_5/src/KUEWKinoAnalysis/BF_bkg_TSlepSlep_yearSeparated/AsymptoticLimits/" + str(sys.argv[1]) + "/limits.json","r") as f1, open("../BF_bkg_TSlepSlep_noMerge/AsymptoticLimits/" + str(sys.argv[1]) + "_tot/limits.json","r") as f2:

#with open("../BF_t6/AsymptoticLimits/" + str(sys.argv[1]) + "/limits.json","r") as f1, open("../BF_bkg_TSlepSlep_yearSeparated_3bins/AsymptoticLimits/" + str(sys.argv[1]) + "/limits.json","r") as f2:

    for line1, line2 in zip(f1,f2): #Iterate over the lines of both files
        #print line1
        if line1.startswith('  "'): #Targeting the mass point
            if len(line1) == 17:
                line1 = line1[:replace_index] + replace_char + line1[replace_index + 1:] #Replace the 0 separating the masses with a -
            elif len(line1) == 18 and line1[7]== "0": #For mass points with parent mass >= 1000 GeV
                line1 = line1[:replace_index + 1] + replace_char + line1[replace_index + 2:] #Replace the 0 separating the masses with a -
            elif len(line1) == 18 and not line1[7]== "0": #For mass points with both parent mass and LSP >= 1000 GeV
                line1 = line1[:replace_index + 1] + replace_char + line1[replace_index + 1:] #Add a - to separate masses
            line1 = line1.replace('  "','',1) #Remove the first occurrance of ", i.e. the beginning of the mass point line
            line1 = line1.replace('.0": {','') #Remove the ending part of the mass point line
            line1 = line1.strip() #Remove \n from the end of each entry
            mass_point_counter1 += 1

        if line2.startswith('  "'): #Targeting the mass point
            if len(line2) == 17:
                line2 = line2[:replace_index] + replace_char + line2[replace_index + 1:] #Replace the 0 separating the masses with a -
            elif len(line2) == 18 and line2[7] == "0": #For mass points with parent mass >= 1000 GeV
                line2 = line2[:replace_index + 1] + replace_char + line2[replace_index + 2:] #Replace the 0 separating the masses with a -
            elif len(line2) == 18 and not line2[7]== "0": #For mass points with both parent mass and LSP >= 1000 GeV
                line2 = line2[:replace_index + 1] + replace_char + line2[replace_index + 1:] #Add a - to separate masses
            line2 = line2.replace('  "','',1) #Remove the first occurrance of ", i.e. the beginning of the mass point line
            line2 = line2.replace('.0": {','') #Remove the ending part of the mass point line
            line2 = line2.strip() #Remove \n from the end of each entry
            mass_point_counter2 += 1
            if not line1 == line2:
                bad_matching = True
                print "line1: ", line1, "  line2: ", line2
            else:
                l_mass_points.append(line1)
                bad_matching = False

        if line1.startswith('    "exp0"') and not bad_matching: #Targeting the expected UL in the first file
            line1 = line1.replace('    "exp0": ','')
            line1 = line1.replace(',','')
            l_mass_points.append(float(line1))

        if line2.startswith('    "exp0"') and not bad_matching: #Targeting the expected UL in the second file
            line2 = line2.replace('    "exp0": ','')
            line2 = line2.replace(',','')
            l_mass_points.append(float(line2))
            l_mass_points.append(float(line2)/float(line1))
            if float(line2) < float(line1):
                l_mass_points.append('******')
            else:
                l_mass_points.append('')
                
#print l_mass_points

index = 0
for element in l_mass_points:
    if index >= 5:
        del row[:]
        index = 0
    if index < 5: #Make rows of 4 elements
        row.append(element)
        #print element
    if index == 4:
        arr.append(copy.deepcopy(row)) #Avoid overriding the same elements from the row list
    index += 1 

#print arr

with open('limits_comparison/2016_2017_Sig_VS_2016_2017_2018_Sig_noMerge_' + str(sys.argv[1]) + '_lumi.csv','w',) as fOut:
    writer = csv.writer(fOut)
    writer.writerow(["m splitting","Nominal","Modified","Ratio(M/N)"])
    writer.writerows(arr)

print
print "MASS POINTS REPORT"
print "##################"
print "The first json contains " + str(mass_point_counter1) + " mass points"
print
print "The second json contains " + str(mass_point_counter2) + " mass points"
print
            
