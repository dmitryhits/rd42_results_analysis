import csv, re, ROOT

OldRunKeys = ["RunNumber","Diamond","Descr","Comments","Voltage","Current start", "Current end", "Repeater card",
              "Noise","Mean PH clustered", "SNR", 
              "Mean PH 2 channels transparent", "SNR 2channels transparent", 
              "Mean PH 4 channels transparent", "SNR 4 channels transparent",	
              "Resolution 2 out 10", "Resolution 2 out 10 in microns",
              "Mean PH 2 out 10 transparent", "SNR 2 out 10 transparent",	
              "Masked channels",
          ]

########## Results copied directly from Webpage http://kinder.ethz.ch/output/new//results.html ##############################
#RunNo	cor	Descr.	Diamond	Voltage	rep. card	cur. begin	cur. end
# noise	noise CMC	CMN	feed through SIL	feed through DIA
# Mean clustered	Mean {2/10} trans	Mean {4/4} trans	Mean {2/2} trans
#conv.	Results table	SVN REV
NewRunKeys = ["RunNumber","Corrected","Descr","Diamond", "Voltage", "Repeater card","Current start", "Current end",
               "Noise", "Noise CMC","CMN", "Feed through SIL","Feed through DIA",
               "Mean PH clustered","Mean PH 2 out 10 transparent","Mean PH 4 channels transparent", "Mean 2 channels transparent",
               "PH conversion", "Results link","SVN Rev"]
################# Results collected in http://kinder.ethz.ch/output/new//results.csv ###########################################
# RunNo;dia;corrected;voltage;repeaterCard;current_begin;current_end;irradiation;#RunNo;descr.;
# Noise;CMCnoi;CMN;CorSil;sigSil;CorDia;
#m_clus;mp_clus;w_clus;gs_clus; clustered
#m2/10;mp2/10;w2/10;sig2/10;m2/2;m4/4; transparent allignemnt
#m2/10;mp2/10;w2/10;sig2/10;m2/2;m4/4; Transperent with transparent allignment
# Res_DG1n;Res_DG2n;Res_SGSn;Res_SGNn;Res_SGFn;
#Res_DG1t;Res_DG2t;Res_SGSt;Res_SGNt;Res_SGFt;REV;REV

NewRunKeys_Extended = ["RunNumber","Diamond","Corrected", "Voltage", "Repeater card","Current start", "Current end","irradiation","RunNumber_x","Descr",
                      "Noise", "Noise CMC","CMN", "Feed through SIL","sigma feed through Sil","Feed through DIA",
                      "Mean PH clustered","Most Probable PH clustered","width clustered","gs_clustered",
                      "Mean PH 2 out 10 transparent","Most Probable 2 out 10 transparent","width 2 out 10 transparent","sigma 2 out 10 transparent",
                      "Mean 2 channels transparent","Mean PH 4 channels transparent",
                      "Mean PH 2 out 10 transparent allign","Most Probable 2 out 10 transparent allign","width 2 out 10 transparent allign","sigma 2 out 10 transparent allign",
                      "Mean 2 channels transparent allign","Mean PH 4 channels transparent allign",
                      "Res_DG1n", "Res_DG2n", "Res_SGSn", "Res_SGNn", "Res_SGFn",
                      "Res_DG1t","Res_DG2t", "Res_SGSt", "Res_SGNt", "Res_SGFt",
                      "REV","REV"]


DifferenceKeys = ["RunNumber","Diamond","Voltage",
                  "Mean PH 2 out 10 transparent old","Mean PH 2 out 10 transparent new","Diff PH new-old transparent",
                  "Mean PH clustered old","Mean PH clustered new", "Diff PH new-old clustered",
                  "Diff PH new transparent-clustered","Diff PH old transparent-clustered",                  
                  "Diff diff new-old",]
Old_Analysis =[]
New_Analysis =[]
New_Analysis_Extended =[]
Analysis_Differences = []

