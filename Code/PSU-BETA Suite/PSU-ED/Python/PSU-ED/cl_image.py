import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
# Manipulate  images
plt.style.use('seaborn-whitegrid')




class htmlImageString:
    def __init__(self):
        self.cubes = []
    def init(self,tag,sides,gaps,dens_type):
        self.dens_type = dens_type
        self.colourmap = 'inferno'
        if dens_type == 'Difference':
            self.colourmap = 'seismic_r'
        self.html = ''
        self.html += '<!DOCTYPE html>\n'
        self.html += '<html lang="en">\n'
        self.html += '<head>\n'
        self.html += '<title>Rachel Alcraft</title>\n'
        self.html += '<style>'
        self.html += 'body {background-color: linen;}'
        self.html += 'table,th,td {border: 1px solid linen;background-color: lemonChiffon;}'
        self.html += '</style>'
        self.html += '</head>\n'
        self.html += '<body>\n'
        self.html += '<div style = "text-align:center;">\n'
        self.html += '<h1>' + tag + '</h1>\n'
    def getFinalString(self):
        self.html += '</div>\n'
        self.html += '</body>\n'
        self.html += '</html>\n'
        return self.html
    def startTable(self):
        self.html += '<table style="width:90%">\n'
    def endTable(self):
        self.html += '</table>\n'
    def addHeader(self,header):
        self.html += '<h2>' + header + '</h2>\n'
    def addBreak(self):
        self.html += '<br/>\n'
    def addRow(self,vals):
        self.html += '<tr>'
        for v in range(0,len(vals)):
            self.html += '<td>' + str(vals[v]) + '</td>'
        self.html += '</tr>\n'

    def add3dImage(self,data,order,newrow,endrow):
        # Copied from
        # https://stackoverflow.com/questions/45969974/what-is-the-most-efficient-way-to-plot-3d-array-in-python
        # Create the x, y, and z coordinate arrays.  We use
        # numpy's broadcasting to do all the hard work for us.
        # We could shorten this even more by using np.meshgrid.
        x = np.arange(data.shape[0])[:, None, None]
        y = np.arange(data.shape[1])[None, :, None]
        z = np.arange(data.shape[2])[None, None, :]
        x, y, z = np.broadcast_arrays(x, y, z)

        # Turn the volumetric data into an RGB array that's
        # just grayscale.  There might be better ways to make
        # ax.scatter happy.
        c = np.tile(data.ravel()[:, None], [1, 3])
        cx=tuple([data[x, y, z], data[x, y, z], data[x, y, z], 1])
        cy = tuple([data[y, z, x], data[y, z, x], data[y, z, x], 1])
        cz = tuple([data[z, x, y], data[z, x, y], data[z, x, y], 1])
        c = np.tile(data.ravel()[:, None], [1, 3])
        # Do the plotting in a single call.
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        if order == 0:
            ax.scatter(x, y, z, c=data.ravel(),cmap=self.colourmap)
            ax.set_xlabel('x', linespacing=2, size=10, fontweight='bold')
            ax.set_ylabel('y', linespacing=2, size=10, fontweight='bold')
            ax.set_zlabel('z', linespacing=2, size=10, fontweight='bold')
        elif order == 1:
            ax.scatter(y, z,x, c=data.ravel(),cmap=self.colourmap)
            ax.set_xlabel('y', linespacing=2, size=10, fontweight='bold')
            ax.set_ylabel('z', linespacing=2, size=10, fontweight='bold')
            ax.set_zlabel('x', linespacing=2, size=10, fontweight='bold')
        else:
            ax.scatter(z,x,y, c=data.ravel(),cmap=self.colourmap)
            ax.set_xlabel('z', linespacing=2, size=10, fontweight='bold')
            ax.set_ylabel('x', linespacing=2, size=10, fontweight='bold')
            ax.set_zlabel('y', linespacing=2, size=10, fontweight='bold')
        #ax.grid(False)
        #plt.axis('off')
        ax.invert_xaxis()
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encodedImage = base64.b64encode(img.getvalue())
        plt.close('all')
        img_html = '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedImage.decode('utf-8')) + '\n'

        # Write to the html
        if newrow:
            self.html += '<tr>\n'
        self.html += img_html
        if endrow:
            self.html += '</tr>\n'

    def addImage(self,data,newrow, endrow,min_e,max_e):
        #print('\t\tmin=', min_e, 'max=', max_e)
        img_html = '<td></td>\n'
        if data != []:
            fig, ax = plt.subplots()
            if self.dens_type == 'Difference': # then we need the max and min to be arranged so tthat the centre is 0
                if min_e == -1 and max_e == -1:
                    min_e, max_e = self.getMinMax(data)
                max_diff = max(max_e,abs(min_e))
                min_diff = -1 * max_diff
                image = plt.imshow(data, cmap=self.colourmap, interpolation='nearest', origin='low', aspect='equal',vmin=min_diff, vmax=max_diff)
            elif min_e == -1 and max_e == -1:
                image = plt.imshow(data, cmap=self.colourmap, interpolation='nearest', origin='low', aspect='equal')
            else:
                image = plt.imshow(data, cmap=self.colourmap, interpolation='nearest', origin='low', aspect='equal', vmin=min_e,vmax=max_e)
            ax.grid(False)
            plt.axis('off')
            img = io.BytesIO()
            fig.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            encodedImage = base64.b64encode(img.getvalue())
            plt.close('all')
            img_html = '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedImage.decode('utf-8'))+ '\n'

        # Write to the html
        if newrow:
            self.html += '<tr>\n'
        self.html += img_html
        if endrow:
            self.html += '</tr>\n'

    def addHistogram(self,data,newrow,endrow):
        #print('\t\tmin=', min_e, 'max=', max_e)

        hist = data.ravel().tolist()

        fig, ax = plt.subplots()

        plt.hist(hist, EdgeColor='k', bins=100)

        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encodedImage = base64.b64encode(img.getvalue())
        plt.close('all')
        img_html = '<td><img width = 95% src="data:image/png;base64, {}"></td>'.format(encodedImage.decode('utf-8'))+ '\n'
        # Write to the html
        if newrow:
            self.html += '<tr>\n'
        self.html += img_html
        if endrow:
            self.html += '</tr>\n'

    def addCube(self,cubeobj,wholedensity,middle,middle_slices,mind,maxd,tag=''):
        # Firstr add header row for the cube
        self.addBreak()
        # a cube is a tuple of: density,pdb_code,central coors, central density, parallel coords, parallel density, plannar coords, planar density
        if cubeobj[1] == 'SUM':
            self.addHeader('Sum of all densities' + ' ' + tag)
        elif cubeobj[1] == 'TRANS':
            self.addHeader('Log-sum of all densities' + ' ' + tag)
        else:
            self.addHeader('Sample='+ cubeobj[2])

        self.startTable()
        if cubeobj[1] != 'SUM' and cubeobj[1] != 'TRANS':
            self.addRow(['pdb_code','central atom','ca density','parallel atom','pa density','planar atom','pl density'])
            self.addRow([cubeobj[1], [round(cubeobj[3][i],2) for i in range(3)], cubeobj[4], [round(cubeobj[5][i],2) for i in range(3)], cubeobj[6], [round(cubeobj[7][i],2) for i in range(3)], cubeobj[8]])

        self.endTable()

        cube = cubeobj[0]

        # first add 3d view
        if middle_slices == -1:
            self.addHeader('3d view of density')
            self.startTable()
            self.addRow(['xyz','yzx','zxy'])
            self.add3dImage(cube,0,True,False)
            self.add3dImage(cube, 1,False,False)
            self.add3dImage(cube, 2,False,True)
            self.endTable()


        #print(cubeobj[1],cube)

        # Add a histogram of the data
        if cubeobj[1] != 'SUM':
            if cubeobj[1] != 'TRANS':
                if middle_slices != 0:
                    self.addHeader('Histograms of densities')
                    self.startTable()
                    self.addRow(['Matrix Histogram', 'Entire Density Histogram'])
                    self.addHistogram(cube,True,False)
                    self.addHistogram(wholedensity,False,True)
                    self.endTable()

        self.addHeader('Slices along x,y and z')
        x, y, z = cube.shape
        maxlength = max(x,y,z)
        self.startTable()
        self.addRow(['Sliced x-wise', 'Sliced y-wise',"Sliced z-wise"])
        for i in range(0, maxlength):
            rowx = ''
            rowy = ''
            rowz = ''
            xslice = []
            yslice = []
            zslice = []
            if x > i:
                rowx = str(i) + '/' + str(x)
                xslice = cube[i,:,:]
            if y > i:
                rowy = str(i) + '/' + str(y)
                yslice = cube[:,i,:]
            if z > i:
                rowz = str(i) + '/' + str(z)
                zslice = cube[:,:,i]
            if middle_slices == -1 or abs(middle-i) <= middle_slices:
                #print('\t\t',rowx, rowy, rowz)
                self.addRow([rowx,rowy,rowz])
                self.addImage(xslice, True, False,mind,maxd)
                self.addImage(yslice, False, False,mind,maxd)
                self.addImage(zslice, False, True,mind,maxd)
        self.endTable()


    def printCubesData(self, cubex,cubey,cubez,density_cube, middle,middle_slices):
        x, y, z = cubex.shape
        maxlength = max(x, y, z)
        print('\t\t cubes data',maxlength,middle,middle_slices)
        self.startTable()
        self.addRow(['i','j','k','x','y',"z","electrons"])
        for i in range(0, maxlength):
            for j in range(0, maxlength):
                for k in range(0, maxlength):
                    x = round(cubex[i, j, k], 3)
                    y = round(cubey[i, j, k], 3)
                    z = round(cubez[i, j, k], 3)
                    density = round(density_cube[i,j,k],3)
                    if middle_slices == -1:
                        self.addRow([i,j,k,x,y,z,density])
                        print('\t\t', [i,j,k,x,y,z,density])
                    elif (abs(i-middle) <= middle_slices) and (abs(j-middle) <= middle_slices) and (abs(k-middle) <= middle_slices):
                        self.addRow([i,j,k,x,y,z,density])
                        print('\t\t', [i,j,k,x,y,z],abs(i-middle),abs(j-middle),abs(k-middle))
        self.endTable()

    def getMinMax(self,data):
        maxd = -1000.0
        mind = 1000.0
        x,y = data.shape
        for i in range(0, x):
            for j in range(0, y):
                mind = min(mind, data[i, j])
                maxd = max(maxd, data[i, j])

        return([mind,maxd])
