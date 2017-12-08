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
	an array of the 4 surrounding input image pixels but bicubic interpolation 
    uses 16 inputs to perform the calculations. Rest of the 12 inputs come from
    derivates. We find X derivative, Y derivative and cross derivative for each 
    of the 4 neighbouring pixels. Then those 16 coefficients are used in the formula 
    to get the interpolated value.
		The first implementation of image rotation ran into problems
	because it seems more difficult to do interpolation based in the rotated
	grid.  The known locations in the rotated grid might not fall on integer
	value rows and columns.
    
    b) Scaling:
        Implementation for scaling images was essentially the same as for
    the homework, except we take the new values for width and height rather
    than multipliers *fx* and *fy*. We instead calculate the *fx* and *fy* 
    values based upon the input image's width and height and the target values.
    
    c) Shearing:
        The shearing algorithm ended up being fairly straightforward, once we
    got the hang of it. To calculate the new image width, we take the original
    width plus the heigh multiplied by the absolute value of the multiplier *m*. 
    The absolute value is important because negative values of *m* will still 
    result in a wider image. For each pixel *i,j* in the new image, we calculate
    the value *x* to which it maps back: *x* = *i* - *mj*. If this value is
    outside the bounds of the original image, we set the value of the new pixel
    to 0 (black). Otherwise, we set it based upon the interpolation method.
        By default, this method works for positive values of *m* and only in
    the vertical direction. Rather than try and make the algorithm more complex,
    we instead transformed the image matrix into one which matches that setup.
        For negative *m*, the issue is that the image shears from the origin.
    Since for negative *m* pixels extend back past the origin, this result in
    pixels being cut off, as if it had been translated. To counter this, if *m*
    is negative, we flip the image horizontally and set *m* to be positive. This
    results in the correct origin being used. Then after the new image is
    calculated, we flip it back again.
        For horizontal shearing, we could implement a different algorithm which
    has essentially the same formulas but targeting different values:
    *y* = *j* - *mi*. However, we can reduce it to the previously solved problem
    by rotating the matrix before and after. When the matrix is rotated 90
    degrees, it matches the matrix which can be sheared vertically. Then once
    the new image is calculated, rotate it -90 degrees back to the original
    orientation.
        In case of both these conditions, we only need to undo them in the
    opposite order we did them in. We chose to rotate -> flip -> calculate
    -> flip -> rotate, but either way works.
    
    d) Translation:
        We determine the left, right, top, and bottom padding based off of the
    x_translation and y_translation variables. Positive values move the image
    down and right, negative values shift it up and left. We use the np.pad
    function to add 0s as needed based on the padding values, then take the
    pixels [bottom_pad:height+bottom_pad, right_pad:width+right_pad].
    The only difficult part was remembering to swap the left/right and up/down
    order in the image. Since x is shifting the column value, it comes second.
    Y is shifting the rows up or down, so it comes first.
