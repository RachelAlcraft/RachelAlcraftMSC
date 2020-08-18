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

text_input = 'none'
rest_col = ''
rest_val = ''
pswd = 'none'
amino = ''
pdb = ''
occupant = ''
setname = 'HIGH'
sql = 'none'
pswd = 'none'


html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
html += hs.middleDescription('/../../~ab002/')




form = cgi.FieldStorage()


if form.getvalue('choices'):
   text_input = form.getvalue('choices')
 
if form.getvalue('rest_col'):
   rest_col = form.getvalue('rest_col')

if form.getvalue('rest_val'):
   rest_val = form.getvalue('rest_val')
 
if form.getvalue('amino'):
   amino = form.getvalue('amino')
   
if form.getvalue('pdb'):
   pdb = form.getvalue('pdb')
   
if form.getvalue('occupant'):
   occupant = form.getvalue('occupant')
 
if form.getvalue('setname'):
   setname = form.getvalue('setname')



sql = hs.getSQLJ(text_input,amino,occupant,pdb,setname,False)

if text_input != 'none':
    #sql = hs.getSQLJ(text_input,amino,occupant,pdb,status,False)
    #html += hs.middleReturnSQL(sql)
    html += hs.middleTestThesis(text_input,pdb,amino,occupant,setname,sql)
else:
    html += hs.middleReturnError('Invalid entries')
   




html += hs.footer()
print(html)

#************************************************************************************************
