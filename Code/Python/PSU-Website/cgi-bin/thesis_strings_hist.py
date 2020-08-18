#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      30/05/2020
Function:  Strings specifically for the histogram pahe
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
import thesis_sql as sqldb
import thesis_strings as ts
import thesis_images as tim
import os, sys
import cgitb

cgitb.enable()

global_stats = []  # global list to acccumulate distributions


# ************************************************************************************************

# def middleReturnHistogram(calc,set_name,maxb,restriction,amino_code, res,rvalue,rfree,resL,rvalueL,rfreeL):
def middleReturnHistogram(sqldatas):
    html = ""
    html += "<table class='outtable'>\n"

    global_stats.append(
        "geo_measure,amino_code,resolution,r_value,r_free,mean,s_d,skew,kurtosis,normality,observations")
    comment = "Histograms per amino acid, with the top 2 and bottom 2 outliers, and "
    comment += "mean, sd and normality (tested by Shapiro-Wilk at 5%)"
    html = ts.middleReturnComment(comment)

    dfList = []

    for aa in sqldatas:
        dfList.append(sqldatas[aa].df)

    axes = tim.maxMinAxes(dfList, 'geox', '', 'double', '')

    html += "<table class='outtable'>\n"

    count = 0
    for aa in sqldatas:
        if count % 4 == 0:
            if count == 0:
                html += "<tr>\n"
            else:
                html += "</tr><tr>\n"
        html += "<td>" + getOneHistogram(sqldatas[aa].df, axes, sqldatas[aa].choices.calcx,
                                         sqldatas[aa].choices.set_name, aa, sqldatas[aa].choices.resolution[0],
                                         sqldatas[aa].choices.rvalue[0], sqldatas[aa].choices.rfree[0], "yes") + "</td>"
        count += 1

    html += "</tr>\n"
    html += "</table>\n"

    html += ts.middleReturnComment("Summary of the distributions")
    html += "<p><textarea rows=10 cols=100>"
    for stat in global_stats:
        html += stat + "\n"
    html += "</textarea></p>"

    return (html)


# ******************************************************************************************
def getDfHistSql(calc, set_name, maxb, amino_code, restriction, res, rval, rfree, resL, rvalueL, rfreeL):
    sql = ''
    if "C@" in calc:  # then this is a contact distribution
        calc = calc[2:]
        sql = sqldb.sqlForHistContact(calc, set_name, maxb, amino_code, restriction, res, rval, rfree, resL, rvalueL,
                                      rfreeL)
    else:
        sql = sqldb.sqlForHistOpt(calc, set_name, maxb, amino_code, restriction, res, rval, rfree, resL, rvalueL,
                                  rfreeL)

    return (sql)


def getDfHist(sql, amino_code):
    try:  # calling the database
        dfaa = sdb.read_sql(sql)
    except:
        dfaa = pd.read_csv(sio(amino_code + ", no data"))
    return (dfaa)


# ************************************************************************************************
def getOneHistogram(dfaa, axes, calc, set_name, amino_code, res, rval, rfree, opt):
    """
    param: pdb code
    returns: html
    """

    html = dataFrameToHist(dfaa, axes, calc, set_name, amino_code)
    # box = dataFrameToBoxPlot(dfaa,axes, calc,set_name, amino_code)
    # html += "<div><p>"
    outs = dataFrameToOutliers(dfaa)
    stats = dataFrameToStats(dfaa, amino_code, calc, res, rval, rfree)
    # html += box

    html += "<table class='outintable'><tr><td>"
    html += outs
    html += "</td></tr><tr><td>"
    html += stats
    html += "</td></tr></table>"

    # html += dataFrameToData(dfaa)

    return (html)


# ************************************************************************************************

def dataFrameToData(df):
    html = "<textarea>"
    rows = len(df.index)
    for r in range(0, rows):
        html += str((df.iloc[r, 1])) + ","
    html += "</textarea>"
    return (html)


# ************************************************************************************************

