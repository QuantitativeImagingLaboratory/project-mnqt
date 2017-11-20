"""
Project MNQT
Scale class
"""

import numpy as np

class Scale:
    """ Scale class to adjust the width of an image """
    
    def resize(self, image, fx, fy, interpolation):
        """ Calls the appropriate function to scale the image based on the interpolation method """
        
        if interpolation == 'nearest_neighbor':
            return self.scale_nearest_neighbor(image, fx, fy)
            
        elif interpolation == 'bilinear':
            return self.scale_bilinear(image, fx, fy)
            
        elif interpolation == 'bicubic':
            return self.scale_bicubic(image, fx, fy)
    
    def scale_nearest_neighbor(self, image, fx, fy):
        """ Scales using nearest neighbor interpolation """
        
        fx = float(fx)
        fy = float(fy)
        width, height = image.shape
        new_width = int(width * fx)
        new_height = int(height * fy)
        
        new_image = np.zeros((new_width, new_height))
        for i in range(new_width):
            for j in range(new_height):
                new_image[i,j] = image[int(i/fx), int(j/fy)]

        return new_image
        
        
    def scale_bilinear(self, image, fx, fy):
        """ Scales using bilinear interpolation """
        
        fx = float(fx)
        fy = float(fy)
        width, height = image.shape
        new_width = int(width * fx)
        new_height = int(height * fy)
        
        new_image = np.zeros((new_width, new_height))
        
        
        return new_image
        
        
    def scale_bicubic(self, image, fx, fy):
        """ Scales using bicubic interpolation """
        
        fx = float(fx)
        fy = float(fy)
        width, height = image.shape
        new_width = int(width * fx)
        new_height = int(height * fy)
        
        new_image = np.zeros((new_width, new_height))
        
        
        return new_image
