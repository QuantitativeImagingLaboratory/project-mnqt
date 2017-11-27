#
# Project MNQT
# Rotation class
#
#
import numpy as np

class RotationCoord:
    """Coordinate in Rotated Domain class, input image coordinates could be fractional """

    def __init__(self, rot_row, rot_col, rot_x, rot_y, inp_x, inp_y):
        self.rot_image_row = rot_row
        self.rot_image_col = rot_col
        self.rot_image_x = rot_x
        self.rot_image_y = rot_y

        self.input_image_x = inp_x
        self.input_image_y = inp_y

        self.input_image_surrounding_points = []
        self.intensity = None

    def __str__(self):
        """ Return string version for printing """

        rot_image_rc_str = "(%d, %d)" % (self.rot_image_row, self.rot_image_col)
        rot_image_xy_str = "(%d, %d)" % (self.rot_image_x, self.rot_image_y)
        inp_image_xy_str = "(%0.2f, %0.2f)" % (self.input_image_x, self.input_image_y)
        return " ( NEW_RC " + rot_image_rc_str + " , NEW_XY " + rot_image_xy_str + " , INP_XY " + inp_image_xy_str + " ), SurroundingPoints: " + str(self.input_image_surrounding_points)

class Rotation2:
    """Rotation class to rotate an image"""

    def __init__(self, image, angle):
        """ Constructor for Rotation2 class """
        self.inputImage = image
        self.rotation_angle = angle
        self.centroid = self.getCentroid(self.inputImage)


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


    def rotateCorners(self):
        """ Rotate the 4 corners of the image to find the extent of the rotated image """
        (N, M) = self.inputImage.shape
        corners = [(0,0), (0, N-1), (M-1, N-1), (M-1, 0)]
        #print(corners)
        rotated_corners = []
        for corner in corners:
            x = corner[0]   # x corresponds to columns
            y = corner[1]   # y corresponds to rows
            vec1 = self.makeVector(x, y, self.centroid)
            rot_vec1 = self.rotateVector(vec1, self.rotation_angle)
            rot_vec1_x = float(rot_vec1[0][0])
            rot_vec1_y = float(rot_vec1[1][0])
            rot_x = int(np.round(rot_vec1_x + self.centroid[0]))
            rot_y = int(np.round(self.centroid[1] - rot_vec1_y))
            rotated_corners.append( (rot_x, rot_y) )
        #print(rotated_corners)
        return rotated_corners


    def minRotatedImageXY(self):
        rotated_corners = self.rotateCorners()
        min_x = None
        min_y = None
        for corner in rotated_corners:
            if min_x is None or corner[0] < min_x :
                min_x = corner[0]
            if min_y is None or corner[1] < min_y :
                min_y = corner[1]
        return (min_x, min_y)


    def maxRotatedImageXY(self):
        rotated_corners = self.rotateCorners()
        max_x = None
        max_y = None
        for corner in rotated_corners:
            if max_x is None or corner[0] > max_x :
                max_x = corner[0]
            if max_y is None or corner[1] > max_y :
                max_y = corner[1]
        return (max_x, max_y)


    def initializeRotationCoordMatrix(self):
        """Make a coordinate matrix from image """
        min_corner = self.minRotatedImageXY()
        max_corner = self.maxRotatedImageXY()

        numRows = max_corner[1] - min_corner[1] + 1
        numCols = max_corner[0] - min_corner[0] + 1

        rotation_coord_matrix = []
        for ii in range(numRows):
            newline = []
            rot_row = ii # y corresponds to rows in the image
            for jj in range(numCols):
                rot_col = jj # x corresponds to cols in the image
                rot_x = rot_col + min_corner[0]
                rot_y = rot_row + min_corner[1]

                vec = self.makeVector(rot_x, rot_y, self.centroid)
                inp_vec = self.rotateVector(vec, self.rotation_angle*-1)
                inp_vec_x = float(inp_vec[0][0]) + self.centroid[0]
                inp_vec_y = self.centroid[1] - float(inp_vec[1][0])
                #print("ROTXY:", (rot_x, rot_y), ", Vec", vec, " InpVec,", inp_vec, " INP_VecXY", (inp_vec_x, inp_vec_y) )

                newRotCoord = RotationCoord(rot_row, rot_col, rot_x, rot_y, inp_vec_x, inp_vec_y)
                newline.append(newRotCoord)
            rotation_coord_matrix.append(newline)

        return rotation_coord_matrix


    def makeEmptyRotatedImage(self):
        """ Return empty rotated image without intensities but for full extent """
        min_corner = self.minRotatedImageXY()
        max_corner = self.maxRotatedImageXY()

        numRows = max_corner[1] - min_corner[1] + 1
        numCols = max_corner[0] - min_corner[0] + 1

        return np.zeros((numRows, numCols), np.uint8)


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


    def get_4_neighborhood(self, rotation_coord_matrix):
        """ Get 4 surrounding input Image points"""
        N = len(rotation_coord_matrix)
        for ii in range(N):
            M = len(rotation_coord_matrix[ii])
            current_row = rotation_coord_matrix[ii]
            for jj in range(M):
                floorRow = int(np.floor(current_row[jj].input_image_y))
                floorCol = int(np.floor(current_row[jj].input_image_x))
                ceilRow = floorRow + 1
                ceilCol = floorCol + 1
                #print("Currently at : xy: ", (current_row[jj].input_image_x, current_row[jj].input_image_y))

                # clear out input_image_surrounding_points list
                size_current_list = len(current_row[jj].input_image_surrounding_points)
                for index in range(size_current_list):
                    del current_row[jj].input_image_surrounding_points[size_current_list - index - 1]

                # get 4 surrounding input image points
                if self.isRCWithinInputImage(floorRow, floorCol):
                    intensity = self.inputImage[floorRow][floorCol]
                    current_row[jj].input_image_surrounding_points.append((floorCol, floorRow, intensity))
                else:
                    current_row[jj].input_image_surrounding_points.append((floorCol, floorRow, 0))

                if self.isRCWithinInputImage(floorRow, ceilCol):
                    intensity = self.inputImage[floorRow][ceilCol]
                    current_row[jj].input_image_surrounding_points.append((ceilCol, floorRow, intensity))
                else:
                    current_row[jj].input_image_surrounding_points.append((ceilCol, floorRow, 0))

                if self.isRCWithinInputImage(ceilRow, floorCol):
                    intensity = self.inputImage[ceilRow][floorCol]
                    current_row[jj].input_image_surrounding_points.append((floorCol, ceilRow, intensity))
                else:
                    current_row[jj].input_image_surrounding_points.append((floorCol, ceilRow, 0))

                if self.isRCWithinInputImage(ceilRow, ceilCol):
                    intensity = self.inputImage[ceilRow][ceilCol]
                    current_row[jj].input_image_surrounding_points.append((ceilCol, ceilRow, intensity))
                else:
                    current_row[jj].input_image_surrounding_points.append((ceilCol, ceilRow, 0))


    def get_16_neighborhood(self, rotation_coord_matrix):
        """ Get 16 surrounding input Image points"""

        N = len(rotation_coord_matrix)
        for ii in range(N):
            M = len(rotation_coord_matrix[ii])
            current_row = rotation_coord_matrix[ii]
            for jj in range(M):
                floor_InpImage_Row = int(np.floor(current_row[jj].input_image_y))
                floor_InpImage_Col = int(np.floor(current_row[jj].input_image_x))
                start_InpImage_Row = floor_InpImage_Row - 1
                start_InpImage_Col = floor_InpImage_Col - 1
                # clear out input_image_surrounding_points list
                size_current_list = len(current_row[jj].input_image_surrounding_points)
                for index in range(size_current_list):
                    del current_row[jj].input_image_surrounding_points[size_current_list - index - 1]
                # get 16 surrounding input image points
                for row_Addition in range(4):
                    for col_Addition in range(4):
                        cur_InpImage_Row = start_InpImage_Row + row_Addition
                        cur_InpImage_Col = start_InpImage_Col + col_Addition

                        if self.isRCWithinInputImage(cur_InpImage_Row, cur_InpImage_Col):
                            intensity = self.inputImage[cur_InpImage_Row][cur_InpImage_Col]
                            current_row[jj].input_image_surrounding_points.append((cur_InpImage_Col, cur_InpImage_Row, intensity))
                        else:
                            current_row[jj].input_image_surrounding_points.append((cur_InpImage_Col, cur_InpImage_Row, 0))


    def isRCWithinInputImage(self, row, col):
        """ Return True if row, column is valid for input image """
        (N, M) = self.inputImage.shape
        if row < 0 or row > N-1:
            return False
        if col < 0 or col > M-1:
            return False
        return True


    def rotateImage_NearestNeighbor(self):
        """ Rotate Image and do Nearest Neighbor """
        if self.rotation_angle % 360 == 0:
            return self.inputImage
        elif self.rotation_angle > 0:
            if self.rotation_angle % 270 == 0:
                return self.rotateImage270()
            elif self.rotation_angle % 180 == 0:
                return self.rotateImage180()
            elif self.rotation_angle % 90 == 0:
                return self.rotateImage90()
        else: # self.rotation_angle < 0
            negative_rotation_angle = np.abs(self.rotation_angle) + 180
            if negative_rotation_angle % 270 == 0:
                return self.rotateImage270()
            elif negative_rotation_angle % 180 == 0:
                return self.rotateImage180()
            elif negative_rotation_angle % 90 == 0:
                return self.rotateImage90()


        rotation_coord_matrix = self.initializeRotationCoordMatrix()
        rotated_image = self.makeEmptyRotatedImage()

        N = len(rotation_coord_matrix)
        for ii in range(N):
            M = len(rotation_coord_matrix[ii])
            curr_row = rotation_coord_matrix[ii]
            for jj in range(M):
                inputImage_NN_row = int(np.round(curr_row[jj].input_image_y))
                inputImage_NN_col = int(np.round(curr_row[jj].input_image_x))

                intensity = 0
                if self.isRCWithinInputImage(inputImage_NN_row, inputImage_NN_col):
                    intensity = self.inputImage[inputImage_NN_row][inputImage_NN_col]

                rotated_image[ii][jj] = intensity

        return rotated_image

    def rotateImage270(self):
        """ Rotate Image 270° """
        (N, M) = self.inputImage.shape
        rotated_image = np.zeros((M, N), np.uint8)
        for ii in range(N):
            for jj in range(M):
                rotated_image[jj][N-ii-1] = self.inputImage[ii][jj]
        return rotated_image

    def rotateImage180(self):
        """ Rotate Image 180° """
        (N, M) = self.inputImage.shape
        rotated_image = np.zeros((N, M), np.uint8)
        for ii in range(N):
            for jj in range(M):
                rotated_image[N-ii-1][jj] = self.inputImage[ii][jj]
        return rotated_image

    def rotateImage90(self):
        """ Rotate Image 90° """
        (N, M) = self.inputImage.shape
        rotated_image = np.zeros((M, N), np.uint8)
        for ii in range(N):
            for jj in range(M):
                rotated_image[jj][ii] = self.inputImage[ii][jj]
        return rotated_image

    def rotateImage_Bilinear(self):
        """ Rotate Image and do Bilinear Interpolation """
        rotated_image = self.rotateImage_NearestNeighbor()
        return rotated_image

    def rotateImage_Bicubic(self):
        """ Rotate Image and do Bicubic Interpolation"""
        rotated_image = self.rotateImage_NearestNeighbor()
        return rotated_image

