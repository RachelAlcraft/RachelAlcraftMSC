#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      04/06/2020
Function:  Currently hardcoded display of the available geo measures
Description:
============
"""

import thesis_read_db_simple as sdb
import thesis_strings as ts
import thesis_sql as sqldb
def getHelp():
    html = ''
    html += '<div class="middle"><p>Histograms: enter Geo Calc X and Distribution A.<br/>'
    html += '        Note for contacts for distance distributions use e.g. C@SG-SG (or C@N-O, C@CA-CA, c@CB-CB)<br/>'
    html += '        Note for bounds the Upper is exclusive and the lower in inclusive<br/>'
    html += 'Scatter plots: enter Geo Calc X and Geo Calc Y, and Distribution A<br/>'
    html += '        The gradient can be entered in the gradient box, any numerical value, eg resolution, rfree, rvalue, residues, amino_no...<br/>'
    html += 'Probability Density: enter Geo Calc X and Geo Calc Y, and Distribution A<br/>'
    html += 'Compare Distributions: enter Geo Calc X and Geo Calc Y, and Distribution A and B for an overlay comparison<br/>'
    html += 'Compare Probability: enter Geo Calc X and Geo Calc Y, and Distribution A and B for an overlay comparison<br/>'
    html += '        Note for the amino code, enter a single 3 letter code, or a comma delim list, or ALL<br/>'
    html += '        Note that this is different for the distance distributions where ALL means all at the same time<br/>'
    html += "A further restriction can be added for the sql, e.g. AND amino_code != 'PRO' </p></div>"
    
    return(html)

    
def getCalcMeasures():
    html = ""
    html = "<table class='cpptable'>\n"
    html += "<tr class='cppinnerheader'>\n"
    html += "<td>AminoAcid</td><td>GeoType</td><td>Atoms</td><td>Alias</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>C-O</td><td>C-O</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>HG-O</td><td>HG-O</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>CP-N</td><td>CP-N</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>N-CA</td><td>N-CA</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>CA-C</td><td>CA-C</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>C-NPP</td><td>C-NPP</td></tr>\n"
    html += "<tr><td>*</td><td>BOND</td><td>HG-NP</td><td>HG-NP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CB-O</td><td>CB-O</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>N-O</td><td>N-O</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>OP-CA</td><td>OP-CA</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>O-CAPP</td><td>O-CAPP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>C-CBPP</td><td>C-CBPP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CB-NPP</td><td>CB-NPP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>OP-CB</td><td>OP-CB</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CP-CB</td><td>CP-CB</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CBP-N</td><td>CBP-N</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CAP-CA</td><td>CAP-CA</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CA-CAPP</td><td>CA-CAPP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>N-NPP</td><td>N-NPP</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>NP-N</td><td>NP-N</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>CP-C</td><td>CP-C</td></tr>\n"
    html += "<tr><td>*</td><td>ONEFOUR</td><td>C-CPP</td><td>C-CPP</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>CP-N-CA</td><td>TAUP</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>N-CA-C</td><td>TAU</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>CA-C-NPP</td><td>TAUPP</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>CA-C-O</td><td>CA-C-O</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>O-C-NPP</td><td>O-C-NPP</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>OP-CP-N</td><td>OP-CP-N</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>N-CA-CB</td><td>N-CA-CB</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>CB-CA-C</td><td>CB-CA-C</td></tr>\n"
    html += "<tr><td>*</td><td>ANGLE</td><td>CA-CB-CG</td><td>CA-CB-CG</td></tr>\n"
    html += "<tr><td>*</td><td>DIHEDRAL</td><td>CP-N-CA-C</td><td>PHI</td></tr>\n"
    html += "<tr><td>*</td><td>DIHEDRAL</td><td>N-CA-C-NPP</td><td>PSI</td></tr>\n"
    html += "<tr><td>*</td><td>DIHEDRAL</td><td>CA-C-NPP-CAPP</td><td>OMEGA</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>ALA</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>ALA</td><td>DIHEDRAL</td><td>C-CA-CB-HB1</td><td>CHI1</td></tr>\n"
    html += "<tr><td>ALA</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>ALA</td><td>IMPROPER</td><td>HB3-CA-CB-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>ARG</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>ARG</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>ARG</td><td>DIHEDRAL</td><td>CA-CB-CG-CD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>ARG</td><td>DIHEDRAL</td><td>CB-CG-CD-NE</td><td>CHI3</td></tr>\n"
    html += "<tr><td>ARG</td><td>DIHEDRAL</td><td>CG-CD-NE-CZ</td><td>CHI4</td></tr>\n"
    html += "<tr><td>ARG</td><td>DIHEDRAL</td><td>CD-NE-CZ-NH1</td><td>CHI5</td></tr>\n"
    html += "<tr><td>ARG</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>ARG</td><td>IMPROPER</td><td>HE-CZ-CD-NE</td><td>IMP2</td></tr>\n"
    html += "<tr><td>ARG</td><td>IMPROPER</td><td>NH2-NH1-NE-CZ</td><td>IMP3</td></tr>\n"
    html += "<tr><td>ARG</td><td>IMPROPER</td><td>NE-HE-NH2-CZ</td><td>IMP4</td></tr>\n"
    html += "<tr><td>ARG</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>ASN</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>ASN</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>ASN</td><td>DIHEDRAL</td><td>CA-CB-CG-OD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>ASN</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>ASN</td><td>IMPROPER</td><td>ND2-OD1-CB-CG</td><td>IMP2</td></tr>\n"
    html += "<tr><td>ASN</td><td>IMPROPER</td><td>CG-CA-CH2-HB1</td><td>IMP3</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>ASP</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>ASP</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>ASP</td><td>DIHEDRAL</td><td>CA-CB-CG-OD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>ASP</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>ASP</td><td>IMPROPER</td><td>OD2-OD1-CB-CG</td><td>IMP2</td></tr>\n"
    html += "<tr><td>ASP</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP3</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>CYS</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>CYS</td><td>DIHEDRAL</td><td>N-CA-CB-SG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>CYS</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>CYS</td><td>IMPROPER</td><td>SG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>CYS</td><td>IMPROPER</td><td>SG-CB-CA-C</td><td>IMP3</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>GLN</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>GLN</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>GLN</td><td>DIHEDRAL</td><td>CA-CB-CG-CD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>GLN</td><td>DIHEDRAL</td><td>CB-CG-CD-OE1</td><td>CHI3</td></tr>\n"
    html += "<tr><td>GLN</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>GLN</td><td>IMPROPER</td><td>NE2-OE1-CG-CD</td><td>IMP2</td></tr>\n"
    html += "<tr><td>GLN</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>GLN</td><td>IMPROPER</td><td>CD-CB-HG2-HG1</td><td>IMP4</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>GLU</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>GLU</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>GLU</td><td>DIHEDRAL</td><td>CA-CB-CG-CD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>GLU</td><td>DIHEDRAL</td><td>CB-CG-CD-OE1</td><td>CHI3</td></tr>\n"
    html += "<tr><td>GLU</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>GLU</td><td>IMPROPER</td><td>OE2-OE1-CG-CD</td><td>IMP2</td></tr>\n"
    html += "<tr><td>GLU</td><td>IMPROPER</td><td>CG-CA-HB1-HB2</td><td>IMP3</td></tr>\n"
    html += "<tr><td>GLU</td><td>IMPROPER</td><td>CD-CG-HG2-HG1</td><td>IMP4</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>GLY</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>GLY</td><td>IMPROPER</td><td>C-N-HA2-HA1</td><td>IMP1</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>HIS</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>HIS</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>HIS</td><td>DIHEDRAL</td><td>CA-CB-CG-ND1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>HIS</td><td>DIHEDRAL</td><td>CA-CB-CG-CD2</td><td>CHI3</td></tr>\n"
    html += "<tr><td>HIS</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>HIS</td><td>IMPROPER</td><td>CD2-ND1-CB-CG</td><td>IMP2</td></tr>\n"
    html += "<tr><td>HIS</td><td>IMPROPER</td><td>CD2-NE2-CE1-ND1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>HIS</td><td>IMPROPER</td><td>NE2-CE1-ND1-CG</td><td>IMP4</td></tr>\n"
    html += "<tr><td>HIS</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>ILE</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>ILE</td><td>DIHEDRAL</td><td>N-CA-CB-CG1</td><td>CHI1</td></tr>\n"
    html += "<tr><td>ILE</td><td>DIHEDRAL</td><td>CA-CB-CG1-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>ILE</td><td>DIHEDRAL</td><td>CB-CG1-CD1-CD11</td><td>CHI3</td></tr>\n"
    html += "<tr><td>ILE</td><td>DIHEDRAL</td><td>CA-CB-CG2-HG21</td><td>CHI4</td></tr>\n"
    html += "<tr><td>ILE</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>ILE</td><td>IMPROPER</td><td>CG1-CG2-CA-HB</td><td>IMP2</td></tr>\n"
    html += "<tr><td>ILE</td><td>IMPROPER</td><td>CD1-CB-HG12-HG11</td><td>IMP3</td></tr>\n"
    html += "<tr><td>ILE</td><td>IMPROPER</td><td>HG23-CB-HG22-HG21</td><td>IMP4</td></tr>\n"
    html += "<tr><td>ILE</td><td>IMPROPER</td><td>HD13-CG1-HD12-HD11</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>LEU</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>LEU</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>LEU</td><td>DIHEDRAL</td><td>CA-CB-CG-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>LEU</td><td>DIHEDRAL</td><td>CB-CG-CD1-HD11</td><td>CHI3</td></tr>\n"
    html += "<tr><td>LEU</td><td>DIHEDRAL</td><td>CB-CG-CD2-HD21</td><td>CHI4</td></tr>\n"
    html += "<tr><td>LEU</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>LEU</td><td>IMPROPER</td><td>CD2-CD1-CB-HG</td><td>IMP2</td></tr>\n"
    html += "<tr><td>LEU</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>LEU</td><td>IMPROPER</td><td>HD13-CG-HD12-HD11</td><td>IMP4</td></tr>\n"
    html += "<tr><td>LEU</td><td>IMPROPER</td><td>HD23-CG-HD22-HD21</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>LYS</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>LYS</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>LYS</td><td>DIHEDRAL</td><td>CA-CB-CG-CD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>LYS</td><td>DIHEDRAL</td><td>CD-CE-NZ-HZ1</td><td>CHI5</td></tr>\n"
    html += "<tr><td>LYS</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>LYS</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>LYS</td><td>IMPROPER</td><td>CD-CB-HG2-HG1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>LYS</td><td>IMPROPER</td><td>NZ-CD-HE2-HE1</td><td>IMP4</td></tr>\n"
    html += "<tr><td>LYS</td><td>IMPROPER</td><td>HZ3-CE-HZ2-HZ1</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>MET</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>MET</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>MET</td><td>DIHEDRAL</td><td>CA-CB-CG-SD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>MET</td><td>DIHEDRAL</td><td>CG-SD-CE-HE1</td><td>CHI4</td></tr>\n"
    html += "<tr><td>MET</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>MET</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>MET</td><td>IMPROPER</td><td>SD-CB-HG2-HG1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>MET</td><td>IMPROPER</td><td>HE3-SD-HE2-HE1</td><td>IMP4</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>PHE</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>PHE</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>PHE</td><td>DIHEDRAL</td><td>CA-CB-CG-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>PHE</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>PHE</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>PHE</td><td>IMPROPER</td><td>CE2-CD2-CG-CB</td><td>IMP3</td></tr>\n"
    html += "<tr><td>PHE</td><td>IMPROPER</td><td>CZ-CE1-CD1-CG</td><td>IMP4</td></tr>\n"
    html += "<tr><td>PHE</td><td>IMPROPER</td><td>CG-CD2-CE2-CZ</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>PRO</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>PRO</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>PRO</td><td>DIHEDRAL</td><td>CA-CB-CG-CD</td><td>CHI2</td></tr>\n"
    html += "<tr><td>PRO</td><td>DIHEDRAL</td><td>CB-CG-CD-N</td><td>CHI3</td></tr>\n"
    html += "<tr><td>PRO</td><td>DIHEDRAL</td><td>CG-CD-N-CA</td><td>CHI4</td></tr>\n"
    html += "<tr><td>PRO</td><td>DIHEDRAL</td><td>CD-N-CA-CB</td><td>CHI5</td></tr>\n"
    html += "<tr><td>PRO</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>PRO</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>PRO</td><td>IMPROPER</td><td>CD-CB-HG2-HG1</td><td>IMP3</td></tr>\n"
    html += "<tr><td>PRO</td><td>IMPROPER</td><td>N-CG-HD2-HD1</td><td>IMP4</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>SER</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>SER</td><td>DIHEDRAL</td><td>N-CA-CB-OG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>SER</td><td>DIHEDRAL</td><td>CA-CB-OG-H</td><td>CHI2</td></tr>\n"
    html += "<tr><td>SER</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>SER</td><td>IMPROPER</td><td>OG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>THR</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>THR</td><td>DIHEDRAL</td><td>N-CA-CB-OG1</td><td>CHI1</td></tr>\n"
    html += "<tr><td>THR</td><td>DIHEDRAL</td><td>CA-CB-CG2-HG21</td><td>CHI2</td></tr>\n"
    html += "<tr><td>THR</td><td>DIHEDRAL</td><td>HG23-CB-OG1-H</td><td>CHI3</td></tr>\n"
    html += "<tr><td>THR</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>THR</td><td>IMPROPER</td><td>CG2-OG1-CA-HB</td><td>IMP2</td></tr>\n"
    html += "<tr><td>THR</td><td>IMPROPER</td><td>HG23-CB-HG22-HG21</td><td>IMP3</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>TRP</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>TRP</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>TRP</td><td>DIHEDRAL</td><td>CA-CB-CG-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>TRP</td><td>DIHEDRAL</td><td>CA-CB-CG-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>TRP</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>TRP</td><td>IMPROPER</td><td>CG-CA-HB2-HB1</td><td>IMP2</td></tr>\n"
    html += "<tr><td>TRP</td><td>IMPROPER</td><td>CZ2-CE2-CD2-CE3</td><td>IMP3</td></tr>\n"
    html += "<tr><td>TRP</td><td>IMPROPER</td><td>CH2-CZ2-CE2-NE1</td><td>IMP4</td></tr>\n"
    html += "<tr><td>TRP</td><td>IMPROPER</td><td>CE2-CD2-CG-CB</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>TYR</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>TYR</td><td>DIHEDRAL</td><td>N-CA-CB-CG</td><td>CHI1</td></tr>\n"
    html += "<tr><td>TYR</td><td>DIHEDRAL</td><td>CA-CB-CG-CD1</td><td>CHI2</td></tr>\n"
    html += "<tr><td>TYR</td><td>DIHEDRAL</td><td>CE2-CZ-OH-HH</td><td>CHI3</td></tr>\n"
    html += "<tr><td>TYR</td><td>IMPROPER</td><td>CD1-CE1-CZ-OH</td><td>IMP1</td></tr>\n"
    html += "<tr><td>TYR</td><td>IMPROPER</td><td>CE2-CD2-CG-CB</td><td>IMP2</td></tr>\n"
    html += "<tr><td>TYR</td><td>IMPROPER</td><td>CZ-CE1-CD1-CG</td><td>IMP3</td></tr>\n"
    html += "<tr><td>TYR</td><td>IMPROPER</td><td>CE2-CZ-CE1-CD1</td><td>IMP4</td></tr>\n"
    html += "<tr><td>TYR</td><td>IMPROPER</td><td>CE1-CD1-CG-CD2</td><td>IMP5</td></tr>\n"
    html += "<tr class='cppinnerheader'><td>VAL</td><td></td><td></td><td></tr>\n"
    html += "<tr><td>VAL</td><td>DIHEDRAL</td><td>N-CA-CB-CG1</td><td>CHI1</td></tr>\n"
    html += "<tr><td>VAL</td><td>DIHEDRAL</td><td>CA-CB-CG1-HG11</td><td>CHI2</td></tr>\n"
    html += "<tr><td>VAL</td><td>DIHEDRAL</td><td>CA-CB-CG2-HG21</td><td>CHI3</td></tr>\n"
    html += "<tr><td>VAL</td><td>IMPROPER</td><td>CB-C-N-HA</td><td>IMP1</td></tr>\n"
    html += "<tr><td>VAL</td><td>IMPROPER</td><td>CG2-CG1-CA-HB</td><td>IMP2</td></tr>\n"
    html += "<tr><td>VAL</td><td>IMPROPER</td><td>HG13-CB-HG12-HG11</td><td>IMP3</td></tr>\n"
    html += "<tr><td>VAL</td><td>IMPROPER</td><td>HG23-CB-HG22-HG21</td><td>IMP4</td></tr></table>\n"
    return (html)
 
def getCalcButton():
    html = ""
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_calcs.cgi" accept-charset="UTF-8">\n'
    html += "<p><input type='Submit' value='Browse Calculations' formaction='/cgi-bin/cgiwrap/ab002/thesis_calcs.cgi'/></p>\n"
    html += '</form>\n'
    return (html)

def getHighButton():
    html = ""
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_highpdb.cgi" accept-charset="UTF-8">\n'
    html += "<p><input type='Submit' value='Browse High Res PDBs' formaction='/cgi-bin/cgiwrap/ab002/thesis_highpdb.cgi'/></p>\n"
    html += '</form>\n'
    return (html)

def get2019Button():
    html = ""
    html += '<form method="post" action="/cgi-bin/cgiwrap/ab002/thesis_2019pdb.cgi" accept-charset="UTF-8">\n'
    html += "<p><input type='Submit' value='Browse 2018-2019 PDBs'' formaction='/cgi-bin/cgiwrap/ab002/thesis_2019pdb.cgi'/></p>\n"
    html += '</form>\n'
    return (html)

def getHighPDBsSql():
    return sqldb.getHighPDBsSql()
    
def get2019PDBsSql():
    return sqldb.get2019PDBsSql()

def getCalcsSql():
    return sqldb.getCalcsSql()
 
def middleReturnPDBs(sql):
    """
    param: datainput - the results from the text box
    returns: the results from the exe in a grid
    """

    try:  # calling the database
        df = sdb.read_sql(sql)
    except:
        df = pd.read_csv(sio("Error calling database,,"))

    # now create the html output
    html = ts.dataFrameToGrid(df)
    html += '<hr/>\n'
    return(html)

    
