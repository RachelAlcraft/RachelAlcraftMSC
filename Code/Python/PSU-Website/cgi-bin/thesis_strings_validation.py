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


def middleValidationDefaults(pdb_code, set_name,
                             res_choice, res_choiceL, rv_choice, rv_choiceL, rf_choice, rf_choiceL,
                             maxb, occ, contact, restriction, gradient, in_set, checked_set,
                             H, B, E, G, I, T, S, U, X):
    '''
    This ensures the defaults are returned back to the screen
    '''

    html = ts.middleReturnComment("Enter appropriate parameters to produce validation reports on a chosen selection")
    html += '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_validation.cgi" accept-charset="UTF-8">\n'
    html += '<div class="smallmiddle">\n'

    # overall table
    html += '<table class="verdsearchtable">'
    html += '<tr class=outinnerheader><td>Choices</td><td>Restrictions</td><td>Secondary Structure</td><td>Hue Choice</td></tr>\n'
    html += '<tr>'
    html += '<td>'  # choices
    html += '<table class="verdsearchtable">'
    html += '<tr><td>PDB Code (overrides all)</td><td><input type="text" size="15" name="pdb_code" value="' + pdb_code + '"/></td></tr>\n'
    html += '<tr><td>Set Name</td><td><input type="text" size="15" name="set_name" value="' + set_name + '"/></td></tr>\n'
    # html += '<tr><td>Amino Code</td><td><input type="text" size="15" name="amino_code" value="' + amino_code + '"/></td></tr>\n'
    html += '<tr><td>Bounds:</td><td>Upper</td><td>Lower</td></tr>\n'
    html += '<tr><td>Resolution</td><td><input type="text" size="6" name="res_choice" value="' + res_choice + '"/></td>\n'
    html += '<td><input type="text" size="6" name="res_choiceL" value="' + res_choiceL + '"/></td></tr>\n'
    html += '<tr><td>R Value</td><td><input type="text" size="6" name="rv_choice" value="' + rv_choice + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rv_choiceL" value="' + rv_choiceL + '"/></td></tr>\n'
    html += '<tr><td>R Free</td><td><input type="text" size="6" name="rf_choice" value="' + rf_choice + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rf_choiceL" value="' + rf_choiceL + '"/></td></tr>\n'
    html += '</table>'
    html += '</td>'
    html += '<td>'  # restrictions
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Max Bfactor</td><td><input type="text" size="6" name="maxb" value="' + maxb + '"/></td></tr>\n'
    html += '<tr><td>Occupant</td><td><input type="text" size="6" name="occ" value="' + occ + '"/></td></tr>\n'
    html += '<tr><td>Contact</td><td><input type="text" size="6" name="contact" value="' + contact + '"/></td></tr>\n'
    html += '<tr><td>Restriction</td><td><input type="text" size="6" name="restriction" value="' + restriction + '"/></td></tr>\n'
    # html += '</table>'

    in_checked = ''
    if in_set == '1':
        in_checked = ' checked="checked"'
    checked_checked = ''
    if checked_set == '1':
        checked_checked = ' checked="checked"'

    # html += '<table class="verdsearchtable">'
    html += '<tr><td><label for="hist">Include IN pdbs</label></td><td><input type="checkbox" id="in_set" name="in_set" value="1" ' + str(
        in_checked) + '"></td></tr>\n'
    html += '<tr><td><label for="hist">Include CHECKED pdbs</label></td><td><input type="checkbox" id="checked_set" name="checked_set" value="1" ' + str(
        checked_checked) + '"></td></tr>\n'
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

    html += '<td>'  # gradient choice
    html += '<table class="verdsearchtable"><tr><td>'

    amino_checked = ''
    if gradient == 'amino_code':
        amino_checked = ' checked="checked"'
    ss_checked = ''
    if gradient == 'ss_psu':
        ss_checked = ' checked="checked"'
    dssp_checked = ''
    if gradient == 'dssp':
        dssp_checked = ' checked="checked"'
    ref_checked = ''
    if gradient == 'refinement':
        ref_checked = ' checked="checked"'
    auth_checked = ''
    if gradient == 'institution':
        auth_checked = ' checked="checked"'
    pdb_checked = ''
    if gradient == 'g.pdb_code':
        pdb_checked = ' checked="checked"'
    res_checked = ''
    if gradient == 'resolution':
        res_checked = ' checked="checked"'
    no_checked = ''
    if gradient == 'amino_no':
        no_checked = ' checked="checked"'
    ch_checked = ''
    if gradient == 'chain':
        ch_checked = ' checked="checked"'

    html += '<input type="radio" id="amino_code" name="gradient" value="amino_code"' + amino_checked + '><label for="amino_code">Amino Code</label><br>'
    html += '<input type="radio" id="ss_psu" name="gradient" value="ss_psu"' + ss_checked + '><label for="ss_psu">Ramachandran Area</label><br>'
    html += '<input type="radio" id="dssp" name="gradient" value="dssp"' + dssp_checked + '><label for="dssp">SS DSSP</label><br>'
    html += '<input type="radio" id="refinement" name="gradient" value="refinement"' + ref_checked + '><label for="refinement">Refinement Software</label><br>'
    html += '<input type="radio" id="institution" name="gradient" value="institution"' + auth_checked + '><label for="institution">Authors</label><br>'
    html += '<input type="radio" id="pdb" name="gradient" value="g.pdb_code"' + pdb_checked + '><label for="pdb">PDB Codes</label><br>'
    html += '<input type="radio" id="resolution" name="gradient" value="resolution"' + res_checked + '><label for="resolution">Resolution</label><br>'
    html += '<input type="radio" id="chain" name="gradient" value="chain"' + ch_checked + '><label for="chain">Chain</label><br>'
    html += '<input type="radio" id="amino_no" name="gradient" value="amino_no"' + no_checked + '><label for="amino_no">Amino No</label><br>'

    html += '</td></tr></table>'
    html += '</td>'

    html += '</tr>'
    html += '<table>'
    html += "<tr><td><div class='buttondist'><input type='Submit' value='Show Validation Reports' formaction='/cgi-bin/cgiwrap/ab002/thesis_validation.cgi'/></div></td></tr>\n"
    html += '</table>'

    # close form
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


