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
#densruns.append(['AtomLists/1US0 TYR.csv','1US0 TYR Ring'])
#densruns.append(['AtomLists/10 FAKE HIGH.csv','10 FAKE HIGH'])
#densruns.append(['AtomLists/10 FAKE MIDDLE.csv','10 FAKE MIDDLE'])
#densruns.append(['AtomLists/10 FAKE LOW.csv','10 FAKE LOW'])
densruns.append(['AtomLists/50 LYS SIDE.csv','50 LYS SIDE'])

diffruns = []
#diffruns.append(['AtomLists/200 GLN AHELICES.csv','200 GLN AHelices'])
#diffruns.append(['AtomLists/1US0 TYR.csv','1US0 TYR Ring'])
#diffruns.append(['AtomLists/10 FAKE HIGH.csv','10 FAKE HIGH'])
#diffruns.append(['AtomLists/10 FAKE MIDDLE.csv','10 FAKE MIDDLE'])
#diffruns.append(['AtomLists/10 FAKE LOW.csv','10 FAKE LOW'])
diffruns.append(['AtomLists/50 LYS SIDE.csv','50 LYS SIDE'])




#runs.append(['AtomLists/200 GLN BSHEETS.csv','200 GLN BSHEETS'])

#runs.append(['AtomLists/500 GLN AHELICES.csv','500 GLN AHelices'])
#runs.append(['AtomLists/30 GLN AHELICES.csv','30 GLN AHelices'])
#runs.append(['AtomLists/TAU 20 MIDDLE.csv','TAU 20 Middle'])
#runs.append(['AtomLists/1EJG THR.csv','TST2 Jelsch 1ejg THR'])
#runs.append(['AtomLists/3O4P_O_N_C.csv','Elias 3o4p O-N-C ILE'])
#runs.append(['AtomLists/3O4P ASP 229.csv','Elias 3o4p ASP 229'])
#runs.append(['AtomLists/1EJG THR.csv','Jelsch 1ejg THR'])
#runs.append(['AtomLists/1PJX_O_N_C.csv','1PJX O-N-C ILE radius 0.5'])
#runs.append(['AtomLists/1PJX_O_N_C_g2.csv','1PJX O-N-C ILE Group 2'])
#runs.append(['AtomLists/1PJX_O_N_C_g3.csv','1PJX O-N-C ILE Group 3'])
#runs.append(['AtomLists/1PJX_O_N_C_g4.csv','1PJX O-N-C ILE Group 4'])

#results_dir = '/home/rachel/Documents/Bioinformatics/ResultsNotSynched'
results_dir = 'ResultsLocal'
conversions_file = 'chain_medians.cfg'
length = 10 # in Angstrom
gaps = 0.1
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
