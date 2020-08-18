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
import thesis_strings as hs
import thesis_strings_hist as hsh
import thesis_strings_overlay as tso
import thesis_strings_hist as hst
import class_sqlData as state
import thesis_images as image
import name_change as nc
import thesis_strings_corr as corr
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
calcX = 'N-O'
calcY = ''
calcZ = ''
gradient="RESOLUTION"
# Distribution A
set_nameA = 'HIGH'
occA = "A"
contactA = ''
restrictionA=""
maxbA= '100'
res_choiceA = "1.10"
res_choiceAL = "ALL"
rv_choiceA = "ALL"
rv_choiceAL = "ALL"
rf_choiceA = "0.3"
rf_choiceAL = "ALL"
amino_codeA = 'PRO'
# Distribution B
set_nameB = '2019'
occB = "A"
contactB = ''
restrictionB=""
maxbB= '100'
res_choiceB = "ALL"
res_choiceBL = "ALL"
rv_choiceB = "ALL"
rv_choiceBL = "ALL"
rf_choiceB = "0.3"
rf_choiceBL = "ALL"
amino_codeB = 'PRO'

# check boxes for images
hist = 0
scatter=0
trace=0
probden=0
breadth=0
depth=0
scatter3 =0

# sets
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
# ssb
Hb=0
Bb=0
Eb=0
Gb=0
Ib=0
Tb=0
Sb=0
Ub=0
Xb=0

# Now get chosen the values out of the form
form = cgi.FieldStorage()

if form.getvalue('calcX'):
   calcX = form.getvalue('calcX')
if form.getvalue('calcY'):
   calcY = form.getvalue('calcY')
if form.getvalue('calcZ'):
   calcZ = form.getvalue('calcZ')
if form.getvalue('set_nameA'):
   set_nameA = form.getvalue('set_nameA')
if form.getvalue('occA'):
   occA = form.getvalue('occA')
if form.getvalue('contactA'):
   contactA = form.getvalue('contactA')
if form.getvalue('restrictionA'):
   restrictionA = form.getvalue('restrictionA')
if form.getvalue('maxbA'):
   maxbA = form.getvalue('maxbA')
if form.getvalue('maxbB'):
   maxbB = form.getvalue('maxbB')
if form.getvalue('gradient'):
   gradient = form.getvalue('gradient')
if form.getvalue('amino_codeA'):
   amino_codeA = form.getvalue('amino_codeA')
if form.getvalue('res_choiceA'):
   res_choiceA = form.getvalue('res_choiceA')
if form.getvalue('res_choiceAL'):
   res_choiceAL = form.getvalue('res_choiceAL')
if form.getvalue('rv_choiceA'):
   rv_choiceA = form.getvalue('rv_choiceA')
if form.getvalue('rv_choiceAL'):
   rv_choiceAL = form.getvalue('rv_choiceAL')
if form.getvalue('rf_choiceA'):
   rf_choiceA = form.getvalue('rf_choiceA')
if form.getvalue('rf_choiceAL'):
   rf_choiceAL = form.getvalue('rf_choiceAL')
if form.getvalue('set_nameB'):
   set_nameB = form.getvalue('set_nameB')
if form.getvalue('occB'):
   occB = form.getvalue('occB')
if form.getvalue('contactB'):
   contactB = form.getvalue('contactB')
if form.getvalue('restrictionB'):
   restrictionB = form.getvalue('restrictionB')
if form.getvalue('amino_codeB'):
   amino_codeB = form.getvalue('amino_codeB')
if form.getvalue('res_choiceB'):
   res_choiceB = form.getvalue('res_choiceB')
if form.getvalue('rv_choiceB'):
   rv_choiceB = form.getvalue('rv_choiceB')
if form.getvalue('rf_choiceB'):
   rf_choiceB = form.getvalue('rf_choiceB')
if form.getvalue('res_choiceBL'):
   res_choiceBL = form.getvalue('res_choiceBL')
