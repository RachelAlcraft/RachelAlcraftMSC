#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      16/06/2020
Function:  Class designed to manage interface choices and sql data
            Built with the forward possibility of state between sessions
Description:
============
"""
###############################################################################################

##### THIS OBJECT IS DESIGNED TO MAINTAIN STATE #######

import os
import thesis_config as cfg
import thesis_read_db_simple as sql
import name_change as nc
from io import StringIO as sio
import pandas as pd


# import Cookie #http://cgi.tutorial.codepoint.net/set-the-cookie

################################################################################################

##class sqlSavedData:
##    #def __init__(self):
##    #    #self.cookie = Cookie.SimpleCookie()
##    #    storeOfData['lastvisit'] = cookie['lastvisit']
##    def dump(self):
##        print ('Set-Cookie: lastvisit=' + str(time.time()))
##    def existsSqlData(self,key):
##        return (key in storeOfData)
##    def addSqlData(self,key,data):
##        storeOfData[key] = data


class sqlChoices:
    def addGeneralChoices(self, calcx, calcy, calcz, maxb, restriction, gradient):
        # self.calcx = calcx
        # self.calcy = calcy
        # self.calcz = calcz
        # self.calcx = self.calcx.replace(".", "_")
        # self.calcx = self.calcx.replace("-", "_")
        # self.calcy = self.calcy.replace(".", "_")
        # self.calcy = self.calcy.replace("-", "_")
        # self.calcz = self.calcz.replace(".", "_")
        # self.calcz = self.calcz.replace("-", "_")
        self.calcx = nc.changeViewToDBMeasure(calcx)
        self.calcy = nc.changeViewToDBMeasure(calcy)
        self.calcz = nc.changeViewToDBMeasure(calcz)
        self.maxb = maxb
        self.restriction = restriction
        self.gradient = gradient

    def addDistribution(self, set_name, chosen_sets, chosen_ss, amino_code, occupant, contact, resolution, rvalue,
                        rfree):
        self.set_name = set_name
        self.occupant = occupant
        self.contact = contact
        if amino_code == "ALL":
            self.amino_codes = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN',
                                'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR']
        else:
            self.amino_codes = amino_code.split(',')

        self.resolution = resolution  # tuple of upper and lif self.contactower
        self.rvalue = rvalue  # tuple of upper and lower
        self.rfree = rfree  # tuple of upper and lower
        self.chosen_sets = chosen_sets
        self.chosen_ss = chosen_ss

    def getSqlStrings(self):
        sqls = {}
        for aa in self.amino_codes:
            sql = self.getSqlString(aa)
            sqls[aa] = sql
        return sqls

    def getSqlString(self, amino_code):  # which is also the unique key
        sql = ""
        if "C@" in self.calcx:
            isContact = True
            calcx = self.calcx[2:]
            calcx = calcx.replace("_", "-")
            sql += self.buildSql_1dContact()
            sql += " \n"
            sql += self.buildTableFromContact()
            sql += self.buildCommonConstraints(True)
            sql += "AND amino_no < amino_no_b \n"
            sql += "AND geo_atoms = '" + calcx + "' \n"
        else:
            if self.calcz != "":
                sql += self.buildSql_3d()
            elif self.calcy != "":
                sql += self.buildSql_2d()
            else:
                sql += self.buildSql_1d()
            sql += " \n"
            sql += self.buildTableFrom()

            sql += self.buildCommonConstraints(False)
            sql += self.buildNotNulls()
            # if self.contact != "":
            #    sql += self.buildContactConstraints()

        sql += self.buildUpperLowerConstraint(self.resolution, 'resolution')
        sql += self.buildUpperLowerConstraint(self.rvalue, 'rvalue')
        sql += self.buildUpperLowerConstraint(self.rfree, 'rfree')
        sql += self.restriction + " \n"
        sql += self.buildAminoConstraint(amino_code)
        sql += self.buildBFactorConstraint()
        if self.contact != "":
            sql += self.buildContactConstraints()
            # sql += " GROUP BY g.amino_no,g.pdb_code,g.chain"
        sql += " ORDER BY geox ASC;"
        return (sql)

    def buildSql_1d(self):
        sql = "SELECT g.pdb_code, g.amino_no, " + self.gradient.lower() + " as gradient, "
        sql += self.calcx + " as geox, g.atoms_" + self.calcx + " as atoms, g.aminos_" + self.calcx + " as aminos"
        return (sql)

    def buildSql_1dContact(self):
        sql = "SELECT g.pdb_code, g.geo_value as geox, g.geo_atoms as atoms, " + self.gradient.lower() + " as gradient, g.amino_code as aminos "
        return (sql)

    def buildSql_2d(self):
        sql = self.buildSql_1d() + ", " + self.calcy + " as geoy"
        return (sql)

    def buildSql_3d(self):
        sql = self.buildSql_2d() + ", " + self.calcz + " as geoz"
        return (sql)

    def buildNotNulls(self):
        sql = "AND " + self.calcx + " IS NOT NULL\n"
        if self.calcy != "":
            sql += "AND " + self.calcy + " IS NOT NULL\n"
        if self.calcz != "":
            sql += "AND " + self.calcz + " IS NOT NULL\n"
        return (sql)

    def buildTableFrom(self):
        sql = ''
        table = cfg.tableCore
        if self.set_name == "HIGH":
            table = cfg.tableCoreHigh
        elif self.set_name == "EXTRA":
            table = cfg.tableCoreExtra
        sql += "FROM " + table + " g, "
        sql += "" + cfg.tableSet + " s, "
        sql += "" + cfg.tablePdb + " p \n"
        return (sql)

    def buildTableFromContact(self):
        sql = ''
        table = cfg.tableContact
        sql += "FROM " + table + " g, "
        sql += "" + cfg.tableSet + " s, "
        sql += "" + cfg.tablePdb + " p \n"
        return (sql)

    def buildCommonConstraints(self, isContact):
        sql = "WHERE s.pdb_code = g.pdb_code\n"
        sql += "AND s.pdb_code = p.pdb_code\n"
        sql += "AND g.pdb_code = p.pdb_code\n"
        sql += "AND g.occupant = '" + self.occupant + "'\n"
        sql += "AND s.set_name = '" + self.set_name + "'\n"
        sql += "AND s.status IN " + self.chosen_sets + "\n"
        if not isContact:
            sql += "AND g.dssp IN " + self.chosen_ss + "\n"
        return (sql)

    def buildUpperLowerConstraint(self, vals, valtype):
        sql = ""
        openbracket = ''
        closebracket = ''
        if vals[0] != 'ALL' and vals[1] != 'ALL':
            openbracket = '('
            closebracket = ') '

        if vals[0] != "ALL":
            sql += "AND " + openbracket + "p." + valtype + " <= " + vals[0] + "\n"
        if vals[1] != "ALL":
            sql += "AND p." + valtype + " > " + vals[1] + "\n"
        sql += closebracket
        return (sql)

    def buildAminoConstraint(self, amino_code):
        sql = ""
        if amino_code != "NON":
            sql = "AND g.amino_code = '" + amino_code + "' \n"
        return (sql)

    def buildBFactorConstraint(self):
        sql = ""
        if self.maxb != '':
            sql = "AND p.bfactor <= " + self.maxb + " \n"
        return (sql)

    def buildContactFrom(self):
        sql = ", " + cfg.tableContact + " o \n"
        return (sql)

    def buildContactConstraints(self):
        sql = ''
        cct = self.contact
        if 'X' in cct:
            cct = cct[1:]
            sql += 'AND g.pdb_code NOT IN \n'
        else:
            sql += 'AND g.pdb_code IN \n'
        sql += '(\n'
        sql += 'select distinct o.pdb_code from ' + cfg.tableContact + ' o, ' + cfg.tableSet + " s\n"
        sql += "WHERE o.pdb_code = s.pdb_code\n"
        sql += "AND o.pdb_code = g.pdb_code\n"
        sql += "AND s.set_name = '" + self.set_name + "'\n"
        sql += "AND o.occupant = '" + self.occupant + "'\n"
        if cct == 'O-N':
            sql += "AND o.geo_atoms = 'N-O'\n"
            sql += "AND o.amino_no_b =  g.amino_no\n"
        else:
            sql += "AND o.geo_atoms = '" + cct + "'\n"
            sql += "AND o.amino_no =  g.amino_no\n"
        sql += "AND o.chain =  g.chain\n"
        sql += 'AND o.geo_value < 3.6\n'
        sql += ')'
        return (sql)


class sqlData:
    def __init__(self, sql, amino_code, choices):
        self.sql = sql
        self.choices = choices
        self.amino_code = amino_code

    def createDataFrame(self):
        try:  # calling the database
            self.df = sql.read_sql(self.sql)
            # data cleaning before we return
            self.df['geox'] = self.df['geox'].astype('float')
            if 'geoy' in self.df.columns:
                self.df['geoy'] = self.df['geoy'].astype('float')
            if 'geoz' in self.df.columns:
                self.df['geoz'] = self.df['geoz'].astype('float')
                # self.df['gradient'] = self.df['gradient'].astype('float')
        except:
            self.df = pd.read_csv(sio(self.amino_code + ", no data"))
        return self.df



