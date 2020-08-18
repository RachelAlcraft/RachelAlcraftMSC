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

html += hs.middleDescription('')
html += hs.middleReturnComment('These pages are part of a student MSc project on high resolution structures.')

inner = ""
inner += '<table><tr>'
inner += '<td>'
inner += '<img src="img/psu.png" alt="PSU" height="300"/>'
inner += '</td>'
inner += '</tr>'
inner += '<tr>'
inner += '<td>'
inner += '<div class="middle"><p>'
inner += 'The project examines ultra high resolution structures to seek new and/or updated information on geometric features.<br/>\n'
inner += 'Geometric data from the pdb has been calculated from a C++ project and uploaded to a MySQL database on the Birkbeck servers.<br/>\n'
inner += 'This website uses python, cgi scripts, numpy, matplotlib and seaborn to examine the database on selected geometric features.<br/>\n'
inner += 'Correlations, probability density plots, histograms and comparisons of resolutions are available.<br/>\n'
inner += 'Close contact analysis is also available for SG-SG, CB-CB, CA-CA and N-O, which is used for additional analysis of secondary structure.<br/>\n'
inner += 'There is also a feature to freely examine the database - if you know the password :-)<br/>\n'
inner += 'Lastly, there is a calculator for distance, angle and dihedral angle which is useful for checking values - the working is shown.<br/>\n'
inner += 'Any comments/problems/questions please email me: <a href = "mailto:rachelalcraft@gmail.com" > Rachel Alcraft </a >\n'
inner += '</p></div></td></tr></table>'

html += inner


html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../thesis.html","w+")
print(html)
f.write(html)
f.close()
