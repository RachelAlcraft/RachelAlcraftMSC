
'''
Author: Rachel Alcraft
Created: 2/07/20
'''

import math
import numpy as np
PI = np.pi

class transformation:
    def __init__(self,A,B,C):
        self.rotations = []
        self.A = A
        self.B = B
        self.C = C
        self.translation = A
        self.A = [self.A[0] - A[0],self.A[1] - A[1],self.A[2] - A[2]] #A is translated to the origibn
        self.B = [self.B[0] - A[0],self.B[1] - A[1],self.B[2] - A[2]]
        self.C = [self.C[0] - A[0],self.C[1] - A[1],self.C[2] - A[2]]
        print('\t\ttransformation object',A,B,C)
        print('\t\ttranslated to', self.A, self.B, self.C)

        #Set it all up in the init
        theta = self.get2dRotationAngle(self.B[0], self.B[1])
        self.rotations.append(['XY', theta])
        self.B[0],self.B[1] = self.addRotation(self.B[0],self.B[1],theta) #holds x and zeroes y
        self.C[0],self.C[1] = self.addRotation(self.C[0],self.C[1],theta)
        print('\t\t\t coords after XY', theta, self.A, self.B, self.C)

        theta = self.get2dRotationAngle(self.B[0], self.B[2])
        self.B[0],self.B[2] = self.addRotation(self.B[0],self.B[2], theta) #holds x and zeroes z
        self.C[0], self.C[2] = self.addRotation(self.C[0], self.C[2],theta)
        self.rotations.append(['XZ', theta])
        print('\t\t\t coords after XZ', theta, self.A, self.B, self.C)

        theta = self.get2dRotationAngle(self.C[1], self.C[2])
        self.C[1], self.C[2] = self.addRotation(self.C[1], self.C[2],theta)  # holds y and zeroes z
        self.rotations.append(['YZ', theta])
        print('\t\t\t coords after YZ', theta, self.A, self.B, self.C)
        # we will end up with [0,0,0], [x,0,0],[x,y,0]

    def applyTransformation(self,point,print_info):
        # we apply these in reverse order
        print_info = False
        if print_info:
            print('\t\t\t\t applying transformation',point)
        point[1],point[2] = self.rotateAboutOrigin(point[1],point[2],360-self.rotations[2][1],print_info)
        if print_info:
            print('\t\t\t\t applying transformation',point,360-self.rotations[2][1])
        point[0], point[2] = self.rotateAboutOrigin(point[0], point[2], 360-self.rotations[1][1],print_info)
        if print_info:
            print('\t\t\t\t applying transformation',point,360-self.rotations[1][1])
        point[0], point[1] = self.rotateAboutOrigin(point[0], point[1], 360-self.rotations[0][1],print_info)
        if print_info:
            print('\t\t\t\t applying transformation',point,360-self.rotations[0][1])
        point[0] = self.translation[0] + point[0]
        point[1] = self.translation[1] + point[1]
        point[2] = self.translation[2] + point[2]
        if print_info:
            print('\t\t\t\t applying transformation',point)
        return (point)


    def addRotation(self,px,py,theta):
        #print('\t\t\t XY theta=',theta)
        # transform B and C for continued transformations
        x,y = self.rotateAboutOrigin(px,py,theta,False)
        return([x,y])

    def addRotationYZ(self):
        theta = self.get2dRotationAngle(self.B[1],self.B[2])
        if theta < 0:
            theta = 360 + theta
        self.rotations.append(['YZ',theta])
        print('\t\t\t YZ theta=', theta)
        # transform B and C for continued transformations
        self.B[1],self.B[2] = self.rotateAboutOrigin(self.B[1],self.B[2],theta,False)
        self.C[1], self.C[2] = self.rotateAboutOrigin(self.C[1],self.C[2], theta,False)

    def addRotationXZ(self):
        theta = self.get2dRotationAngle(self.C[0],self.C[2])
        if theta < 0:
            theta = 360 + theta
        self.rotations.append(['XZ',theta])
        print('\t\t\t XZ theta=', theta)
        # transform B and C for continued transformations
        self.C[0],self.C[1] = self.rotateAboutOrigin(self.C[0],self.C[2],theta,False)

    def get2dRotationAngle(self,x,y):
        '''
        :param x: Coordinate 1 in the flat plane
        :param y: Coordinate 2 in the flat plane
        :return: the angle of rotation
        Description:
        We need to track which quartile we are going from and to
        '''
        theta = 0
        quartile_from = self.getQuartile(x,y)

        mag_o_b_sq = (x ** 2 + y ** 2)
        mag_o_b = math.sqrt((x*x + y*y))

        if mag_o_b > 0.00001:# the magnitude must be > 0 or the angle is lets say 0, we are not moving anywhere
            vector_o_a = np.array([x,y])
            vector_o_b = np.array([mag_o_b,0])
            vector_a_b = vector_o_a - vector_o_b
            mag_a_b_sq = vector_a_b[0] ** 2 + vector_a_b[1] ** 2
            mag_a_b = (vector_a_b[0]**2 + vector_a_b[1]**2)**0.5
            # Find theta with the cosine rule
            # a2 = b2 + c2 - 2bc(cosA)
            # where a2 = mag_a_b_sq, b2 = c2 = mag_o_b_sq and bc = mag_o_b_sq
            cos_theta = ((2*mag_o_b_sq) - mag_a_b_sq)/(2*mag_o_b_sq)
            theta = math.acos(cos_theta)# in radians
            theta /= (2*PI)
            theta *= 360 # in degrees
            if quartile_from == 4 or quartile_from == 3:
                theta = 360 - theta
            print('\t\t\t\t theta 2d calc',vector_o_a,vector_o_b,vector_a_b,mag_a_b_sq,cos_theta,theta)

        if theta < 0:
            theta = 360 + theta

        return float(theta)

    def rotateAboutOrigin(self,x,y,alpha,print_info):
        '''
        :param x: coord 1 to rotate
        :param y: coord 2 to rotate
        :param theta: angle to rotate, clockwise
        :return: the new coordinates
        Description:
        This wraps the main rotation function, splitting the rotation into quadrants
        '''
        #print('\tRotate:', x, y, theta)
        angle_to_apply = float(alpha)
        angle_remaining = float(alpha)
        if angle_to_apply > 90.0:
            angle_to_apply = 90.0
            angle_remaining = alpha - 90.0
        else:
            angle_remaining = 0
        if print_info:
            print('\t\t\t\t angles',angle_to_apply,angle_remaining)
        while angle_to_apply > 0.0:
            x,y = self.rotateAboutOriginSingleQuadrant(x, y, angle_to_apply,print_info)
            if angle_remaining > 0.0001:
                if angle_remaining > 90:
                    angle_to_apply = 90
                    angle_remaining = angle_remaining - 90
                else:
                    angle_to_apply = angle_remaining
                    angle_remaining = 0
            else:
                angle_to_apply = 0
        return([x,y])

    def rotateAboutOriginSingleQuadrant(self, x, y, theta,print_info):
        '''
        :param x: the 1st coord
        :param y: the 2nd coord
        :param theta: the angle of rotation, no more than 90 degrees
        :return: the new coordinates given the rotation
        Description
        Triangle has points origin, o, original point, a and new point b
        '''
        #print(x, y)
        theta = (theta/360) * (2*PI)
        vec_o_a = np.array([x,y])
        mag_o_a = math.sqrt(vec_o_a[0]**2 + vec_o_a[1]**2) # this is the hypotenuse of a right angled triangle with the x axis
        if mag_o_a > 0.0001: # or we are not really moving at all
            quartile_from = self.getQuartile(x,y) # need to establish the quartiles
            #print('\t\tFrom', quartile_from, x,y,theta)

            sin_A = abs(y)/mag_o_a
            angle_A = math.asin(sin_A)
            # subtract theta and we have the angle made with the x axis for the lower side of the triangle
            angle_B = round(angle_A - theta,5)
            if abs(angle_B) < 0.0001:
                angle_B = 0 # ie it is going to lie flat on the axis
            if quartile_from == 2 or quartile_from == 4:
                angle_B = angle_A + theta
            # Our new x and y are the points at the end of this triangle
            # Our max quadrant change is 1 due to the 90 degree restriction
            quartile_to = quartile_from
            if quartile_from == 1:
                if theta > angle_A:
                    angle_B = round(theta - angle_A,5)
                    quartile_to = 4
            elif quartile_from == 2:
                if angle_A + theta > PI/2:
                    angle_B = PI - (angle_A + theta)
                    quartile_to = 1
            elif quartile_from == 3:
                if theta > angle_A:
                    angle_B = theta - angle_A
                    quartile_to = 2
            else: # MUST bu Q4
                if angle_A + theta > PI/2:
                    angle_B = PI - (theta + angle_A)
                    quartile_to = 3
            # Now we can find x and y
            x = math.cos(angle_B) * mag_o_a
            y = math.sin(angle_B) * mag_o_a
            #print('\t\t\t\t rotation - To', quartile_to, x, y,theta,angle_A,angle_B)
            if quartile_to == 2 or quartile_to == 3:
                x *= -1
            if quartile_to == 3 or quartile_to == 4:
                y *= -1
        #print(x,y)
        return ([round(x,5),round(y,5)])

    def getQuartile(self,x,y):
        quartile = 1
        #Handle 0,0 and >< 0 seperately
        if x == 0 and y == 0:
            quartile = 1
        elif x > 0 and y == 0:
            quartile = 1
        elif x == 0 and y > 0:
            quartile = 2
        elif x < 0 and y == 0:
            quartile = 3
        elif x == 0 and y < 0:
            quartile = 4
        elif (x > 0 and y > 0):
            quartile = 1
        elif (x < 0 and y > 0):
            quartile = 2
        elif (x < 0 and y < 0):
            quartile = 3
        elif (x > 0 and y < 0):
            quartile = 4
        return quartile