def oldcsv_to_dict():
    import csv, re
    """ Parse the csv file created by coping old analysis results from website
    https://duck42.ethz.ch/trac42/wiki/TestBeamResults
    and Return a dictionary of "Old' Results """

    OldRunKeys = ["RunNumber","Diamond","Descr","Comments","Voltage","Current start", "Current end", "Repeater card",
                  "Noise","Mean PH clustered", "SNR", 
                  "Mean PH 2 channels transparent", "SNR 2channels transparent", 
                  "Mean PH 4 channels transparent", "SNR 4 channels transparent",	
                  "Resolution 2 out 10", "Resolution 2 out 10 in microns",
                  "Mean PH 2 out 10 transparent", "SNR 2 out 10 transparent",	
                  "Masked channels",
              ]
    Old_Analysis = []

    #read csv files for old and new resutls
    results_old = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/Old_analysis_results_editted.csv", "rU"))

    #####################################################################################
    #Create a list of dictionaries for the old results
    oldrownum = 0
    diamond = "wrong diamond"
    for row in results_old:
        #if oldrownum <140 and oldrownum>100:
        #    print "original"
        #    print row
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
                if entry != "plot" and  entry!="plots" and n_entry>0:
#                    print "in the loop"
                    #If found star characters, write only part of the entry before the first star (*) character and strip white spaces if any 
                    if entry.count("*")>0:
                        row_modified.append(entry[:entry.find("*")].strip())
                    else:
                        row_modified.append(entry.strip())
                n_entry+=1
            if oldrownum <140 and oldrownum>100:
                print "modified"
                print row_modified
                                                
            run_dict_old = dict(zip(OldRunKeys,row_modified))
            Old_Analysis.append(run_dict_old)
        oldrownum+=1
    return Old_Analysis

#######################################################################################
