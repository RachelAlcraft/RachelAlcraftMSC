#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      30/05/2020
Function:  A CGI file to take text and access the database
Description: 
============
This CGI file is run from the press of a button on cpp.html
It is proof of concept code for running an external C++ application
The code is minimal in order to ensure:
  - Ability to test, most of the functions are accessible through test functions in python scripts
  - Visual consistency, by calling to a cpp_strings file
"""

#************************************************************************************************

import cgi
import time
import thesis_strings as hs
import thesis_strings_corr as hsc
import thesis_strings_overlay as tso

# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

start = time.time()

# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")


# Define the defaults
# Common settings
calcX = 'CHI1'
calcY = 'CHI2'
calcZ = ''
maxb= ''
restriction=""
gradient="RESOLUTION"
optim = "yes"
scatter = "probability"
# Distribution A
set_nameA = 'HIGH' 
res_choiceA = "1.10"
res_choiceAL = "ALL"
rv_choiceA = "ALL"
rv_choiceAL = "ALL"
rf_choiceA = "0.3"
rf_choiceAL = "ALL"
amino_codeA = 'PRO'
# Distribution B
set_nameB = '2019' 
res_choiceB = "ALL"
res_choiceBL = "ALL"
rv_choiceB = "ALL"
rv_choiceBL = "ALL"
rf_choiceB = "ALL"
rf_choiceBL = "ALL"
amino_codeB = 'PRO'

# Now get chosen the values out of the form
form = cgi.FieldStorage()

if form.getvalue('calcX'):
   calcX = form.getvalue('calcX')
if form.getvalue('calcY'):
   calcY = form.getvalue('calcY')
if form.getvalue('calcZ'):
   calcZ = form.getvalue('calcZ')
if form.getvalue('maxb'):
   maxb = form.getvalue('maxb')
if form.getvalue('set_nameA'):
   set_nameA = form.getvalue('set_nameA')
if form.getvalue('restriction'):
   restriction = form.getvalue('restriction')
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

html_dir = '/../../~ab002/'
html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')


html += tso.middleOverlayDefaults(calcX,calcY,calcZ,maxb,set_nameA,res_choiceA,res_choiceAL, rv_choiceA,rv_choiceAL,rf_choiceA, rf_choiceAL,amino_codeA,set_nameB,res_choiceB,res_choiceBL,rv_choiceB,rv_choiceBL, rf_choiceB, rf_choiceBL, amino_codeB,restriction,gradient,html_dir)


html += hsc.middleReturnCorrelation(calcX,calcY,maxb,set_nameA,restriction,gradient,res_choiceA,rv_choiceA,rf_choiceA,res_choiceAL,rv_choiceAL,rf_choiceAL,amino_codeA,"probability")

end = time.time()
time_diff = end-start
mins = int(time_diff/60)
secs = int(time_diff%60)

html += "Time taken = " + str(mins) + "m " + str(secs) + "s" 

   
html += hs.footer()
print(html)

#************************************************************************************************
