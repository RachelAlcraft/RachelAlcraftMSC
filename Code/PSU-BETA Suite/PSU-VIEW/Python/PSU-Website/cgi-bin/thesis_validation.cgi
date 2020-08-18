#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      17/06/2020
Function:  A CGI file to take text and access the database
Description: 
============
Consolidated CGI page with state for optimization of image views
"""

#************************************************************************************************
import cgi;
import pandas as pd
import thesis_strings as hs
import thesis_strings_validation as val
import class_sqlData2 as state
import thesis_images as image
import time
from datetime import datetime
import class_logger as log

start = time.time()
timestring = ''
timestring += "Start:" + datetime.now().strftime("%H:%M:%S")
# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser


# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")


weblog = log.logger(False) # choose whether to print debug messages
weblog.log("Hello, I am in debug mode")

# Define the defaults
# Common settings
pdb_code = ''
set_name = 'HIGH'
maxb= '100'
restriction=""
occ = "A"
contact = ''

# Distribution A
res_choice = "1.10"
res_choiceL = "ALL"
rv_choice = "ALL"
rv_choiceL = "ALL"
rf_choice = "0.3"
rf_choiceL = "ALL"

gradient = 'amino_code'
in_set = ''
checked_set = ''

# ss
H=0
B=0
E=0
G=0
I=0
T=0
S=0
U=0
X=0


# Now get chosen the values out of the form
form = cgi.FieldStorage()
if form.getvalue('pdb_code'):
   pdb_code = form.getvalue('pdb_code')
if form.getvalue('set_name'):
   set_name = form.getvalue('set_name')
if form.getvalue('maxb'):
   maxb = form.getvalue('maxb')
if form.getvalue('restriction'):
   restriction = form.getvalue('restriction')
if form.getvalue('occ'):
   occ = form.getvalue('occ')
if form.getvalue('contact'):
   contact = form.getvalue('contact')
if form.getvalue('res_choice'):
   res_choice = form.getvalue('res_choice')
if form.getvalue('rv_choice'):
   rv_choice = form.getvalue('rv_choice')
if form.getvalue('rf_choice'):
   rf_choice = form.getvalue('rf_choice')
if form.getvalue('res_choiceL'):
   res_choiceL = form.getvalue('res_choiceL')
if form.getvalue('rv_choiceL'):
   rv_choiceL = form.getvalue('rv_choiceL')
if form.getvalue('rf_choiceL'):
   rf_choiceL = form.getvalue('rf_choiceL')
if form.getvalue('gradient'):
   gradient = form.getvalue('gradient')
   weblog.log(gradient)
if form.getvalue('in_set'):
   in_set = form.getvalue('in_set')
if form.getvalue('checked_set'):
   checked_set = form.getvalue('checked_set')

# SECONDARY STRUCTURE
if form.getvalue('H'):
   H=form.getvalue('H')
if form.getvalue('B'):
   B=form.getvalue('B')
if form.getvalue('E'):
   E=form.getvalue('E')
if form.getvalue('G'):
   G=form.getvalue('G')
if form.getvalue('I'):
   I=form.getvalue('I')
if form.getvalue('T'):
   T=form.getvalue('T')
if form.getvalue('S'):
   S=form.getvalue('S')
if form.getvalue('U'):
   U=form.getvalue('U')
if form.getvalue('X'):
   X=form.getvalue('X')

#gradient = 'ss_psu'
#gradient = 'refinement'
chosen_sets = '('
if in_set == '1':
   chosen_sets += "'IN'"
if checked_set == '1':
   if chosen_sets == "('IN'":
      chosen_sets += ','
   chosen_sets += "'CHECKED'"
chosen_sets += ')'

chosen_ss = '('
if H == '1':
   chosen_ss += "'H',"
if B == '1':
   chosen_ss += "'B',"
if E == '1':
   chosen_ss += "'E',"
if G == '1':
   chosen_ss += "'G',"
if I == '1':
   chosen_ss += "'I',"
if T == '1':
   chosen_ss += "'T',"
if S == '1':
   chosen_ss += "'S',"
if U == '1':
   chosen_ss += "'U',"
if X == '1':
   chosen_ss += "'-',"
chosen_ss += "'z')" # THERE IS NO Z IT JUST ENSURES A VALID SELECTION


# This returns the header for the general website
html_dir = '/../../~ab002/'
html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')
# This returns back the search boxes with the information filled in as sent
html += val.middleValidationDefaults(pdb_code, set_name,
                                res_choice,res_choiceL,rv_choice,rv_choiceL, rf_choice, rf_choiceL,
                                maxb, occ, contact, restriction,gradient,in_set, checked_set,
                                 H,B,E,G,I,T,S,U,X)

# Specify all the reports we want to run
reports = []

reports.append(['PHI','PSI','NON'])
reports.append(['N-CA','CA-C','NON'])
reports.append(['CHI1','CHI2','NON'])
reports.append(['CHI3','CHI4','NON'])

reports.append(['PSI','N-O','NON'])
reports.append(['PSI','CB-O','NON'])
reports.append(['N-O','CB-O','NON'])
reports.append(['PSI','N-CA-C-O','NON'])

reports.append(['PHI','C1N-C','NON'])
reports.append(['PHI','C1N-CB','NON'])
reports.append(['OMEGA','TAU','NON'])
reports.append(['CHI2','CHI3','HIS'])


reports.append(['CHI1','CA-CB-CG','PRO'])
reports.append(['CA-CA1C','CA1N-CA','NON'])
reports.append(['CA2N-CA1N-CA','CA-CA1C-CA2C','NON'])
reports.append(['TAU1N','TAU1C','NON'])


#reports.append(['OMEGA','N-NPP','NON'])
#reports.append(['CHI1','CB-CA-C','NON'])

# Now create the sql strings for each distribution
allsqls = {}



ch = state.sqlChoices()
df_creator = state.sqlData()


for r in reports:

    xcalc = r[0]
    ycalc = r[1]
    aacalc = r[2]
    category = xcalc + ":" + ycalc + ":" + aacalc
    ch.addGeneralChoices(xcalc,ycalc,"",maxb,restriction,gradient)
    ch.addDistribution(set_name,chosen_sets,chosen_ss,aacalc,occ,contact,[res_choice,res_choiceL],[rv_choice,rv_choiceL],[rf_choice,rf_choiceL])
    ch.addPdbCode(pdb_code)
    sqls = ch.getSqlStrings()
    allsqls[category] = sqls
weblog.log(allsqls)

for category in allsqls:
   for aa in allsqls[category]:
       sql = allsqls[category][aa]
       weblog.log("Adding sql for " + category + ": " + sql)
       vals = category.split(':')
       df_creator.add(sql,aa,ch,vals[1],vals[0],category,aa)



# Create the dataframes from sql
timestring += " - Create sql:" + datetime.now().strftime("%H:%M:%S")
dfs = df_creator.createDataFrames()

# Now create the images
timestring += " - Create images:" + datetime.now().strftime("%H:%M:%S")
html += val.middleReturnValidation(dfs,reports,gradient)

###now return the data to the webpage
##timestring += " - Show data:" + datetime.now().strftime("%H:%M:%S")
##for df in dfs:
##   html += hs.dataFrameToCSV(df)





end = time.time()
timestring += " - End:" + datetime.now().strftime("%H:%M:%S")

time_diff = end-start



html += timestring
html += "<br/>Total time taken = " + str(int(time_diff/60)) + "m " + str(int(time_diff%60)) + "s" 

   
html += hs.footer()
print(html)

#************************************************************************************************
