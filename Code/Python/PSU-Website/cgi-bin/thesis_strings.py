#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  This is the main file for producing all html strings in the look and feel of the thesis pages
Description:
============
There are a number of functions to produce code that follows a look and feel for the c++ pages
They may need to have cgi or html path strings passed
A page can be assembled by these strings easily in either CGI or a script to create the pages
"""

# ************************************************************************************************

# import runCpp as cpp;
import pandas as pd
import matplotlib
from io import StringIO as sio
import thesis_read_database as tdb
import thesis_read_databaseJ as tdbj
import thesis_read_db_simple as sdb
import thesis_geo as calc
import thesis_images as tim
import os, sys
import cgitb

cgitb.enable()


# ************************************************************************************************

def header(html_path):
    """
    param: html_path the relative path for html strings
    returns: The header html string
    """
    html = '<!DOCTYPE html>\n'
    html += '<html lang="en">\n'
    html += '<head>\n'
    html += '<link rel="icon" href="' + html_path + 'img/c9.png"><title>Rachel Alcraft</title>\n'
    html += '<link type="text/css" rel="stylesheet" href="' + html_path + 'css/thesis.css">\n'
    html += '</head>\n'
    return (html)


# ************************************************************************************************

def menuBar(html_path):
    """
    param: html_path the relative path for html strings
    returns: The menu bar, home page style
    """
    html = '<body>\n'
    html += '<div id="top-menu">\n'
    html += '<div class="table">\n'
    html += '<ul id="horizontal-list">\n'
    html += '<li><a href="http://www.bbk.ac.uk/" target="_blank"><img src="' + html_path + 'img/bbk.png" width="100" alt=""/></a></li>\n'
    html += '<li><a href="' + html_path + 'index.html"><img src="' + html_path + 'img/home.png" width="100" alt="home" /></a></li>\n'
    html += '<li><a href="' + html_path + 'Chme9.html"><img src="' + html_path + 'img/chme9.png" width="100" alt="chme9" /></a></li>\n'
    html += '<li><a href="' + html_path + 'cpp.html"><img src="' + html_path + 'img/cpp.png" width="100" alt="C++" /></a></li>\n'
    html += '<li><a href="' + html_path + 'thesis.html"><img src="' + html_path + 'img/project.png" width="100" alt="C++" /></a></li>\n'
    html += '<li><a href="http://www.bbk.ac.uk/" target="_blank"><img src="' + html_path + 'img/bbk.png" width="100" alt=""/></a></li>\n'
    html += '</ul>\n'
    html += '</div>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************
def intraMenuBar(html_path):
    """
    param: html_path the relative path for html strings
    returns: The second menu bar, home page style
    """
    html = '<div id="two-menu">\n'
    html += '<div class="table_two">\n'
    html += '<ul id="horizontal_two">\n'
    html += '<li><a href="' + html_path + 'thesis.html"><img src="' + html_path + 'img/project.png" width="100" alt="C++" /></a></li>\n'
    html += '</ul>\n'
    html += '</div>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleDescription(html_path):
    """
    param: none
    returns: Some personal info, html formatted
    """
    html = '<h1>\n'
    #html += 'Rachel Alcraft MSc Project\n'
    html += 'Protein Structure Utility : PSU-View\n'
    html += '</h1>\n'
    html += '<div class="thesisheader">\n'
    html += '<span>'
    html += '<a href="' + html_path + 'thesis.html" title="Home" target="_self">Home</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<span>'
    html += '<a href="' + html_path + 'data.html" title="Help" target="_self">Help</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<a href="' + html_path + 'contact.html" title="ContactMap" target="_self">Contact Maps</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<a href="' + html_path + 'distributions.html" title="Distributions" target="_self">Distributions</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<a href="' + html_path + 'resolution.html" title="Resolution" target="_self">Resolution</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<a href="' + html_path + 'validation.html" title="Correlations" target="_self">Correlations</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<a href="' + html_path + 'database.html" title="Database" target="_self">Database</a>\n'
    html += '</span>'
    html += '<span>'
    html += " ~ "
    html += '</span>'
    html += '<span>'
    html += '<a href="' + html_path + 'calc.html" title="GeoCalc" target="_self">Geo Calculator</a>\n'
    html += '</span>'
    html += '</div>\n'
    html += '<hr/>\n'
    html += '<div class="middle"><p>\n'
    html += 'This is a student project for the Birkbeck College MSc Bioinformatics and Systems Biology, 2019/2020\n'
    html += '</p></div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleContactRequest(pdb):
    """
    param: pdb code
    returns: The box for the contact report request
    """
    html = middleReturnComment("Choose a pdb code for SG-SG and N-O Contact Maps")
    html += '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_contact.cgi" accept-charset="UTF-8">\n'
    html += '<div class="smallmiddle">\n'
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Pdb Code</td><td><input type="text" name="pdb" value="' + pdb + '"/></td></tr>\n'
    html += '</table>'
    html += "<p><input type='Submit' value='Create Contact Maps' formaction='/cgi-bin/cgiwrap/ab002/thesis_contact.cgi'/></p>\n"

    # close form
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleTestThesis(calcs, pdb, amino, occupant, setname, sql):
    """
    param: none
    returns: The secret SQL box
    """
    html = '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_datastring.cgi" accept-charset="UTF-8">\n'
    # html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_database.cgi" accept-charset="UTF-8">\n'

    html += '<div class="smallmiddle">\n'
    html += '<table class="searchtable">'
    html += '<tr class="searchheader"><td>Choose pre-calculated geometric measures</td></tr>'
    html += '<tr>'
    html += '<td>'
    html += 'E.g.<br/>Backbone bond lengths: N-CA, CA-C<br/>\n'
    html += 'Phi=CP-N-CA-C<br/>a\n'
    html += 'Psi=N-CA-C-NPP<br/>\n'
    html += 'Omega=CA-C-NPP-CAPP<br/>\n'
    html += 'C-alpha angles before and next: CAP-CA-CAPP<br/>\n'
    html += 'Distance between N-O 3 residues apart: O-NPP4<br/>\n'
    html += 'Intra residue 1-4 backbone: CB-O, N-O<br/>\n'
    html += '</td>'
    html += '<td><TEXTAREA rows=6 cols=20 name="choices">' + calcs + '</TEXTAREA></td>\n'
    html += '</tr>'
    html += '<tr class="searchheader"><td>Enter optional restraints on your selection</td></tr>\n'
    html += '<tr><td>Pdb Code</td><td><input type="text" name="pdb" value="' + pdb + '"/></td></tr>\n'
    html += "<tr><td>Amino Acid</td><td><input type='text' name='amino' value='" + amino + "'/></td></tr>\n"
    html += "<tr><td>Occupant</td><td><input type='text' name='occupant' value='" + occupant + "'/></td></tr>\n"
    html += "<tr><td>Set Name</td><td><input type='text' name='setname' value='" + setname + "'/></td></tr>\n"
    html += '</table>'
    html += "<p><input type='Submit' value='Generate sql' formaction='/cgi-bin/cgiwrap/ab002/thesis_datastring.cgi'/></p>\n"

    # optionally include the sql output that can be edited
    if sql != '':
        html += middleReturnComment("SQL for the query")

        html += '<p><TEXTAREA rows=10 cols=100 name="sql">' + sql + '</TEXTAREA></p>\n'
        html += "<p><span>Enter password</span><span><input type='text' name='password'/></span></p>\n"
        html += '</table>'
        html += "<p><input type='Submit' value='Execute query' formaction='/cgi-bin/cgiwrap/ab002/thesis_database.cgi'/></p>\n"

        # close form either way
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleSqlOnly(sql):
    """
    param: none
    returns: The secret SQL box
    """
    html = '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_datastring.cgi" accept-charset="UTF-8">\n'

    # optionally include the sql output that can be edited
    if sql != '':
        html += middleReturnComment("SQL for the query")

        html += '<p><TEXTAREA rows=10 cols=100 name="sql">' + sql + '</TEXTAREA></p>\n'
        html += "<p><span>Enter password</span><span><input type='text' name='password'/></span></p>\n"
        html += '</table>'
        html += "<p><input type='Submit' value='Execute query' formaction='/cgi-bin/cgiwrap/ab002/thesis_database.cgi'/></p>\n"

        # close form either way
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************
def middleCalculator(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    """
    param: none
    returns: The secret SQL box
    """
    html = '<div class="middle">\n'
    html += '<p>Enter 2-4 atoms coordinates to validate and verify geometric calculations</p>\n'
    html += '<div class="smallmiddle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_distance.cgi" accept-charset="UTF-8">\n'
    html += '<table class="calctable">'
    html += "<tr class='calcinnerheader'>\n"
    html += "<td></td>"
    html += "<td>x</td>"
    html += "<td>y</td>"
    html += "<td>z</td>"
    html += '</tr>'
    html += '<tr class="calcnnertable">'
    html += "<td>Atom 1</td>"
    html += "<td><input type='text' name='x1' value='" + x1 + "'/></td>\n"
    html += "<td><input type='text' name='y1' value='" + y1 + "'/></td>\n"
    html += "<td><input type='text' name='z1' value='" + z1 + "'/></td>\n"
    html += '</tr>'
    html += '<tr class="calcinnertable">'
    html += "<td>Atom 2</td>"
    html += "<td><input type='text' name='x2' value='" + x2 + "'/></td>\n"
    html += "<td><input type='text' name='y2' value='" + y2 + "'/></td>\n"
    html += "<td><input type='text' name='z2' value='" + z2 + "'/></td>\n"
    html += '</tr>'
    html += '<tr class="calcinnertable">'
    html += "<td>Atom 3</td>"
    html += "<td><input type='text' name='x3' value='" + x3 + "'/></td>\n"
    html += "<td><input type='text' name='y3' value='" + y3 + "'/></td>\n"
    html += "<td><input type='text' name='z3' value='" + z3 + "'/></td>\n"
    html += '</tr>'
    html += '<tr class="calcinnertable">'
    html += "<td>Atom 4</td>"
    html += "<td><input type='text' name='x4' value='" + x4 + "'/></td>\n"
    html += "<td><input type='text' name='y4' value='" + y4 + "'/></td>\n"
    html += "<td><input type='text' name='z4' value='" + z4 + "'/></td>\n"
    html += '</tr>'
    html += '</table>'
    html += "<p class='button'><input type='Submit' value='Calculate geometry'/></p>\n"
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************
def middleReturnCalc(dcalc, acalc, tcalc):
    """
    param: none
    returns: The secret SQL box
    """
    html = '<div class="middle">\n'
    html += '<p>Calculations results</p>\n'
    html += '<div class="smallmiddle">\n'
    html += '<table class="calctable">'
    html += "<tr class='calcinnerheader'>\n"
    html += "<td>Distance</td>"
    html += "<td>Angle</td>"
    html += "<td>Torsion</td>"
    html += '</tr>'
    html += '<tr>'
    html += "<td>" + dcalc + "</td>"
    html += "<td>" + acalc + "</td>"
    html += "<td>" + tcalc + "</td>"
    html += '</tr>'
    html += '</table>'
    html += '</div>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleReturnThesis(dataInput):
    """
    param: datainput - the results from the text box
    returns: the results from the exe in a grid
    """

    try:  # calling the database
        df = tdb.read_sql(dataInput)
    except:
        df = pd.read_csv(sio("Error calling database,,"))

    # now create the html output
    html = '<hr/>\n'
    html += '<div class="results">\n'
    html += dataFrameToCSV(df)

    return (html)


# ************************************************************************************************
def getSQL(dataInput, rest_col, rest_val, amino, pdb, occupant):
    # input data to list
    calcs = dataInput.split()
    sql = ''
    if len(calcs) == 1:
        sql = tdb.make_sqlstringA(calcs[0], rest_col, rest_val, amino, pdb, occupant)
    elif len(calcs) == 2:
        sql = tdb.make_sqlstringB(calcs[0], calcs[1], rest_col, rest_val, amino, pdb, occupant)
    elif len(calcs) == 3:
        sql = tdb.make_sqlstringC(calcs[0], calcs[1], calcs[2], rest_col, rest_val, amino, pdb, occupant)
    else:  # len(calcs) == 4:
        sql = tdb.make_sqlstringD(calcs[0], calcs[1], calcs[2], calcs[3], rest_col, rest_val, amino, pdb, occupant)
    return (sql)


def getSQLJ(dataInput, aa, occ, pdb, status, letNull):
    # input data to list
    calcs = dataInput.split()
    sql = tdbj.createSql(calcs, aa, occ, pdb, status, False)
    # sql = sdb.createSql(calcs, aa, occ, pdb, status, False)
    return (sql)


# ********************************************************************

def getSQLContact(pdb, contact_atoms):
    # input data to list
    sql = tdbj.createSqlContacts(pdb, contact_atoms)
    return (sql)


# ********************************************************************
def getCalcDistance(x1, y1, z1, x2, y2, z2):
    """
    param: coordinates of atoms
    returns: calculation for distance
    """
    return (calc.distance(x1, y1, z1, x2, y2, z2))


# ********************************************************************
def getCalcAngle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """
    param: coordinates of atoms
    returns: calculation for angle
    """
    return (calc.angle(x1, y1, z1, x2, y2, z2, x3, y3, z3))


# ********************************************************************
def getCalcTorsion(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    """
    param: coordinates of atoms
    returns: calculation for torsion
    """
    return (calc.torsion(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4))


# ************************************************************************************************

def middleReturnComment(comment):
    """
    param: datainput - a comment to make in the html
    returns the html for the comment
    """
    # now create the html output
    # html = '<hr/>\n'
    html = '<div class="banner">\n'
    html += '<p>\n'
    html += comment
    html += '</p>\n'
    html += '</div>\n'
    return (html)


# ************************************************************************************************
def middleReturnSQL(sql):
    """
    param: datainput - the results from the text box
    returns: the proposed sql query
    """

    html = middleReturnComment("SQL for the query")

    html += '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_database.cgi" accept-charset="UTF-8">\n'
    html += '<p><TEXTAREA rows=10 cols=100 name="sql">' + sql + '</TEXTAREA></p>\n'
    html += "<p><span>Enter password</span><span><input type='text' name='password'/></span></p>\n"
    html += '</table>'
    html += "<p><input type='Submit' value='Execute query' /></p>\n"
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************
def middleReturnSearch(sql):
    """
    param: datainput - the results from the text box
    returns: the results from the exe in a grid
    """

    try:  # calling the database
        # df = tdb.read_sql(sql)
        df = sdb.read_sql(sql)
        # df = tdb.read_sql('')
    except:
        df = pd.read_csv(sio("Error calling database,,"))

    # now create the html output
    html = middleReturnComment("Grid View of Data")
    html += dataFrameToGrid(df)
    html += '<hr/>\n'

    html += middleReturnComment("CSV View of Data")
    html += '<div class="results">\n'
    html += dataFrameToCSV(df)
    html += '<hr/>\n'

    # html += middleReturnComment("SQL used for the query")
    # html += '<div class="sqlresults"><p><textarea rows=10 cols=100>' + sql + '</textarea></div></p>\n'
    # html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def middleReturnContact(pdb, sqlsg, sqlno, sqlca, sqlcb):
    """
    param: datainput - the results from the text box
    returns: the results from the exe in a grid
    """
    html = ""
    hasSG = True
    hasNO = True
    hasCA = True
    hasCB = True

    dfList = []

    try:  # SG-SG calling the database
        dfsg = sdb.read_sql(sqlsg)
        hasSG = True
        dfList.append(dfsg)
    except:
        dfsg = pd.read_csv(sio("Error, no data"))
        hasSG = False

    try:  # N-O calling the database
        dfno = sdb.read_sql(sqlno)
        hasNO = True
        dfList.append(dfno)
    except:
        dfno = pd.read_csv(sio("Error, no data"))
        hasNO = False

    try:  # CA-CA calling the database
        dfca = sdb.read_sql(sqlca)
        hasCA = True
        dfList.append(dfno)
    except:
        dfca = pd.read_csv(sio("Error, no data"))
        hasCA = False

    try:  # CB-CB calling the database
        dfcb = sdb.read_sql(sqlcb)
        hasCB = True
        dfList.append(dfcb)
    except:
        dfcb = pd.read_csv(sio("Error, no data"))
        hasCB = False

    axes = tim.maxMinAxes(dfList, 'residue_no', 'residue_no_b', 'int', 'int')

    # html += str(axes[0]) + ":"+ str(axes[1]) + ":" + str(axes[2]) + ":" +str(axes[3])

    # Add in images
    html += middleReturnComment(pdb + " Contacts")
    html += "<table><tr>"
    html += "<td>SG-SG Contact Map</td>"
    html += "<td>N-O Contact Map</td>"
    html += "<td>CA-CA Contact Map</td>"
    html += "<td>CB-CB Contact Map</td>"
    html += "</tr><tr>"

    # Blob plots
    html += "<td>"
    if hasSG:
        html += tim.dataFrameToContactImage(dfsg, 'SG', 'SG', pdb, axes, False)
    html += "</td>"

    html += "<td>"
    if hasNO:
        html += tim.dataFrameToContactImage(dfno, 'N', 'O', pdb, axes, False)
    html += "</td>"

    html += "<td>"
    if hasCA:
        html += tim.dataFrameToContactImage(dfca, 'CA', 'CA', pdb, axes, False)
    html += "</td>"

    html += "<td>"
    if hasCB:
        html += tim.dataFrameToContactImage(dfcb, 'CB', 'CB', pdb, axes, False)
    html += "</td>"

    # Same but as dots
    '''
    html += "</tr><tr>"
    html += "<td>"
    if hasSG:
        html += tim.dataFrameToContactImage(dfsg,'SG','SG',pdb,axes,True)
    html += "</td>"

    html += "<td>"
    if hasNO:
        html += tim.dataFrameToContactImage(dfno,'N','O',pdb,axes,True)
    html += "</td>"

    html += "<td>"
    if hasCA:
        html += tim.dataFrameToContactImage(dfca,'CA','CA',pdb,axes,True)
    html += "</td>"

    html += "<td>"
    if hasCB:
        html += tim.dataFrameToContactImage(dfcb,'CB','CB',pdb,axes,True)
    html += "</td>"

    '''
    html += "</tr></table>"
    html += '<hr/>\n'

    # Add in the SG-SG data
    html += middleReturnComment(pdb + " SG-SG Data")
    html += dataFrameToGridVeridia(dfsg)
    html += '<hr/>\n'
    if hasSG:
        html += middleReturnComment(pdb + " SG-SG Csv")
        html += '<div class="results">\n'
        html += dataFrameToCSV(dfsg)
        # html += dataFrameToSQL(sqlsg)
        html += '<hr/>\n'

    # Add in the N-O data
    html += middleReturnComment(pdb + " N-O Data")
    html += dataFrameToGridVeridia(dfno)
    html += '<hr/>\n'
    if hasNO:
        html += middleReturnComment(pdb + " N-O Csv")
        html += '<div class="results">\n'
        html += dataFrameToCSV(dfno)
        # html += dataFrameToSQL(sqlno)
        html += '<hr/>\n'

    # Add in the CA-CA data
    html += middleReturnComment(pdb + " CA-CA Data")
    html += dataFrameToGridVeridia(dfca)
    html += '<hr/>\n'
    if hasCA:
        html += middleReturnComment(pdb + " CA-CA Csv")
        html += '<div class="results">\n'
        html += dataFrameToCSV(dfca)
        # html += dataFrameToSQL(sqlno)
        html += '<hr/>\n'

    # Add in the CB-CB data
    html += middleReturnComment(pdb + " CB-CB Data")
    html += dataFrameToGridVeridia(dfcb)
    html += '<hr/>\n'
    if hasNO:
        html += middleReturnComment(pdb + " CB-CB Csv")
        html += '<div class="results">\n'
        html += dataFrameToCSV(dfcb)
        # html += dataFrameToSQL(sqlno)
        html += '<hr/>\n'

    return (html)


# ************************************************************************************************
def middleReturnError(msg):
    """
    param: datainput - the results from the text box
    returns: an error message by return
    """
    # now create the html output
    # html = '<hr/>\n'
    html = '<div class="middle">\n'
    html += '<p>\n'
    html += ' You have entered invalid data, have you forgotten the password?<br/>'
    html += msg
    html += '</p>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)


# ************************************************************************************************

def footer():
    """
    param: none
    returns: footer home page style
    """
    html = '<div id="bottom">\n'
    html += '<p>\n'
    html += 'Created by: Rachel Alcraft<br/>\n'
    html += '<a href="http://mscb.cryst.bbk.ac.uk/" title="MScBio" target="_blank">Birkbeck MSc Bioinformatics 2019/2020</a>\n'
    html += '</p>\n'
    html += '</div>\n'
    html += '</body>\n'
    return (html)


# ************************************************************************************************
def dataFrameToGrid(df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    cols = len(df.columns)
    rows = len(df.index)
    html = "<table class='cpptable'>\n"
    html += "<tr class='cppinnerheader'>\n"
    for col in df.columns:
        html += "<td>" + col + "</td>\n"
    html += "</tr>\n"

    for c in range(0, rows):
        html += "<tr class='cppinnertable'>\n"
        for r in range(0, cols):
            html += "<td>" + str((df.iloc[c, r])) + "</td>\n"
        html += "</tr>\n"
    html += "</table>\n"
    return (html)


def dataFrameToGridVeridia(df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    cols = len(df.columns)
    rows = len(df.index)
    html = "<table class='verdtable'>\n"
    html += "<tr class='verdinnerheader'>\n"
    for col in df.columns:
        html += "<td>" + col + "</td>\n"
    html += "</tr>\n"

    for c in range(0, rows):
        html += "<tr class='cppinnertable'>\n"
        for r in range(0, cols):
            html += "<td>" + str((df.iloc[c, r])) + "</td>\n"
        html += "</tr>\n"
    html += "</table>\n"
    return (html)


def dataFrameToCSV(df):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    cols = len(df.columns)
    rows = len(df.index)
    # html = '<div class="middle">\n'
    html = "<p>\n"
    html += '<TEXTAREA rows=10 cols=100>'
    # html += "<pre>\n"
    colhtml = ''
    for col in df.columns:
        colhtml += col + ","
    colhtml = colhtml[:-1]

    html += colhtml + "\n"

    for c in range(0, rows):
        rowhtml = ''
        for r in range(0, cols):
            rowhtml += str((df.iloc[c, r])) + ","
        rowhtml = rowhtml[:-1]
        html += rowhtml + "\n"
        # html+= "</pre>\n"
    html += '</TEXTAREA>'
    html += "</p>\n"
    # html+= "</div>\n"
    return (html)


def dataFrameToSQL(sql):
    """
    param: df - data in a dataframe object
    returns: the df formatted into an html grid
    """
    # html = '<div class="middle">\n'
    html = "<p>\n"
    html += '<TEXTAREA rows=10 cols=100>'
    html += sql
    html += '</TEXTAREA>'
    html += "</p>\n"
    # html+= "</div>\n"
    return (html)
