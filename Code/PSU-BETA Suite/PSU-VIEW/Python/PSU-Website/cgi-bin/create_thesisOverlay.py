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
calcX = 'CHI1'
calcY = 'CHI2'
optim = "yes"
scatter = "probability"
# Distribution A
set_nameA = 'HIGH' 
res_choiceA = "1.10"
rv_choiceA = "ALL"
rf_choiceA = "0.3"
amino_codeA = 'PRO'
# Distribution B
set_nameB = '2019' 
res_choiceB = "ALL"
rv_choiceB = "ALL"
rf_choiceB = "ALL"
amino_codeB = 'PRO'

html += hs.middleDescription('')
#html += hs.middleReturnComment('The OVERLAY facility is currently under construction.')
html += tso.middleOverlayDefaults(calcX,calcY,set_nameA,res_choiceA,rv_choiceA,rf_choiceA, amino_codeA,set_nameB,res_choiceB,rv_choiceB,rf_choiceB, amino_codeB)

html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../overlay.html","w+")
print(html)
f.write(html)
f.close()
