'''
Author: Rachel Alcraft
Created: 08/07/20
Description: maanage the writing to file and creation of directory for the program
'''

import os
from datetime import datetime
from numpy import savetxt
import numpy as np

class files:
    def __init__(self,root,tag):
        self.root = root
        self.tag = tag
        self.dir = root + '/' + tag + '/'
        self.log = self.dir + 'log.txt'
        try:
            os.mkdir(self.dir)
        except OSError:
            print('E')
        else:
            print("Successfully created the directory %s " % self.dir)

    def getFilePath(self,filename):
        return(self.dir + filename)

    def print(self,text,filename):
        with open(self.dir + filename, 'w') as f:
            f.write(text)
            f.close()

    def saveMatrix(self,matrix,filename):
        x,y,z = matrix.shape
        with open(self.dir + filename, 'w') as outfile:
            savetxt(outfile, [int(x),int(y),int(z)], delimiter=',',fmt='%1.0f')
            for i in range(0,x):
                savetxt(outfile, matrix[0:x,0:y,i], delimiter=',',fmt='%1.5f')

    def saveMatrixInfo(self, tag, filename):
        with open(self.dir + filename + '_info.txt', 'w') as outfile:
            for t in tag:
                outfile.write(str(t) + str(','))

        # array = np.arange(27).reshape(3, 3, 3)
        # array[0, 0, 0] = '000'
        # array[0, 1, 0] = '010'
        # array[1, 1, 1] = '111'
        # array[2, 2, 2] = '111'
        #
        # with open(self.dir + filename + '.tst', 'w') as outfile2:
        #     for i in range(0,3):
        #         savetxt(outfile2, array[i], delimiter=',')

    def log(self,message):
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),message)

    def end(self,start,end):
        taken = end - start
        print('time taken=',taken)

