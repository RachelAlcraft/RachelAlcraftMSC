#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  Enter the pdb_file file into the database, this would only be done at the beginning and if there were any config changes 
"""

import pymysql.cursors
import pandas as pd
from datetime import datetime

#########################################################################

# Set parameters
dbname   = "ab002"
dbhost   = "hope"
dbuser   = "ab002"
dbpass   = "4603v58-3"
port     = 3306

# Load csv file for write
df = pd.read_csv('csvfiles/list_2019_95_annotated.csv')
print(df)

# create list of tuples
csv_data = []
rows = len(df.index)
cols = len(df.columns)
print(rows)
print(cols)
for r in range(0,rows):
    row = ()
    for c in range(0,cols):
        #print (r,c,df.iloc[r,c])
        if c == 0 or c==11 or  c==14:
            row = row + (str((df.iloc[r,c])),)            
    print(row)
    csv_data.append(row)
#print(csv_data)

# Create SQL statement to find information for proteins from Leishmania
sql = "REPLACE INTO protein_structure_b ("#) VALUES "
sql += "pdb_code,"
sql += "residues,"
sql += "institution) VALUES ("
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