if form.getvalue('rv_choiceBL'):
   rv_choiceBL = form.getvalue('rv_choiceBL')
if form.getvalue('rf_choiceBL'):
   rf_choiceBL = form.getvalue('rf_choiceBL')
# images
ps1= str(hist) + str(scatter) + str(probden) + str(breadth) + str(depth) + str(scatter3)
if form.getvalue('hist'):
   hist = form.getvalue('hist')
if form.getvalue('scatter'):
   scatter = form.getvalue('scatter')
if form.getvalue('trace'):
   trace = form.getvalue('trace')
if form.getvalue('probden'):
   probden = form.getvalue('probden')
if form.getvalue('breadth'):
   breadth = form.getvalue('breadth')
if form.getvalue('depth'):
   depth = form.getvalue('depth')
if form.getvalue('scatter3'):
   scatter3 = form.getvalue('scatter3')
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
# SECONDARY STRUCTURE
if form.getvalue('Hb'):
   Hb=form.getvalue('Hb')
if form.getvalue('Bb'):
   Bb=form.getvalue('Bb')
if form.getvalue('Eb'):
   Eb=form.getvalue('Eb')
if form.getvalue('Gb'):
   Gb=form.getvalue('Gb')
if form.getvalue('Ib'):
   Ib=form.getvalue('Ib')
if form.getvalue('Tb'):
   Tb=form.getvalue('Tb')
if form.getvalue('Sb'):
   Sb=form.getvalue('Sb')
if form.getvalue('Ub'):
   Ub=form.getvalue('Ub')
if form.getvalue('Xb'):
   Xb=form.getvalue('Xb')

ps2= str(hist) + str(scatter) + str(probden) + str(breadth) + str(depth) + str(scatter3)

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

chosen_ssb = '('
if Hb == '1':
   chosen_ssb += "'H',"
if Bb == '1':
   chosen_ssb += "'B',"
if Eb == '1':
   chosen_ssb += "'E',"
if Gb == '1':
   chosen_ssb += "'G',"
if Ib == '1':
   chosen_ssb += "'I',"
if Tb == '1':
   chosen_ssb += "'T',"
if Sb == '1':
   chosen_ssb += "'S',"
if Ub == '1':
   chosen_ssb += "'U',"
if Xb == '1':
   chosen_ssb += "'-',"
chosen_ssb += "'z')" # THERE IS NO Z IT JUST ENSURES A VALID SELECTION




# This returns the header for the general website
html_dir = '/../../~ab002/'
html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')
# This returns back the search boxes with the information filled in as sent
html += tso.middleOverlayDefaults(
                           calcX,calcY,calcZ,maxbA,maxbB,
                           set_nameA,occA, contactA, res_choiceA,res_choiceAL, rv_choiceA,rv_choiceAL,rf_choiceA, rf_choiceAL,amino_codeA,
                           set_nameB,occB, contactB, res_choiceB,res_choiceBL,rv_choiceB,rv_choiceBL, rf_choiceB, rf_choiceBL, amino_codeB,
                           restrictionA,restrictionB,gradient,html_dir,hist,scatter,trace,probden,breadth,depth,scatter3,in_set, checked_set,
                           H,B,E,G,I,T,S,U,X,
                           Hb,Bb,Eb,Gb,Ib,Tb,Sb,Ub,Xb)

ps3 = str(hist) + str(scatter) + str(probden) + str(breadth) + str(depth) + str(scatter3)
#html += ps1 + ps2 + ps3

gradient = nc.changeViewToDBMeasure(gradient)


