#!/d/msc/s/anaconda/v5.3.0/bin/python
'''
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  This is the main file for images from dataframes
Description:
============
'''
# ************************************************************************************************

import pandas as pd
import matplotlib
from scipy.stats import gaussian_kde
import math
import numpy as np
from io import StringIO as sio
import os, sys
import cgitb

cgitb.enable()
import name_change as nc
import io
import base64

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm as CM
from scipy.stats import kde
import numpy as np


# ************************************************************************************************

def maxMinAxes(dfList, colKeyX, colKeyY, colTypeX, colTypeY):
    minX = 1000
    maxX = -1000
    minY = 1000
    maxY = -1000
    for df in dfList:
        rows = len(df.index)
        if rows > 1:
            df[colKeyX] = df[colKeyX].astype(colTypeX)
            thisMinX = min(df[colKeyX])
            thisMaxX = max(df[colKeyX])
            if thisMinX < minX:
                minX = thisMinX
            if thisMaxX > maxX:
                maxX = thisMaxX

            if colKeyY != "":
                df[colKeyY] = df[colKeyY].astype(colTypeY)
                thisMinY = min(df[colKeyY])
                thisMaxY = max(df[colKeyY])
                if thisMinY < minY:
                    minY = thisMinY
                if thisMaxY > maxY:
                    maxY = thisMaxY

    return ((minX, maxX, minY, maxY))


# ************************************************************************************************

def maxMinAxis(dfList, colKeyX, colTypeX):
    minX = 1000
    maxX = -1000
    for df in dfList:
        rows = len(df.index)
        if rows > 1:
            df[colKeyX] = df[colKeyX].astype(colTypeX)
            thisMinX = min(df[colKeyX])
            thisMaxX = max(df[colKeyX])
            if thisMinX < minX:
                minX = thisMinX
            if thisMaxX > maxX:
                maxX = thisMaxX

    return ((minX, maxX))


# ******************************************************
def dataFrameToContactImage(df, xax, yax, pdb, axes, isDot):
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

    fig, ax = plt.subplots()

    # data cleaning
    df['residue_no'] = df['residue_no'].astype('int')
    df['residue_no_b'] = df['residue_no_b'].astype('int')
    maxvalx = max(df['residue_no'])
    maxvaly = max(df['residue_no_b'])

    # df = df.sort_values(by='geo_value', ascending=True)
    df = df.sort(['residue_no', 'residue_no_b'], ascending=[True, True])
    rows = len(df.index)

    if isDot:

        scales = np.full((rows, 1), 7)

        ops = (7 - df['geo_value'].astype('double')) / 6.0

        rgba_colors = np.zeros((rows, 4))
        rgba_colors[:, 0] = 0.5
        # the fourth column needs to be your alphas
        rgba_colors[:, 3] = ops
        plt.scatter(df['residue_no'], df['residue_no_b'], color=rgba_colors, s=scales)
    else:
        scales = 1 / df['geo_value'].astype('double')
        scales = scales * 100
        scales = scales ** 2
        scales = scales / 5
        plt.scatter(df['residue_no'], df['residue_no_b'], c=df['geo_value'], s=scales, cmap='viridis', alpha=0.7,
                    vmin=2.5, vmax=6)
        plt.colorbar()

    plt.title(pdb + ': contact between residues (Angstrom)')
    ax.set_xlabel(xax)
    ax.set_ylabel(yax)
    plt.axis([axes[0], axes[1] + 10, axes[2], axes[3] + 10])

    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())

    html = '<img width = 95% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
    plt.close('all')
    return (html)


# ************************************************************************************************
def dataFrameToHistImage(x, y, axes, xName, yName, title, palette, override, data, bins):
    xName = nc.changeDBToViewMeasure(xName)
    yName = nc.changeDBToViewMeasure(yName)

    plt.style.use('seaborn-whitegrid')
    extent = axes[0], axes[1], axes[2], axes[3]
    fig, ax = plt.subplots()
    plt.axis([axes[0], axes[1], axes[2], axes[3]])

    retArray = data

    if override:

        image = plt.imshow(data, cmap=palette, interpolation='nearest', origin='low', extent=extent, aspect='auto')
        maxZ = 0
        for r in range(data.shape[0]):
            for c in range(data.shape[1]):
                maxZ = max(maxZ, abs(data[r, c]))
        minZ = 0 - maxZ
        plt.clim(minZ, maxZ)
        cbar = fig.colorbar(image, ax=ax)
        cbar.set_clim(minZ, maxZ)
        cbar.remove()

    else:
        # retArray,xedges,yedges,image = ax.hist2d(y,x, bins=bins)#oddly transposed?
        retArray, xedges, yedges = np.histogram2d(y, x, bins=bins)  # oddly transposed?
        image = plt.imshow(retArray, cmap=palette, interpolation='nearest', origin='low', extent=extent, aspect='auto')

    plt.title(title)
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)

    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')

    return (retArray, encoded)


