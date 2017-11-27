from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
from Rotation2 import Rotation2
from scale import Scale


class ProjectMNQT_UI:

    # cv2 images
    inputImage = None

    # gui labels
    inputImageLabel = None
    outputImageLabel = None

    # gui entries
    rotationAngleEntry = None
    scaling_x_Entry = None
    scaling_y_Entry = None
    translation_x_Entry = None
    translation_y_Entry = None

    # gui pulldown
    interpVar = None
    reflectionVar = None

    mainframe = None

    # radio buttons
    transformationSelection = None

    # image sizes
    IMAGE_SIZE = (500, 500)

    def __init__(self, master): # master means root or main window

        master.configure(background="gainsboro")

        ## ****** Main Menu ******
        menu = Menu(master)

        master.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=quit)

        ## ****** Set Font ******
        myLargeFont = Font(family="Arial", size=24)
        mySmallFont = Font(family="Arial", size=16)

        ## ****** Top Toolbar ******
        toolbar = Frame(master, bg="slate gray")

        getImageButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        getImageButton.pack(side=LEFT, padx=20, pady=20)

        projectNameLabel = Label(toolbar, text = "Image Geometric Transformation Project", font=myLargeFont, bg="slate gray")
        projectNameLabel.pack(side=LEFT, padx=100, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)

        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        self.mainframe = Frame(root, bg="gainsboro")  # frame is a blank widget
        self.mainframe.pack()

        self.mainframe.columnconfigure(1, weight=1)


        ## ****** Input image ******
        self.inputImageLabel = Label(self.mainframe)
        self.inputImageLabel.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)


        ### ****** Transform Button ******
        transformButton = Button(self.mainframe, text="Transform", bd=0, highlightthickness=0, relief='ridge',
                                   command=self.runTransformation)
        transformButton.grid(row=0, column=4, columnspan=1, rowspan=4, sticky=W, padx=25, pady=25)

        buttonImage = cv2.imread("greenArrow.png")
        buttonImageDisplay = self.makeDisplayImage(buttonImage, (70, 70))
        transformButton.configure(image=buttonImageDisplay)
        transformButton.image = buttonImageDisplay


        ## ****** Output Image ******
        self.outputImageLabel = Label(self.mainframe)
        self.outputImageLabel.grid(row=0, column=5, columnspan=4, rowspan=4, sticky=E, padx=50, pady=30)


        ## ****** Put Empty Image in Image Labels ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, self.IMAGE_SIZE)
        self.inputImageLabel.configure(image=empty_image_display)
        self.inputImageLabel.image = empty_image_display
        self.outputImageLabel.configure(image=empty_image_display)
        self.outputImageLabel.image = empty_image_display



        ## ****** Rotate Widget ******
        self.transformationSelection = IntVar()
        self.transformationSelection.set(0)
        rotationRadioButton = Radiobutton(self.mainframe, text="  Rotation (° counter clockwise)", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 1)
        rotationRadioButton.grid(row=4, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.rotationAngleEntry = Entry(self.mainframe)
        self.rotationAngleEntry.grid(row=4, column=2, columnspan=1, rowspan=1, sticky=W)
        self.rotationAngleEntry.insert(0, '0')

        ## ****** Scaling Widget ******
        scalingRadioButton = Radiobutton(self.mainframe, text="  Scaling", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 2)
        scalingRadioButton.grid(row=5, column=0, columnspan=1, rowspan=1, sticky=W, padx=50, pady=20)

        self.scaling_x_Entry = Entry(self.mainframe)
        self.scaling_x_Entry.grid(row=5, column=1, columnspan=1, rowspan=1, sticky=W)
        self.scaling_x_Entry.insert(0, 'Height')

        self.scaling_y_Entry = Entry(self.mainframe)
        self.scaling_y_Entry.grid(row=5, column=2, columnspan=1, rowspan=1, sticky=W)
        self.scaling_y_Entry.insert(0, 'Width')

        ## ****** Interpolation Pulldown ******
        interpolationLabel = Label(self.mainframe, text="        Interpolation:", bg="gainsboro", font=mySmallFont)
        interpolationLabel.grid(row=6, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.interpVar = StringVar(self.mainframe)
        self.interpVar.set("Interpolation");

        interpolationPullDown = OptionMenu(self.mainframe, self.interpVar, "Nearest Neighbor", "Bilinear", "Bicubic")
        interpolationPullDown.grid(row=6, column=2, columnspan=2, rowspan=1, sticky=W, padx=0, pady=20)

        ## ****** Reflection Widget ******
        reflectionRadioButton = Radiobutton(self.mainframe, text="  Reflection", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 3)
        reflectionRadioButton.grid(row=4, column=5, columnspan=1, rowspan=1, sticky=W, padx=0, pady=20)

        self.reflectionVar = StringVar(self.mainframe)
        self.reflectionVar.set("Flip Type");

        reflectionPullDown = OptionMenu(self.mainframe, self.reflectionVar, "Left Right", "Top Bottom", "Diagonal")
        reflectionPullDown.grid(row=4, column=6, columnspan=2, rowspan=1, sticky=W, padx=0, pady=20)

        ## ****** Scaling Widget ******
        translationRadioButton = Radiobutton(self.mainframe, text="  Translation", font=mySmallFont, bg="gainsboro",
                                         variable=self.transformationSelection, value=4)
        translationRadioButton.grid(row=5, column=5, columnspan=1, rowspan=1, sticky=W, padx=0, pady=20)

        self.translation_x_Entry = Entry(self.mainframe)
        self.translation_x_Entry.grid(row=5, column=6, columnspan=1, rowspan=1, sticky=W)
        self.translation_x_Entry.insert(0, 'x:px')

        self.translation_y_Entry = Entry(self.mainframe)
        self.translation_y_Entry.grid(row=5, column=7, columnspan=1, rowspan=1, sticky=W)
        self.translation_y_Entry.insert(0, 'y:px')

    def getInputImage(self):
        filename = filedialog.askopenfilename()

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        self.displayImageOnLabel(self.inputImageLabel, self.inputImage, self.IMAGE_SIZE)
        self.setStatus("Loaded input image: " + filename)

    def runTransformation(self):
        if self.inputImage is None:
            self.setStatus("Please load and input image.")
            return

        if self.transformationSelection.get() == 1:
            rotationObject = Rotation2(self.inputImage, self.retrieveRotationAngle())

            rotationType = None
            rotated_image = None
            if self.interpVar.get() == "Bilinear":
                rotated_image = rotationObject.rotateImage_Bilinear()
                rotationType = "Bilinear"
            elif self.interpVar.get() == "Bicubic":
                rotated_image = rotationObject.rotateImage_Bicubic()
                rotationType = "Bicubic"
            else:
                rotated_image = rotationObject.rotateImage_NearestNeighbor()
                rotationType = "Nearest Neighbor"

            rotated_image_display = self.makeDisplayImage(rotated_image, self.IMAGE_SIZE)
            self.outputImageLabel.configure(image=rotated_image_display)
            self.outputImageLabel.image = rotated_image_display

            self.setStatus("Rotated image " + str(self.retrieveRotationAngle()) + "° using " + rotationType +
                            " interpolation.")

        elif self.transformationSelection.get() == 2:
            scale_object = Scale()
            
            scaled_image = scale_object.resize(self.inputImage, self.scaling_x_Entry.get(), self.scaling_y_Entry.get(), self.interpVar.get())
            scaled_image_display = self.makeDisplayImage(scaled_image, self.IMAGE_SIZE)
            self.outputImageLabel.configure(image=scaled_image_display)
            self.outputImageLabel.image = scaled_image_display
            
            self.setStatus("Scaled image using " + self.interpVar.get() + " interpolation.")

        elif self.transformationSelection.get() == 3:
            print("Reflection Radio Button Selected")
            self.setStatus("Reflecting image.")

        elif self.transformationSelection.get() == 4:
            print("Translation Radio Button Selected")
            self.setStatus("Translating image.")

        else:
            self.setStatus("No image geometric transformation is selected.")


    def retrieveRotationAngle(self):
        rotationAngleString = self.rotationAngleEntry.get()
        rotationAngle = 0
        try:
            rotationAngle = float(rotationAngleString)
            self.setStatus("Setting rotation angle to " + str(rotationAngle) + "°")
        except ValueError:
            self.setStatus("Setting default rotation angle to 0°")
        return rotationAngle


    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString


    def displayImageOnLabel(self, label, image, image_size):
        """ Display input image on input label"""
        displayImage = self.makeDisplayImage(image, image_size)

        label.configure(image=displayImage)
        label.image = displayImage


    def makeDisplayImage(self, cv2_image, shape):
        disp_im = Image.fromarray(cv2_image)
        disp_im = disp_im.resize(shape, Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)


    def doNothing(self):
        print("Not implemented yet.")




# start Project GUI
root = Tk()

p = ProjectMNQT_UI(root)

root.mainloop()

