""" for a give masked file with format 'pixd col row' 
it finds the maximum and minimum unmasked rows and columns, 
counts the number of unasked pixels and calculates the unmasked area """

cols_rows = []
unmasked = []

#path = input("path to the mask file please!")
f = open("/Users/hits/module.ini_2A87E","r")
#f = open("/Users/hits/module.ini","r")
#f = open("/Users/hits/module.ini_plt_s129","r")
#f = open("/Users/hits/module.ini_plt_s30","r")
#f = open("/Users/hits/module.ini_plt_s97","r")
for line in f:
    line_data = line.split(" ")
    l = [int(line_data[1]), int(line_data[2])]
    cols_rows.append(l)
n_unmasked = 0
mincol = 100
maxcol = -1
minrow = 100
maxrow = -1
for col in range(0,52):
    for row in range(0,80):
        if [col,row] not in cols_rows:
            unmasked.append([col,row])
            #print [col,row]
            n_unmasked+=1
            if col < mincol:
                mincol = col
            if col > maxcol:
                maxcol = col
            if row < minrow:
                minrow = row
            if row > maxrow:
                maxrow = row
print "max unmasked row  "  + str(maxrow)     
print "min unmasked row  "  + str(minrow)     
print "max unmasked col  "  + str(maxcol)     
print "min unmasked col  "  + str(mincol)     
print "number of unmasked pixels  " + str(n_unmasked)
print "total unmasked area in square cm " + str(n_unmasked*0.00015)
