"""
Project MNQT
Scale class
"""

import math
import numpy as np

class Scale:
    """ Scale class to adjust the rows of an image """
    
    def resize(self, image, new_rows, new_cols, interpolation):
        """ Calls the appropriate function to scale the image based on the interpolation method """
        
        new_rows = int(new_rows)
        new_cols = int(new_cols)
            
        if interpolation == 'Bilinear':
            return self.scale_bilinear(image, new_rows, new_cols)
            
        elif interpolation == 'Bicubic':
            return self.scale_bicubic(image, new_rows, new_cols)
            
        else: # default to nearest neighbor
            return self.scale_nearest_neighbor(image, new_rows, new_cols)
        
        
    def scale_nearest_neighbor(self, image, new_rows, new_cols):
        """ Scales using nearest neighbor interpolation """
        
        rows, cols = image.shape
        fx = float(new_rows)/rows
        fy = float(new_cols)/cols
        
        new_image = np.zeros((new_rows, new_cols))
        for i in range(new_rows):
            for j in range(new_cols):
                new_image[i,j] = image[int(i/fx), int(j/fy)]

        return new_image
        
    def scale_bilinear(self, image, new_rows, new_cols):
        """ Scales using bilinear interpolation """
        
        rows, cols = image.shape
        fx = float(new_rows)/rows
        fy = float(new_cols)/cols
        
        new_image = np.zeros((new_rows, new_cols))
        
        for i in range(new_rows):
            for j in range(new_cols):
                x = i/fx
                y = j/fy
                
                # find 4 nearest neighbors
                # ex: x = 20.5, y = 33.3 -> x1 = 20, x2 = 21, y1 = 33, y2 = 34
                x1 = math.floor(x)
                x2 = math.ceil(x)
                if x2 >= rows:
                    x2 = rows - 1
                    
                y1 = math.floor(y)
                y2 = math.ceil(y)
                if y2 >= cols:
                    y2 = cols - 1
            
                # interpolate
                new_image[i,j] = 0
        
        return new_image
        
    def scale_bicubic(self, image, new_rows, new_cols):
        """ Scales using bicubic interpolation """
        
        rows, cols = image.shape
        fx = float(new_rows)/rows
        fy = float(new_cols)/cols
        
        new_image = np.zeros
        
        for i in range(new_rows):
            for j in range(new_cols):
                x = i/fx
                y = j/fy
                
                # find 16 nearest neighbors
                x1 = math.floor(x)
                x2 = math.ceil(x)
                if x2 >= rows:
                    x2 = rows - 1
                if x1 == x2:
                    x0 = x1
                    x3 = x2
                else:
                    x0 = 0 if x1 <= 0 else x1 - 1
                    x3 = rows - 1 if x2 >= rows - 1 else x2 + 1
                    
                y1 = math.floor(y)
                y2 = math.ceil(y)
                if y2 >= cols:
                    y2 = cols - 1
                if y1 == y2:
                    y0 = y1
                    y3 = y2
                else:
                    y0 = 0 if y1 <= 0 else y1 - 1
                    y3 = cols - 1 if y2 >= cols - 1 else y2 + 1
                
                # interpolate
                new_image[i,j] = 0
        
        return new_image