#read csv files for old and new resutls
results_old = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/Old_analysis_results_editted.csv", "rU"))
results_new = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/new_results.csv", "rU"),delimiter = ',')
results_new_extended = csv.reader(open("/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/new_results_extended_latest.csv", "rU"),delimiter = ';')

######################################################################################################
#Create another list of dictionaries for the new results
for row in results_new:
    #print "NEW" + str(row)
    run_dict_new = dict(zip(NewRunKeys,row))
    New_Analysis.append(run_dict_new)

######################################################################################################
#Create another list of dictionaries for the extended new results
counter_extended = 0
for row in results_new_extended:
    run_dict_new_extended = dict(zip(NewRunKeys_Extended,row))
    New_Analysis_Extended.append(run_dict_new_extended)
    #if counter_extended < 1000:
        #print "Extended : " + str(row)
        #print run_dict_new_extended["Mean PH 2 out 10 transparent"]
    counter_extended+=1
#####################################################################################
#Create a list of dictionaries for the old results
oldrownum = 0
diamond = "wrong diamond"
for row in results_old:
    #if oldrownum <140 and oldrownum>100:
        #print "original"
        #print row
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
        #if oldrownum <140 and oldrownum>100:
            #print "modified"
            #print row_modified

        run_dict_old = dict(zip(OldRunKeys,row_modified))
        Old_Analysis.append(run_dict_old)
    oldrownum+=1
#######################################################################################
#################### Histograms ###########################################################
mean_trans_diff=ROOT.TH1F("mean_trans_diff","Difference of the Mean Transparent (new-old)/old;ratio;#runs",400,-0.5,0.5)
mean_trans_diff=ROOT.TH1F("mean_trans_diff","Difference of the Mean Transparent (new-old)/old;ratio;#runs",400,-0.5,0.5)
mean_trans_diff=ROOT.TH1F("mean_trans_diff","Difference of the Mean Transparent (new-old)/old;ratio;#runs",400,-0.5,0.5)
mean_clust_diff=ROOT.TH1F("mean_clust_diff","Difference of the Mean Clustered  (new-old)/old;ratio;#runs",400,-0.5,0.5)
noise_diff=ROOT.TH1F("noise_diff","Difference of the Noise (new-old)/old;ratio;#runs",400,-0.5,0.5)
resolution_old=ROOT.TH1F("resolution_old","Resoltuion Old;ratio;#runs",400,0,50)

list_of_diff_runs = []
list_of_checked_runs = []
ofile  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference.csv', "wb")
ofile_dict  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference_dict.csv', "wb")
ofile_felix  = open('/Users/hits/Documents/Diamonds/RD42_SPS_TestBeamAnalysis/difference_felix.csv', "wb")

