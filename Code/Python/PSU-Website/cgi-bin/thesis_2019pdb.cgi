#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
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

import cgi;
import thesis_strings as hs
import thesis_strings_measures as hsm


# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")


pdb = '5NQO' # this will not allow the possibility of ALL


html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')


html += hs.middleReturnComment('These geometric measures have been pre-calculated for non-similar high resolution structures from the pdb (<=1.3A) and a 2018-2019 set.')
html += hsm.getCalcButton()

html += hs.middleReturnComment('For the HIGH resolution structures included...')
html += hsm.getHighButton()


html += hs.middleReturnComment('For the 2018-2019 structures included...')
sql= hsm.get2019PDBsSql()
#html += sql
html += hsm.middleReturnPDBs(sql)

html += hs.footer()
print(html)

#************************************************************************************************


