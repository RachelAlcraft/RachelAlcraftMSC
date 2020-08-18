#!/usr/bin/env python3
'''
Author:    Rachel Alcraft
Date:      11/05/2020
Function:  Creates the page for the calculator
Description: 
============
In order to ensure consitency across the web pages and cgi scripts, all html is python generated.
Once all changes have been made, there are 3 fixed pages that need to be regenerated with the generation scripts:
'''

#************************************************************************************************

import thesis_strings as hs

html = ''
html += hs.header('')
html += hs.menuBar('')
#html += hs.intraMenuBar('')
html += hs.middleDescription('')
html += hs.middleCalculator('0','0','0','0','0','0','','','','','','')
html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../calc.html","w+")
print(html)
f.write(html)
f.close()
