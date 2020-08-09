'''
Author: Rachel Alcraft
Created: 16/07/20
To minimise use and dependence on librari4s, this file contains the density matrix for a pdb
It can be created seperately to any other programs running to minimise memory problems
'''


import numpy as np
import math

class densityFile:
    def __init__(self,pdb_code,den_type,path):
        self.pdb_code = pdb_code
        self.path = path
        self.file_name_dens = path + pdb_code + '_density.txt'
        self.file_name_diff = path + pdb_code + '_density_diff.txt'
        self.den_type = den_type

    def exists(self):
        exists = True
        try:
            f = open(self.file_name_dens, "r")
            print('Exists', self.file_name_dens)
        except:
            print('File does not exist', self.file_name_dens)
            exists = False
        return exists

    def loadMatrix(self):
        f = open(self.file_name_dens, "r")
        lines = f.readlines()
        numlines = len(lines)
        f.close()

        self.alpha = lines[0]
        self.beta = lines[1]
        self.gamma = lines[2]
        self.origin = lines[3].split(',')
        self.origin = [float(self.origin[i]) for i in range(3)]
        self.gridLength = lines[4].split(',')
        self.gridLength = [float(self.gridLength[i]) for i in range(3)]
        self.xyzInterval = lines[5].split(',')
        self.xyzInterval = [int(self.xyzInterval[i]) for i in range(3)]
        self.crsStart = lines[6].split(',')
        self.crsStart = [int(self.crsStart[i]) for i in range(3)]
        self.map2xyz = lines[7].split(',')
        self.map2xyz = [int(self.map2xyz[i]) for i in range(3)]
        self.map2crs = lines[8].split(',')
        self.map2crs = [int(self.map2crs[i]) for i in range(3)]
        xdim, ydim, zdim = float(lines[9]), float(lines[10]), float(lines[11])
        self.deOrthoMat = np.zeros((3,3))
        self.deOrthoMat[0,0] = lines[12]
        self.deOrthoMat[0,1] = lines[13]
        self.deOrthoMat[0,2] = lines[14]
        self.deOrthoMat[1,0] = lines[15]
        self.deOrthoMat[1,1] = lines[16]
        self.deOrthoMat[1,2] = lines[17]
        self.deOrthoMat[2,0] = lines[18]
        self.deOrthoMat[2,1] = lines[19]
        self.deOrthoMat[2,2] = lines[20]

        one_cube = np.zeros((int(xdim),int(ydim),int(zdim)))
        x,y,z = 0,0,0
        for p in range(21,numlines):
            line = lines[p].split(',')
            for y in range(0,int(ydim)):
                one_cube[x,y,z] = float(line[y])
            x += 1
            if x%xdim == 0:
                x = 0
                z += 1

        if self.den_type == 'Difference':
            self.loadDiffMatrix()
        else:
            self.whole_density = one_cube


    def loadDiffMatrix(self):
        f = open(self.file_name_diff, "r")
        lines = f.readlines()
        numlines = len(lines)
        f.close()
        # I am going to assume everything is the same but the numbers for now otherwise it doesn't make sense
        xdim, ydim, zdim = float(lines[9]), float(lines[10]), float(lines[11])
        one_cube = np.zeros((int(xdim), int(ydim), int(zdim)))
        x, y, z = 0, 0, 0
        for p in range(21, numlines):
            line = lines[p].split(',')
            for y in range(0, int(ydim)):
                one_cube[x, y, z] = float(line[y])
            x += 1
            if x % xdim == 0:
                x = 0
                z += 1

        self.whole_density = one_cube


    def saveMatrix(self):
        import pdb_eda # keep the library load to a minimum

        analyser = pdb_eda.densityAnalysis.fromPDBid(self.pdb_code)

        self.alpha = analyser.densityObj.header.alpha
        self.beta = analyser.densityObj.header.beta
        self.gamma = analyser.densityObj.header.gamma
        self.origin = analyser.densityObj.header.origin
        self.gridLength = analyser.densityObj.header.gridLength
        self.deOrthoMat = analyser.densityObj.header.deOrthoMat
        self.xyzInterval = analyser.densityObj.header.xyzInterval
        self.crsStart = analyser.densityObj.header.crsStart
        self.map2xyz = analyser.densityObj.header.map2xyz
        self.map2crs = analyser.densityObj.header.map2crs

        # Standardise density data by preferred methof
        #densdata = self.createZeroHundredDensity(densdata)

        # density matrix
        densdata = analyser.densityObj.density
        densdata, mind,spread = self.createModeFiftyDensity(densdata,-1,-1)
        self.writeDensityMatrix(densdata,self.file_name_dens)

        # density difference matrix
        densdiffdata = analyser.diffDensityObj.density
        densdiffdata,mind,spread = self.createModeFiftyDensity(densdiffdata,mind,spread) # the difference matrix is transformed by the same values as the density matrix
        self.writeDensityMatrix(densdiffdata,self.file_name_diff)



    def writeDensityMatrix(self,densdata,filename):
        x, y, z = densdata.shape
        with open(filename, 'w') as outfile:
            outfile.write(str(self.alpha) + '\n') #90.0
            outfile.write(str(self.beta)+ '\n') #117.81999969482422
            outfile.write(str(self.gamma)+ '\n') #90.0
            outfile.write(str(self.origin[0]) + ',' + str(self.origin[1]) + ',' + str(self.origin[2]) + '\n')
            outfile.write(str(self.gridLength[0]) + ',' + str(self.gridLength[1]) + ',' + str(self.gridLength[2]) + '\n')
            outfile.write(str(self.xyzInterval[0]) + ',' + str(self.xyzInterval[1]) + ',' + str(self.xyzInterval[2]) + '\n')
            outfile.write(str(self.crsStart[0]) + ',' + str(self.crsStart[1]) + ',' + str(self.crsStart[2]) + '\n')
            outfile.write(str(self.map2xyz[0]) + ',' + str(self.map2xyz[1]) + ',' + str(self.map2xyz[2]) + '\n')
            outfile.write(str(self.map2crs[0]) + ',' + str(self.map2crs[1]) + ',' + str(self.map2crs[2]) + '\n')
            outfile.write(str(x) + '\n')
            outfile.write(str(y) + '\n')
            outfile.write(str(z) + '\n')
            np.savetxt(outfile, self.deOrthoMat.ravel(), delimiter=',', fmt='%1.5f')
            for i in range(0, z):
                np.savetxt(outfile, densdata[0:x, 0:y, i], delimiter=',', fmt='%1.5f')

    def getElectronsAroundPoints(self,points): # the triple of points passed in
        ca = points[0]
        pa = points[1]
        pl = points[2]
        ce_electrons = round((self.getInterpolatedPointDensity(ca[0], ca[1], ca[2])), 4)
        pa_electrons = round((self.getInterpolatedPointDensity(pa[0], pa[1], pa[2])), 4)
        pl_electrons = round((self.getInterpolatedPointDensity(pl[0], pl[1], pl[2])), 4)
        return ([ce_electrons, pa_electrons, pl_electrons])

    def getInterpolatedPointDensity(self,x,y,z):
        # There would be 3 solutions but starting with just 1 and not suer I would have a way to choose which one anyway...
        x,y,z = round(x,8),round(y,8),round(z,8)
        crs = self.eda_xyz2crsCoord([x,y,z])
        c = crs[0]
        r = crs[1]
        s = crs[2]
        cl,cu = math.floor(c),math.ceil(c)
        rl,ru = math.floor(r),math.ceil(r)
        sl, su = math.floor(s), math.ceil(s)

        aafrac = self.getFraction([c, r, s], [cl, rl, sl], [cl, ru, sl])
        bbfrac = self.getFraction([c, r, s], [cu, rl, sl], [cu, ru, sl])
        ccfrac = self.getFraction([c, r, s], [cl, rl, su], [cl, ru, su])
        ddfrac = self.getFraction([c, r, s], [cu, rl, su], [cu, ru, su])
        abfrac = self.getFraction([c, r, s], [cl, rl, sl], [cu, rl, sl])
        acfrac = self.getFraction([c, r, s], [cl, rl, sl], [cl, rl, su])


        a1 = self.getPointDensityFromCrs([cl, rl, sl])
        a2 = self.getPointDensityFromCrs([cl, ru, sl])
        b1 = self.getPointDensityFromCrs([cu, rl, sl])
        b2 = self.getPointDensityFromCrs([cu, ru, sl])
        c1 = self.getPointDensityFromCrs([cl, rl, su])
        c2 = self.getPointDensityFromCrs([cl, ru, su])
        d1 = self.getPointDensityFromCrs([cu, rl, su])
        d2 = self.getPointDensityFromCrs([cu, ru, su])


        # interpolate as to bs and cs to ds then together
        adense,ap = self.getInterpVal(a1,a2,[cl,rl,sl],[cl,ru,sl],aafrac)
        bdense,bp = self.getInterpVal(b1,b2,[cu,rl,sl],[cu,ru,sl],bbfrac)
        cdense,cp = self.getInterpVal(c1,c2,[cl,rl,su],[cl,ru,su],ccfrac)
        ddense,dp = self.getInterpVal(d1,d2,[cu,rl,su],[cu,ru,su],ddfrac)

        #interpolates a to b and c to d
        abdense,abp = self.getInterpVal(adense,bdense,ap,bp,abfrac)
        cddense, cdp = self.getInterpVal(cdense,ddense,cp,dp,abfrac)
        #final
        dense, p = self.getInterpVal(abdense, cddense, abp, cdp, acfrac)
        #print(4, crs_density, a1, a2, b1, b2, c1, c2, d1, d2,dense)
        #print('Rounded=',sphere_density,'Interpolated=',dense)
        #return sphere_density
        return dense

    def eda_xyz2crsCoord(self, xyzCoord):
        """
        Convert the xyz coordinates into crs coordinates.
        :param xyzCoord: xyz coordinates.
        :type xyzCoord: A :py:obj:`list` of :py:obj:`float`
        :return: crs coordinates.
        :rtype: A :py:obj:`list` of :py:obj:`int`.
        """
        if self.alpha == self.beta == self.gamma == 90:
            #crsGridPos = [int(round((xyzCoord[i] - self.origin[i]) / self.gridLength[i])) for i in range(3)]
            crsGridPos = [int(round((xyzCoord[i] - self.origin[i]) / self.gridLength[i])) for i in range(3)]
            crsGridPos = [round((xyzCoord[i] - self.origin[i]) / self.gridLength[i]) for i in range(3)]
            crsGridPos = [(xyzCoord[i] - self.origin[i]) / self.gridLength[i] for i in range(3)]
        else:
            fraction = np.dot(self.deOrthoMat, xyzCoord)
            crsGridPos = [fraction[i] * self.xyzInterval[i] - self.crsStart[self.map2xyz[i]] for i in range(3)]
        return [crsGridPos[self.map2crs[i]] for i in range(3)]


    def getFraction(self, po, p1, p2):
        d1 = math.sqrt((po[0] - p1[0]) ** 2 + (po[1] - p1[1]) ** 2 + (po[1] - p1[1]) ** 2)
        d2 = math.sqrt((po[0] - p2[0]) ** 2 + (po[1] - p2[1]) ** 2 + (po[1] - p2[1]) ** 2)
        if d1 + d2 == 0:
            fraction = 0
        else:
            fraction = d1 / (d1 + d2)
        return (fraction)

    def getPointDensityFromCrs(self,crs):
        pd = self.whole_density[crs[2], crs[1], crs[0]]
        return(pd)

    def getInterpVal(self,v1,v2,p1,p2,fraction):
        v = v1 + fraction*(v2 - v1)
        x = p1[0] + fraction * (p2[0] - p1[0])
        y = p1[1] + fraction * (p2[1] - p1[1])
        z = p1[2] + fraction * (p2[2] - p1[2])
        return (v,[x,y,z])

    def createZeroHundredDensity(self,densdata):
        mind = 1000
        maxd = -1000
        x, y, z = densdata.shape
        for i in range(0,x):
            for j in range(0,y):
                for k in range(0,z):
                    mind = min(mind,densdata[i, j, k])
                    maxd = max(maxd, densdata[i, j, k])
        spread = float(maxd-mind)
        spread = 100.0/spread

        for i in range(0, x):
            for j in range(0, y):
                for k in range(0, z):
                    vald = densdata[i, j, k]
                    vald -= mind
                    vald *= spread
                    densdata[i, j, k] = vald
        # verify that the max and min are 0 and 100
        mind = 1000
        maxd = -1000
        for i in range(0, x):
            for j in range(0, y):
                for k in range(0, z):
                    mind = min(mind, densdata[i, j, k])
                    maxd = max(maxd, densdata[i, j, k])

        return densdata

    def createModeFiftyDensity(self,densdata, mind, spread):
        modeden = np.median(densdata.ravel())

        x, y, z = densdata.shape

        if mind == spread == -1: # if we pass in these values then do not recalc, ie for the difference
            mind = 1000
            maxd = -1000
            for i in range(0,x):
                for j in range(0,y):
                    for k in range(0,z):
                        mind = min(mind,densdata[i, j, k])
                        maxd = max(maxd, densdata[i, j, k])
            spread = float(modeden-mind)
            spread = 50.0/spread
        else:
            mind = 0 # surely we don't transpose the difference matrix that makes no sense?

        for i in range(0, x):
            for j in range(0, y):
                for k in range(0, z):
                    vald = densdata[i, j, k]
                    vald -= mind
                    vald *= spread
                    densdata[i, j, k] = vald

        return densdata, mind, spread