# ************************************************************************************************
def getProbabilityDensityImage(x, y, axes, xName, yName, title, palette, override, zgrid, bins, zeroMiddle, minVal,
                               maxVal):
    '''
    https://jakevdp.github.io/PythonDataScienceHandbook/04.05-histograms-and-binnings.html
    '''
    from statsmodels.nonparametric.kernel_density import KDEMultivariate
    xName = nc.changeDBToViewMeasure(xName)
    yName = nc.changeDBToViewMeasure(yName)

    # settings for KDE
    valnum = 12  # contours
    kde = 0.10

    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    plt.axis([axes[0], axes[1], axes[2], axes[3]])

    xgrid = np.linspace(axes[0], axes[1], bins)
    ygrid = np.linspace(axes[2], axes[3], bins)

    method = 'gaussian'
    if not override:
        if method == 'gaussian':
            xgrid, ygrid, zgrid = kde2D_scipy(x, y, kde, axes, bins)
        else:
            xgrid, ygrid, zgrid = kde2D_Scilearn(x, y, 1.0, xbins=90j, ybins=90j)

    # Plot the result as an image

    plt.title(title)
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)
    ax.set_axisbelow(False)
    ax.grid(True, which='major', axis='both', linestyle='-', color=(0.8, 0.8, 0.8), alpha=0.3)

    if minVal == 0 and maxVal == 0:
        im = plt.pcolormesh(xgrid, ygrid, zgrid, shading='gouraud', cmap=palette)
        cs = plt.contour(xgrid, ygrid, zgrid, valnum, colors='0.7', linewidths=0.4)
    else:
        im = plt.pcolormesh(xgrid, ygrid, zgrid, shading='gouraud', cmap=palette, vmin=minVal, vmax=maxVal)
        cs = plt.contour(xgrid, ygrid, zgrid, valnum, colors='tab:purple', linewidths=0.05)
    # else:
    #    cs = plt.contour(xgrid,ygrid,zgrid,valnum)

    # plt.clim(-500,500)#minZ,maxZ)
    cbar = fig.colorbar(im, ax=ax)
    # cbar.set_clim(minZ, maxZ)
    cbar.remove()

    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')
    return (encoded)


# ************************************************************************************************
# FUNTION COPIED FROM https://stackoverflow.com/questions/41577705/how-does-2d-kernel-density-estimation-in-python-sklearn-work
# ************************************************************************************************
def kde2D_Scilearn(x, y, bandwidth, xbins=100j, ybins=100j, **kwargs):
    """ Build 2D kernel density estimate (KDE).
        https://scikit-learn.org/stable/modules/density.html
        https://stackoverflow.com/questions/41577705/how-does-2d-kernel-density-estimation-in-python-sklearn-work
        kernels = ['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
    """
    from sklearn.neighbors import KernelDensity
    # create grid of sample locations (default: 100x100)
    xx, yy = np.mgrid[x.min():x.max():xbins, y.min():y.max():ybins]
    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train = np.vstack([y, x]).T
    kde_skl = KernelDensity(kernel='gaussian', bandwidth=bandwidth, **kwargs)
    kde_skl.fit(xy_train)
    # score_samples() returns the log-likelihood of the samples
    z = np.exp(kde_skl.score_samples(xy_sample))
    return xx, yy, np.reshape(z, xx.shape)


# ************************************************************************************************
def kde2D_scipy(x, y, bandwidth, axes, bins):
    data = np.vstack([x, y])
    xgrid = np.linspace(axes[0], axes[1], bins)
    ygrid = np.linspace(axes[2], axes[3], bins)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    grid_sized = np.vstack([Xgrid.ravel(), Ygrid.ravel()])
    # fit an array of size [Ndim, Nsamples]
    kde = gaussian_kde(data, bw_method=bandwidth)
    # evaluate on a regular grid
    Z = kde.evaluate(grid_sized)
    zgrid = Z.reshape(Xgrid.shape)
    return xgrid, ygrid, zgrid


