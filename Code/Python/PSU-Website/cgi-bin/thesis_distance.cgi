#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      11/05/2020
Function:  A CGI file to calculate the basic geometric values
Description: 
============
A validation check for the values in the database
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

x1=''
y1=''
z1=''
x2=''
y2=''
z2=''
x3=''
y3=''
z3=''
x4=''
y4=''
z4=''

form = cgi.FieldStorage()

if form.getvalue('x1'):
   x1 = form.getvalue('x1')
if form.getvalue('y1'):
   y1 = form.getvalue('y1')
if form.getvalue('z1'):
   z1 = form.getvalue('z1')
   
if form.getvalue('x2'):
   x2 = form.getvalue('x2')
if form.getvalue('y2'):
   y2 = form.getvalue('y2')
if form.getvalue('z2'):
   z2 = form.getvalue('z2')

if form.getvalue('x3'):
   x3 = form.getvalue('x3')
if form.getvalue('y3'):
   y3 = form.getvalue('y3')
if form.getvalue('z3'):
   z3 = form.getvalue('z3')

if form.getvalue('x4'):
   x4 = form.getvalue('x4')
if form.getvalue('y4'):
   y4 = form.getvalue('y4')
if form.getvalue('z4'):
   z4 = form.getvalue('z4')

html = hs.header('/../../~ab002/')
html += hs.menuBar('/../../~ab002/')
#html += hs.intraMenuBar('/../../~ab002/')

html += hs.middleDescription('/../../~ab002/')
html += hs.middleCalculator(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4)

dcalc = hs.getCalcDistance(x1,y1,z1,x2,y2,z2)
acalc = hs.getCalcAngle(x1,y1,z1,x2,y2,z2,x3,y3,z3)
tcalc = hs.getCalcTorsion(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4)

html += hs.middleReturnCalc(dcalc,acalc,tcalc)

html += hs.footer()

print(html)