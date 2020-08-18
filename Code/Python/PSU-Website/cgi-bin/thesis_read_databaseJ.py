#!/usr/bin/python3
"""
Author:    Rachel Alcraft
Date:      12/05/2020
Function:  Read the given sql from the database and return as a dataframe
===========================================================
Optimised with the help of Justin Barton
============================================================
"""

import pymysql.cursors
import pandas as pd


#########################################################################

def read_sql(sql):
    # Set parameters
    dbname = "ab002"
    dbhost = "hope"
    dbuser = "ab002"
    dbpass = "4603v58-3"
    port = 3306

    # Connect to the database
    db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname,
                         cursorclass=pymysql.cursors.DictCursor)

    # Create a cursor and execute the SQL on it
    cursor = db.cursor()
    cursor.execute(sql)

    # turn it into a dataframe
    df = pd.DataFrame(cursor.fetchall())
    # df.columns = cursor.keys()

    # close the cursor
    cursor.close()
    return (df)


#########################################################################

def createOneMeasure(measure, col, recol, letNull):
    # remeasure = origmeasure.replace('-','_')
    sql = ''
    # sql += "IF(a.geo_atoms = '" + measure + "', a.geo_value, NULL)"
    sql += "MAX(IF(a.alias = '" + measure + "', " + col + ", NULL))"
    sql += " AS `" + recol + measure + "`,\n"
    return (sql)


def createMeasures(measures, col, recol, letNull):
    sql = ''
    for measure in measures:
        sql += createOneMeasure(measure, col,recol,letNull)
    return (sql)


def createOneColumn(measure):
    origmeasure = measure
    remeasure = origmeasure.replace('-', '_')
    sql = ''
    sql += 'g.' + remeasure + ','
    return (sql)


def createColumns(measures):
    sql = ''
    for measure in measures:
        sql += createOneColumn(measure)
    return (sql)


def createAtoms(measures):
    sql = 'a.alias IN ('
    count = 0
    for measure in measures:
        if count > 0:
            sql += ",'"
        else:
            sql += "'"
        sql += measure + "'"
        count += 1
    sql += ')\n'
    return (sql)


def createNotNulls(measures):
    sql = ''
    count = 0
    for measure in measures:
        # remeasure = measure.replace('-','_')
        if count == 0:
            sql += "WHERE b.`" + measure + "` IS NOT NULL "
        else:
            sql += "AND b.`" + measure + "` IS NOT NULL "
        count += 1
    return (sql)

    
################################################################################
def get_restriction(col, val):
    sql = ''
    if val != '':
        sql = 'AND ' + col + "='" + val + "' \n"
    return (sql)

################################################################################
def createSql(measures, aa, occ, pdb, setname, letNull):
    sql = ''
    sql += 'SELECT g.*, \n'
    sql += 'SUBSTRING(p.institution,1,20) as `authors`, SUBSTRING(p.refinement,1,20) as `refinement`, \n'
    sql += 'p.resolution, p.residues, p.rfree, p.occupancy, m.volume, m.donicity \n'
    sql += 'FROM \n'
    sql += '(SELECT \n'
    sql += 'a.pdb_code,\n'
    sql += createMeasures(measures, 'a.geo_value', '', letNull)
    sql += createMeasures(measures, 'a.amino_codes', 'aa_codes_', letNull)
    sql += createMeasures(measures, 'a.amino_nos', 'aa_nos_', letNull)
    sql += createMeasures(measures, 'a.atom_nos', 'atoms_', letNull)    
    sql += 'a.occupant,\n'
    sql += 'a.chain,\n'
    sql += 'a.ss_psu,\n'
    sql += 'a.amino_no,\n'
    sql += 'a.amino_code \n'
    sql += 'FROM \n'
    sql += 'geo_measure_b a \n'
    sql += 'WHERE \n'
    sql += createAtoms(measures)
    sql += get_restriction('a.amino_code', aa)
    sql += get_restriction('a.pdb_code', pdb)
    sql += get_restriction('a.occupant', occ)
    sql += ' GROUP BY \n'
    sql += 'a.pdb_code,\n'
    sql += 'a.occupant,\n'
    sql += 'a.chain,\n'
    sql += 'a.amino_no) g, protein_structure_c p, amino_acid m, protein_set_c s \n'
    sql += 'WHERE g.pdb_code = p.pdb_code \n'
    sql += get_restriction('s.status', 'IN')
    sql += get_restriction('s.set_name', setname)
    sql += 'AND s.pdb_code = g.pdb_code\n'
    sql += 'AND g.amino_code = m.amino_code;'
    return (sql)


###### TEST CODE TO TRY THE DATA #############
'''
print("***********************************")
dataInput = "CP-N-CA-C N-CA-C-NPP"
calcs = dataInput.split()
df = createSql(calcs,'','A','4rek','in',False)
print(df)
#rows = len(df.index)
#cols = len(df.columns)
#print(rows)
#print(cols)
'''
