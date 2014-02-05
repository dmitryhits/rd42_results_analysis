import csv, re

OldRunKeys = ["RunNumber",
              "Diamond",
              "Descr",
              "Comments",    
              "Voltage",
              "Current start",	
              "Current end",	
              "Repeater card",
              "Noise",
              "Mean PH 2 out 10 clustered",	
              "SNR",	
              "Mean PH 2 channels transparent",
              "SNR 2channels transparent",
              "Mean PH 4 channels transparent",	
              "SNR 4 channels transparent",	
              "Resolution 2 out 10",
              "Resolution 2 out 10 in microns",
              "Mean PH 2 out 10 transparent",
              "SNR 2 out 10 transparent",	
              "Masked channels",
          ]

NewRunKeys2 = ["RunNumber",	
               "Corrected",
               "Descr",
               "Diamond",
               "Voltage",	
               "Repeater card",
               "Noise",	
               "Noise CMC",
               "CMN",
               "Feed through SIL",
               "Feed through DIA",
               "Mean PH 2 out 10 clustered",
               "Mean PH 2 out 10 transparent",
               "Mean PH 4 channels transparent",
               "Mean 2 channels transparent",
               "Results link",
               "SVN Rev"]

NewRunKeys = ["RunNumber", 
              "Diamond",
              "Corrected",
              "Voltage",
              "N_tries",
              "Descr",
              "Noise",
              "Noise CMC",
              "CMN",
              "Feed through SIL",
              "Feed through spread SIL",
              "Feed through DIA",
              "Mean PH 2 out 10 transparent",
              "MP PH 2 out 10 transparent",
              "Width PH 2 out 10 transparent",
              "Sigma PH 2 out 10 transparent",
              "Mean PH 2 channels transparent",
              "Mean PH 4 channels transparent",
              "Mean PH 2 out 10 transparent alligned",
              "MP PH 2 out 10 transparent alligned",
              "Width PH 2 out 10_transparent alligned",
              "Sigma PH 2 out 10_transparent alligned",
              "Mean PH 2 channels transparent alligned",
              "Mean PH 4 channels transparent alligned",
              "res1 transparent",
              "res2 transparent",
              "res3 transparent",
              "res4 transparent",
              "res5 transparent",
              "res1 transparent alligned",
              "res2 transparent alligned",
              "res3 transparent alligned",
              "res4 transparent alligned",
              "res5 transparent alligned",
              "REV"	
       ]

DifferenceKeys = ["RunNumber",
                  "Mean PH 2 out 10 transparent old",
                  "Mean PH 2 out 10 transparent new",
                  "Diff PH new-old transparent",
                  "Mean PH 2 out 10 clustered old",
                  "Mean PH 2 out 10 clustered new",
                  "Diff PH new-old clustered",
                  "Diff PH new transparent-clustered",
                  "Diff PH old transparent-clustered",                  
                  "Diff diff new-old",                  
              ]
Old_Analysis =[]
New_Analysis =[]
New_Analysis2 =[]
Analysis_Differences = []

#read csv files for old and new resutls
results_old = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/Old_analysis_results.csv", "rU"))
results_new = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/New_analysis_results.csv", "rU"),delimiter = ';')
results_new2 = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/New_analysis_results2.csv", "rU"),delimiter = ',')
######################################################################################################
#Create a list of dictionaries for the new results
for row in results_new:
    #print row
    run_dict_new = dict(zip(NewRunKeys,row))
    New_Analysis.append(run_dict_new)

#####################################################################################
#Create another list of dictionaries for the new results
for row2 in results_new2:
    #print "OLD" + str(row2)
    run_dict_new2 = dict(zip(NewRunKeys2,row2))
    New_Analysis2.append(run_dict_new2)

#####################################################################################
#Create a list of dictionaries for the old results
oldrownum = 0
diamond = "wrong diamond"
for row in results_old:
    if oldrownum <140 and oldrownum>130:
        print "original"
        print row
    row_modified = []
# Check whether it is a diamond row, the lines following this row will be for the same diamond
    if not re.match(r"[0-9][0-9][0-9][0-9][0-9]",row[0]) and not re.match("sample",row[0]):
        diamond = row[0]
#Check if it is a regular run row
    if re.match(r"[0-9][0-9][0-9][0-9][0-9]",row[0]):
        # Now add other entries removing "plot" entries
        n_entry =0
        for entry in row:
            if n_entry == 0:
                #1st add the run number. First 5 characters are the run number
                row_modified.append(entry[:5]) 
                # 2nd add diamond to the list 
                row_modified.append(diamond)
                # 3rd add description "left", "right"
                descr =""
                if entry.find("left")>=0: 
                    descr = "left"
                if entry.find("right")>=0: 
                    descr = "right"
                row_modified.append(descr)
                # 3rd add a comment
                comment = ""
                if descr != "": 
                    pos = entry.find(descr)+len(descr)
                    #print pos
                    #print len(entry)
                    #print entry[pos]
                    if len(entry)>pos and entry[pos] == ")":
                        pos = pos+1
                    if pos < len(entry):
                        comment = entry[pos:]
                else:
                    pos = 5
                    if pos < len(entry):
                        comment = entry[pos:]
                row_modified.append(comment)
                # Finally check all other entries and add them "as is" but ignoring "plot" entries
            if entry != "plot" and n_entry>0:
