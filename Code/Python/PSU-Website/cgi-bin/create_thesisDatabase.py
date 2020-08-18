#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  Creates the page for the thesis html
Description: 
============
yIn order to ensure consitency across the web pages and cgi scripts, all html is python generated.
Once all changes have been made, there are 3 fixed pages that need to be regenerated with the generation scripts:
    - createHTML_index.py generates index.html
    - createHTML_chme9.py generates Chme9.html
    - createHTML_CppIndex.py generates cpp.html
"""

#************************************************************************************************

import thesis_strings as hs

html = ''
html += hs.header('')
html += hs.menuBar('')
#html += hs.intraMenuBar('')
html += hs.middleDescription('')
#html += hs.middleTestThesis('N-CA','4REK','','A','HIGH','')

sql = "SELECT * FROM geo_core LIMIT 10;"
html += hs.middleSqlOnly(sql)


html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../database.html","w+")
print(html)
f.write(html)
f.close()
