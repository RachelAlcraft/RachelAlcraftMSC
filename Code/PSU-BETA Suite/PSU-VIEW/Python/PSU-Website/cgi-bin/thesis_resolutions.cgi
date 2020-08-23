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
import thesis_strings_resolutions as res
import class_sqlData2 as state
import thesis_images as image
import name_change as nc
import time
from datetime import datetime
import class_logger as log

start = time.time()
timestring = ''
timestring += "<br/>Start:" + datetime.now().strftime("%H:%M:%S")
# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser


# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")

weblog = log.logger(False) # choose whether to print debug messages
weblog.log("Hello, I am in debug mode")


# Define the defaults
# Common settings
set_name = 'DEFAULT'
calcs = 'N-CA,CA-C'
buckets = '0,1.15,1.3,1.45,1.6,2,2.5,4'
maxb= '50'
rv_choice = "0.16"
rv_choiceL = "ALL"
rf_choice = "0.3"
rf_choiceL = "ALL"
restriction=""
occ = "A"
contact = ''
amino_code = 'NON'
gradient='resolution'
#options
hist = '0'
box = '0'
violin = '0'
line = '0'

# structures
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
if form.getvalue('set_name'):
   set_name = form.getvalue('set_name')
if form.getvalue('calcs'):
   calcs = form.getvalue('calcs')
if form.getvalue('buckets'):
   buckets = form.getvalue('buckets')
if form.getvalue('maxb'):
   maxb = form.getvalue('maxb')
if form.getvalue('restriction'):
   restriction = form.getvalue('restriction')
if form.getvalue('occ'):
   occ = form.getvalue('occ')
if form.getvalue('contact'):
   contact = form.getvalue('contact')
if form.getvalue('maxb'):
   maxb = form.getvalue('maxb')
if form.getvalue('restriction'):
   restriction = form.getvalue('restriction')
if form.getvalue('gradient'):
   gradient = form.getvalue('gradient')
if form.getvalue('amino_code'):
   amino_code = form.getvalue('amino_code')
# report options
if form.getvalue('hist'):
   hist = form.getvalue('hist')
if form.getvalue('box'):
   box = form.getvalue('box')
if form.getvalue('violin'):
   violin = form.getvalue('violin')
if form.getvalue('line'):
   line = form.getvalue('line')
# structure status
if form.getvalue('in_set'):
   in_set = form.getvalue('in_set')
if form.getvalue('checked_set'):
   checked_set = form.getvalue('checked_set')
# rvalues
if form.getvalue('rv_choice'):
   rv_choice = form.getvalue('rv_choice')
if form.getvalue('rf_choice'):
   rf_choice = form.getvalue('rf_choice')
if form.getvalue('rv_choiceL'):
   rv_choiceL = form.getvalue('rv_choiceL')
if form.getvalue('rf_choiceL'):
   rf_choiceL = form.getvalue('rf_choiceL')

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

# This returns the header for the general website
html_dir = '/../../~ab002/'
html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')

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

# This returns back the search boxes with the information filled in as sent
html += res.middleResolutionDefaults(set_name,calcs,buckets,amino_code,gradient,maxb,occ,contact,restriction,
                                     hist,box,violin,line,in_set, checked_set,
                                     rv_choice, rv_choiceL, rf_choice, rf_choiceL,
                                     H,B,E,G,I,T,S,U,X)

dataframes = {}
datarows = []

resolutions = buckets.split(",")
measures = calcs.split(",")

df_creator = state.sqlData()

timestring += " - SQL:" + datetime.now().strftime("%H:%M:%S")
for i in range(0,(len(resolutions)-1)):
   for measure in measures:
      measure = nc.changeDBToViewMeasure(measure)
      lower = resolutions[i]
      upper = resolutions[i+1]
      buck = lower + "-" + upper
      ch = state.sqlChoices()
      ch.addGeneralChoices(measure,"","",maxb,restriction,gradient)
      my_set = set_name

      if set_name == "DEFAULT":
         my_set = 'HIGH'
         if float(upper) > 1.3:
            my_set = '2019'


      ch.addDistribution(my_set,chosen_sets,chosen_ss,amino_code,occ,contact,[upper,lower],[rv_choice,rv_choiceL],[rf_choice,rf_choiceL])
      sqls = ch.getSqlStrings()
      for aa in sqls:
         category = measure + " " + aa + " " + buck
         weblog.log("Adding sql for " + category + ": " + sqls[aa])
         df_creator.add(sqls[aa],aa,ch,measure,buck,category,aa)

dfs = df_creator.createDataFrames()
timestring += " - Summary stats:" + datetime.now().strftime("%H:%M:%S")
# And turn it into 1 big dataframe
for i in range(0,len(dfs)):
   #create the summary details
   df = dfs[i]
   rows = len(df.index)
   if rows > 2:
      dfnew = df[['geox']]
      aas = df.aminoview.unique()
      cats = df.category.unique()
      for aa in aas:
         if aa in dataframes:
            newdf = dataframes[aa].append(df)
            dataframes[aa] = newdf
         else:
            dataframes[aa] = df

      for cat in cats: # therre should only be one!!!
         row = res.dataSummaryToRow(cat, dfnew)
         datarows.append(row)
         weblog.log("Row of summary data=" + row)

timestring += " - Generate images:" + datetime.now().strftime("%H:%M:%S")
if hist == '1':
   html += res.middleReturnCompare(dataframes,'Histogram')
if box == '1':
   html += res.middleReturnCompare(dataframes,'Box Plot')
if violin == '1':
   html += res.middleReturnCompare(dataframes,'Violin Plot')
if line == '1':
   html += res.middleReturnCompare(dataframes,'Line Plot')


html += hs.middleReturnComment("Summary statistics for each distribution")

html += "<table class='cpptable'>\n"
html += res.listToRow(['data','count','mean','std','min','25%','50%','75%','max','skew','kurtosis','normality'])
for row in datarows:
   html += row
html += "</table>\n"


end = time.time()
timestring += " - End:" + datetime.now().strftime("%H:%M:%S")
time_diff = end-start
html += timestring
html += "<br/>Total time taken = " + str(int(time_diff/60)) + "m " + str(int(time_diff%60)) + "s"
html += hs.footer()
print(html)

#************************************************************************************************
