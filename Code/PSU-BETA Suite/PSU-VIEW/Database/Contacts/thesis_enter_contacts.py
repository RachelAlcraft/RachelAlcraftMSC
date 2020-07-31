#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      28/05/2020
Function:  Enter the geo_contact calculated by PSU. 
format is
pdb_code,amino_code,amino_no,chain,residue_no,atom_no,occupant,ss_psu,amino_code_b,amino_no_b,chain,residue_no_b,atom_no_b,occupant_b,ss_psu_b,geo_atoms,geo_type,geo_value
5NQO,CYS,24,A,24,174,A,A,CYS,28,A,28,205,A,A,SG-SG,CONTACT,4.28121
"""

import pymysql.cursors
import pandas as pd
import os

#########################################################################

def enterOneValueFile(file_name):
# Set parameters
    dbname   = "ab002"
    dbhost   = "hope"
    dbuser   = "ab002"
    dbpass   = "4603v58-3"
    port     = 3306

    # Load csv file for write
    df = pd.read_csv(file_name)
    #print(df)

    # create list of tuples
    csv_data = []
    rows = len(df.index)
    cols = len(df.columns)
    print(rows)
    print(cols)
    for r in range(0,rows):
        row = ()
        for c in range(0,cols):            
            row = row + (str((df.iloc[r,c])),)                
        #print(row)
        csv_data.append(row)

            
    # Create SQL statement to find information for proteins from Leishmania    
    sql = "REPLACE INTO geo_contact ("
    sql += "pdb_code,"
    sql += "amino_code,"
    sql += "amino_no,"
    sql += "chain,"
    sql += "residue_no,"
    sql += "atom_no,"
    sql += "occupant,"
    sql += "ss_psu,"
    sql += "amino_code_b,"
    sql += "amino_no_b,"
    sql += "chain_b,"
    sql += "residue_no_b,"
    sql += "atom_no_b,"
    sql += "occupant_b,"
    sql += "ss_psu_b,"
    sql += "geo_atoms,"
    sql += "geo_type,"    
    sql += "geo_value) VALUES ("       
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"    
    sql += "%s)"
    
    # Connect to the database
    db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname)
    # Create a cursor and execute the SQL on it
    cursor = db.cursor()    
    cursor.executemany(sql,csv_data)
    db.commit()        
    cursor.close()


#########################################################
os. chdir("DataSets/Version1/29May20")
arr = os.listdir()
print(arr)
i = 0
for fl in arr:
    i += 1
    print(i,fl)
    #try:
    enterOneValueFile(fl)
    #except:
    #    print('error', fl)
