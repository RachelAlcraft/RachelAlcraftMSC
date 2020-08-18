#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      07/05/2020
Function:  Read the given sql from the database and return as a dataframe
"""


import pymysql.cursors
import pandas as pd

#########################################################################

def read_sql(sql):
    # Set parameters
    dbname   = "ab002"
    dbhost   = "hope"
    dbuser   = "ab002"
    dbpass   = "4603v58-3"
    port     = 3306
    
    # Connect to the database
    db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname,cursorclass=pymysql.cursors.DictCursor)

    # Create a cursor and execute the SQL on it
    cursor = db.cursor()
    cursor.execute(sql)

    # turn it into a dataframe
    df = pd.DataFrame(cursor.fetchall())
    #df.columns = cursor.keys()

    #close the cursor
    cursor.close()
    return(df)

#########################################################################
def get_restriction(col,val):
    sql = ''
    if val != '':
        sql = 'AND a.' + col + "='" + val + "' "
    return(sql)

def make_sqlstringA(calc1,col,val,amino, pdb, occupant):    
    sql = "SELECT  "
    sql += "a.pdb_code, "
    sql += "a.occupant, "
    sql += "a.amino_no, "
    sql += "a.amino_codes as 'a_value', "
    sql += "a.geo_atoms as 'a_geo_type', " 
    sql += "a.geo_value as 'a_value', " 
    sql += "c.resolution, "
    sql += "c.residues, "
    sql += "c.rfree, "
    sql += "c.occupancy, "
    sql += "d.volume, "
    sql += "d.donicity "
    sql += "FROM geo_measure a, protein_structure c, amino_acid d "
    sql += "WHERE a.pdb_code = c.pdb_code "
    sql += get_restriction(col,val)
    sql += get_restriction('amino_code',amino)
    sql += get_restriction('pdb_code',pdb)
    sql += get_restriction('occupant',occupant)
    sql += "AND a.geo_atoms = '" + calc1 + "' "
    sql += "AND a.amino_code = d.amino_code "    
    sql += "AND c.status = 'IN';"
    return(sql)  

def make_sqlstringB(calc1,calc2,col,val, amino, pdb, occupant):      
    sql = "SELECT  "
    sql += "a.pdb_code, "
    sql += "a.occupant, "
    sql += "a.amino_no, "
    sql += "a.amino_codes as 'a_codes', "
    sql += "a.geo_atoms as 'a_geo_type', " 
    sql += "a.geo_value as 'a_value', " 
    sql += "b.amino_codes as 'b_codes', "
    sql += "b.geo_atoms as 'b_geo_type', " 
    sql += "b.geo_value as 'b_value', " 
    sql += "c.resolution, "
    sql += "c.residues, "
    sql += "c.rfree, "
    sql += "c.occupancy, "
    sql += "d.volume, "
    sql += "d.donicity "
    sql += "FROM geo_measure a, geo_measure b, protein_structure c, amino_acid d "
    sql += "WHERE a.pdb_code = b.pdb_code "
    sql += get_restriction(col,val)
    sql += get_restriction('amino_code',amino)
    sql += get_restriction('pdb_code',pdb)
    sql += get_restriction('occupant',occupant)
    sql += "AND a.occupant = b.occupant "
    sql += "AND a.chain = b.chain "
    sql += "AND a.amino_no = b.amino_no "
    sql += "AND a.geo_atoms = '" + calc1 + "' "
    sql += "AND b.geo_atoms = '" + calc2 + "' "
    sql += "AND a.pdb_code = c.pdb_code "    
    sql += "AND a.amino_code = d.amino_code "
    sql += "AND c.status = 'IN';"
    return(sql)  

def make_sqlstringC(calc1,calc2,calc3,col,val, amino, pdb, occupant):      
    sql = "SELECT  "
    sql += "a.pdb_code, "
    sql += "a.occupant, "
    sql += "a.amino_no, "
    sql += "a.amino_codes as 'a_codes', "
    sql += "a.geo_atoms as 'a_geo_type', " 
    sql += "a.geo_value as 'a_value', " 
    sql += "b.amino_codes as 'b_codes', "
    sql += "b.geo_atoms as 'b_geo_type', " 
    sql += "b.geo_value as 'b_value', " 
    sql += "c.amino_codes as 'c_codes', "
    sql += "c.geo_atoms as 'c_geo_type', " 
    sql += "c.geo_value as 'c_value', " 
    sql += "p.resolution, "
    sql += "p.residues, "
    sql += "p.rfree, "
    sql += "p.occupancy, "
    sql += "m.volume, "
    sql += "m.donicity "
    sql += "FROM geo_measure a, geo_measure b,geo_measure c, protein_structure p, amino_acid m "
    sql += "WHERE a.pdb_code = b.pdb_code "
    sql += get_restriction(col,val)
    sql += get_restriction('amino_code',amino)
    sql += get_restriction('pdb_code',pdb)
    sql += get_restriction('occupant',occupant)
    sql += "AND a.pdb_code = c.pdb_code "
    sql += "AND b.pdb_code = c.pdb_code "
    sql += "AND a.occupant = b.occupant "
    sql += "AND a.occupant = c.occupant "
    sql += "AND c.occupant = b.occupant "
    sql += "AND a.chain = b.chain "
    sql += "AND a.chain = c.chain "
    sql += "AND c.chain = b.chain "
    sql += "AND a.amino_no = b.amino_no "    
    sql += "AND a.amino_no = c.amino_no "
    sql += "AND c.amino_no = b.amino_no "
    sql += "AND a.geo_atoms = '" + calc1 + "' "
    sql += "AND b.geo_atoms = '" + calc2 + "' "
    sql += "AND c.geo_atoms = '" + calc3 + "' "
    sql += "AND a.pdb_code = p.pdb_code "
    sql += "AND a.amino_code = m.amino_code "
    sql += "AND p.status = 'IN';"
    return(sql)  

def make_sqlstringD(calc1,calc2,calc3,calc4,col,val, amino, pdb, occupant):       
    sql = "SELECT  "
    sql += "a.pdb_code, "
    sql += "a.occupant, "
    sql += "a.amino_no, "
    sql += "b.amino_codes as 'b_codes', "
    sql += "b.geo_atoms as 'b_geo_type', " 
    sql += "b.geo_value as 'b_value', " 
    sql += "c.amino_codes as 'c_codes', "
    sql += "c.geo_atoms as 'c_geo_type', " 
    sql += "c.geo_value as 'c_value', " 
    sql += "d.amino_codes as 'd_codes', "
    sql += "d.geo_atoms as 'd_geo_type', " 
    sql += "d.geo_value as 'd_value', " 
    sql += "p.resolution, "
    sql += "p.residues, "
    sql += "p.rfree, "
    sql += "p.occupancy, "
    sql += "m.volume, "
    sql += "m.donicity "
    sql += "FROM geo_measure a, geo_measure b,geo_measure c,geo_measure d, protein_structure p, amino_acid m "
    sql += "WHERE a.pdb_code = b.pdb_code "
    sql += get_restriction(col,val)
    sql += get_restriction('amino_code',amino)
    sql += get_restriction('pdb_code',pdb)
    sql += get_restriction('occupant',occupant)
    sql += "AND a.pdb_code = c.pdb_code "
    sql += "AND b.pdb_code = c.pdb_code "    
    sql += "AND b.pdb_code = d.pdb_code "
    sql += "AND b.pdb_code = c.pdb_code "
    sql += "AND a.occupant = b.occupant "
    sql += "AND c.occupant = b.occupant "
    sql += "AND a.occupant = c.occupant "
    sql += "AND a.occupant = d.occupant "
    sql += "AND b.occupant = d.occupant "
    sql += "AND c.occupant = d.occupant "
    sql += "AND a.chain = b.chain "
    sql += "AND a.chain = c.chain "
    sql += "AND c.chain = b.chain "
    sql += "AND a.chain = d.chain "
    sql += "AND b.chain = d.chain "
    sql += "AND c.chain = d.chain "
    sql += "AND a.amino_no = b.amino_no "
    sql += "AND a.amino_no = c.amino_no "
    sql += "AND c.amino_no = b.amino_no "
    sql += "AND a.amino_no = d.amino_no "
    sql += "AND b.amino_no = d.amino_no "
    sql += "AND c.amino_no = d.amino_no "
    sql += "AND a.geo_atoms = '" + calc1 + "' "
    sql += "AND b.geo_atoms = '" + calc2 + "' "
    sql += "AND c.geo_atoms = '" + calc3 + "' "
    sql += "AND d.geo_atoms = '" + calc4 + "' "
    sql += "AND a.pdb_code = p.pdb_code "
    sql += "AND a.amino_code = m.amino_code "
    sql += "AND p.status = 'IN';"
    return(sql)  
################################################################

###### TEST CODE TO TRY THE DATA #############
'''
print("***********************************")
#dataInput = "CP FG"
#calcs = dataInput.split()
#calc1 = calcs[0]
#calc2 = calcs[1]
##df = read_sql("select * from geo_measure")
#df = search_sql(calc1,calc2)
#print(df.keys())
#print(df)
#rows = len(df.index)
#cols = len(df.columns)
#print(rows)
#print(cols)
'''