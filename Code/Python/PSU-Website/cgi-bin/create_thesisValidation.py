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
import thesis_strings_validation as val

html = ''
html += hs.header('')
html += hs.menuBar('')

# Define the defaults
# Common settings
pdb_code = ''
set_name = 'HIGH'
maxb= '40'
restriction=""
occ = "A"
contact = ''

# Distribution A
res_choice = "1"
res_choiceL = "ALL"
rv_choice = "ALL"
rv_choiceL = "ALL"
rf_choice = "0.3"
rf_choiceL = "ALL"

gradient = 'ss_psu'
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

html += hs.middleDescription('')
# This returns back the search boxes with the information filled in as sent
html += val.middleValidationDefaults(pdb_code, set_name,
                                res_choice,res_choiceL,rv_choice,rv_choiceL, rf_choice, rf_choiceL,
                                maxb, occ, contact, restriction,gradient,in_set,checked_set,
                                     H,B,E,G,I,T,S,U,X)

html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../validation.html","w+")
print(html)
f.write(html)
f.close()
