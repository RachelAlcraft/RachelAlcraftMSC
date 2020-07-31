from Bio.PDB import PDBParser
from copy_dssp import DSSP as HSSP
from Bio.PDB.DSSP import DSSP
import pandas as pd
from datetime import datetime

'''
    H = α-helix
    B = residue in isolated β-bridge
    E = extended strand, participates in β ladder
    G = 3-helix (310 helix)
    I = 5 helix (π-helix)
    T = hydrogen bonded turn
    S = bend 
    making - U = unknown

    output per residue
    (3,     'L',    'B',           0.524390243902439, -62.4, 144.9, -2,-0.3,   514,-0.3,   514, -0.2,      2, -0.1)
    RESIDUE AA      STRUCTURE       BP1                 BP2     ACC   N-H-->O   O-->H-N     N-H-->O      O-->H-N
'''

# ################ ENTER INPUTS #######################

file_name = '2019_in.csv'
file_out = '2019_dssp'
min = 3314
max = -1

#pdb_local = "/home/rachel/Documents/Bioinformatics/DSSP/local-pdb/"
file_out = file_out + str(max) + '.csv'
pdb_local = "/home/rachel/Documents/Bioinformatics/DSSP/pdbdata/"
file_dir = '/home/rachel/Documents/Bioinformatics/DSSP/'


# Housekeepint

start = datetime.now()


p = PDBParser()
pdb_out_dssp = pd.DataFrame(columns=('pdb_code','chain','occupant','amino_no','dssp'))

pdb_names = pd.read_csv(file_dir + file_name)
rows = len(pdb_names.index)
if min == -1:
    min = 0
if max == -1:
    max = rows

for i in range(min, max):
    pdb_code = pdb_names.iloc[i, 0].upper()
    print(i,'/',rows,pdb_code)

    #pdb_code = '6NU8'
    pdb_file = pdb_local + pdb_code + ".pdb"
    #print(pdb_file)
    structure = p.get_structure(pdb_code, pdb_file)
    model = structure[0]
    #for chain in model:
        #for residue in chain:
            #for atom in residue:
                #print(atom)

    dssp = DSSP(model,pdb_file)
    #print(dssp)
    #dssp['A']

    for akey in  list(dssp.keys()):
        chain = akey[0]
        res_no = akey[1][1]

        row = dssp[akey]
        #print(row)
        ss = row[2]
        if ss == '-':
            ss = 'U'

        nextrow = len(pdb_out_dssp)
        pdb_out_dssp.loc[nextrow] = (pdb_code, chain,'A',res_no,ss)

    # print each pdb due to memory errors we don;t want to lose everything
    pdb_out_dssp.to_csv(file_dir + file_out, index=False)

end = datetime.now()
taken = end - start
print('time taken=',taken)
# output file: pdb_code,occupant'chain,amino_no,dssp
