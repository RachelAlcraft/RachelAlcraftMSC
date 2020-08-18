'''
Author: RAchel Alcraft
Created: 4/07/20
This file takes a format of csv file more inuitive than atom coordinates and first uses biopython to get the coordinates
pdb_code, central_atom_no, parallel_atom_no, planar_atom_no
'''

import pandas as pd

from datetime import datetime



# Some global variables



def getOneAtoms(pdb_code,ca,pa,pl):
    import pdb_eda as eda
    analyser = eda.densityAnalysis.fromPDBid(pdb_code)  # force the download in analyser format
    print("Date=", analyser.pdbObj.header.date)
    import Bio.PDB as bio
    parser = bio.PDBParser()
    structure = parser.get_structure(pdb_code, 'pdb_data/pdb' + pdb_code + '.ent')
    model = structure[0]

    # central atom
    chain = model[ca[0]]
    for residue in chain:
        res_no = residue.get_full_id()[3][1]
        # print(res_no,ca[1])
        if str(res_no) == str(ca[1]):
            ca_atom = residue[ca[2]]
            break
    # parallel atom
    chain = model[pa[0]]
    for residue in chain:
        res_no = residue.get_full_id()[3][1]
        # print(res_no, pa[1])
        if str(res_no) == str(pa[1]):
            pa_atom = residue[pa[2]]
            break
    # planar atom
    chain = model[pl[0]]
    for residue in chain:
        res_no = residue.get_full_id()[3][1]
        # print(res_no, pl[1])
        if str(res_no) == str(pl[1]):
            pl_atom = residue[pl[2]]
            break

    ca_coords = ca_atom.get_vector()
    pa_coords = pa_atom.get_vector()
    pl_coords = pl_atom.get_vector()

    del analyser
    return ([ca_coords, pa_coords, pl_coords])


def convertAtomsToCoords(atoms_file):
    '''
    :param atoms_file:
    :return: data file in coordinate format
    Description, the csv file is in the foprmat
    pdb_code, central_atom, parallel_atom, planar_atom
    where each atom is in the format
    chain:amino_no:atom_name
    in order to be able to get the coord info from biopython
    atom = structure[0]['A'][100]['CA']
    '''
    # create empty datafram
    print(datetime.now().strftime("%H:%M:%S"), 'Converting atoms to coordinates')
    pdb_data_coords = pd.DataFrame(columns=('tag','pdb_code','c_atom_x','c_atom_y','c_atom_z','pa_atom_x','pa_atom_y','pa_atom_z','pl_atom_x','pl_atom_y','pl_atom_z'))
    bad_data_coords = pd.DataFrame(columns=('tag','pdb_code','x'))

    pdb_data_atoms = pd.read_csv(atoms_file)
    print(pdb_data_atoms)

    try:
        pdb_data_coords = pd.read_csv(atoms_file + "_coords.csv")

    except:
        pdb_data_coords = pd.DataFrame(columns=('tag','pdb_code', 'c_atom_x', 'c_atom_y', 'c_atom_z', 'pa_atom_x', 'pa_atom_y', 'pa_atom_z', 'pl_atom_x', 'pl_atom_y','pl_atom_z'))

    try:
        bad_data_coords = pd.read_csv(atoms_file + "_bad.csv")
    except:
        bad_data_coords = pd.DataFrame(columns=('tag','pdb_code','x'))




    rows = len(pdb_data_atoms.index)

    for i in range(0, rows):
        pdb_code = pdb_data_atoms.iloc[i, 0].lower()
        col1 = pdb_data_atoms.iloc[i, 1].lower()
        col2 = pdb_data_atoms.iloc[i, 2].lower()
        col3 = pdb_data_atoms.iloc[i, 3].lower()

        tag = pdb_code + '-' + col1 + '-' + col2 + '-' + col3

        new_file_name = atoms_file + '_coords.csv'
        bad_file_name = atoms_file + '_bad.csv'

        try:
        #if True:
            got_coords = False
            dfrow = pdb_data_coords[pdb_data_coords['tag'] == tag]
            dfbad = bad_data_coords[bad_data_coords['tag'] == tag]
            if (len(dfrow.index) + len(dfbad.index)) > 0:
                got_coords = True
                print(datetime.now().strftime("%H:%M:%S"), i,'/',rows,'already converted',pdb_code)
            if not got_coords:
                print(datetime.now().strftime("%H:%M:%S"), i, '/', rows, pdb_code)

                #url = "http://www.ebi.ac.uk/pdbe/coordinates/files/" + pdb_code + '.ent'
                #wget.download(url, 'pdb_data/pdb' + pdb_code + '.ent')

                print(pdb_data_atoms.iloc[i, 1])
                ca = (pdb_data_atoms.iloc[i, 1]).split(':')
                pa = (pdb_data_atoms.iloc[i, 2]).split(':')
                pl = (pdb_data_atoms.iloc[i, 3]).split(':')

                ca_coords,pa_coords,pl_coords = getOneAtoms(pdb_code,ca,pa,pl)

                nextrow = len(pdb_data_coords)
                pdb_data_coords.loc[nextrow] = (tag,pdb_code, ca_coords[0],ca_coords[1],ca_coords[2],pa_coords[0],pa_coords[1],pa_coords[2],pl_coords[0],pl_coords[1],pl_coords[2])
                # print each time due to memory errors we don;t want to lose everything
                new_file_name = atoms_file + '_coords.csv'
                pdb_data_coords.to_csv(new_file_name, index=False)
                #print(pdb_data_coords)
                structure = None
                model = None
                chain = None
                #del structure
        except:
            print('Error getting',pdb_code)
            nextrow = len(bad_data_coords)
            bad_data_coords.loc[nextrow] = (tag,pdb_code,'x')
            bad_data_coords.to_csv(bad_file_name, index=False)
            # and remove the pdb from future use

    return (new_file_name)


