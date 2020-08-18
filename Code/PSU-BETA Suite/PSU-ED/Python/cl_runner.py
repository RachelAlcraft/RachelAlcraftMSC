'''
Author: Rachel Alcraft
Created 08/08/20
Description: Manage the input information and data to start a density image run
Features include:
Is the input file
    a single corrdinate
    a list of coordinates
    a list of atom definitions
Also inputs will choose whether to create the entire cubes which has a large impact on speed
'''
import pandas as pd
from datetime import datetime
import fu_convertAtomsToCoords as convert
import cl_cube
import cl_density
import cl_image
import cl_files
import cl_matrix
import numpy as np
import cl_densityFile


class runner:
    def __init__(self,inputs):
        self.start = datetime.now()
        self.inputs = inputs
        self.coordlist = []
        self.cube_maker = cl_cube.cube()
        self.image_summary = cl_image.htmlImageString()
        dir_tag = self.inputs.getRunSummary()
        self.file_maker = cl_files.files(self.inputs.out_dir,dir_tag)



    def runCreateCoordsFile(self):
        if self.inputs.in_file == 'single':
            self.coordlist = [self.inputs.coords[0],self.inputs.coords[1],1,self.inputs.coords[2],self.inputs.coords[3],self.inputs.coords[4]]
        else:
            # Does the input file exist in the coordinate format
            # Also does the original names file exist for annotation
            coords_exists = True
            try:
                input_data_coords = pd.read_csv(self.inputs.in_file + "_coords.csv")
            except:
                coords_exists = False
            names_exists = True
            try:
                input_data_names = pd.read_csv(self.inputs.in_file)
            except:
                names_exists = False

            convert.convertAtomsToCoords(self.inputs.in_file)
            input_data_coords = pd.read_csv(self.inputs.in_file + "_coords.csv")

            rows = len(input_data_coords.index)
            for i in range(0, rows):
                tag = input_data_coords.iloc[i, 0]
                pdb_code = input_data_coords.iloc[i, 1]
                print(i,rows,pdb_code)
                central_atom = [input_data_coords.iloc[i, 2], input_data_coords.iloc[i, 3], input_data_coords.iloc[i, 4]]
                parallel_atom = [input_data_coords.iloc[i, 5], input_data_coords.iloc[i, 6], input_data_coords.iloc[i, 7]]
                planar_atom = [input_data_coords.iloc[i, 8], input_data_coords.iloc[i, 9], input_data_coords.iloc[i, 10]]
                desc_ce = ''
                desc_pa = ''
                desc_pl = ''
                #if names_exists:
                #    desc_ce = input_data_names.iloc[i, 1]
                #    desc_pa = input_data_names.iloc[i, 2]
                #    desc_pl = input_data_names.iloc[i, 3]
                #    tag += "-" + desc_ce + "-" + desc_pa + "-" + desc_pl
                # dummy value for conversion factor of 1
                self.coordlist.append([pdb_code,tag, 1,central_atom, parallel_atom,planar_atom])  # pdb_code, tag,conversion,central atom, parallel atom, planar atom
            print(self.coordlist)


    def runCreateEachDensityMatrix(self):
        count = 0
        rows = len(self.coordlist)
        for row in self.coordlist:  # # pdb_code, tag,conversion,central atom, parallel atom, planar atom
            count += 1
            pdb_code = row[0]
            self.log([count, rows, 'Creating density matrix', pdb_code])
            psu_mat = cl_densityFile.densityFile(pdb_code,self.inputs.difference,'psu_density/')
            if not psu_mat.exists():
                psu_mat.saveMatrix()


    def runCreateEachMatrix(self):
        count = 0
        rows = len(self.coordlist)
        for row in self.coordlist:  # # pdb_code, tag,conversion,central atom, parallel atom, planar atom
            count += 1
            pdb_code = row[0]
            tag = row[1]
            ca = row[3]
            pa = row[4]
            pl = row[5]
            self.log([count,rows,'Creating matrix',pdb_code])
            fn = self.inputs.getFileName(count, rows, 'matrix', 'csv')
            dens_mat = cl_densityFile.densityFile(pdb_code,self.inputs.difference,'psu_density/')
            if dens_mat.exists():
                dens_mat.loadMatrix()
                run_one = cl_matrix.psu_matrix(pdb_code, fn,self.file_maker,tag,ca, pa, pl,dens_mat)
                if not run_one.existsMatrix():
                    densdata, mind,maxd,ce_electrons, pa_electrons, pl_electrons = run_one.createMatrix(self.inputs.sides,self.inputs.num_slices,self.inputs.gaps,self.inputs.radius)
                    # save each one as a file in otself with its own max min
                    im_maker = cl_image.htmlImageString()
                    fni = self.inputs.getFileName(count, rows, 'image', 'html')
                    im_maker.init(self.inputs.getTag(), self.inputs.sides, self.inputs.gaps,self.inputs.difference)
                    im_maker.addCube([densdata, pdb_code, tag, ca, ce_electrons, pa, pa_electrons, pl, pl_electrons], dens_mat.whole_density,self.inputs.sides, self.inputs.num_slices, mind, maxd)
                    html = im_maker.getFinalString()
                    self.file_maker.print(html, fni)
                    del im_maker
                del run_one

    def runGetEachMatrixAndSum(self):
        cube_maker = cl_cube.cube()
        cube_maker.init(self.inputs.sides, self.inputs.gaps)
        image_summary = cl_image.htmlImageString()
        image_summary.init(self.inputs.getTag(), self.inputs.sides, self.inputs.gaps,self.inputs.difference)

        count = 0
        rows = len(self.coordlist)
        for row in self.coordlist:  # # pdb_code, tag,conversion,central atom, parallel atom, planar atom
            count += 1
            pdb_code = row[0]
            tag = row[1]
            ca = row[3]
            pa = row[4]
            pl = row[5]
            self.log([count,rows,'Summing matrix',pdb_code])
            fn = self.inputs.getFileName(count, rows, 'matrix', 'csv')
            run_one = cl_matrix.psu_matrix(pdb_code, fn,self.file_maker,tag,ca, pa, pl,None)
            if run_one.existsMatrix():
                denscube, ce_electrons, pa_electrons, pl_electrons = run_one.getMatrix()
                cube_maker.addCube(denscube, pdb_code, tag, ca, ce_electrons, pa, pa_electrons, pl, pl_electrons)

        # 5 Outputs
        # 1 The summed matrix
        summed_cubes, mind, maxd,mini,maxi = cube_maker.getSummedCubes()
        fn = self.inputs.getFileName(0, rows, 'matrix', 'csv')
        self.file_maker.saveMatrix(summed_cubes, fn)

        # 2 The summed image
        im_maker = cl_image.htmlImageString()
        im_maker.init(self.inputs.getTag(), self.inputs.sides, self.inputs.gaps,self.inputs.difference)
        summed_cube_tuple = [summed_cubes, 'SUM', self.inputs.tag]
        im_maker.addCube(summed_cube_tuple, None,self.inputs.sides, self.inputs.num_slices, mind, maxd)
        html = im_maker.getFinalString()
        fni = self.inputs.getFileName(0, rows, 'image', 'html')
        self.file_maker.print(html, fni)

        # 3 The summed transformed image
        trans1, mine, maxe = cube_maker.getSummedCubesTransformed()
        fn1 = self.inputs.getFileName(0, rows, 'matrixX', 'csv')
        self.file_maker.saveMatrix(trans1, fn1)

        # 4 The summed transformed image
        im_maker = cl_image.htmlImageString()
        im_maker.init(self.inputs.getTag(), self.inputs.sides, self.inputs.gaps,self.inputs.difference)
        trans_cube_tuple = [trans1, 'TRANS', self.inputs.tag]
        im_maker.addCube(trans_cube_tuple, None, self.inputs.sides, self.inputs.num_slices, mine, maxe)
        html = im_maker.getFinalString()
        fni = self.inputs.getFileName(0, rows, 'imageX', 'html')
        self.file_maker.print(html, fni)

        # 5 The summary images with a central slice for each sample
        for cube in cube_maker.cubes:
           image_summary.addCube(cube,None,self.inputs.sides, 0, mini,maxi)


        fni = self.inputs.getFileName(0, rows, 'all', 'html')
        image_summary.addCube(summed_cube_tuple, None, self.inputs.sides, 0, -1, -1)
        image_summary.addCube(trans_cube_tuple, None, self.inputs.sides, 0, -1, -1, 'transformed values')
        html = image_summary.getFinalString()
        self.file_maker.print(html, fni)

    def end(self):
        end = datetime.now()
        self.file_maker.end(self.start,end)

    def log(self,message):
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), message)

