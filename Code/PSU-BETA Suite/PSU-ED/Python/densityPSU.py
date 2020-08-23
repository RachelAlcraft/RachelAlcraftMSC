'''
Author: Rachel Alcraft
Created: 09/07/20
Description: Main runner page
'''
import cl_input
import cl_runner



############  USER INPUTS ############################

densruns = []
#densruns.append(['AtomLists/200 GLN AHELICES.csv','200 GLN AHelices'])
#densruns.append(['AtomLists/200 GLN AHELICES PLUS.csv','200 GLN AHelices Plus'])
#densruns.append(['AtomLists/200 GLN AHELICES MINUS.csv','200 GLN AHelices Minus'])
#densruns.append(['AtomLists/1US0 TYR.csv','1US0 TYR Ring 2'])
#densruns.append(['AtomLists/10 FAKE HIGH.csv','10 FAKE HIGH'])
#densruns.append(['AtomLists/10 FAKE MIDDLE.csv','10 FAKE MIDDLE'])
#densruns.append(['AtomLists/10 FAKE LOW.csv','10 FAKE LOW'])
#densruns.append(['AtomLists/50 LYS SIDE.csv','50 LYS SIDE'])
#densruns.append(['AtomLists/1EJG PEPTIDE MANY.csv','JELSCH MANY'])
#densruns.append(['AtomLists/1EJG PEPTIDE BOND.csv','JELSCH BOND 2'])

diffruns = []
#diffruns.append(['AtomLists/200 GLN AHELICES PLUS.csv','200 GLN AHelices Plus'])
#diffruns.append(['AtomLists/200 GLN AHELICES MINUS.csv','200 GLN AHelices Minus'])
#diffruns.append(['AtomLists/200 GLN AHELICES.csv','200 GLN AHelices'])
diffruns.append(['AtomLists/1US0 TYR.csv','1US0 TYR Ring 2'])
#diffruns.append(['AtomLists/10 FAKE HIGH.csv','10 FAKE HIGH'])
#diffruns.append(['AtomLists/10 FAKE MIDDLE.csv','10 FAKE MIDDLE'])
#diffruns.append(['AtomLists/10 FAKE LOW.csv','10 FAKE LOW'])
#diffruns.append(['AtomLists/50 LYS SIDE.csv','50 LYS SIDE'])
#diffruns.append(['AtomLists/1EJG PEPTIDE MANY.csv','JELSCH MANY'])
#diffruns.append(['AtomLists/1EJG PEPTIDE BOND.csv','JELSCH BOND 2'])




#results_dir = '/home/rachel/Documents/Bioinformatics/ResultsNotSynched'
results_dir = 'ResultsLocal'
conversions_file = 'chain_medians.cfg'
length = 10 # in Angstrom
gaps = 0.15
middle_slices = -1 # -1 means all
radius = 0 # 0 means interpolated point density

# PROGRAM EXECUTION BEGINS ############################################
for run in densruns:
    csv_file_input = run[0]
    tag = run[1]
    psu_inputs = cl_input.inputs(tag,radius,gaps,length,middle_slices,False,csv_file_input,None,results_dir)
    psu_runner = cl_runner.runner(psu_inputs)
    psu_runner.runCreateCoordsFile()
    psu_runner.runCreateEachDensityMatrix()
    psu_runner.runCreateEachMatrix()
    psu_runner.runGetEachMatrixAndSum()
    psu_runner.end()

for run in diffruns:
    csv_file_input = run[0]
    tag = run[1]
    psu_inputs = cl_input.inputs(tag,radius,gaps,length,middle_slices,True,csv_file_input,None,results_dir)
    psu_runner = cl_runner.runner(psu_inputs)
    psu_runner.runCreateCoordsFile()
    psu_runner.runCreateEachDensityMatrix()
    psu_runner.runCreateEachMatrix()
    psu_runner.runGetEachMatrixAndSum()
    psu_runner.end()
