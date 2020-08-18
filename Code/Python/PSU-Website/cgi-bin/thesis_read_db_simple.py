#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      13/05/2020
Function:  Read the given sql from the database and return as a dataframe
===========================================================

============================================================
"""

import pymysql.cursors
import pandas as pd
# Useful debugging output
import cgitb

cgitb.enable()  # Send errors to browser


# cgitb.enable(display=0, logdir="/path/to/logdir") # log errors to a file

#########################################################################

def read_sql(sql):
    # Set parameters
    dbname = "ab002"
    dbhost = "thoth.cryst.bbk.ac.uk"
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
# Read multiple sqls in one go
#########################################################################
def read_sqls(sqls, measures, buckets, categories, aminoviews):
    # Set parameters
    dfs = []
    dbname = "ab002"
    dbhost = "thoth.cryst.bbk.ac.uk"
    dbuser = "ab002"
    dbpass = "4603v58-3"
    port = 3306

    # Connect to the database
    db = pymysql.connect(host=dbhost, port=port, user=dbuser, passwd=dbpass, db=dbname,
                         cursorclass=pymysql.cursors.DictCursor)

    dfs = []
    # Create a cursor and execute the SQL on it
    cursor = db.cursor()
    for i in range(0, len(sqls)):
        sql = sqls[i]
        cursor.execute(sql)
        # turn it into a dataframe
        # print(sql)
        df = pd.DataFrame()
        if cursor.rowcount > 0:
            df = pd.DataFrame(cursor.fetchall())

            if 'geox' in df.columns:
                df['geox'] = df['geox'].astype('float')
            if 'geoy' in df.columns:
                df['geoy'] = df['geoy'].astype('float')
            if 'geoz' in df.columns:
                df['geoz'] = df['geoz'].astype('float')
            # if 'gradient' in df.columns:
            #    df['gradient'] = df['gradient'].astype('float')

            # print(df)
            df['bucket'] = buckets[i]
            df['measure'] = measures[i]
            df['category'] = categories[i]
            df['aminoview'] = aminoviews[i]
        dfs.append(df)

    # close the cursor
    cursor.close()
    # print(dfs)
    return (dfs)

#########################################################################