def dataFrameToStats(df, aa, calc, res, rval, rfree):
    """
    Resources:
    https://machinelearningmastery.com/a-gentle-introduction-to-normality-tests-in-python/
    https://pythontic.com/numpy/ndarray/mean_std_var
    """
    from scipy.stats import shapiro
    from scipy.stats import normaltest
    from scipy.stats import skew
    from scipy.stats import kurtosis

    rows = len(df.index)
    html = ""

    stats_string = calc + "," + aa + "," + res + "," + rval + "," + rfree + ","

    if rows > 8:
        df['geox'] = df['geox'].astype('float')

        vals = df['geox'].values

        mean = round(vals.mean(), 3)
        sd = round(vals.std(), 3)
        sk = round(skew(vals), 3)
        kr = round(kurtosis(vals), 3)

        alpha = 0.05

        stats_string += str(mean) + "," + str(sd) + "," + str(sk) + "," + str(kr) + ","

        html += "<table>"
        html += "<tr class='outinnerheader'><td>Stats measure</td><td>Value</td></tr>"
        html += "<tr class='outinnertable'><td>mean</td><td>" + str(mean) + "</td></tr>"
        html += "<tr class='outinnertable'><td>s.d</td><td>" + str(sd) + "</td></tr>"
        html += "<tr class='outinnertable'><td>skew</td><td>" + str(sk) + "</td></tr>"
        html += "<tr class='outinnertable'><td>kurtosis</td><td>" + str(kr) + "</td></tr>"
        # html += "</td>"

        stat, p = shapiro(vals)

        if p > alpha:
            html += "<tr class='outinnertable'><td>Normal</td><td>True (p = " + str(round(p, 5)) + ")</td></tr>"
            stats_string += "1"
        else:
            html += "<tr class='outinnertable'><td>Normal</td><td>False (p = " + str(round(p, 5)) + ")</td></tr>"
            stats_string += "0"

        # stat, p = normaltest(vals)

        # if p > alpha:
        #    html += "<tr><td>skew normal =</td><td>True (p = " + str(round(p,5))+ ")</td></tr>"
        # else:
        #    html += "<tr><td>skew normal =</td><td>False (p = " + str(round(p,5))+ ")</td></tr>"

        html += "</table>"
        stats_string += "," + str(rows)
        global_stats.append(stats_string)

    else:
        html = ""

    return (html)


# ************************************************************************************************

def dataFrameToOutliers(df):
    outrows = 0
    rows = len(df.index)
    if rows > 3:
        outrows = 4
        out = df.iloc[[0, 1, -2, -1]]
    elif rows > 1:
        outrows = 2
        out = df.iloc[[0, -1]]

    if outrows > 0:

        out = out[['aminos', 'atoms', 'geox', 'pdb_code']]

        cols = len(out.columns)
        rows = len(out.index)
        html = "<table>\n"
        html += "<tr class='outinnerheader'>\n"
        for col in out.columns:
            html += "<td>" + col + "</td>\n"
        html += "</tr>\n"

        for c in range(0, rows):
            html += "<tr class='outinnertable'>\n"
            for r in range(0, cols):
                html += "<td>" + str((out.iloc[c, r])) + "</td>\n"
            html += "</tr>\n"
        html += "</table>\n"
    else:
        html = 'No data'

    return (html)


def dataFrameToHist(df, axes, calc, set_name, amino_code):
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
    plt.style.use('seaborn-whitegrid')

    rows = len(df.index)

    if rows > 2:

        fig, ax = plt.subplots()

        # data cleaning
        df['geox'] = df['geox'].astype('float')
        plt.hist(df['geox'], EdgeColor='k', bins=50)

        ax.set_xlim([axes[0], axes[1]])
        # plt.axis([axes[0],axes[1]])

        plt.title(amino_code)
        ax.set_xlabel(calc)
        ax.set_ylabel('count')

        # save image to byte data
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())

        html = '<img width = 95% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    else:
        html = '<p>' + amino_code + '</p>'
    plt.close('all')
    return (html)
# ************************************************************************************************


