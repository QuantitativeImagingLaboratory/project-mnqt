import numpy as np
import cv2
import printImage as pim
from Rotation import Rotation



lenna = cv2.imread("lennaGreySmall.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

print("Lenna shape: ", lenna.shape)
cv2.imshow("Input Image", lenna)
cv2.waitKey()

print("\n\nInput Image:")
pim.printUnsignedImage(lenna)

rotationObject = Rotation(lenna)



rotatedCoordMatrix = rotationObject.getRotatedCoordMatrix(lenna, 90)
rotationObject.printImageCoordMatrix(rotatedCoordMatrix)


rotated_image = rotationObject.temporaryRotatedImage(90)
cv2.imshow("Rotated Image", rotated_image)                              # negative angle is clockwise
cv2.waitKey()

print("\n\nRotated Image:")
pim.printUnsignedImage(rotated_image)


empty_rotated_coord_matrix = rotationObject.makeEmptyRotatedImageCoordMatrix(rotatedCoordMatrix)

rotationObject.printImageCoordMatrix(empty_rotated_coord_matrix)

rotated_coord_matrix_with_values = rotationObject.rotateBackwards_NearestNeighbor(empty_rotated_coord_matrix, -45)
rotationObject.printImageCoordMatrix(rotated_coord_matrix_with_values)