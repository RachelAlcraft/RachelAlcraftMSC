'''
Author: Rachel Alcraft
Created:
'''

import pandas as pd
import cl_cube
import cl_density
import numpy as np

class psu_matrix:
    def __init__(self,pdb_code, filename,file_maker,tag,c_atom, pa_atom, pl_atom,dens_mat):
        self.pdb_code = pdb_code
        self.filename = filename
        self.exists = False
        self.tag = tag
        self.central_atom = c_atom
        self.linear_atom = pa_atom
        self.planar_atom = pl_atom
        self.file_maker = file_maker
        self.density_matrix = dens_mat

    def existsMatrix(self):
        try:
            file_path = self.file_maker.getFilePath(self.filename)
            f = open(file_path, "r")
            print('File already exists', self.filename)
            self.exists = True
        except:
            print('File does not exist', self.filename)
            self.exists = False
        return self.exists


    def createMatrix(self,sides,slices,gaps,radius):
        cube_maker = cl_cube.cube()
        cube_maker.init(sides, gaps)
        xs, ys, zs = cube_maker.generateCube(self.central_atom, self.linear_atom, self.planar_atom, sides, slices)

        density_maker = cl_density.density('unset',self.density_matrix)
        density_maker.init(self.pdb_code, 1, radius)
        self.wholecube = density_maker.densdata
        ce_electrons, pa_electrons, pl_electrons = density_maker.getElectronsAroundPoints([self.central_atom, self.linear_atom, self.planar_atom])
        density_cube, min_e, max_e = density_maker.getDensityCube(xs, ys, zs, sides, slices)
        self.densdata = density_cube
        self.minmax = [min_e,max_e]
        # MATRIX save to the formatted file we want to use
        self.file_maker.saveMatrix(density_cube, self.filename)
        self.file_maker.saveMatrixInfo([self.tag,ce_electrons, pa_electrons, pl_electrons], self.filename)
        return([density_cube,min_e,max_e,ce_electrons, pa_electrons, pl_electrons])

    def getMatrix(self):
        file_path = self.file_maker.getFilePath(self.filename)
        f = open(file_path, "r")
        lines = f.readlines()
        numlines = len(lines)
        f.close()
        xdim,ydim,zdim = float(lines[0]),float(lines[1]),float(lines[2])
        one_cube = np.zeros((int(xdim),int(ydim),int(zdim)))
        x,y,z = 0,0,0
        for p in range(3,numlines):
            line = lines[p].split(',')
            for y in range(0,int(ydim)):
                one_cube[x,y,z] = float(line[y])
            x += 1
            if x%xdim == 0:
                x = 0
                z += 1
        self.densdata = one_cube

        ff = open(file_path + '_info.txt', "r")
        infoline = ff.readlines()[0].split(',')
        f.close()
        return [one_cube,infoline[1],infoline[2],infoline[3]]





