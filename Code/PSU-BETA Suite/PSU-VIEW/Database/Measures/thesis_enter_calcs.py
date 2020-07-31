#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  Enter the pdb_file file into the database, this would only be done at the beginning and if there were any config changes 
"""

import pymysql.cursors
import pandas as pd

#########################################################################

def enter_sets(filename,setname,status):

    # Set parameters
    dbname   = "ab002"
    dbhost   = "hope"
    dbuser   = "ab002"
    dbpass   = "4603v58-3"
    port     = 3306

    # Load csv file for write
    df = pd.read_csv(filename)
    print(df)

    # create list of tuples
    csv_data = []
    rows = len(df.index)
    cols = len(df.columns)
    print(rows)
    print(cols)
    for r in range(0,rows):
        row = ()
        for c in range(0,4):            
            row = row + (str((df.iloc[r,c])),)    
        
        csv_data.append(row)
    print(csv_data)

    # Create SQL statement to find information for proteins from Leishmania
    sql = "REPLACE INTO geo_calcs ("#) VALUES "
    sql += "amino_code,"
    sql += "calc_type,"
    sql += "calc_atoms," 
    sql += "calc_alias) VALUES ("
    sql += "%s,"
    sql += "%s,"
    sql += "%s,"      
    sql += "%s)"


    # Connect to the database
    db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname)

    # Create a cursor and execute the SQL on it
    cursor = db.cursor()
    #nrows  = cursor.execute(sql)
    cursor.executemany(sql,csv_data)
    db.commit()

    # There will only be 1 row hopefully
    #data   = cursor.fetchone()
    cursor.close()

############################################################
## Main progranm executuion ##

#enter_sets('csvfiles/list_2019_95_annotated.csv','2019','IN')
enter_sets('calcs.csv','2019','OUT')
