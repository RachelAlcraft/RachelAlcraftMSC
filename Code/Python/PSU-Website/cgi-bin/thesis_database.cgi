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
import blapi as bl;
import thesis_strings as hs

# Useful debugging output
import cgitb
cgitb.enable()  # Send errors to browser
# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

# Print the HTML MIME-TYPE header
print ("Content-Type: text/html\n")

sql = 'none'
pswd = 'none'

text_input = 'none'
rest_col = ''
rest_val = ''
pswd = 'none'
amino = ''
pdb = ''
occupant = ''
setname = 'HIGH'

form = cgi.FieldStorage()

if form.getvalue('sql'):
   sql = form.getvalue('sql')
if form.getvalue('password'):
   pswd = form.getvalue('password')



#text_content = "N-O CA-CB"

html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
#html += hs.intraMenuBar('/../../~ab002/')

html += hs.middleDescription('/../../~ab002/')
html += hs.middleSqlOnly(sql)
#html += hs.middleReturnSQL(sql)
if pswd == 'cinderelephant':
    html += hs.middleReturnSearch(sql)
else:
    html += hs.middleReturnError('')

html += hs.footer()




print(html)

#************************************************************************************************
