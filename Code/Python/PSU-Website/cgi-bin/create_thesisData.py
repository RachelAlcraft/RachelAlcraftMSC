#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      04/06/2020
Function:  Creates the page to view available Geo Measures html
Description: 
============

"""

#************************************************************************************************

import thesis_strings as hs
import thesis_strings_measures as hsm

html = ''
html += hs.header('')
html += hs.menuBar('')
html += hs.middleDescription('')

html += hs.middleReturnComment('Some prelimary help for the distributions page')
html += hsm.getHelp()

html += hs.middleReturnComment('These geometric measures have been pre-calculated for non-similar high resolution structures from the pdb (<=1.3A) and a 2018-2019 set.')
html += hsm.getCalcButton()

html += hs.middleReturnComment('For the HIGH resolution structures included...')
html += hsm.getHighButton()

html += hs.middleReturnComment('For the 2018-2019 structures included...')
html += hsm.get2019Button()

html += hs.footer()

# create the cpp.html so that all the look and feel is consistent
f= open("../data.html","w+")
print(html)
f.write(html)
f.close()
