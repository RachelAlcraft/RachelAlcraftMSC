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
    
    
    #0=PdbCode
    #1=Occupant
    #2=Chain
    #3=AminoNo
    #4=GeoAtoms
    #5=Alias
    #6=AminoCode
    #7=AminoNos
    #8=AminoCodes
    #9=AtomNos
    #10=SecStruct
    #11=GeoType
    #12=Value

    #6V7G,A,A,46,N-CA,N-CA,ASN,46-46,ASN-ASN,1-2,U,COREBOND,1.485
    
    # each row is entered into the same database row potentially, has to be done per row
    rows = len(df.index)
    cols = len(df.columns)
    print(rows)
    print(cols)
    for r in range(0,rows):
    # create list of tuples
        csv_data = []    
        colval = df.iloc[r,5]
        # replace the - or . with a _
        colval = colval.replace("-","_")
        colval = colval.replace(".","_")
        colatoms = "atoms_" + colval
        colaminos = "aminos_" + colval
        colcodes = "codes_" + colval    
        #print(colval,colatoms,colaminos,colcodes)
        
        row = ()
        
        
        row += (str(df.iloc[r,0]),) # pdb code        
        row += (str(df.iloc[r,1]),) # occupant
        row += (str(df.iloc[r,2]),) # chain`
        row += (str(df.iloc[r,3]),) # amino_no
        row += (str(df.iloc[r,6]),) # amino_code
        row += (str(df.iloc[r,10]),) # ss_psu        
        row += (str(round(df.iloc[r,12],3)),) # value
        row += (str(df.iloc[r,9]),) # atoms
        row += (str(df.iloc[r,7]),) # aminos
        row += (str(df.iloc[r,8]),) # codes
        # double these???
        #row += (str(round(df.iloc[r,12],3)),) # value
        #row += (str(df.iloc[r,9]),) # atoms
        #row += (str(df.iloc[r,7]),) # aminos
        #row += (str(df.iloc[r,8]),) # codes
                 
        csv_data.append(row)
            
        # Create SQL statement to find information for proteins from Leishmania
        
        sql = "INSERT INTO geo_core ("
        sql += "pdb_code,"
        sql += "occupant,"
        sql += "chain,"
        sql += "amino_no,"
        sql += "amino_code,"
        sql += "ss_psu,"
        sql += colval + ","
        sql += colatoms + ","
        sql += colaminos + ","      
        sql += colcodes + ") \nVALUES ("    
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
        sql += "\nON DUPLICATE KEY UPDATE "
        sql += colval + "=%s, "
        sql += colatoms + "=%s, "
        sql += colaminos + "=%s, "
        sql += colcodes + "=%s"
        
        sql2 = "INSERT INTO geo_core ("
        sql2 += "pdb_code,"
        sql2 += "occupant,"
        sql2 += "chain,"
        sql2 += "amino_no,"
        sql2 += "amino_code,"
        sql2 += "ss_psu,"
        sql2 += colval + ","
        sql2 += colatoms + ","
        sql2 += colaminos + ","      
        sql2 += colcodes + ") \nVALUES ("    
        sql2 += "'" + str(df.iloc[r,0]) + "',"
        sql2 += "'" + str(df.iloc[r,1]) + "',"
        sql2 += "'" + str(df.iloc[r,2]) + "',"
        sql2 += "'" + str(df.iloc[r,3]) + "',"
        sql2 += "'" + str(df.iloc[r,6]) + "',"
        sql2 += "'" + str(df.iloc[r,10]) + "',"
        sql2 += "'" + str(round(df.iloc[r,12],3)) + "',"
        sql2 += "'" + str(df.iloc[r,9]) + "',"
        sql2 += "'" + str(df.iloc[r,7]) + "'," 
        sql2 += "'" + str(df.iloc[r,8]) + "')"
        sql2 += "\nON DUPLICATE KEY UPDATE "
        sql2 += colval + "='" + str(round(df.iloc[r,12],3)) + "', "
        sql2 += colatoms + "='" + str(df.iloc[r,9]) + "', "
        sql2 += colaminos + "='" + str(df.iloc[r,7]) + "', "
        sql2 += colcodes + "='" + str(df.iloc[r,8]) + "'"

        #if r%100 == 0:
        print(r,"/",rows)
        print(sql)
        print(csv_data)
        
        # Connect to the database
        db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname)
        # Create a cursor and execute the SQL on it
        cursor = db.cursor()    
        #cursor.executemany(sql,csv_data)
        cursor.execute(sql2)
        db.commit()        
        cursor.close()


#########################################################
os. chdir("DataSets/Version3/01June20/Core/")
arr = os.listdir()
print(arr)
i = 0
for fl in arr:
    #if i == 0:
    i += 1
    print(i,fl)
    try:
        enterOneValueFile(fl)
    except:
        print('error', fl)