## Create any 1 dimensional data requested
choicesA = state.sqlChoices()
choicesA.addGeneralChoices(calcX,calcY,calcZ,maxbA,restrictionA,gradient)
choicesA.addDistribution(set_nameA, chosen_sets,chosen_ss,amino_codeA, occA, contactA, [res_choiceA,res_choiceAL], [rv_choiceA,rv_choiceAL],[rf_choiceA, rf_choiceAL])
a_dataframes = {}
if int(depth) + int(breadth)  + int(hist) + int(scatter) + int(probden) + int(scatter3)  + int(trace)  > 0:
   a_sqlStrings = choicesA.getSqlStrings()
   start_sqlA = time.time() ## timer
   timestring += " - Get sql A:" + datetime.now().strftime("%H:%M:%S")
   for aa in a_sqlStrings:
      sql = a_sqlStrings[aa]
      weblog.log('SQL=' + sql)

      #html += sql ## remove after debugging
      sqldata = state.sqlData(sql,aa,choicesA)
      dfA = sqldata.createDataFrame()
      a_dataframes[aa] = sqldata
      #html += hs.dataFrameToGrid(dfA)## remove after debugging

   if str(hist) == "1":
      timestring += " - Get histograms:" + datetime.now().strftime("%H:%M:%S")
      html += hst.middleReturnHistogram(a_dataframes)



## Create any 2 dimensional data requested,
## we already have the dataframes so we don't need to redo them

if choicesA.calcy != "" and "C@" not in calcX:
   if str(scatter)=="1":
      timestring += " - Get scatter:" + datetime.now().strftime("%H:%M:%S")
      html += corr.middleReturnCorrelation(a_dataframes,gradient,"scatter")
   if str(trace)=="1":
      timestring += " - Get density trace:" + datetime.now().strftime("%H:%M:%S")
      html += corr.middleReturnCorrelation(a_dataframes,gradient,"trace")
   if str(probden)=="1":
      timestring += " - Get prob dense:" + datetime.now().strftime("%H:%M:%S")
      html += corr.middleReturnCorrelation(a_dataframes,gradient,"probability")


## Create any 3 dimensional data requested,
if choicesA.calcz != "" and str(scatter3)=="1" and "C@" not in calcX:
   timestring += " - Get scatter 3d:" + datetime.now().strftime("%H:%M:%S")
   html += corr.middleReturnScatter3d(a_dataframes,gradient)


## Create a second set of data if comparisons required
choicesB = state.sqlChoices()
choicesB.addGeneralChoices(calcX,calcY,calcZ,maxbB,restrictionB,gradient)
choicesB.addDistribution(set_nameB, chosen_sets,chosen_ssb,amino_codeB, occB, contactB, [res_choiceB,res_choiceBL], [rv_choiceB,rv_choiceBL],[rf_choiceB, rf_choiceBL])

if choicesB.set_name != "" and int(depth) + int(breadth) > 0 and "C@" not in calcX and choicesA.calcy != "":
   timestring += " - SQL B:" + datetime.now().strftime("%H:%M:%S")
   b_sqlStrings = choicesB.getSqlStrings()
   b_dataframes = {}
   for aa in b_sqlStrings:
      sql = b_sqlStrings[aa]
      #html += sql ## remove after debugging
      sqldata = state.sqlData(sql,aa,choicesB)
      sqldata.createDataFrame()
      b_dataframes[aa] = sqldata   
   # Compare breadth
   bothAll = False
   if amino_codeA == "ALL" and amino_codeB == "All":
      bothAll = True
   if str(breadth)=="1":
      timestring += " - Compare breadth:" + datetime.now().strftime("%H:%M:%S")
      html += tso.middleOverlayRequest(a_dataframes,b_dataframes,bothAll)
   if str(depth)=="1":
      timestring += " - Compare depth:" + datetime.now().strftime("%H:%M:%S")
      html += tso.middleProbDiffRequest(a_dataframes,b_dataframes,bothAll)



end = time.time()
timestring += " - End:" + datetime.now().strftime("%H:%M:%S")

time_diff = end-start



html += timestring
html += "<br/>Total time taken = " + str(int(time_diff/60)) + "m " + str(int(time_diff%60)) + "s" 

   
html += hs.footer()
print(html)

#************************************************************************************************
