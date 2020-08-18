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

import cgi;
import pandas as pd
import thesis_strings as hs
import thesis_strings_resolutions as res
import class_sqlData as state
import thesis_images as image
import time


html = ''
html += hs.header('')
html += hs.menuBar('')

# Define the defaults
# Common settings
set_name = 'DEFAULT'
calcs = 'N-CA,CA-C'
buckets = '0,1,1.15,1.2,1.25,1.3,1.5,1.8,2,10'
maxb= '50'
restriction=""
occ = "A"
contact = ''
amino_code = 'NON'
gradient='resolution'
#options
hist = '0'
box = '0'
violin = '1'
line = '0'
in_set = '1'
checked_set = '1'
rv_choice = "0.16"
rv_choiceL = "ALL"
rf_choice = "0.3"
rf_choiceL = "ALL"
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

html += res.middleResolutionDefaults(set_name,calcs,buckets,amino_code,gradient,maxb,occ,contact,restriction,
                                     hist, box, violin, line,in_set,checked_set,
                                        rv_choice, rv_choiceL, rf_choice, rf_choiceL,
                                        H,B,E,G,I,T,S,U,X)


html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../resolution.html","w+")
print(html)
f.write(html)
f.close()
