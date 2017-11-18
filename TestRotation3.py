import numpy as np
import cv2
import printImage as pim
from Rotation import Rotation
from Rotation2 import Rotation2



lenna = cv2.imread("lennaGreySmall.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

print("\n\nlenna Image:")
pim.printUnsignedImage(lenna)

print("Lenna shape: ", lenna.shape)
cv2.imshow("Input Image", lenna)
cv2.waitKey()

rotObject = Rotation2(lenna, 90)
rotated_corners = rotObject.rotateCorners()
rotation_coord_matrix = rotObject.initializeRotationCoordMatrix()
rotObject.printImageCoordMatrix(rotation_coord_matrix)
rotObject.get_4_neighborhood(rotation_coord_matrix)
rotObject.printImageCoordMatrix(rotation_coord_matrix)

# rotated_image = rotObject.rotateImage_NearestNeighbor()
#
# print("\n\nRotated Image:")
# pim.printUnsignedImage(rotated_image)
#
# print("rotated_image shape: ", rotated_image.shape)
# cv2.imshow("rotated_image Image", rotated_image)
# cv2.waitKey()