diffwriter = csv.writer(ofile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
diffwriter_dict = csv.DictWriter(ofile_dict, DifferenceKeys, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
diffwriter_dict.writeheader()
print Old_Analysis[1]
for old_entry in Old_Analysis:
    #if old_entry["RunNumber"] == "11000":
        #print old_entry
#    for new_entry in New_Analysis:
    for new_entry in New_Analysis_Extended:
        #if old_entry["RunNumber"] == "11000" and new_entry["RunNumber"]=="11000":
            #print new_entry
        if (old_entry["RunNumber"] == new_entry["RunNumber"]  and old_entry["Diamond"] == new_entry["Diamond"] 
            and list_of_checked_runs.count([new_entry["RunNumber"],new_entry["Diamond"]])==0 
            and int(new_entry["Corrected"]) == 1):
            list_of_checked_runs.append([new_entry["RunNumber"],new_entry["Diamond"]])
            #print old_entry
            #print  "OLD " + old_entry["RunNumber"] + " " + old_entry["Diamond"] + " = " + new_entry["RunNumber"] + " NEW"
            if old_entry["Mean PH 2 out 10 transparent"] == "??" or float(new_entry["Mean PH 2 out 10 transparent"])<=0 or float(old_entry["Mean PH 2 out 10 transparent"])<=0:
                print old_entry["RunNumber"]
            else:
                ################################## Fill Histograms ############################################################
                mean_trans_diff.Fill((float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"]))/float(old_entry["Mean PH 2 out 10 transparent"]))
                
                if abs((float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"]))/float(old_entry["Mean PH 2 out 10 transparent"]))>0.1:
                    ## print out runs with large pulse height differnece
                    print new_entry["Diamond"] + " : " + new_entry["RunNumber"] + " : Pulse Height new:old= " + new_entry["Mean PH 2 out 10 transparent"] +" : " + old_entry["Mean PH 2 out 10 transparent"] + " : bad runs" 
                mean_clust_diff.Fill((float(new_entry["Mean PH clustered"])-float(old_entry["Mean PH clustered"]))/float(old_entry["Mean PH clustered"]))
                noise_diff.Fill((float(new_entry["Noise"])-float(old_entry["Noise"]))/float(old_entry["Noise"]))
                resolution_old.Fill(float(old_entry["Resolution 2 out 10 in microns"]))
                ###################################### difference dictionary ######################################################
                diff_dict={"RunNumber":old_entry["RunNumber"],
                           "Diamond":old_entry["Diamond"],
                           "Voltage":old_entry["Voltage"],
                           "Mean PH 2 out 10 transparent old":old_entry["Mean PH 2 out 10 transparent"],
                           "Mean PH 2 out 10 transparent new":new_entry["Mean PH 2 out 10 transparent"],
                           "Diff PH new-old transparent":'{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH 2 out 10 transparent"])),
                           "Mean PH clustered old":old_entry["Mean PH clustered"],
                           "Mean PH clustered new":new_entry["Mean PH clustered"],
                           "Diff PH new-old clustered":'{:+.2f}'.format(float(new_entry["Mean PH clustered"])-float(old_entry["Mean PH clustered"])),
                           "Diff PH new transparent-clustered":'{:+.2f}'.format(float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH clustered"])),
                           "Diff PH old transparent-clustered":'{:+.2f}'.format(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH clustered"])),                  
                           "Diff diff new-old":'{:+.2f}'.format((float(new_entry["Mean PH 2 out 10 transparent"])-float(new_entry["Mean PH clustered"]))-(float(old_entry["Mean PH 2 out 10 transparent"])-float(old_entry["Mean PH clustered"]))),                  
                       }
                       
                       
            #print diff_dict
            diffwriter_dict.writerow(diff_dict)
            list_of_diff_runs.append(diff_dict)
############## Plot stuff ######################################################
c2 = ROOT.TCanvas("c2","window",1200,800)
c2.Divide(2,2)
c2.cd(1)
mean_trans_diff.Draw()
c2.cd(2)
mean_clust_diff.Draw()
c2.cd(3)
noise_diff.Draw()
c2.cd(4)
resolution_old.Draw()

#        if new_entry["RunNumber"] == "15005" and old_entry["RunNumber"] == "15005":
#            print   "OLD " + old_entry["RunNumber"] + " = " + new_entry["RunNumber"] + " NEW"
#            print  "OLD " + old_entry["Diamond"] + " = " + new_entry["Diamond"] + " NEW"
#            print  "Corrected " + new_entry["Corrected"] + " = " + new_entry["SVN Rev"] + " NEW"
#            print "SNV Rev" + new_entry["SVN Rev"].rstrip("M")
#        if (old_entry["RunNumber"] == new_entry["RunNumber"]  and old_entry["Diamond"] == new_entry["Diamond"] 
#            and list_of_checked_runs.count([new_entry["RunNumber"],new_entry["Diamond"]])==0 
#            and int(new_entry["Corrected"]) == 1 and int(new_entry["SVN Rev"].rstrip("M"))>= 987):
#            list_of_checked_runs.append([new_entry["RunNumber"],new_entry["Diamond"]])
