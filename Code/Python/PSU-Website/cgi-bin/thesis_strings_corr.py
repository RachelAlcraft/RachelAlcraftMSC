#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      30/05/2020
Function:  Strings specifically for the histogram pahe
Description:
============
There are a number of functions to produce code that follows a look and feel for the c++ pages
They may need to have cgi or htgetProbabilityDensityImageml path strings passed
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
import thesis_strings as ts
import thesis_sql as sqldb
import thesis_images as tim
import name_change as nc
import os, sys
import cgitb

cgitb.enable()


# ************************************************************************************************

def middleReturnCorrelation(sqldatas, gradient, scatter):
    """
    param: pdb code
    returns: html
    """

    gradient = nc.changeDBToViewMeasure(gradient)

    if scatter == "scatter":
        html = ts.middleReturnComment("Correlations, coloured on " + gradient)
    elif scatter == "trace":
        html = ts.middleReturnComment("Correlations, as a density trace")
    else:
        html = ts.middleReturnComment("Correlations, as a probability density plot")

    dfList = []
    for aa in sqldatas:
        dfList.append(sqldatas[aa].df)

    axes = tim.maxMinAxes(dfList, 'geox', 'geoy', 'double', 'double')

    grads = -1, -1
    try:
        grads = tim.maxMinAxis(dfList, "gradient", 'double')
    except:
        grads = -1, -1  # not numeric

    html += "<table class='outtable'>\n"
    count = 0
    for aa in sqldatas:
        if count % 4 == 0:
            if count == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"
        html += "<td>" + getOneCorrelation(sqldatas[aa].df, axes, sqldatas[aa].choices.calcx,
                                           sqldatas[aa].choices.calcy, sqldatas[aa].choices.set_name, aa,
                                           sqldatas[aa].choices.resolution, sqldatas[aa].choices.rvalue,
                                           sqldatas[aa].choices.rfree, scatter, gradient, grads) + "</td>"
        count += 1

    html += "</tr>\n"
    html += "</table>\n"

    return (html)


# ************************************************************************
def middleReturnScatter3d(sqldatas, gradient):
    """
    param: pdb code
    returns: html
    """

    comment = "Each row has 3 orientations for a single amino acid: x-y-x, y-z-x, z-x-y\n"

    comment += "Graduated on " + gradient

    html = ts.middleReturnComment(comment)

    dfList = []
    for aa in sqldatas:
        dfList.append(sqldatas[aa].df)

    axesX = tim.maxMinAxis(dfList, 'geox', 'double')
    axesY = tim.maxMinAxis(dfList, 'geoy', 'double')
    axesZ = tim.maxMinAxis(dfList, 'geoz', 'double')

    # html += str(axes[0]) + ":" + str(axes[1]) + ":" + str(axes[2]) + ":" + str(axes[3])
    html += "<table class='outtable'>\n"
    count = 0
    for aa in sqldatas:
        if count % 1 == 0:
            if count == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"
        html += getOneCorrelation3d(sqldatas[aa].df, axesX, axesY, axesZ, sqldatas[aa].choices.calcx,
                                    sqldatas[aa].choices.calcy, sqldatas[aa].choices.calcz,
                                    sqldatas[aa].choices.set_name, aa)
        count += 1

    html += "</tr>\n"
    html += "</table>\n"

    return (html)


# ******************************************************************************************

def getDfCorrelation(calcX, calcY, maxb, set_name, restriction, gradient, amino_code, res, rval, rfree, resL, rvalueL,
                     rfreeL):
    """
    param: sql
    returns: df
    """
    sql = ""

    sql = sqldb.sqlForCorrOpt(calcX, calcY, maxb, set_name, restriction, gradient, amino_code, res, rval, rfree, resL,
                              rvalueL, rfreeL)

    try:  # calling the database
        dfaa = sdb.read_sql(sql)
    except:
        dfaa = pd.read_csv(sio(amino_code + ", no data"))
    return dfaa


# ******************************************************************************************
def getDf3d(sql, amino_code):
    """
    param: sql
    returns: df
    """

    try:  # calling the database
        dfaa = sdb.read_sql(sql)
    except:
        dfaa = pd.read_csv(sio(amino_code + ", no data"))
    return dfaa


# ******************************************************************************************

def getOneCorrelation(dfaa, axes, calcX, calcY, set_name, amino_code, res, rval, rfree, scatter, gradient, grads):
    """
    param: pdb code
    returns: html
    """
    html = ""
    html += dataFrameToScatter(dfaa, axes, calcX, calcY, set_name, amino_code, scatter, gradient, grads)
    return (html)


# ************************************************************************************************
def getOneCorrelation3d(dfaa, axesX, axesY, axesZ, calcX, calcY, calcZ, set_name, amino_code):
    """
    param: pdb code
    returns: html
    """
    html = ""
    html += dataFrameToScatter3d(dfaa, axesX, axesY, axesZ, calcX, calcY, calcZ, set_name, amino_code)
    return (html)


