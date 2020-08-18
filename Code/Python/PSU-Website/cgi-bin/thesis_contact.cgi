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
import thesis_sql as sqldb


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


form = cgi.FieldStorage()

if form.getvalue('pdb'):
   pdb = form.getvalue('pdb')

html += hs.middleContactRequest(pdb)
   
sqlsg = sqldb.createSqlContacts(pdb,"SG-SG")
sqlno = sqldb.createSqlContacts(pdb,"N-O")
sqlca = sqldb.createSqlContacts(pdb,"CA-CA")
sqlcb = sqldb.createSqlContacts(pdb,"CB-CB")



html += hs.middleReturnContact(pdb,sqlsg,sqlno,sqlca,sqlcb)

#html += hs.middleReturnComment(sqlsg)
#html += hs.middleReturnComment(sqlno)


   




html += hs.footer()
print(html)

#************************************************************************************************


