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
    dbhost   = "thoth.cryst.bbk.ac.uk"
    dbuser   = "ab002"
    dbpass   = "4603v58-3"
    port     = 3306

    # Load csv file for write
    df = pd.read_csv(file_name)
    
    
    #0=PdbCode
    #1=Chain
    #1=Occupant    
    #3=AminoNo    
    #4=dssp
    

    #6V7G,A,A,46,N-CA,N-CA,ASN,46-46,ASN-ASN,1-2,U,COREBOND,1.485
    
    # each row is entered into the same database row potentially, has to be done per row
    rows = len(df.index)
    cols = len(df.columns)
    print(rows)
    print(cols)
    for r in range(0,rows):
    # create list of tuples
                            
        sql2 = "INSERT INTO geo_high_v1 ("
        sql2 += "pdb_code,"
        sql2 += "chain,"
        sql2 += "occupant,"        
        sql2 += "amino_no,"        
        sql2 += "dssp) \nVALUES ("    
        sql2 += "'" + str(df.iloc[r,0]) + "',"
        sql2 += "'" + str(df.iloc[r,1]) + "',"
        sql2 += "'" + str(df.iloc[r,2]) + "',"
        sql2 += "'" + str(df.iloc[r,3]) + "',"        
        sql2 += "'" + str(df.iloc[r,4]) + "')"
        sql2 += "\nON DUPLICATE KEY UPDATE "
        #sql2 += "dssp='" + str(df.iloc[r,4]) + "', "
        sql2 += "dssp='" + str(df.iloc[r,4]) + "'"
        
        if r%100 == 0:
            print(r,"/",rows)
        
        #print(sql2)
        
        # Connect to the database
        db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname)
        # Create a cursor and execute the SQL on it
        cursor = db.cursor()        
        cursor.execute(sql2)
        db.commit()        

    cursor.close()


#########################################################

enterOneValueFile('high_dssp350.csv')
