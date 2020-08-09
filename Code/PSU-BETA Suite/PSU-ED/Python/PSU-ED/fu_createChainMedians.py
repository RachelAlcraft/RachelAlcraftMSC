'''
Author: RAchel Alcraft
Created: 4/07/20
Description: This creates a csv file of chainMedians from the pda_edm library
Each pdb file taskes about 5 minutes to caluclate the median but it is always the same, so best to make it seperate and use via a config file
'''

import pandas as pd
import pdb_eda as eda
from datetime import datetime
import Bio.PDB as bio

elements_map = {('C',6),('N',7),('O',8)}


def createChainMedians(pdb_input, chain_median_file,useMyMethod):
    start = datetime.now()

    median_data = None
    try:
        median_data = pd.read_csv(chain_median_file)
    except:
        print('File does not exist, creating...',chain_median_file)
        median_data = pd.DataFrame(columns=('pdb_code', 'chain_median'))

    pdb_data = pd.read_csv(pdb_input)

    rows = len(pdb_data.index)
    for i in range(0, rows):
        pdb_code = str(pdb_data.iloc[i, 0].upper())
        # try to get the chainMedian from the saved file
        dfrow = median_data[median_data['pdb_code'] == pdb_code]
        if len(dfrow.index) == 0: # then we need to add it
            pdb_code = str(pdb_data.iloc[i, 0].lower())
            print(datetime.now().strftime("%H:%M:%S"),i,'/',rows,' - Loading chainMedian for', pdb_code)
            try:
                analyser = eda.densityAnalysis.fromPDBid(pdb_code)
                analyser.aggregateCloud()
                chainMedian = 0
                if useMyMethod == True:
                    total_density = 0
                    densdata = analyser.densityObj.density
                    electrons = 0
                    x, y, z = densdata.shape
                    for i in range(0,x):
                        for j in range(0, y):
                            for k in range(0, z):
                                total_density += densdata[i,j,k]

                    atoms = analyser.atomList()
                    for atom in atoms:
                        element = atom.element
                        occ = atom.occupancy
                        bfac = atom.bfactor
                        if element in elements_map: # for now just ignore it otherwise, this is obviously only a first cut!
                            electrons += elements_map[element]

                    chainMedian = total_density/electrons
                    print(total_density, electrons, chainMedian)
                else:
                    #analyser.aggregateCloud()
                    chainMedian = analyser.chainMedian
                print('\t',datetime.now().strftime("%H:%M:%S"), pdb_code, chainMedian)

                nextrow = len(median_data)
                median_data.loc[nextrow] = (pdb_code.upper(),chainMedian)

                # it might seem inefficient, but the chainMedian takes about 5 minutes so I want to print out every time
                median_data.to_csv(chain_median_file,index=False)
                analyser = None
                del analyser
            except:
                # no structure factors perhaps
                print("No density for",pdb_code)
        else:
            print("\t\t\tchainMedian:", pdb_code)

    end = datetime.now()
    print('Time taken=',end-start)