# ************************************************************************************************
def getProbabilityDensityImageDifference(xA, yA, xB, yB, axes, xName, yName, palette):
    '''
    https://jakevdp.github.io/PythonDataScienceHandbook/04.05-histograms-and-binnings.html
    '''
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    plt.axis([axes[0], axes[1], axes[2], axes[3]])

    xName = nc.changeDBToViewMeasure(xName)
    yName = nc.changeDBToViewMeasure(yName)

    # normalise the data
    ##    lenA = len(xA.index)
    ##    lenB = len(xB.index)
    ##    if lenB > lenA:
    ##        fact = lenB//lenA
    ##        #fact  math.round(fact,0)
    ##        fact = int(fact)
    ##        normsX = []
    ##        normsY = []
    ##        for i in range(fact):
    ##            for j in range(lenA):
    ##                normsX.append(pd.Series(xA[j]))
    ##                normsY.append(pd.Series(yA[j]))
    ##        xA.append(normsX)
    ##        yA.append(normsY)
    ##    elif lenA > lenB:
    ##        fact = lenA//lenB
    ##        #fact  math.round(fact,0)
    ##        fact = int(fact)
    ##        normsX = []
    ##        normsY = []
    ##        for i in range(fact):
    ##            for j in range(lenB):
    ##                normsX.append(pd.Series(xB[j]))
    ##                normsY.append(pd.Series(yB[j]))
    ##        xB.append(normsX)
    ##        yB.append(normsY)

    # Data A
    # fit an array of size [Ndim, Nsamples]

    bandwidth = 0.18

    dataA = np.vstack([xA, yA])
    kdeA = gaussian_kde(dataA, bw_method=bandwidth)

    # evaluate on a regular grid
    xgridA = np.linspace(axes[0], axes[1], 75)
    ygridA = np.linspace(axes[2], axes[3], 75)
    XgridA, YgridA = np.meshgrid(xgridA, ygridA)
    ZA = kdeA.evaluate(np.vstack([XgridA.ravel(), YgridA.ravel()]))
    zgridA = ZA.reshape(XgridA.shape)

    # Data B
    dataB = np.vstack([xB, yB])
    kdeB = gaussian_kde(dataB, bw_method=bandwidth)

    # evaluate on a regular grid
    xgridB = np.linspace(axes[0], axes[1], 75)
    ygridB = np.linspace(axes[2], axes[3], 75)
    XgridB, YgridB = np.meshgrid(xgridB, ygridB)
    ZB = kdeB.evaluate(np.vstack([XgridB.ravel(), YgridB.ravel()]))
    zgridB = ZB.reshape(XgridB.shape)

    # zgridA *= len(xB.index)
    # zgridB *= len(xA.index)

    xdiff = xgridB  # - xgridA
    ydiff = ygridB  # - ygridA
    zdiff = zgridA - zgridB

    rows, cols = zdiff.shape
    maxZ = 0
    for r in range(rows):
        for c in range(cols):
            maxZ = max(maxZ, abs(zdiff[r, c]))
    minZ = 0 - maxZ

    # maxZ = max(max(zdiff.any()),abs(min(zdiff.any())))

    # Plot the result as an image
    valnum = 5
    im = ax.pcolormesh(xdiff, ydiff, zdiff, shading='gouraud', cmap=palette)
    cs = plt.contour(xdiff, ydiff, zdiff, valnum)
    plt.clim(minZ, maxZ)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_clim(minZ, maxZ)
    cbar.remove()

    ax.set_xlabel(xName)
    ax.set_ylabel(yName)
    ax.set_axisbelow(False)
    ax.grid(True, which='major', axis='both', linestyle='-', color=(0.8, 0.8, 0.8), alpha=0.3)

    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')
    return (encoded)


# ************************************************************************************************

