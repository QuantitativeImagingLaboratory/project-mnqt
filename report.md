# Report 
#
# Project: Image Geometric Transformation
# 
# Team: MNQT
#

1. GUI

	We used tkinter for the GUI for our project. Right now it configures
all display images to be 400 x 400 pixels in the GUI display.  This means that
non-square images should be distorted.

2. Implementation

	a) Rotation:
		
		In implementing image rotation, we rotated the 4 corners of the
	input image to get the extent of the rotated image.  Then we constructed
	an empty rotated image.  For each pixel in the empty rotated image, we
	rotated back to the original image pixel grid to find an interpolation
	value.  For the bilinear interpolation, we created an array of the 4
	surrounding input image pixels. For the bicubic interpolation, we created
	an array of the 16 surrounding input image pixels.
		The first implementation of image rotation ran into problems
	because it seems more difficult to do interpolation based in the rotated
	grid.  The known locations in the rotated grid might not fall on integer
	value rows and columns.
