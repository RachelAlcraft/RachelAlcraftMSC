#!/d/msc/s/anaconda/v5.3.0/bin/python
"""
Author:    Rachel Alcraft
Date:      11/08/2020
Function:  Class designed to manage calculation names

Description:
============
The calculation maes have been changed. In version 2 of the database they will be changed there,
but this provides an wrapper meanwhile
"""
###############################################################################################

view_db = {}
db_view = {}


def changeViewToDBMeasure(measure):
    calc = measure
    calc = calc.replace(".", "_")
    calc = calc.replace("-", "_")
    calc = calc.replace("CB1C", "CBPP")
    calc = calc.replace("CA1N", "CAP")
    calc = calc.replace("CA2N", "CAP2")
    calc = calc.replace("CA1C", "CAPP")
    calc = calc.replace("CA2C", "CAPP2")
    calc = calc.replace("CB1N", "CBP")
    calc = calc.replace("C1N", "CP")
    calc = calc.replace("C1C", "CPP")
    calc = calc.replace("N1N", "NP")
    calc = calc.replace("N1C", "NPP")
    calc = calc.replace("O1N", "OP")
    calc = calc.replace("TAU1N", "TAUP")
    calc = calc.replace("TAU1C", "TAUPP")
    return (calc)


def changeDBToViewMeasure(measure):
    calc = measure
    calc = calc.replace("_", "-")
    measures = calc.split("-")
    calcs = "."
    for mea in measures:
        mea = changeOneDBToViewMeasure(mea)
        if calcs == ".":
            calcs = mea
        else:
            calcs += "-" + mea
    return (calcs)


def changeOneDBToViewMeasure(measure):
    # careful to replace in order
    calc = measure
    if 'CP' in calc:
        if 'CPP' in calc:
            calc = calc.replace("CPP", "C1C")
        else:
            calc = calc.replace("CP", "C1N")
    if 'NP' in calc:
        if 'NPP' in calc:
            calc = calc.replace("NPP", "N1C")
        else:
            calc = calc.replace("NP", "N1N")
    if 'CBP' in calc:
        if 'CBPP' in calc:
            calc = calc.replace("CBPP", "CB1C")
        else:
            calc = calc.replace("CBP", "CB1N")
    if 'OP' in calc:
        if 'OPP' in calc:
            calc = calc.replace("OPP", "O1C")
        else:
            calc = calc.replace("OP", "O1N")
    if 'TAUP' in calc:
        if 'TAUPP' in calc:
            calc = calc.replace("TAUPP", "TAU1C")
        else:
            calc = calc.replace("TAUP", "TAU1N")
    if 'CAP' in calc:
        if 'CAPP2' in calc:
            calc = calc.replace("CAPP2", "CA2C")
        elif 'CAPP' in calc:
            calc = calc.replace("CAPP", "CA1C")
        elif 'CAP2' in calc:
            calc = calc.replace("CAP2", "CA2N")
        else:
            calc = calc.replace("CAP", "CA1N")

    return (calc)


