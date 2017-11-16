import numpy as np
import cv2
import printImage as pim


class Coord:
    """Coordinate class"""
    x = None
    y = None
    intensity = None

    def __init__(self, xValue, yValue, intensityValue):
        self.x = xValue
        self.y = yValue
        self.intensity = intensityValue

    def __str__(self):
        """return string of coord"""
        #formatted_X = "%02d" % x
        return "( %.2f" % self.x + ", %.2f" % self.y + ", " + str(self.intensity) + ")"

class Rotation:
    """ Image Rotation class"""

    inputImage = None

    def __init__(self, image):
        """ Constructor for Rotation class """
        self.inputImage = image


    def getCentroid(self, image):
        """Return center of image"""
        centerX = 0.0
        centerY = 0.0
        (N, M) = self.inputImage.shape
        for x in range(M):
            centerX = centerX + x
        centerX = centerX / M
        for y in range(N):
            centerY = centerY + y
        centerY = centerY / N
        return(centerX, centerY)


    def rotateVector(self, vector, angle):
        """Rotates counter clockwise vector by angle"""
        angleRad = np.deg2rad(angle)
        RotationMatrix = np.matrix([[np.cos(angleRad), -1 * np.sin(angleRad)], [np.sin(angleRad), np.cos(angleRad)]])
        outputVector = RotationMatrix * vector
        return outputVector


    def makeVector(self, x, y, centroid):
        """Return a vector of x and y"""
        (centerX, centerY) = centroid
        xV = x - centerX
        yV = centerY - y
        return [[xV], [yV]]

    def initializeCoordMatrix(self, image):
        """Make a coordinate matrix from image """
        coordMatrix = []
        (N, M) = image.shape
        for ii in range(N):
            newline = []
            for jj in range(M):
                newline.append(Coord(ii, jj, image[ii][jj]))
            coordMatrix.append(newline)
        return coordMatrix

    def printImageCoordMatrix(self, imageCoordMatrix):
        """ Image Coord Matrix is 2D matrix """
        print("\n\n")
        N = len(imageCoordMatrix)
        for ii in range(N):
            M = len(imageCoordMatrix[ii])
            eachLine = imageCoordMatrix[ii]
            for jj in range(M):
                print(eachLine[jj], end="\t")
            print("", end="\n")

    def getRotatedCoordMatrix(self, image, angle):
        """ Get Rotated Coords as Coord Matrix """
        input_coords = self.initializeCoordMatrix(image)
        rotated_coords = []
        centroid = self.getCentroid(image)
        N = len(input_coords)
        for ii in range(N):
            M = len(input_coords[ii])
            eachInputLine = input_coords[ii]
            eachRotatedLine = []
            for jj in range(M):
                x = eachInputLine[jj].x
                y = eachInputLine[jj].y
                intensity = eachInputLine[jj].intensity
                vec = self.makeVector(x, y, centroid)
                rotvec = self.rotateVector(vec, angle)
                rotX = float(rotvec[0][0])
                rotY = float(rotvec[1][0])
                eachRotatedLine.append(Coord(centroid[0] + rotX , centroid[1] - rotY, intensity))
            rotated_coords.append(eachRotatedLine)
        return rotated_coords

    def getMinRowColRotatedCoords(self, rotated_coord_matrix):
        """ Return integer minimum Row of rotated coordinate matrix """
        N = len(rotated_coord_matrix)
        minRow = None
        minCol = None
        for ii in range(N):
            M = len(rotated_coord_matrix[ii])
            eachInputLine = rotated_coord_matrix[ii]
            for jj in range(M):
                rowValue = eachInputLine[jj].y
                colValue = eachInputLine[jj].x
                if minRow is None or rowValue < minRow:
                    minRow = rowValue
                if minCol is None or colValue < minCol:
                    minCol = colValue
        minRowInt = int(np.round(minRow))
        minColInt = int(np.round(minCol))
        return (minRowInt, minColInt)

    def getMaxRowColRotatedCoords(self, rotated_coord_matrix):
        """ Return integer minimum Row of rotated coordinate matrix """
        N = len(rotated_coord_matrix)
        maxRow = None
        maxCol = None
        for ii in range(N):
            M = len(rotated_coord_matrix[ii])
            eachInputLine = rotated_coord_matrix[ii]
            for jj in range(M):
                rowValue = eachInputLine[jj].y
                colValue = eachInputLine[jj].x
                if maxRow is None or rowValue > maxRow:
                    maxRow = rowValue
                if maxCol is None or colValue > maxCol:
                    maxCol = colValue
        maxRowInt = int(np.round(maxRow))
        maxColInt = int(np.round(maxCol))
        return (maxRowInt, maxColInt)

    def makeEmptyRotatedImage(self, rotated_coord_matrix):
        """ Return empty rotated image without intensities but for full extent """
        (minRow, minCol) = self.getMinRowColRotatedCoords(rotated_coord_matrix)
        (maxRow, maxCol) = self.getMaxRowColRotatedCoords(rotated_coord_matrix)

        numRows = maxRow - minRow + 1  # these will make the size of the rotated image
        numCols = maxCol - minCol + 1

        return np.zeros((numRows, numCols), np.uint8)

    def temporaryRotatedImage(self, angle):
        """Return nearest neighbor rotated image"""
        rotatedCoordMatrix = self.getRotatedCoordMatrix(self.inputImage, angle)  # positive angle is counter clockwise
        (minRotRow, minRotCol) = self.getMinRowColRotatedCoords(rotatedCoordMatrix)

        rotated_image = self.makeEmptyRotatedImage(rotatedCoordMatrix)
        NR = len(rotatedCoordMatrix)
        for ii in range(NR):
            MR = len(rotatedCoordMatrix[ii])
            eachInputLine = rotatedCoordMatrix[ii]
            for jj in range(MR):
                imageRow = int(np.round(eachInputLine[jj].y)) + -1*minRotRow
                imageCol = int(np.round(eachInputLine[jj].x)) + -1*minRotCol
                intensity = eachInputLine[jj].intensity
                rotated_image[imageRow][imageCol] = intensity
        return rotated_image
