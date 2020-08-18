

#import pdb_eda
#import Bio.PDB as bio
import math
#import cl_conversions

import numpy as np
import scipy.spatial

class density:
    def __init__(self, pdb_code,dens_data):
        self.pdb_code = pdb_code
        self.densdata = dens_data  # self.conversions.densities[pdb_code]

    def init(self,pdb_code,conversion,radius):
        self.pdb_code = pdb_code
        self.success = True
        #self.conversions = cl_conversions.densityConverted(pdb_code)

    def getDensityCube(self,xs,ys,zs,middle,middle_slices):
        xl,yl,zl = xs.shape # they are all cubes the same size
        density_cube = np.zeros((xl,yl,zl))
        min_e = 1000
        max_e = -1000
        for i in range(0,xl):
            for j in range(0, yl):
                for k in range(0, zl):
                    x = xs[i,j,k]
                    y = ys[i,j,k]
                    z = zs[i,j,k]
                    point_density = 0
                    sphere_density = 0
                    if middle_slices == -1 or (abs(i-middle) <= middle_slices) or (abs(j-middle) <= middle_slices) or (abs(k-middle) <= middle_slices):
                        #if self.radius == 0:
                        sphere_density = self.getInterpolatedPointDensity(x,y,z)
                        #else:
                        #    sphere_density = self.analyser.densityObj.getTotalDensityFromXyz([x,y,z], self.radius)
                        min_e = min(min_e,sphere_density)
                        max_e = max(max_e, sphere_density)
                        #print('\t\tDensity for:',x,y,z,'=',point_density,'min=',min_e,'max=',max_e)
                    density_cube[i,j,k] = sphere_density

        return([density_cube,min_e,max_e])



    def getElectronsAroundPoints(self,points): # the triple of points passed in
        return (self.densdata.getElectronsAroundPoints(points))

    def getInterpolatedPointDensity(self,x,y,z):
        return (self.densdata.getInterpolatedPointDensity(x,y,z))









