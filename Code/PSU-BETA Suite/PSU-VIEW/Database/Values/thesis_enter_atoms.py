#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  Enter the geo_measures calculated by PSU. 
This is a 1-off at the beginning with all calculated data, but may be used if more measures are added.
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
            if c == 0 or c == 1 or c == 2 or c == 3:
                row = row + (str((df.iloc[r,c])),)                
            else:
                rval = float(df.iloc[r,c])
                rval = round(rval,3)
                row = row + (str(rval),)
            
        #print(row)
        csv_data.append(row)
            
    # Create SQL statement to find information for proteins from Leishmania
    

    sql = "REPLACE INTO protein_atom_b ("
    sql += "pdb_code,"
    sql += "atom_no,"
    sql += "occupant,"
    sql += "element,"
    sql += "xcoord,"
    sql += "ycoord,"
    sql += "zcoord,"
    sql += "occupancy,"    
    sql += "bfactor) VALUES ("
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
os. chdir("DataSets/Version2/23May20_High3/Atoms/")
arr = os.listdir()
print(arr)
i = 0
for fl in arr:
    i += 1
    print(i,fl)
    try:
      enterOneValueFile(fl)
    except:
      print('error', fl)
