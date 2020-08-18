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
import name_change as nc
from PIL import Image
import numpy as np
from scipy.stats import gaussian_kde

###################################################################################################################
def getOverlayButton():
    html = ""
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_overlay.cgi" accept-charset="UTF-8">\n'
    html += "<p><input type='Submit' value='Overlay Distributions' formaction='/cgi-bin/cgiwrap/ab002/thesis_overlay.cgi'/></p>\n"
    html += '</form>\n'
    return (html)

###################################################################################################################


def middleOverlayDefaults(calcX,calcY,calcZ,maxbA,maxbB,
                          set_nameA,occA, contactA, res_choiceA,res_choiceAL,
                          rv_choiceA, rv_choiceAL,rf_choiceA,rf_choiceAL,
                          amino_codeA,set_nameB,occB, contactB, res_choiceB,res_choiceBL,
                          rv_choiceB,rv_choiceBL, rf_choiceB, rf_choiceBL,
                          amino_codeB, restrictionA,restrictionB,gradient,html_path,
                          hist,scatter,trace,probden,breadth,depth,scatter3,
                          in_set, checked_set,
                          H,B,E,G,I,T,S,U,X,
                          Hb,Bb,Eb,Gb,Ib,Tb,Sb,Ub,Xb):
    '''
    This ensures the defaults are returned back to the screen
    '''
    html = '<div class="middle">\n'
    html += ts.middleReturnComment("For help and available calculations click below:")
    html += '<p><a href="' + html_path + 'data.html" title="GeoMeasures" target="_self">Help and geo measures</a></p>\n'
    html += '</div>\n'

    html += ts.middleReturnComment("Enter appropriate parameters to view distributions")
    html += '<div class="middle">\n'
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_correlation.cgi" accept-charset="UTF-8">\n'
    html += '<div class="smallmiddle">\n'


    # overall table
    html += '<table class="verdsearchtable">'
    html += '<tr class=outinnerheader><td>Overall Distribution</td><td>Distribution A</td><td>Secondary Structure For A or B </td><td>Distribution B</td><td>Choose Images</td></tr>\n'
    html += '<tr>'
    html += '<td>' # options for both distributions
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Geo Calc X</td><td><input type="text" size="6" name="calcX" value="' + calcX + '"/></td></tr>\n'
    html += '<tr><td>Geo Calc Y</td><td><input type="text" size="6" name="calcY" value="' + calcY + '"/></td></tr>\n'
    html += '<tr><td>Geo Calc Z</td><td><input type="text" size="6" name="calcZ" value="' + calcZ + '"/></td></tr>\n'
    #html += '<tr><td>Max BFactor</td><td><input type="text" size="6" name="maxb" value="' + maxb + '"/></td></tr>\n'
    #html += '<tr><td>Restriction</td><td><input type="text" size="6" name="restriction" value="' + restriction + '"/></td></tr>\n'
    html += '<tr><td>Hue Choice</td><td><input type="text" size="6" name="gradient" value="' + gradient + '"/></td></tr>\n'


    in_checked = ''
    if in_set == '1':
        in_checked = ' checked="checked"'
    checked_checked = ''
    if checked_set == '1':
        checked_checked = ' checked="checked"'

    html += '<tr><td><label for="hist">Include IN pdbs</label></td><td><input type="checkbox" id="in_set" name="in_set" value="1" ' + str(in_checked) + '"></td></tr>\n'
    html += '<tr><td><label for="hist">Include CHECKED pdbs</label></td><td><input type="checkbox" id="checked_set" name="checked_set" value="1" ' + str(checked_checked) + '"></td></tr>\n'


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

    Hcheckb = ''
    if Hb == "1":
        Hcheckb = "checked='checked'"
    Bcheckb = ''
    if Bb == "1":
        Bcheckb = "checked='checked'"
    Echeckb = ''
    if Eb == "1":
        Echeckb = "checked='checked'"
    Gcheckb = ''
    if Gb == "1":
        Gcheckb = "checked='checked'"
    Icheckb = ''
    if Ib == "1":
        Icheckb = "checked='checked'"
    Tcheckb = ''
    if Tb == "1":
        Tcheckb = "checked='checked'"
    Scheckb = ''
    if Sb == "1":
        Scheckb = "checked='checked'"
    Ucheckb = ''
    if Ub == "1":
        Ucheckb = "checked='checked'"
    Xcheckb = ''
    if Xb == "1":
        Xcheckb = "checked='checked'"




    html += '</table>'
    html += '</td>'
    html += '<td>' # options for distribution A
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Set Name</td><td><input type="text" size="6" name="set_nameA" value="' + set_nameA + '"/></td></tr>\n'
    html += '<tr><td>Amino Code</td><td><input type="text" size="6" name="amino_codeA" value="' + amino_codeA + '"/></td></tr>\n'
    html += '<tr><td>Occupant</td><td><input type="text" size="6" name="occA" value="' + occA + '"/></td></tr>\n'
    html += '<tr><td>Contact</td><td><input type="text" size="6" name="contactA" value="' + contactA + '"/></td></tr>\n'
    html += '<tr><td>Restriction</td><td colspan="2"><input type="text" size="15" name="restrictionA" value="' + restrictionA + '"/></td></tr>\n'
    html += '<tr><td>Max BFactor</td><td><input type="text" size="6" name="maxbA" value="' + maxbA + '"/></td></tr>\n'
    html += '<tr><td>Bounds:</td><td>Upper</td><td>Lower</td></tr>\n'
    html += '<tr><td>Resolution</td><td><input type="text" size="6" name="res_choiceA" value="' + res_choiceA + '"/></td>\n'
    html += '<td><input type="text" size="6" name="res_choiceAL" value="' + res_choiceAL + '"/></td></tr>\n'
    html += '<tr><td>R Value</td><td><input type="text" size="6" name="rv_choiceA" value="' + rv_choiceA + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rv_choiceAL" value="' + rv_choiceAL + '"/></td></tr>\n'
    html += '<tr><td>R Free</td><td><input type="text" size="6" name="rf_choiceA" value="' + rf_choiceA + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rf_choiceAL" value="' + rf_choiceAL + '"/></td></tr>\n'

    html += '</table>'
    html += '</td>'
    html += '<td>' # options for Secondary Structure
    html += '<table class="verdsearchtable">'

    html += '<tr><td><label for="H">H=α-helix</label></td><td><input type="checkbox" id="H" name="H" value="1" ' + str(Hcheck) + '"></td><td><input type="checkbox" id="Hb" name="Hb" value="1" ' + str(Hcheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="B">B=residue in isolated β-bridge</label></td><td><input type="checkbox" id="B" name="B" value="1" ' + str(Bcheck) + '"></td><td><input type="checkbox" id="Bb" name="Bb" value="1" ' + str(Bcheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="E">E=extended strand, participates in β ladder</label></td><td><input type="checkbox" id="E" name="E" value="1" ' + str(Echeck) + '"></td><td><input type="checkbox" id="Eb" name="Eb" value="1" ' + str(Echeckb) + '"></td></tr>\n'
    html += '<tr><td><label for="G">G=3-helix (310 helix)</label></td><td><input type="checkbox" id="G" name="G" value="1" ' + str(Gcheck) + '"></td><td><input type="checkbox" id="Gb" name="Gb" value="1" ' + str(Gcheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="I">I=5 helix (π-helix)</label></td><td><input type="checkbox" id="I" name="I" value="1" ' + str(Icheck) + '"></td><td><input type="checkbox" id="Ib" name="Ib" value="1" ' + str(Icheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="T">T=hydrogen bonded turn</label></td><td><input type="checkbox" id="T" name="T" value="1" ' + str(Tcheck) + '"></td><td><input type="checkbox" id="Tb" name="Tb" value="1" ' + str(Tcheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="S">S=bend </label></td><td><input type="checkbox" id="S" name="S" value="1" ' + str(Scheck) + '"></td><td><input type="checkbox" id="Sb" name="Sb" value="1" ' + str(Scheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="U">U=unknown</label></td><td><input type="checkbox" id="U" name="U" value="1" ' + str(Ucheck) + '"></td><td><input type="checkbox" id="Ub" name="Ub" value="1" ' + str(Ucheckb) + '"></td></tr>\n'
    html += '<tr><td><label for="X">X=Unassigned</label></td><td><input type="checkbox" id="X" name="X" value="1" ' + str(Xcheck) + '"></td><td><input type="checkbox" id="Xb" name="Xb" value="1" ' + str(Xcheckb) + '"></td></tr>\n'



    html += '</table>'
    html += '</td>'
    html += '<td>' # options for distribution B
    html += '<table class="verdsearchtable">'
    html += '<tr><td>Set Name</td><td><input type="text" size="6" name="set_nameB" value="' + set_nameB + '"/></td></tr>\n'
    html += '<tr><td>Amino Code</td><td><input type="text" size="6" name="amino_codeB" value="' + amino_codeB + '"/></td></tr>\n'
    html += '<tr><td>Occupant</td><td><input type="text" size="6" name="occB" value="' + occB + '"/></td></tr>\n'
    html += '<tr><td>Contact</td><td><input type="text" size="6" name="contactB" value="' + contactB + '"/></td></tr>\n'
    html += '<tr><td>Restriction</td><td colspan="2"><input type="text" size="15" name="restrictionB" value="' + restrictionB + '"/></td></tr>\n'
    html += '<tr><td>Max BFactor</td><td><input type="text" size="6" name="maxbB" value="' + maxbB + '"/></td></tr>\n'
    html += '<tr><td>Bounds:</td><td>Upper</td><td>Lower</td></tr>\n'
    html += '<tr><td>Resolution</td><td><input type="text" size="6" name="res_choiceB" value="' + res_choiceB + '"/></td>\n'
    html += '<td><input type="text" size="6" name="res_choiceBL" value="' + res_choiceBL + '"/></td></tr>\n'
    html += '<tr><td>R Value</td><td><input type="text" size="6" name="rv_choiceB" value="' + rv_choiceB + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rv_choiceBL" value="' + rv_choiceBL + '"/></td></tr>\n'
    html += '<tr><td>R Free</td><td><input type="text" size="6" name="rf_choiceB" value="' + rf_choiceB + '"/></td>\n'
    html += '<td><input type="text" size="6" name="rf_choiceBL" value="' + rf_choiceBL + '"/></td></tr>\n'
    html += '</table>'
    html += '</td>'
    html += '<td>' # Distribution buttons
    html += '<table class="verdsearchtable">'
    html += ""
    histcheck = ''
    if hist == "1":
        histcheck = "checked='checked'"
    scattercheck = ''
    if scatter == "1":
        scattercheck = "checked='checked'"
    tracecheck = ''
    if trace == "1":
        tracecheck = "checked='checked'"
    probdencheck = ''
    if probden == "1":
        probdencheck = "checked='checked'"
    breadthcheck =''
    if breadth == "1":
        breadthcheck = "checked='checked'"
    depthcheck = ''
    if depth == "1":
        depthcheck = "checked='checked'"
    scatter3check = ''
    if scatter3 == "1":
        scatter3check = "checked='checked'"
    html += '<tr><td><label for="hist">1d Histogram</label></td><td><input type="checkbox" id="hist" name="hist" value="1" ' + str(histcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="scatter">2d Scatter</label></td><td><input type="checkbox" id="scatter" name="scatter" value="1" ' + str(scattercheck) + '"></td></tr>\n'
    html += '<tr><td><label for="trace">2d Density Trace</label></td><td><input type="checkbox" id="trace" name="trace" value="1" ' + str(tracecheck) + '"></td></tr>\n'
    html += '<tr><td><label for="probden">2d Probability Density</label></td><td><input type="checkbox" id="probden" name="probden" value="1" ' + str(probdencheck) + '"></td></tr>\n'
    html += '<tr><td><label for="breadth">2dx2d Breadth Compare</label></td><td><input type="checkbox" id="breadth" name="breadth" value="1" ' + str(breadthcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="depth">2dx2d Depth Compare</label></td><td><input type="checkbox" id="depth" name="depth" value="1" ' + str(depthcheck) + '"></td></tr>\n'
    html += '<tr><td><label for="scatter3">3d Scatter</label></td><td><input type="checkbox" id="scatter3" name="scatter3" value="1" ' + str(scatter3check) + '"></td></tr>\n'
    #html += "<tr><td>2d</td><td><div class='buttondist'><input type='Submit' value='Scatter Plot' formaction='/cgi-bin/cgiwrap/ab002/thesis_correlation.cgi'/></div></td></tr>\n"
    #html += "<tr><td>2d</td><td><div class='buttondist'><input type='Submit' value='Probability Density' formaction='/cgi-bin/cgiwrap/ab002/thesis_density.cgi'/></div></td></tr>\n"
    #html += "<tr><td>2d x 2d</td><td><div class='buttondist'><input type='Submit' value='Compare Distributions' formaction='/cgi-bin/cgiwrap/ab002/thesis_overlay.cgi'/></div></td></tr>\n"
    #html += "<tr><td>2d x 2d</td><td><div class='buttondist'><input type='Submit' value='Compare Probability' formaction='/cgi-bin/cgiwrap/ab002/thesis_diffprob.cgi'/></div></td></tr>\n"
    #html += "<tr><td>3d</td><td><div class='buttondist'><input type='Submit' value='3D Scatter' formaction='/cgi-bin/cgiwrap/ab002/thesis_scatter3d.cgi'/></div></td></tr>\n"
    html += '</table>'
    html += '</td>'
    html += '</tr>'
    html += "<tr><td><div class='buttondist'><input type='Submit' value='Create Distribution Images' formaction='/cgi-bin/cgiwrap/ab002/thesis_distributions.cgi'/></div></td></tr>\n"
    html += '</table>'



    #close form
    html += '</div>\n'
    html += '</form>\n'
    html += '</div>\n'
    html += '<hr/>\n'
    return (html)

###################################################################################################################
def middleOverlayRequest(datasA, datasB, bothAll):
    '''
    This ensures the defaults are returned back to the screen
    '''
    html = ""
    message = "The masked image metric shows percentage of similarity of the LHS:RHS"
    html += ts.middleReturnComment(message)

    html += "<table class='outtable'>\n"

    # don;t allow it to cross multiply 400
    aLen = len(datasA)
    bLen = len(datasB)

    for aa in datasA:
           for ab in datasB:
            if aa == ab or (aLen+bLen < 10):
                dfList = []
                dfList.append(datasA[aa].df)
                dfList.append(datasB[ab].df)
                axes =tim.maxMinAxes(dfList,'geox','geoy','double','double')
                html += dataFrameToImage(datasA[aa].df, datasB[ab].df,axes,datasA[aa].choices.calcx,datasA[aa].choices.calcy,aa,ab)



    html += "</table>\n"

    return (html)

###################################################################################################################
def middleProbDiffRequest(datasA, datasB, bothAll):
    '''
    This ensures the defaults are returned back to the screen
    '''
    html = ""
    message = "The Image Depth Difference shows which side has a greater depth, red for the left and blue for the right."
    html += ts.middleReturnComment(message)

    html += "<table class='outtable'>\n"

    # don;t allow it to cross multiply 400
    aLen = len(datasA)
    bLen = len(datasB)

    for aa in datasA:
           for ab in datasB:
            if aa == ab or (aLen+bLen < 10):
                dfList = []
                dfList.append(datasA[aa].df)
                dfList.append(datasB[ab].df)
                axes =tim.maxMinAxes(dfList,'geox','geoy','double','double')
                html += dataFrameToProbDiffImage(datasA[aa].df, datasB[ab].df,axes,datasA[aa].choices.calcx,datasA[aa].choices.calcy,aa,ab)



    html += "</table>\n"

    return (html)
###################################################################################################################
def getDfFromSql(sql, amino_code):
    """
    param: sql
    returns: df
    """
    try:  # calling the database
        dfaa = sdb.read_sql(sql)
    except:
        dfaa = pd.read_csv(sio(amino_code + ", no data"))
    return dfaa


############################################################################
def dataFrameToProbDiffImage(dfA, dfB,axes, calcX,calcY, amino_codeA, amino_codeB):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    Resource used:
    https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly
    https://pythonspot.com/matplotlib-scatterplot/
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_custom_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-custom-symbol-py
    """
    import matplotlib
    import io
    import base64
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import cm as CM
    from scipy.stats import kde
    import numpy as np

    plt.style.use('seaborn-whitegrid')

    rowsA = len(dfA.index)
    rowsB = len(dfB.index)

    cMax = 3


    if rowsA > 2 and rowsB > 2:
        # Get df for the data
        #dfA['geox'] = dfA['geox'].astype('float')
        #dfA['geoy'] = dfA['geoy'].astype('float')
        #dfA['gradient'] = dfA['gradient'].astype('float')
        rowsA = len(dfA.index)
        xA =  dfA['geox']
        yA =  dfA['geoy']
        titleA = amino_codeA + " obs=" +  str(rowsA)

        #dfB['geox'] = dfB['geox'].astype('float')
        #dfB['geoy'] = dfB['geoy'].astype('float')
        #dfB['gradient'] = dfB['gradient'].astype('float')
        rowsB = len(dfB.index)
        xB =  dfB['geox']
        yB =  dfB['geoy']
        titleB = amino_codeB + " obs=" +  str(rowsB)



        colA = CM.PRGn
        colB = CM.PRGn_r
        colDiff = CM.PRGn

        colAp = CM.seismic
        colBp = CM.seismic_r
        colDiffp = CM.seismic

        bins = 180


        useProb = True

        if useProb:
            # Set up A and B gaussian grids
            #EITHER AS PROBABILITY
            bandwidth = 0.1

            xgridA,ygridA,zgridA= tim.kde2D_scipy(xA,yA,bandwidth,axes,bins)

            xgridB,ygridB,zgridB= tim.kde2D_scipy(xB,yB,bandwidth,axes,bins)



            # Normailise data

            #factor = rowsB//rowsA
            #for i in range (zgridA.shape[0]):
            #    for j in range (zgridA.shape[1]):
            #        zgridA[i,j] *= factor
            arDiff = zgridA -zgridB

            maxVal = 0
            minVal = 0
            for i in range (zgridA.shape[0]):
                for j in range (zgridA.shape[1]):
                    maxVal = max(zgridA[i,j],zgridB[i,j],arDiff[i,j],maxVal)
                    minVal = min(zgridA[i,j],zgridB[i,j],arDiff[i,j],minVal)
            maxVal = max(maxVal,0-minVal)
            minVal = min(minVal,0-maxVal)



            encodedA = tim.getProbabilityDensityImage(xA,yA,axes,calcX,calcY,"",colAp,True,zgridA,bins,True,minVal,maxVal)
            encodedB = tim.getProbabilityDensityImage(xB,yB,axes,calcX,calcY,"",colBp,True,zgridB,bins,True,minVal,maxVal)
            encodedDiff = tim.getProbabilityDensityImage(xB,yB,axes,calcX,calcY,"",colDiffp,True,arDiff,bins,True,minVal,maxVal)
        else:
            #OR AS 2D HISTOGRAM




            arA, encodedA = tim.dataFrameToHistImage(xA,yA,axes,calcX,calcY,"",colA,False,None,bins)
            arB, encodedB = tim.dataFrameToHistImage(xB,yB,axes,calcX,calcY,"",colB,False,None,bins)

            # Normalise data, it needs to be the smaller one scaled up.
            maxVal = 0
            minVal = 0
            factorA = 1
            factorB = 1
            if rowsA > rowsB:
                factorB = rowsA//rowsB
            else:
                factorA = rowsB//rowsA

            for i in range (arA.shape[0]):
                for j in range (arA.shape[1]):
                    arA[i,j] *= factorA
                    arB[i,j] *= factorB

            arDiff = arA -arB

            for i in range (arA.shape[0]):
                for j in range (arA.shape[1]):
                   maxVal = max(maxVal,arA[i,j])
                   minVal = min(minVal,arA[i,j])

            for i in range (arB.shape[0]):
                for j in range (arB.shape[1]):
                   maxVal = max(maxVal,arB[i,j])
                   minVal = min(minVal,arB[i,j])

            maxVal = max(maxVal,abs(minVal))
            minVal = 0-maxVal

            #encoded = tim.getProbabilityDensityImage(x,y,axes,calcX,calcY,title,CM.GnBu,False,None,180,False,0,0)

            encodedA = tim.getProbabilityDensityImage(xA,yA,axes,calcX,calcY,"",colA,True,arA,bins,False,minVal,maxVal)
            encodedB = tim.getProbabilityDensityImage(xB,yB,axes,calcX,calcY,"",colB,True,arB,bins,False,minVal,maxVal)


            arD, encodedDiff = tim.dataFrameToHistImage(xB,yB,axes,calcX,calcY,"",colDiff,True,arDiff,bins)
            encodedDiff = tim.getProbabilityDensityImage(xB,yB,axes,calcX,calcY,"",colDiff,True,arDiff,bins,True,minVal,maxVal)



        html = '<tr class="outinnerheader"><td>' + titleA + '</td></td><td>Image Depth Difference</td><td>' + titleB + '</tr>'
        html += '<tr>'
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedA.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedDiff.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedB.decode('utf-8'))
        html += '</tr>'
    else:
        html = '<tr class="outinnerheader"><td>' + amino_codeA + "-" + amino_codeB + '</td></tr>'
        html += '<tr>'
        html += '<td> no data</td>'
        html += '</tr>'
    return (html)

###################################################################################################################

def dataFrameToImage(dfA, dfB,axes, calcX,calcY, amino_codeA, amino_codeB):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    Resource used:
    https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly
    https://pythonspot.com/matplotlib-scatterplot/
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_custom_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-custom-symbol-py
    """
    import matplotlib
    import io
    import base64
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import cm as CM
    from scipy.stats import kde
    import numpy as np

    plt.style.use('seaborn-whitegrid')

    rowsA = len(dfA.index)
    rowsB = len(dfB.index)

    cMax = 3
    paletteBoth = CM.Purples
    paletteLHS = CM.Greens
    paletteRHS = CM.Purples

    calcX = nc.changeDBToViewMeasure(calcX)
    calcY = nc.changeDBToViewMeasure(calcY)

    if rowsA > 2 and rowsB > 2:

        # Get df for the data
        dfA['geox'] = dfA['geox'].astype('float')
        dfA['geoy'] = dfA['geoy'].astype('float')
        try:
            dfA['gradient'] = dfA['gradient'].astype('float')
        except:
            dfA['gradient'] = dfA['gradient']
        rowsA = len(dfA.index)

        dfB['geox'] = dfB['geox'].astype('float')
        dfB['geoy'] = dfB['geoy'].astype('float')
        try:
            dfB['gradient'] = dfB['gradient'].astype('float')
        except:
            dfB['gradient'] = dfB['gradient']

        rowsB = len(dfB.index)

        # Create Image 1 for compare
        figA, axA = plt.subplots()
        plt.axis([axes[0],axes[1],axes[2],axes[3]])
        plt.hexbin(dfA['geox'],dfA['geoy'],cmap=paletteBoth, bins=None)
        plt.clim(0,cMax)
        axA.set_xlabel(calcX)
        axA.set_ylabel(calcY)
        axA.grid(False)
        #set axis colour
        axA.spines['bottom'].set_color('k')
        axA.spines['top'].set_color('k')
        axA.spines['right'].set_color('k')
        axA.spines['left'].set_color('k')
        axA.yaxis.label.set_color('k')
        axA.xaxis.label.set_color('k')
        #save image to byte data
        imgA = io.BytesIO()
        figA.savefig(imgA, format='png', bbox_inches='tight')
        imgA.seek(0)
        encodedA = base64.b64encode(imgA.getvalue())

        # Create Image 1 for display
        figLHS, axLHS = plt.subplots()
        plt.axis([axes[0],axes[1],axes[2],axes[3]])
        plt.hexbin(dfA['geox'],dfA['geoy'],cmap=paletteLHS, bins=None)
        plt.clim(0,cMax)
        axLHS.set_xlabel(calcX)
        axLHS.set_ylabel(calcY)
        axLHS.grid(False)
        #set axis colour
        axLHS.spines['bottom'].set_color('k')
        axLHS.spines['top'].set_color('k')
        axLHS.spines['right'].set_color('k')
        axLHS.spines['left'].set_color('k')
        axLHS.yaxis.label.set_color('k')
        axLHS.xaxis.label.set_color('k')
        #save image to byte data
        imgLHS = io.BytesIO()
        figLHS.savefig(imgLHS, format='png', bbox_inches='tight')
        imgLHS.seek(0)
        encodedLHS = base64.b64encode(imgLHS.getvalue())

        # Create Image 2 the same way
        figB, axB = plt.subplots()
        plt.axis([axes[0],axes[1],axes[2],axes[3]])
        plt.hexbin(dfB['geox'],dfB['geoy'],cmap=paletteBoth, bins=None)
        plt.clim(0,cMax)
        axB.set_xlabel(calcX)
        axB.set_ylabel(calcY)
        axB.grid(False)
        #set axis colour
        axB.spines['bottom'].set_color('k')
        axB.spines['top'].set_color('k')
        axB.spines['right'].set_color('k')
        axB.spines['left'].set_color('k')
        axB.yaxis.label.set_color('k')
        axB.xaxis.label.set_color('k')
        #save image to byte data
        imgB = io.BytesIO()
        figB.savefig(imgB, format='png', bbox_inches='tight')
        imgB.seek(0)
        encodedB = base64.b64encode(imgB.getvalue())

        # Create Image 2 for display
        figRHS, axRHS = plt.subplots()
        plt.axis([axes[0],axes[1],axes[2],axes[3]])
        plt.hexbin(dfB['geox'],dfB['geoy'],cmap=paletteRHS, bins=None)
        plt.clim(0,cMax)
        axRHS.set_xlabel(calcX)
        axRHS.set_ylabel(calcY)
        axRHS.grid(False)
        #set axis colour
        axRHS.spines['bottom'].set_color('k')
        axRHS.spines['top'].set_color('k')
        axRHS.spines['right'].set_color('k')
        axRHS.spines['left'].set_color('k')
        axRHS.yaxis.label.set_color('k')
        axRHS.xaxis.label.set_color('k')
        #save image to byte data
        imgRHS = io.BytesIO()
        figRHS.savefig(imgRHS, format='png', bbox_inches='tight')
        imgRHS.seek(0)
        encodedRHS = base64.b64encode(imgRHS.getvalue())




        #Create the mask image
        figD, axD = plt.subplots()
        extent = axes[0],axes[1],axes[2],axes[3]
        arA = np.asarray(Image.open(imgA))
        arB = np.asarray(Image.open(imgB))
        arLHS = np.asarray(Image.open(imgLHS))
        arRHS = np.asarray(Image.open(imgRHS))
        arD = arB+arA


        #process the image, comparing the same way but adding the reverse
        matches = 0.0
        amatches = 0.0
        bmatches = 0.0
        pixels = 0
        apixels = 0
        bpixels = 0

        numX = arD.shape[0]
        numY = arD.shape[1]
        numZ = arD.shape[2]
        vals = []
        for x in range(numX):
            for y in range(numY):
                rA = int(arA[x,y,0])
                gA = int(arA[x,y,1])
                bA = int(arA[x,y,2])
                rB = int(arB[x,y,0])
                gB = int(arB[x,y,1])
                bB = int(arB[x,y,2])
                diff = abs(rA-rB) + abs(gA-gB) + abs(bA-bB)
                totalA = rA+gA+bA
                totalB = rB+gB+bB
                thesame = False
                iswhite = False
                aGrey = rA==gA==bA
                bGrey = rB==gB==bB
                whitecap = 3*200
                increment = 1
                partincrement = 1

                # A and B are both white
                if totalA > whitecap and totalB > whitecap:
                    arD[x,y,0] = 255
                    arD[x,y,1] = 255
                    arD[x,y,2] = 255

                # A and B are both grey scale, ie axes
                elif aGrey and bGrey:
                    arD[x,y,0] = 0
                    arD[x,y,1] = 0
                    arD[x,y,2] = 0

                # A and B are equal
                elif totalA == totalB:
                    matches += increment
                    amatches += increment
                    bmatches += increment
                    pixels += increment
                    apixels += increment
                    bpixels += increment

                    arD[x,y,0] = 255
                    arD[x,y,1] = 255
                    arD[x,y,2] = 255

                # A and B both have meaningful data but not the same
                elif totalA <= whitecap  and totalB <= whitecap :
                    matches += partincrement
                    amatches += partincrement
                    bmatches += partincrement
                    pixels += increment
                    apixels += increment
                    bpixels += increment
                    if totalA < totalB:
                        arD[x,y,0] = 255#200
                        arD[x,y,1] = 255#220
                        arD[x,y,2] = 255#200
                    else:
                        arD[x,y,0] = 255#200
                        arD[x,y,1] = 255#200
                        arD[x,y,2] = 255#220

                # Only A has meaningful data
                elif totalA <= whitecap:
                    pixels += increment
                    apixels += increment

                    arD[x,y,0] = arLHS[x,y,0]#min(rA+50,255)
                    arD[x,y,1] = arLHS[x,y,1]#min(gA+10,255)
                    arD[x,y,2] = arLHS[x,y,2]#max(bA-50,0)

                # Only B has meaningful data
                elif totalB <= whitecap:
                    pixels += increment
                    bpixels += increment

                    arD[x,y,0] = arRHS[x,y,0]#max(rB-50,0)
                    arD[x,y,1] = arRHS[x,y,1]#min(gB+10,255)
                    arD[x,y,2] = arRHS[x,y,2]#min(bB+50,255)



        reversed_arr = arD[::-1]
        mask = Image.fromarray(reversed_arr)

        fig = plt.imshow(mask,cmap=paletteBoth, interpolation='nearest',origin='low',extent=extent,aspect='auto')
        plt.clim(0,cMax)
        plt.gca().set_position([0, 0, 1, 1])
        #plt.tight_layout()
        #plt.axis('tight')
        plt.axis([axes[0],axes[1],axes[2],axes[3]])
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        axD.set_xlabel(calcX)
        axD.set_ylabel(calcY)
        axD.grid(False)
        #save image to byte data
        imgD = io.BytesIO()
        figD.savefig(imgD, format='png', bbox_inches='tight')
        imgD.seek(0)
        encodedD = base64.b64encode(imgD.getvalue())

        # Metrics for the images
        all_metric = int(float(matches*100)/float(pixels))
        a_metric = int(float(amatches*100)/float(apixels))
        b_metric = int(float(bmatches*100)/float(bpixels))

        # Image titles
        titleA = amino_codeA + " obs=" +  str(rowsA)
        titleB = amino_codeB + " obs=" +  str(rowsB)
        titleM = "Masked image metric = " + str(a_metric) + ":" + str(b_metric)

        # New image function
        #encodedDiff = tim.getProbabilityDensityImageDifference(dfA['geox'],dfA['geoy'],dfB['geox'],dfB['geoy'],axes,calcX,calcY,'PRGn')




        # Create the images as html
        html = ""
        html += '<tr class="outinnerheader"><td>' + titleA + '</td><td>' + titleM +  '</td></td><td>' + titleB + '</tr>'
        html += '<tr>'
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedLHS.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedD.decode('utf-8'))
        #html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedDiff.decode('utf-8'))
        html += '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedRHS.decode('utf-8'))
        html += '</tr>'
    else:
        html = '<tr class="outinnerheader"><td>' + amino_codeA + "-" + amino_codeB + '</td></tr>'
        html += '<tr>'
        html += '<td> no data</td>'
        html += '</tr>'


    plt.close('all')
    return (html)