#                    print "in the loop"
                    row_modified.append(entry)
            n_entry+=1
        if oldrownum <140 and oldrownum>130:
            print "modified"
            print row_modified

        run_dict_old = dict(zip(OldRunKeys,row_modified))
        Old_Analysis.append(run_dict_old)
    oldrownum+=1
#######################################################################################
list_of_diff_runs = []
list_of_checked_runs = []
ofile  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference.csv', "wb")
ofile_dict  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference_dict.csv', "wb")
ofile_felix  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference_felix.csv', "wb")

diffwriter = csv.writer(ofile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
diffwriter_dict = csv.DictWriter(ofile_dict, DifferenceKeys, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
dict_felix_keys = ["RunNumber","Current start", "Current end", "Repeater card"]
diffwriter_felix = csv.DictWriter(ofile_felix, dict_felix_keys, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
diffwriter_dict.writeheader()
diffwriter_felix.writeheader()
for felix_entry in Old_Analysis:
    felix_entry_small = dict((k,felix_entry[k]) for k in dict_felix_keys if k in felix_entry)
    diffwriter_felix.writerow(felix_entry_small)
#for new_entry_temp in New_Analysis2:
#    print new_entry_temp

for old_entry in Old_Analysis:
    for new_entry in New_Analysis2:
        if old_entry["RunNumber"] == new_entry["RunNumber"]  and old_entry["Diamond"] == new_entry["Diamond"] and list_of_checked_runs.count([new_entry["RunNumber"],new_entry["Diamond"]])==0 and int(new_entry["Corrected"]) == 1 and new_entry["SVN Rev"]== "987M":
            list_of_checked_runs.append([new_entry["RunNumber"],new_entry["Diamond"]])
            #print old_entry
 #           print  "OLD " + old_entry["RunNumber"] + " = " + new_entry["RunNumber"] + " NEW"  
            diff_dict={"RunNumber":old_entry["RunNumber"],
                       "Mean PH 2 out 10 transparent old":old_entry["Mean PH 2 out 10 transparent"],
                       "Mean PH 2 out 10 transparent new":new_entry["Mean PH 2 out 10 transparent"],
                       "Diff PH new-old transparent":'{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"])),
                       "Mean PH 2 out 10 clustered old":old_entry["Mean PH 2 out 10 clustered"],
                       "Mean PH 2 out 10 clustered new":new_entry["Mean PH 2 out 10 clustered"],
                       "Diff PH new-old clustered":'{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 clustered"])-float(old_entry["Mean PH 2 out 10 clustered"])),
                       "Diff PH new transparent-clustered":'{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH 2 out 10 clustered"])),
                       "Diff PH old transparent-clustered":'{:+.2f}'.format(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"])),                  
                       "Diff diff new-old":'{:+.2f}'.format((float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH 2 out 10 clustered"]))-(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"]))),                  
                   }
#            print [old_entry["RunNumber"],
#                   old_entry["Mean PH 2 out 10 transparent"],
#                   new_entry["Mean PH 2 out 10 transparent"],
#                   '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"])),
#                   old_entry["Mean PH 2 out 10 clustered"],
#                   # new_entry["Mean PH 2 out 10 clustered"],
#                   # '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 clustered"])-float(old_entry["Mean PH 2 out 10 clustered"])),
#                   # '{:+.2f}'.format(new_entry["Mean PH 2 out 10 transparent"]-new_entry["Mean PH 2 out 10 clustered"]),
#                   '{:+.2f}'.format(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"])),                  
#                   # '{:+.2f}'.format((new_entry["Mean PH 2 out 10 transparent"]-new_entry["Mean PH 2 out 10 clustered"])-(old_entry["Mean PH 2 out 10 transparent"]-old_entry["Mean PH 2 out 10 clustered"])))
 #                        ]
            l =  [old_entry["RunNumber"],
                  old_entry["Voltage"],
                   old_entry["Mean PH 2 out 10 transparent"],
                   new_entry["Mean PH 2 out 10 transparent"],
                   '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"])),
                   old_entry["Mean PH 2 out 10 clustered"],
                   # new_entry["Mean PH 2 out 10 clustered"],
                   # '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 clustered"])-float(old_entry["Mean PH 2 out 10 clustered"])),
                   # '{:+.2f}'.format(new_entry["Mean PH 2 out 10 transparent"]-new_entry["Mean PH 2 out 10 clustered"]),
                   '{:+.2f}'.format(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"])),                  
                   # '{:+.2f}'.format((new_entry["Mean PH 2 out 10 transparent"]-new_entry["Mean PH 2 out 10 clustered"])-(old_entry["Mean PH 2 out 10 transparent"]-old_entry["Mean PH 2 out 10 clustered"])))
              ]
            print str(l)
            #diffwriter.writerow(l)
            diffwriter.writerow([old_entry["RunNumber"],
                                 old_entry["Mean PH 2 out 10 transparent"],
                                 new_entry["Mean PH 2 out 10 transparent"],
                                 '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"])),
                                 old_entry["Mean PH 2 out 10 clustered"],
                                 new_entry["Mean PH 2 out 10 clustered"],
                                 '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 clustered"])-float(old_entry["Mean PH 2 out 10 clustered"])),
                                 '{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH 2 out 10 clustered"])),
                                 '{:+.2f}'.format(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"])),                  
                                 '{:+.2f}'.format((float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH 2 out 10 clustered"]))-(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 clustered"])))
                             ])
            #print diff_dict
            diffwriter_dict.writerow(diff_dict)
            list_of_diff_runs.append(diff_dict)