def getScatterPlotImage(x, y, z, axes, xName, yName, title, palette, grads):
    plt.style.use('seaborn-whitegrid')

    xName = nc.changeDBToViewMeasure(xName)
    yName = nc.changeDBToViewMeasure(yName)

    fig, ax = plt.subplots()
    plt.axis([axes[0], axes[1], axes[2], axes[3]])

    if palette == 'none':
        plt.scatter(x, y, color='blueviolet', alpha=0.05)
    else:
        im = plt.scatter(x, y, c=z, cmap=palette, edgecolors='0', linewidth=0.05)
        if palette != 'viridis_r':  # which really means if it dssp
            cbar = fig.colorbar(im, ax=ax)
            cbar.set_clim(0, 8)
        elif grads[0] + grads[1] != -2:
            cbar = fig.colorbar(im, ax=ax)
            cbar.set_clim(grads[0], grads[1])
        else:
            plt.colorbar()

    plt.title(title)
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)
    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')
    return (encoded)


# ************************************************************************************************

def getScatter3dImage(x, y, z, col, axesX, axesY, axesZ, xName, yName, zName, title, palette):
    plt.style.use('seaborn-whitegrid')

    xName = nc.changeDBToViewMeasure(xName)
    yName = nc.changeDBToViewMeasure(yName)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plt.axis([axesX[0],axesX[1],axesY[0],axesY[1],axesZ[0],axesZ[1]])

    ax.scatter(x, y, z, c=col, cmap=palette)
    ax.set_xlim(axesX[0], axesX[1])
    ax.set_ylim(axesY[0], axesY[1])
    ax.set_zlim(axesZ[0], axesZ[1])

    # plt.colorbar()
    plt.title(title)
    ax.set_xlabel(xName, linespacing=2, size=10, fontweight='bold')
    ax.set_ylabel(yName, linespacing=2, size=10, fontweight='bold')
    ax.set_zlabel(zName, linespacing=2, size=10, fontweight='bold', rotation=90)
    # save image to byte data
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    plt.close('all')
    return (encoded)


# ************************************************************************************************
def dataFrameToBoxPlot(df, amino_code, axes, view):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    """
    import io
    import base64
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('seaborn-whitegrid')

    rows = len(df.index)
    # print("debug 2",rows)

    if rows > 2:

        fig, ax = plt.subplots()

        if view == 'Histogram':
            measures = df.measure.unique()
            buckets = df.bucket.unique()

            for meas in measures:
                for buck in buckets:
                    label = meas + " " + buck
                    dfx = df[df['measure'] == meas]
                    dfx = df[df['bucket'] == buck]

                    sns.distplot(dfx["geox"], label=label, norm_hist=True, kde=False)
            plt.legend()
            ax.set_xlabel("")
        else:
            ax.set_ylim([axes[0], axes[1]])
            if view == 'Box Plot':
                sns.boxplot(x='bucket', y='geox', hue="measure", data=df, palette="Set1")
            elif view == 'Swarm Plot':
                # print("debug 3")
                sns.swarmplot(x='bucket', y='geox', hue="measure", data=df, palette="Set1")
            elif view == 'Violin Plot':
                sns.violinplot(x='bucket', y='geox', hue="measure", data=df, palette="Set1")  # ,inner="quart")
            elif view == 'Line Plot':
                sns.lineplot(x='bucket', y='geox', hue="measure", data=df, palette="Set1", ci=95)
            ax.set_xlabel("Resolution bucket")
        ax.set_ylabel('')

        if amino_code == "NON":
            plt.title('All residues')
        else:
            plt.title(amino_code)

        # print("debug 4")
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
def dataFrameToValidationReport(df, gradients):
    """
    param: df - data in a dataframe object
    returns: the image as an embedded numpy array
    """
    import io
    import base64
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('seaborn-whitegrid')

    rows = len(df.index)

    if rows > 2:

        fig, ax = plt.subplots()
        category = df.category.unique()[0]
        calcx = df.bucket.unique()[0]
        calcy = df.measure.unique()[0]
        aa = df.aminoview.unique()[0]

        sns.scatterplot(x='geox', y='geoy', hue="gradient", data=df, palette=gradients,
                        linewidth=0, alpha=0.8, markers=False, legend=False)

        ax.set_xlabel(calcx)
        ax.set_ylabel(calcy)

        title = aa
        if aa == "NON":
            title = "All residues"
        title += " count=" + str(rows)

        plt.title(title)

        # save image to byte data
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())

        html = '<img width = 95% src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    else:
        html = '<p>'  '</p>'
    plt.close('all')
    return (html)




