'''
Author: Rachel Alcraft
Created: 08/07/20
Description: manage the imputs from the program or command line for the program
'''

import cl_conversions

class inputs:
    def __init__(self,tag,radius,gaps,length,num_slices,difference,in_file,coords,out_dir):
        self.tag = tag
        self.radius = radius
        self.gaps = gaps
        self.length = length
        self.num_slices = num_slices
        self.in_file = in_file
        self.coords = coords
        self.out_dir = out_dir
        self.sides = int((length/gaps)/2)
        self.difference = "Density"
        if difference:
            self.difference = "Difference"

    def getRunSummary(self):
        return (self.tag + " Radius=" + str(round(self.radius,2)) + " Gaps=" + str(round(self.gaps,2)) + " Width=" + str(round(self.length,2)) + ' ' + self.difference)
    def getFileName(self, number,total,runtype,ext):
        return (str(number) + '_' + str(total) + '_' + self.tag + "_" + str(round(self.radius, 2)) + "_" + str(round(self.gaps, 2)) + "_" + str(round(self.length, 2))  + '_' + self.difference + '_' + runtype + '.' + ext)
    def getTag(self):
        return (self.tag + "_" + str(round(self.radius, 2)) + "_" + str(round(self.gaps, 2)) + "_" + str(round(self.length, 2)) + '_' + self.difference)
