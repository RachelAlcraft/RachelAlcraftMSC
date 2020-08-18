#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      05/06/2020
Function:  The overlay facility to compare distributions
Description:
============

######!/d/msc/s/anaconda/v5.3.0/bin/python
######!/usr/bin/env python3
"""
import pandas as pd
from io import StringIO as sio
import thesis_read_db_simple as sdb
import thesis_strings as ts
import thesis_strings_corr as tsc
import thesis_images as tim
import thesis_sql as sqldb
from PIL import Image
import numpy as np
from scipy.stats import gaussian_kde


###################################################################################################################


def middleResolutionDefaults(set_name, calcs, buckets, amino_code, gradient, maxb, occ, contact, restriction,
                             hist, box, violin, line, in_set, checked_set,
                             rv_choice, rv_choiceL, rf_choice, rf_choiceL,
                             H, B, E, G, I, T, S, U, X):
    '''
    This ensures the defaults are returned back to the screen
    '''

    html = ts.middleReturnComment("Enter appropriate parameters to compare distributions on resolution")
    html += '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_resolutions.cgi" accept-charset="UTF-8">\n'
    html += '<div class="smallmiddle">\n'

    # overall table
    html += '<table class="verdsearchtable">'
    html += '<tr class=outinnerheader><td>Choices</td><td>Secondary Structure</td><td>Restrictions</td><td>Select views</td><td>Structure Status</td></tr>\n'
    html += '<tr>'
    html += '<td>'  # choices
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Set Name</td><td><input type="text" size="15" name="set_name" value="' + set_name + '"/></td></tr>\n'
    html += '<tr><td>Amino Code</td><td><input type="text" size="15" name="amino_code" value="' + amino_code + '"/></td></tr>\n'
    html += '<tr><td>Calcs (comma list)</td><td><input type="text" size="15" name="calcs" value="' + calcs + '"/></td></tr>\n'
    html += '<tr><td>Buckets (comma list)</td><td><input type="text" size="15" name="buckets" value="' + buckets + '"/></td></tr>\n'
    # html += '<tr><td>Gradient</td><td><input type="text" size="15" name="gradient" value="' + gradient + '"/></td></tr>\n'
    html += '</table>'
    html += '</td>'

    # Secondary Structure selection

    Hcheck = ''
    if H == "1":
        Hcheck = "checked='checked'"
    Bcheck = ''
    if B == "1":
        Bcheck = "checked='checked'"
    Echeck = ''
    if E == "1":
        Echeck = "checked='checked'"
    Gcheck = ''
    if G == "1":
        Gcheck = "checked='checked'"
    Icheck = ''
    if I == "1":
        Icheck = "checked='checked'"
    Tcheck = ''
    if T == "1":
        Tcheck = "checked='checked'"
    Scheck = ''
    if S == "1":
        Scheck = "checked='checked'"
    Ucheck = ''
    if U == "1":
        Ucheck = "checked='checked'"
    Xcheck = ''
    if X == "1":
        Xcheck = "checked='checked'"

    html += '<td>'  # options for Secondary Structure
    html += '<table class="verdsearchtable">'
    html += '<tr><td><label for="H">H=α-helix</label></td><td><input type="checkbox" id="H" name="H" value="1" ' + str(
        Hcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="B">B=residue in isolated β-bridge</label></td><td><input type="checkbox" id="B" name="B" value="1" ' + str(
        Bcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="E">E=extended strand, participates in β ladder</label></td><td><input type="checkbox" id="E" name="E" value="1" ' + str(
        Echeck) + '"></td></tr>\n'
    html += '<tr><td><label for="G">G=3-helix (310 helix)</label></td><td><input type="checkbox" id="G" name="G" value="1" ' + str(
        Gcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="I">I=5 helix (π-helix)</label></td><td><input type="checkbox" id="I" name="I" value="1" ' + str(
        Icheck) + '"></td></tr>\n'
    html += '<tr><td><label for="T">T=hydrogen bonded turn</label></td><td><input type="checkbox" id="T" name="T" value="1" ' + str(
        Tcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="S">S=bend </label></td><td><input type="checkbox" id="S" name="S" value="1" ' + str(
        Scheck) + '"></td></tr>\n'
    html += '<tr><td><label for="U">U=unknown</label></td><td><input type="checkbox" id="U" name="U" value="1" ' + str(
        Ucheck) + '"></td></tr>\n'
    html += '<tr><td><label for="X">X=Unassigned</label></td><td><input type="checkbox" id="X" name="X" value="1" ' + str(
        Xcheck) + '"></td></tr>\n'
    html += '</table>'
    html += '</td>'

    html += '<td>'  # restrictions
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Max Bfactor</td><td><input type="text" size="6" name="maxb" value="' + maxb + '"/></td></tr>\n'
    html += '<tr><td>R Value</td><td><input type="text" size="6" name="rv_choice" value="' + rv_choice + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rv_choiceL" value="' + rv_choiceL + '"/></td></tr>\n'
    html += '<tr><td>R Free</td><td><input type="text" size="6" name="rf_choice" value="' + rf_choice + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rf_choiceL" value="' + rf_choiceL + '"/></td></tr>\n'
    html += '<tr><td>Occupant</td><td><input type="text" size="6" name="occ" value="' + occ + '"/></td></tr>\n'
    html += '<tr><td>Contact</td><td><input type="text" size="6" name="contact" value="' + contact + '"/></td></tr>\n'
    html += '<tr><td>Restriction</td><td colspan="2"><input type="text" size="15" name="restriction" value="' + restriction + '"/></td></tr>\n'
    html += '</table>'
    html += '</td>'
    html += '<td>'  # Distribution buttons
    html += '<table class="verdsearchtable">'
    html += ""
    histcheck = ''
    if hist == "1":
        histcheck = "checked='checked'"
    boxcheck = ''
    if box == "1":
        boxcheck = "checked='checked'"
    violincheck = ''
    if violin == "1":
        violincheck = "checked='checked'"
    linecheck = ''
    if line == "1":
        linecheck = "checked='checked'"
    html += '<tr><td><label for="scatter">Box Plots</label></td><td><input type="checkbox" id="box" name="box" value="1" ' + str(
        boxcheck) + '"></td></tr>\n'
    # html += '<tr><td><label for="trace">Swarm Plots</label></td><td><input type="checkbox" id="swarm" name="swarm" value="1" ' + str(swarmcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="probden">Violin Plots</label></td><td><input type="checkbox" id="violin" name="violin" value="1" ' + str(
        violincheck) + '"></td></tr>\n'
    html += '<tr><td><label for="breadth">Line Plots</label></td><td><input type="checkbox" id="line" name="line" value="1" ' + str(
        linecheck) + '"></td></tr>\n'
    html += '<tr><td><label for="hist">Histograms</label></td><td><input type="checkbox" id="hist" name="hist" value="1" ' + str(
        histcheck) + '"></td></tr>\n'
    html += '</table>'

    in_checked = ''
    if in_set == '1':
        in_checked = ' checked="checked"'
    checked_checked = ''
    if checked_set == '1':
        checked_checked = ' checked="checked"'

    html += '<td><table class="verdsearchtable">'
    html += '<tr><td><label for="hist">Include IN pdbs</label></td><td><input type="checkbox" id="in_set" name="in_set" value="1" ' + str(
        in_checked) + '"></td></tr>\n'
    html += '<tr><td><label for="hist">Include CHECKED pdbs</label></td><td><input type="checkbox" id="checked_set" name="checked_set" value="1" ' + str(
        checked_checked) + '"></td></tr>\n'
    html += '</td></table>'

    html += '</td>'
    html += '</tr>'
    html += '<table>'
    html += "<tr><td><div class='buttondist'><input type='Submit' value='Compare Distributions' formaction='/cgi-bin/cgiwrap/ab002/thesis_resolutions.cgi'/></div></td></tr>\n"
    html += '</table>'

    # close form
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


###################################################################################################################
def middleReturnCompare(sqldatas, view):
    html = ""
    html += "<table class='outtable'>\n"

    html = ts.middleReturnComment("Comparison of data at given resolution buckets: " + view)
    dfList = []

    for aa in sqldatas:
        dfList.append(sqldatas[aa])

    axes = tim.maxMinAxes(dfList, 'geox', '', 'double', '')

    html += "<table class='outtable'>\n"

    count = 0
    for aa in sqldatas:
        if count % 4 == 0:
            if count == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"
        html += "<td>" + getOneCompare(sqldatas[aa], aa, axes, view) + "</td>"
        count += 1

    html += "</tr>\n"
    html += "</table>\n"

    # print(html)

    return (html)


# ************************************************************************************************
def getOneCompare(dfaa, aa, axes, view):
    """
    param: pdb code
    returns: html
    """
    # print("debug 1")

    html = tim.dataFrameToBoxPlot(dfaa, aa, axes, view)
    # html = tim.dataFrameToLinesErrors(dfaa,aa,axes)

    return (html)


# ************************************************************************************************
def listToRow(list):
    html = "<tr class='cppinnerheader'>\n"
    for ls in list:
        html += "<td>" + ls + "</td>\n"
    html += "</tr>\n"
    return (html)


def dataSummaryToRow(name, df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    from scipy.stats import shapiro
    from scipy.stats import normaltest
    from scipy.stats import skew
    from scipy.stats import kurtosis

    dfdesc = df.describe()
    # cols = 0
    rows = 0
    # html = "<table class='cpptable'>\n"
    rows = len(dfdesc.index)
    html = "<tr>\n"
    html += "<td>" + name + "</td>\n"
    for r in range(0, rows):
        html += "<td>" + str((round(dfdesc.iloc[r, 0], 4))) + "</td>\n"

    # Add on the skew, kurtosis and normality
    vals = df['geox'].values
    sk = round(skew(vals), 3)
    html += "<td>" + str(sk) + "</td>\n"
    kr = round(kurtosis(vals), 3)
    html += "<td>" + str(kr) + "</td>\n"
    stat, p = shapiro(vals)
    isNormal = "N"
    alpha = 0.05
    if p > alpha:
        isNormal = "Y"
    html += "<td>" + isNormal + "</td>\n"
    html += "</tr>\n"
    return (html)
