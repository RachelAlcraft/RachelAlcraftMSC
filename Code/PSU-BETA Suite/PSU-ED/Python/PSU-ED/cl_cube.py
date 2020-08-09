'''
Author: Rachel Alcraft
Created: 30/06/20
'''
import numpy as np
import math
import cl_transformation as t

PI = np.pi

class cube:
    def __init__(self):
        self.length = 1
        self.gap = 0.1

    def init(self,length,gap):
        self.length = length
        self.matrix_length = (self.length * 2) + 1 # The length is actually created from centre plus and minus so it is length*2 + 1
        self.gap = gap
        self.cubes = []
    def generateCube(self,central_atom,parallel_atom,planar_atom,middle,middle_slices):
        #numpy arrays cannot store tuples so we need a cube per coordinate
        vectorA = np.array([central_atom[0], central_atom[1], central_atom[2]])
        vectorB = np.array([parallel_atom[0]-central_atom[0],parallel_atom[1]-central_atom[1],parallel_atom[2]-central_atom[2]])
        vectorC = np.array([planar_atom[0]-central_atom[0], planar_atom[1]-central_atom[1], planar_atom[2]-central_atom[2]])

        #Create the transformation that would take us from whereever the atoms live to the origin.
        #We will then apply this transformation to all the coordinates in the cube
        self.transformation = t.transformation(central_atom,parallel_atom,planar_atom)
        cube_x, cube_y, cube_z = self.generateEmptyCube()
        count = 0
        for i in range(0,self.matrix_length):
            for j in range(0, self.matrix_length):
                for k in range(0, self.matrix_length):

                    x = cube_x[i,j,k]
                    y = cube_y[i,j,k]
                    z = cube_z[i,j,k]
                    count += 1
                    if count%500000 == 0:
                        print('\t\t\t\t applying',i,j,k)
                    if middle_slices == -1 or (abs(i - middle) <= middle_slices) or (abs(j - middle) <= middle_slices) or (abs(k - middle) <= middle_slices):
                        x, y, z = self.transformation.applyTransformation([x, y, z],False)
                    else:
                        x, y, z = [0,0,0] # we don't waste time transforming coordinatres we are not going to look at
                    cube_x[i,j,k] = x
                    cube_y[i,j,k] = y
                    cube_z[i,j,k] = z

        return([cube_x, cube_y, cube_z])

    def addCube(self,cube,pdb_code, tag, central_atom,ce_electrons, parallel_atom, pa_electrons, planar_atom, pl_electrons):
        self.cubes.append([cube,pdb_code,tag, central_atom,ce_electrons, parallel_atom, pa_electrons, planar_atom, pl_electrons])

    def getSummedCubes(self):

        summed_cubes = np.zeros((self.matrix_length, self.matrix_length, self.matrix_length))
        maxi = -1000
        mini = 1000
        for cube in self.cubes:
            for i in range(0,self.matrix_length):
                for j in range(0, self.matrix_length):
                    for k in range(0, self.matrix_length):
                        summed_cubes[i,j,k] += cube[0][i,j,k]
                        mini = min(mini, cube[0][i,j,k])
                        maxi = max(maxi, cube[0][i,j,k])
        maxd = -1000
        mind = 1000

        for i in range(0, self.matrix_length):
            for j in range(0, self.matrix_length):
                for k in range(0, self.matrix_length):
                    mind = min(mind,summed_cubes[i, j, k])
                    maxd = max(maxd, summed_cubes[i, j, k])

        return([summed_cubes,mind,maxd,mini,maxi]) # the min max of the sum and the inputs

    def getSummedCubesTransformed(self):
        trans_cubes1 = np.zeros((self.matrix_length, self.matrix_length, self.matrix_length))
        #trans_cubes2 = np.zeros((self.matrix_length, self.matrix_length, self.matrix_length))
        mind = 1000
        for cube in self.cubes:
            for i in range(0,self.matrix_length):
                for j in range(0, self.matrix_length):
                    for k in range(0, self.matrix_length):
                        mind = min(mind,cube[0][i,j,k])
        # transform everything by mind + 1 so 1 is the minumium, or 0.0001 is the minimum? For the density difference it would be better.
        for cube in self.cubes:
            for i in range(0,self.matrix_length):
                for j in range(0, self.matrix_length):
                    for k in range(0, self.matrix_length):
                        #summed_cubes[i,j,k] += math.sqrt(cube[0][i,j,k]+1 - mind)
                        val = math.log(cube[0][i, j, k] + 1 - mind)
                        trans_cubes1[i, j, k] += val
                        #trans_cubes2[i, j, k] += math.log(val + 1)
                        #summed_cubes[i,j,k] += (cube[0][i,j,k]+1 - mind)**(1/3)

        maxd = -1000
        mind = 1000
        for i in range(0, self.matrix_length):
            for j in range(0, self.matrix_length):
                for k in range(0, self.matrix_length):
                    mind = min(mind, trans_cubes1[i, j, k])
                    maxd = max(maxd, trans_cubes1[i, j, k])

        return([trans_cubes1,mind,maxd])


    def generateEmptyCube(self):
        cube_x = np.zeros((self.matrix_length,self.matrix_length,self.matrix_length))
        cube_y = np.zeros((self.matrix_length,self.matrix_length,self.matrix_length))
        cube_z = np.zeros((self.matrix_length,self.matrix_length,self.matrix_length))

        for i in range(0,self.matrix_length):
            for j in range(0, self.matrix_length):
                for k in range(0, self.matrix_length):
                    x = (i - self.length) * self.gap
                    y = (j - self.length) * self.gap
                    z = (k - self.length) * self.gap
                    cube_x[i,j,k] = x
                    cube_y[i,j,k] = y
                    cube_z[i,j,k] = z
                    #print(i,j,k,'=',x,y,z)
        return ([cube_x,cube_y,cube_z])

