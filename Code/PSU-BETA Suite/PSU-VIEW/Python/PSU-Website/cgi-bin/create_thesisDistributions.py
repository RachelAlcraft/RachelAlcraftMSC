#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      04/06/2020
Function:  Creates the page for the overlay html
Description: 
============
Page ready for overlaying and comparing 2 distributions
"""

#************************************************************************************************

import thesis_strings as hs
import thesis_strings_overlay as tso

html = ''
html += hs.header('')
html += hs.menuBar('')

# Define the defaults
# Common settings
calcX = 'PHI'
calcY = 'PSI'
calcZ = ''
maxbA= '100'
maxbB= '100'
restrictionA=""
restrictionB=""
gradient="RESOLUTION"
# Distribution A
set_nameA = 'HIGH'
occA = "A"
contactA = ''
res_choiceA = "1.25"
res_choiceAL = "ALL"
rv_choiceA = "ALL"
rv_choiceAL = "ALL"
rf_choiceA = "0.3"
rf_choiceAL = "ALL"
amino_codeA = 'PRO'
# Distribution B
set_nameB = 'HIGH'
occB = "A"
contactB = ''
res_choiceB = "ALL"
res_choiceBL = "1.25"
rv_choiceB = "ALL"
rv_choiceBL = "ALL"
rf_choiceB = "0.3"
rf_choiceBL = "ALL"
amino_codeB = 'PRO'
# check boxes for images
hist = ""
scatter="1"
trace = ""
probden="1"
breadth=""
depth=""
scatter3 =""
in_set = '1'
checked_set = '1'
# ss
H='1'
B='1'
E='1'
G='1'
I='1'
T='1'
S='1'
U='1'
X='1'
# ss
Hb='1'
Bb='1'
Eb='1'
Gb='1'
Ib='1'
Tb='1'
Sb='1'
Ub='1'
Xb='1'
html += hs.middleDescription('')

html += tso.middleOverlayDefaults(calcX,calcY,calcZ,
                                  maxbA,maxbB,set_nameA,occA,contactA,res_choiceA,res_choiceAL, rv_choiceA,rv_choiceAL,rf_choiceA, rf_choiceAL,amino_codeA,
                                  set_nameB,occB,contactB,res_choiceB,res_choiceBL,rv_choiceB,rv_choiceBL, rf_choiceB, rf_choiceBL, amino_codeB,
                                  restrictionA,restrictionB,gradient,'',
                                  hist,scatter,trace,probden,breadth,depth,scatter3,in_set,checked_set,
                                  H,B,E,G,I,T,S,U,X,
                                  Hb,Bb,Eb,Gb,Ib,Tb,Sb,Ub,Xb)

html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../distributions.html","w+")
print(html)
f.write(html)
f.close()
