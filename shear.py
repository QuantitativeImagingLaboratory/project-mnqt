"""
Project MNQT
Shear class
"""

import math
import numpy as np

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
            
        if is_m_negative:
            new_image = reflector.reflectOnAxisY(new_image)
                    
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