# ******************************************************************************************
def dataFrameToScatter(df, axes, calcX, calcY, set_name, amino_code, scatter, gradient, grads):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    Resource used:
    https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly
    https://pythonspot.com/matplotlib-scatterplot/
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_custom_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-custom-symbol-py
    """
    import io
    import base64
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import cm as CM
    from scipy.stats import kde
    import numpy as np

    plt.style.use('seaborn-whitegrid')

    rows = len(df.index)
    html = ""

    if rows > 2:

        # fig, ax = plt.subplots()

        # plt.axis([axes[0],axes[1],axes[2],axes[3]])

        df['geox'] = df['geox'].astype('float')
        df['geoy'] = df['geoy'].astype('float')
        # sort by resolution as the higher res are rarer and meaningful
        colourmap = 'viridis_r'

        # if gradient is dssp then we know what we want
        if scatter == "scatter":

            if gradient == 'dssp':

                df['gradient'] = df['gradient']  # it may actually not be resolution but anything

                colourmap = 'nipy_spectral_r'
                colourmap = 'Set1_r'

                vals = ['U', 'H', 'S', 'G', 'E', '-', 'T', 'B', 'I']
                valnames = ['U:Unknown', 'H:a-helix', 'S:bend', 'G:3-helix', 'E:extended strand', '-:Missing',
                            'T:h-bond turn', 'B:isolated b-bridge', 'I:5-helix']

                v = 0
                html += "key:"
                for val in vals:
                    html += str(v)
                    html += "="
                    html += str(valnames[v])
                    html += " "
                    try:
                        df.loc[df.gradient == val, 'gradient'] = v
                    except:
                        msg = 'there are none, fine'
                    v += 1


            else:
                try:
                    df['gradient'] = df['gradient'].astype('float')
                    df = df.sort_values(by='gradient', ascending=False)

                except:
                    df['gradient'] = df['gradient']  # it may actually not be resolution but anything
                    vals = df['gradient'].unique()
                    v = 0
                    html += "key:"
                    for val in vals:
                        # df['gradient'][df['gradient']== val] = v #https://www.dataquest.io/blog/settingwithcopywarning/
                        html += val + "=" + str(v) + " "
                        df.loc[df.gradient == val, 'gradient'] = v
                        v += 1

        x = df['geox']
        y = df['geoy']
        z = df['gradient']

        rows = len(df.index)

        title = amino_code + " obs=" + str(rows)

        if scatter == "scatter":
            encoded = tim.getScatterPlotImage(x, y, z, axes, calcX, calcY, title, colourmap, grads)
        elif scatter == "trace":
            encoded = tim.getScatterPlotImage(x, y, z, axes, calcX, calcY, title, 'none', (-1, -1))
        else:
            encoded = tim.getProbabilityDensityImage(x, y, axes, calcX, calcY, title, CM.GnBu, False, None, 90, False,
                                                     0, 0)

        html += '<img width = 95% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
    else:
        html += '<p>' + amino_code + ' No data</p>'

    return (html)


# *******************************************************************************
def dataFrameToScatter3d(df, axesX, axesY, axesZ, calcX, calcY, calcZ, set_name, amino_code):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    Resource used:
    https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly
    https://pythonspot.com/matplotlib-scatterplot/
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_custom_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-custom-symbol-py
    """

    rows = len(df.index)

    html = ""

    if rows > 2:
        df['geox'] = df['geox'].astype('float')
        df['geoy'] = df['geoy'].astype('float')
        df['geoz'] = df['geoz'].astype('float')
        # sort by resolution as the higher res are rarer and meaningful
        try:
            df['gradient'] = df['gradient'].astype('float')
            df = df.sort_values(by='gradient', ascending=False)

        except:
            df['gradient'] = df['gradient']  # it may actually not be resolution but anything
            vals = df['gradient'].unique()
            v = 0
            html += "key:"
            for val in vals:
                # df['gradient'][df['gradient']== val] = v #https://www.dataquest.io/blog/settingwithcopywarning/
                html += val + "=" + str(v) + " "
                df.loc[df.gradient == val, 'gradient'] = v
                v += 1

        df = df.sort_values(by='gradient', ascending=False)

        x = df['geox']
        y = df['geoy']
        z = df['geoz']
        c = df['gradient']

        rows = len(df.index)

        title = amino_code + " obs=" + str(rows)

        # html += title

        encodedX = tim.getScatter3dImage(x, y, z, c, axesX, axesY, axesZ, calcX, calcY, calcZ, title, 'viridis_r')
        encodedY = tim.getScatter3dImage(y, z, x, c, axesY, axesZ, axesX, calcY, calcZ, calcX, title, 'viridis_r')
        encodedZ = tim.getScatter3dImage(z, x, y, c, axesZ, axesX, axesY, calcZ, calcX, calcY, title, 'viridis_r')

        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedX.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedY.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedZ.decode('utf-8'))
    else:
        html += '<p>' + amino_code + ' No data</p>'

    return (html)
