#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      13/06/2020
Function:  All sql strings created here
Description:
============
"""

import thesis_config as cfg

# ************************************************************************************************

def sqlForHistOpt(calc,set_name,maxb,restriction,amino_code,res,rvalue,rfree,resL,rvalueL,rfreeL):

    # allow calc to be N-CA or N.CA or N_CA and convert it
    calc = calc.replace(".","_")
    calc = calc.replace("-","_")


    res_constraint = ""
    if res != "ALL":
        res_constraint =  "AND p.resolution < " + res + "\n"
    rval_constraint = ""
    if rvalue != "ALL":
        rval_constraint =  "AND p.rvalue < " +  rvalue + "\n"
    rfree_constraint = ""
    if rfree != "ALL":
        rfree_constraint =  "AND p.rfree < " + rfree + "\n"

    res_constraintL = ""
    if resL != "ALL":
        res_constraintL =  "AND p.resolution >= " + resL + "\n"
    rval_constraintL = ""
    if rvalueL != "ALL":
        rval_constraintL =  "AND p.rvalue >= " +  rvalueL + "\n"
    rfree_constraintL = ""
    if rfreeL != "ALL":
        rfree_constraintL =  "AND p.rfree >= " + rfreeL + "\n"

    bfactor_restraint = ""
    if maxb != '':
        bfactor_restraint = "AND p.bfactor < " + maxb + " \n"

    amino_restraint = ""
    if amino_code != "NON":
        amino_restraint = "AND g.amino_code = '" + amino_code + "' \n"

    html = ""

    html += "SELECT g.pdb_code, " + calc + " as geo, g.atoms_" + calc + " as atoms, g.aminos_" + calc + " as aminos \n"
    #html += "from geo_core g, protein_set_c s, protein_structure_c p \n"
    html += "from " + cfg.tableCore + " g, " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"
    html += "WHERE " + calc + " IS NOT NULL\n"
    html += "AND s.pdb_code = g.pdb_code\n"
    html += "AND s.pdb_code = p.pdb_code\n"
    html += "AND g.pdb_code = p.pdb_code\n"
    html += "AND g.occupant = 'A'\n"
    html += "AND s.status = 'IN'\n"
    html += bfactor_restraint
    html += amino_restraint
    html += "AND s.set_name = '" + set_name + "'\n"
    html += res_constraint + rval_constraint + rfree_constraint
    html += res_constraintL + rval_constraintL + rfree_constraintL
    html += restriction
    html += " ORDER BY geo ASC;"
    return (html)
# ************************************************************************************************

def sqlForHistContact(calc,set_name,maxb,restriction, amino_code,res,rvalue,rfree,resL,rvalueL,rfreeL):

    # allow calc to be N-CA or N.CA or N_CA and convert it
    calc = calc.replace(".","-")
    calc = calc.replace("_","-")


    res_constraint = ""
    if res != "ALL":
        res_constraint =  "AND p.resolution < " + res + "\n"
    rval_constraint = ""
    if rvalue != "ALL":
        rval_constraint =  "AND p.rvalue < " +  rvalue + "\n"
    rfree_constraint = ""
    if rfree != "ALL":
        rfree_constraint =  "AND p.rfree < " + rfree + "\n"

    amino_restraint = ""
    if amino_code != "NON":
        amino_restraint += "AND g.amino_code = '" + amino_code + "'\n"

    res_constraintL = ""
    if resL != "ALL":
        res_constraintL =  "AND p.resolution >= " + resL + "\n"
    rval_constraintL = ""
    if rvalueL != "ALL":
        rval_constraintL =  "AND p.rvalue >= " +  rvalueL + "\n"
    rfree_constraintL = ""
    if rfreeL != "ALL":
        rfree_constraintL =  "AND p.rfree >= " + rfreeL + "\n"

    bfactor_restraint = ""
    if maxb != '':
        bfactor_restraint = "AND p.bfactor < " + maxb + " \n"

    html = ""

    html += "SELECT g.pdb_code, g.geo_value as geo, g.geo_atoms as atoms \n"
    #html += "from geo_contact g, protein_set_c s, protein_structure_c p \n"
    html += "from " + cfg.tableContact + " g, " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"
    html += "WHERE g.geo_atoms = '" + calc + "' \n"
    html += "AND s.pdb_code = g.pdb_code\n"
    html += "AND s.pdb_code = p.pdb_code\n"
    html += "AND g.pdb_code = p.pdb_code\n"
    html += "AND g.occupant = 'A'\n"
    html += "AND s.status = 'IN'\n"
    html += bfactor_restraint
    html += "AND amino_no < amino_no_b \n"
    html += "AND s.set_name = '" + set_name + "'\n"
    html += res_constraint + rval_constraint + rfree_constraint + amino_restraint
    html += res_constraintL + rval_constraintL + rfree_constraintL
    html += restriction + " \n"
    html += " ORDER BY geo ASC;"
    return (html)


# ************************************************************************************************

def sqlForCorrOpt(calcX,calcY,maxb,set_name, restriction,gradient,amino_code,res,rvalue,rfree,resL,rvalueL,rfreeL):

    # allow calc to be N-CA or N.CA or N_CA and convert it
    calcX = calcX.replace(".","_")
    calcX = calcX.replace("-","_")

    calcY = calcY.replace(".","_")
    calcY = calcY.replace("-","_")

    res_constraint = ""
    if res != "ALL":
        res_constraint =  "AND p.resolution < " + res + "\n"
    rval_constraint = ""
    if rvalue != "ALL":
        rval_constraint =  "AND p.rvalue < " +  rvalue + "\n"
    rfree_constraint = ""
    if rfree != "ALL":
        rfree_constraint =  "AND p.rfree < " + rfree + "\n"

    res_constraintL = ""
    if resL != "ALL":
        res_constraintL =  "AND p.resolution >= " + resL + "\n"
    rval_constraintL = ""
    if rvalueL != "ALL":
        rval_constraintL =  "AND p.rvalue >= " +  rvalueL + "\n"
    rfree_constraintL = ""
    if rfreeL != "ALL":
        rfree_constraintL =  "AND p.rfree >= " + rfreeL + "\n"

    bfactor_restraint = ""
    if maxb != '':
        bfactor_restraint = "AND p.bfactor < " + maxb + " \n"

    amino_restraint = ""
    if amino_code != "NON":
        amino_restraint = "AND g.amino_code = '" + amino_code + "' \n"

    html = ""

    
    html += "SELECT g.pdb_code, " + calcX + " as geox, " + calcY + " as geoy, " + gradient.lower() + " as resolution \n"
    #html += "from geo_core g, protein_set_c s, protein_structure_c p \n"
    html += "from " + cfg.tableCore + " g, " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"

    html += "WHERE " + calcX + " IS NOT NULL\n"
    html += "AND " + calcY + " IS NOT NULL\n"
    
    html += "AND s.pdb_code = g.pdb_code\n"
    html += "AND s.pdb_code = p.pdb_code\n"
    html += "AND g.pdb_code = p.pdb_code\n"
    html += "AND g.occupant = 'A'\n"
    html += bfactor_restraint
    html += amino_restraint
    html += "AND s.set_name = '" + set_name + "'\n"
    html += res_constraint + rval_constraint + rfree_constraint
    html += res_constraintL + rval_constraintL + rfree_constraintL
    html += restriction
    html += " AND s.status = 'IN';"
    return (html)
# ************************************************************************************************

def sqlForScatter3d(calcX,calcY,calcZ,maxb,set_name, restriction,gradient,amino_code,res,rvalue,rfree,resL,rvalueL,rfreeL):

    # allow calc to be N-CA or N.CA or N_CA and convert it
    calcX = calcX.replace(".","_")
    calcX = calcX.replace("-","_")

    calcY = calcY.replace(".","_")
    calcY = calcY.replace("-","_")

    calcZ = calcZ.replace(".","_")
    calcZ = calcZ.replace("-","_")

    res_constraint = ""
    if res != "ALL":
        res_constraint =  "AND p.resolution < " + res + "\n"
    rval_constraint = ""
    if rvalue != "ALL":
        rval_constraint =  "AND p.rvalue < " +  rvalue + "\n"
    rfree_constraint = ""
    if rfree != "ALL":
        rfree_constraint =  "AND p.rfree < " + rfree + "\n"

    res_constraintL = ""
    if resL != "ALL":
        res_constraintL =  "AND p.resolution >= " + resL + "\n"
    rval_constraintL = ""
    if rvalueL != "ALL":
        rval_constraintL =  "AND p.rvalue >= " +  rvalueL + "\n"
    rfree_constraintL = ""
    if rfreeL != "ALL":
        rfree_constraintL =  "AND p.rfree >= " + rfreeL + "\n"

    bfactor_restraint = ""
    if maxb != '':
        bfactor_restraint = "AND p.bfactor < " + maxb + " \n"

    amino_restraint = ""
    if amino_code != "NON":
        amino_restraint = "AND g.amino_code = '" + amino_code + "' \n"
        
    html = ""

    
    html += "SELECT g.pdb_code, " + calcX + " as geox, " + calcY + " as geoy, " + calcZ + " as geoz, " + gradient.lower() + " as resolution \n"
    #html += "from geo_core g, protein_set_c s, protein_structure_c p \n"
    html += "from " + cfg.tableCore + " g, " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"

    html += "WHERE " + calcX + " IS NOT NULL\n"
    html += "AND " + calcY + " IS NOT NULL\n"
    html += "AND " + calcZ + " IS NOT NULL\n"
    
    html += "AND s.pdb_code = g.pdb_code\n"
    html += "AND s.pdb_code = p.pdb_code\n"
    html += "AND g.pdb_code = p.pdb_code\n"
    html += "AND g.occupant = 'A'\n"
    html += bfactor_restraint
    html += amino_restraint
    html += "AND s.set_name = '" + set_name + "'\n"
    html += res_constraint + rval_constraint + rfree_constraint
    html += res_constraintL + rval_constraintL + rfree_constraintL
    html += restriction
    html += " AND s.status = 'IN';"
    return (html)

####################################################################################################



def sqlForOverlay(calcX,calcY,maxb,set_name,restriction, amino_code,res,rvalue,rfree,resL,rvalueL,rfreeL):

    # allow calc to be N-CA or N.CA or N_CA and convert it
    calcX = calcX.replace(".","_")
    calcX = calcX.replace("-","_")

    calcY = calcY.replace(".","_")
    calcY = calcY.replace("-","_")

    res_constraint = ""
    if res != "ALL":
        res_constraint =  "AND p.resolution < " + res + "\n"
    rval_constraint = ""
    if rvalue != "ALL":
        rval_constraint =  "AND p.rvalue < " +  rvalue + "\n"
    rfree_constraint = ""
    if rfree != "ALL":
        rfree_constraint =  "AND p.rfree < " + rfree + "\n"

    res_constraintL = ""
    if resL != "ALL":
        res_constraintL =  "AND p.resolution >= " + resL + "\n"
    rval_constraintL = ""
    if rvalueL != "ALL":
        rval_constraintL =  "AND p.rvalue >= " +  rvalueL + "\n"
    rfree_constraintL = ""
    if rfreeL != "ALL":
        rfree_constraintL =  "AND p.rfree >= " + rfreeL + "\n"

    bfactor_restraint = ""
    if maxb != '':
        bfactor_restraint = "AND p.bfactor < " + maxb + " \n"

    amino_restraint = ""
    if amino_code != "NON":
        amino_restraint = "AND g.amino_code = '" + amino_code + "' \n"        
        
    html = ""

    html += "SELECT g.pdb_code, " + calcX + " as geox, " + calcY + " as geoy, p.resolution \n"
    #html += "from geo_core g, protein_set_c s, protein_structure_c p \n"
    html += "from " + cfg.tableCore + " g, " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"

    html += "WHERE " + calcX + " IS NOT NULL\n"
    html += "AND " + calcY + " IS NOT NULL\n"

    html += "AND s.pdb_code = g.pdb_code\n"
    html += "AND s.pdb_code = p.pdb_code\n"
    html += "AND g.pdb_code = p.pdb_code\n"
    html += "AND g.occupant = 'A'\n"
    html += bfactor_restraint
    html += amino_restraint
    html += "AND s.set_name = '" + set_name + "'\n"
    html += res_constraint + rval_constraint + rfree_constraint
    html += res_constraintL + rval_constraintL + rfree_constraintL
    html += restriction + " \n"
    html += "AND s.status = 'IN';"
    return (html)

################################################################################
def createSqlContacts(pdb, contact_atoms):
    sql = "select * from " + cfg.tableContact + " \n"
    sql += "WHERE pdb_code = '" + pdb + "'\n"
    sql += "AND geo_value < 6 \n"
    sql += "AND geo_atoms = '" + contact_atoms + "';"
    return sql
################################################################################
def getHighPDBsSql():
    sql = ""
    sql += "select p.pdb_code, p.resolution, left(p.institution,20) as authors, left(p.refinement,10) as software, p.rfree,p.rvalue,p.residues "
    #sql += "FROM protein_structure_c p, protein_set_c s "
    sql += "from " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"
    sql += "where p.pdb_code = s.pdb_code "
    sql += "AND s.set_name = 'HIGH'"
    sql += "AND s.status = 'IN' "
    sql += "order by p.pdb_code ASC;"
    return sql
################################################################################   
def get2019PDBsSql():
    sql = ""
    sql += "select p.pdb_code, p.resolution, left(p.institution,20) as authors, left(p.refinement,10) as software, p.rfree,p.rvalue,p.residues "
    #sql += "FROM protein_structure_c p, protein_set_c s "
    sql += "from " + cfg.tableSet + " s, " + cfg.tablePdb + " p \n"
    sql += "where p.pdb_code = s.pdb_code "
    sql += "AND s.set_name = '2019'"
    sql += "AND s.status = 'IN' "
    sql += "order by p.pdb_code ASC;"
    return sql
################################################################################   
def getCalcsSql():
    sql = ""
    sql += "select * "
    sql += "from " + cfg.tableCalcs + ";"
    return sql

