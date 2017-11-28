"""
Project MNQT
Reflection class
"""

import numpy as np

class Reflection:

    def reflectOnAxisX(self, image):

        row, col = image.shape
        new_image = np.zeros((row, col))

        for x in range(row):
            for y in range(col):
                new_image[x, y] = image[row - x -1 , y]

        return new_image


    def reflectOnAxisY(self, image):
        row, col = image.shape
        new_image = np.zeros((row, col))

        for x in range(row):
            for y in range(col):
                new_image[x, y] = image[x, col - y - 1]

        return new_image
