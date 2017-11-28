"""
Project MNQT
Shear class
"""

import math
import numpy as np

from Interpolation import Interpolation
from Reflection import Reflection

class Shear:
    """ Shear class to displace image horizontally or vertically proportionally to its distance from the origin """
    
    def shear(self, image, m, direction, interpolation):
        """ Calls the appropriate function to shear the image based on the interpolation method """
        
        m = float(m)
        is_horizontal = direction == "Horizontal"
        is_m_negative = m < 0
        reflector = Reflection()
        
        # shears vertically by default, if horizontal just rotate by 90 then rotate back after
        if is_horizontal:
            image = reflector.reflectOnAxisY(image).T
            
        # if m is negative, flip image to set the origin properly then flip back after
        if is_m_negative:
            image = reflector.reflectOnAxisY(image)
            m = -m
            
        if interpolation == 'Bilinear':
            new_image = self.shear_bilinear(image, m)
            
        elif interpolation == 'Bicubic':
            new_image = self.shear_bicubic(image, m)
            
        else: # default to nearest neighbor
            new_image = self.shear_nearest_neighbor(image, m)
            
        # flip back if necessary
        if is_m_negative:
            new_image = reflector.reflectOnAxisY(new_image)
        
        # rotate back if necessary
        if is_horizontal:
            new_image = reflector.reflectOnAxisY(new_image.T)
        
        return new_image
        
    def shear_nearest_neighbor(self, image, m):
        
        rows, cols = image.shape
        new_rows = int(rows + abs(m)*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # x' = x + m*y -> x = x' - m*y 
                x = int(i - m*j)
                
                if x < 0:
                    new_image[i,j] = 0
                elif x >= rows:
                    new_image[i,j] = 0
                else:
                    new_image[i,j] = image[x, j]
        
        return new_image
        
    def shear_bilinear(self, image, m):
        
        interpol = Interpolation()
        
        rows, cols = image.shape
        new_rows = int(rows + abs(m)*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # x' = x + m*y -> x = x' - m*y 
                y = i - m*j
                
                if int(y) < 0:
                    new_image[i,j] = 0
                elif int(y) >= rows:
                    new_image[i,j] = 0
                else:
                    # find 4 nearest neighbors
                    # ex: x = 20.5, y = 33.3 -> x1 = 20, x2 = 21, y1 = 33, y2 = 34
                    y1 = math.floor(y)
                    y2 = math.ceil(y)
                    if y2 >= rows:
                        y2 = rows - 1
                    x = x1 = x2 = j
                
                    # interpolate

                                                #          _C O L S__
                                                #           x1     dX     x2
                    q11 = image[y1,x1]          #R      y1| q11    r1    q21
                    q12 = image[y1,x1]          #O      dY|        P
                    q21 = image[y2,x2]          #W        |
                    q22 = image[y2,x2]          #S      y2| q12    r2    q22

                    new_image[i, j] = interpol.bilinear_interpolation((x1, q11, q12), (x2, q21, q22), y2, y1, (x, y))
        
        return new_image
        
    def shear_bicubic(self, image, m):
        
        rows, cols = image.shape
        new_rows = int(rows + m*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # x' = x + m*y -> x = x' - m*y 
                x = i - m*j
                
                if x < 0:
                    x = 0
                if x >= rows:
                    x = rows - 1
        
        return new_image
