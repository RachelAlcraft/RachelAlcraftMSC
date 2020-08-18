
'''
Author: Rachel Alcraft
Created: 13/07/20
Description: A selection of different methods for creating a density conversion factor
This does pre-suppose a single conversion factor for the entire strucutre
'''


import pandas as pd
import pdb_eda as eda

class densityConverted:
    def __init__(self,pdb_code):
        '''
        :param conversions_file: the file name where the pdb
        There are the following possible methods, which currently are chosen in the code
        0 = The chain median as per the pdd_eda linrary
        1 = My first method, changging all the density values in a density matric to be between 0 and 11
        2 = My electron approx method, approximating the number fo electrons from the number of atoms and scaling the density matrix with that
        # The class therefore handles the density values itself using the crs coordinates and contains a dictionary of
        [pdb_code,converted matrix]
        '''
        print('Creating converted density matrix',pdb_code)
        self.method = 1
        self.densities = {}

        if pdb_code not in self.densities:
            # try to get the conversion from the saved file
            if self.method == 1:
                print('Create ZeroHundredDensity...')
                self.createZeroHundredDensity(pdb_code)
                print('...Created')
            elif self.method == 2:
                self.createApproxAtomsDensity(pdb_code)

    def createZeroHundredDensity(self,pdb_code):
        try:
            analyser = eda.densityAnalysis.fromPDBid(pdb_code)
            densdata = analyser.densityObj.density
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
            print('Created Zero100 Density',pdb_code,mind,maxd)
            self.densities[pdb_code] = densdata
            del analyser
        except:
            print('!!! Cannot create Zero100 Density', pdb_code)


    def createApproxAtomsDensity(self,pdb_code):
        conversion = 1.0
        try:
            analyser = eda.densityAnalysis.fromPDBid(pdb_code)
            analyser.aggregateCloud()
            densdata = analyser.densityObj.density
            atoms = analyser.atomList()
            numatoms = len(atoms)
            x, y, z = densdata.shape
            for i in range(0, x):
                for j in range(0, y):
                    for k in range(0, z):
                        vald = densdata[i, j, k]
                        vald = vald/numatoms
                        vald *= 100.0
                        densdata[i, j, k] = vald
            # For interest, check what the max and min are
            mind = 1000
            maxd = -1000
            for i in range(0, x):
                for j in range(0, y):
                    for k in range(0, z):
                        mind = min(mind, densdata[i, j, k])
                        maxd = max(maxd, densdata[i, j, k])
            print('Created Atoms Density', pdb_code, mind, maxd)
            self.densities[pdb_code] = densdata
        except:
            print('!!! Cannot create Atoms Density', pdb_code)


def getDensityValue(self,pdb_code,crs):
    return(self.densities[pdb_code][crs[2],crs[1],crs[0]])