###################################################################################################################
def middleReturnValidation(dataframelist, reports, gradient):
    from matplotlib import cm
    html = ""
    html += "<table class='outtable'>\n"

    html = ts.middleReturnComment("Validation report on selection")

    # Can't use axes all the reports are on different measures
    # we need to create a dictionary of all possible gradient values
    # https://kite.com/python/answers/how-to-use-a-colormap-to-set-the-color-of-lines-in-a-matplotlib-line-graph-in-python
    gradients = {}
    isSS = False
    isDSSP = False
    for df in dataframelist:
        rows = len(df.index)
        if rows > 2:
            try:
                df['gradient'] = df['gradient'].astype('float')
            except:
                df['gradient'] = df['gradient']  # not numeric fine
            df = df.sort_values(by=['gradient'])
            grads = df.gradient.unique()

            if gradient == 'ss_psu':
                isSS = True
            elif gradient == 'dssp':
                isDSSP = True

            # if len(grads) > 2:
            #    if grads[0] == 'A' and grads[2] != 'C':  # we want the ss which are A etc BUT NOT chains which are ABCD
            #        isSS = True
            #    elif (grads[0] == 'B'or grads[0] == '-') and grads[2] != 'C':
            #        isDSSP = True

            for grad in grads:
                gradients[grad] = 'brown'

    evenly_spaced_interval = np.linspace(0, 1, len(gradients))
    colors = [cm.jet(x) for x in evenly_spaced_interval]

    # We create a shared legend area
    html += '<div class="greyparagraph">\n'
    html += '<p>Legend shared for all images</p>'
    if isSS:
        html += '<p>A very basic secondary structure assignment using the MSc Structural Bioinformatics course notes and a simple grid assignment from the Ramachandran plot.</p>'
    if isDSSP:
        html += '<p>Secondary Strcture implemented from DSSP, reference https://swift.cmbi.umcn.nl/gv/dssp/</p>'

    html += "<table>\n"

    ss_dict = {}
    if isSS:
        ss_dict['A'] = '=right-handed helix (inc. αR and 3-10)'
        ss_dict['B'] = '=ideal β-strand, parallel and anti-parallel β-sheet'
        ss_dict['P'] = '=named after the polyproline helix, but is also a common β-strand conformation '
        ss_dict['L'] = '=left-handed α-helix '
        ss_dict['G'] = '=left-handed glycine ‘helix’ '
        ss_dict['E'] = '=extended conformation of glycine'
        ss_dict['U'] = '=unknown'
    else:
        ss_dict['H'] = '=α-helix'
        ss_dict['B'] = '=residue in isolated β-bridge'
        ss_dict['E'] = '=extended strand, participates in β ladder'
        ss_dict['G'] = '=3-helix (310 helix)'
        ss_dict['I'] = '=5 helix (π-helix)'
        ss_dict['T'] = '=hydrogen bonded turn'
        ss_dict['S'] = '=bend'
        ss_dict['U'] = '=unknown'
        ss_dict['-'] = '=not calculated'

    i = 0
    for g in gradients:
        gradients[g] = colors[i]

        if i % 10 == 0:
            if i == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"

        html += '<td><div style="color:rgb'
        rgbcolours = [int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255)]

        html += '('
        html += str(rgbcolours[0]) + ','
        html += str(rgbcolours[1]) + ','
        html += str(rgbcolours[2])
        html += ')'

        if isSS or isDSSP:
            try:
                html += '">' + str(g) + str(ss_dict[g]) + '</div></td>'
            except:
                html += '">' + str(g) + '</div></td>'
        else:
            html += '">' + str(g) + '</div></td>'

        i += 1

    html += '</tr></table></div>'
    html += "<table class='outtable'>\n"
    count = 0

    # for r in reports:
    for df in dataframelist:
        if count % 4 == 0:
            if count == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"
        html += "<td>" + getOneValidation(df, gradients) + "</td>"
        count += 1

    html += "</tr>\n"
    html += "</table>\n"

    # print(html)

    return (html)


# ************************************************************************************************
def getOneValidation(df, gradients):
    """
    param: pdb code
    returns: html
    """
    html = ''
    # print("debug 1")

    html += tim.dataFrameToValidationReport(df, gradients)

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
