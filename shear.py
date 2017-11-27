"""
Project MNQT
Shear class
"""

import math
import numpy as np

class Shear:
    """ Shear class to displace image horizontally or vertically proportionally to its distance from the origin """
    
    def shear(self, image, m, direction, interpolation):
        """ Calls the appropriate function to shear the image based on the interpolation method """
        
        m = float(m)
        is_horizontal = direction == "Horizontal"
        is_m_negative = m < 0
        
        # shears vertically by default, if horizontal just rotate by 90 then rotate back after
        if is_horizontal:
            image = np.rot90(image)
            
        # if m is negative, flip image to set the origin properly then flip back after
        if is_m_negative:
            image = np.fliplr(image)
            m = -m
            
        if interpolation == 'Bilinear':
            new_image = self.shear_bilinear(image, m)
            
        elif interpolation == 'Bicubic':
            new_image = self.shear_bicubic(image, m)
            
        else: # default to nearest neighbor
            new_image = self.shear_nearest_neighbor(image, m)
            
        if is_m_negative:
            new_image = np.fliplr(new_image)
                    
        if is_horizontal:
            new_image = np.rot90(new_image, -1)
                    
        return new_image
        
    def shear_nearest_neighbor(self, image, m):
        
        width, height = image.shape
        new_width = int(width + abs(m)*height)
        new_height = height
        new_image = np.zeros((new_width, new_height))
        
        for i in range(new_width):
            for j in range(new_height):
                # x' = x + m*y -> x = i - m*y 
                x = int(i - m*j)
                
                if x < 0:
                    new_image[i,j] = 0
                elif x >= width:
                    new_image[i,j] = 0
                else:
                    new_image[i,j] = image[x, j]
        
        return new_image
        
    def shear_bilinear(self, image, m):
        
        width, height = image.shape
        new_width = int(width + m*height)
        new_height = height
        new_image = np.zeros((new_width, new_height))
        
        for i in range(new_width):
            for j in range(new_height):
                # x' = x + m*y -> x = i - m*y 
                x = int(i - m*j)
                
                if x < 0:
                    x = 0
                if x >= width:
                    x = width - 1
        
        return new_image
        
    def shear_bicubic(self, image, m):
        
        width, height = image.shape
        new_width = int(width + m*height)
        new_height = height
        new_image = np.zeros((new_width, new_height))
        
        for i in range(new_width):
            for j in range(new_height):
                # x' = x + m*y -> x = x' - m*y 
                x = int(i - m*j)
                
                if x < 0:
                    x = 0
                if x >= width:
                    x = width - 1
        
        return new_image
