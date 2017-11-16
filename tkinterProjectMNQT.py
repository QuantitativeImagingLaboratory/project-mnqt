from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
from Rotation import Rotation


class ProjectMNQT_UI:

    # cv2 images
    inputImage = None

    # gui labels
    inputImageLabel = None
    outputImageLabel = None

    # gui entries
    rotationAngleEntry = None

    # gui pulldown
    interpVar = None

    mainframe = None

    # radio buttons
    rotationSelection = None
    scalingSelection = None

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

        ## ****** Top Toolbar ******
        toolbar = Frame(master, bg="azure3")

        getImageButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        getImageButton.pack(side=LEFT, padx=20, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)

        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        self.mainframe = Frame(root, bg="gainsboro")  # frame is a blank widget
        self.mainframe.pack()


        ## ****** Input image ******
        self.inputImageLabel = Label(self.mainframe)
        self.inputImageLabel.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)


        ### ****** Transform Button ******
        transformButton = Button(self.mainframe, text="Transform", bd=0, highlightthickness=0, relief='ridge',
                                   command=self.runTransformation)
        transformButton.grid(row=0, column=5, columnspan=1, rowspan=4, sticky=W, padx=25, pady=25)

        buttonImage = cv2.imread("greenArrow.png")
        buttonImageDisplay = self.makeDisplayImage(buttonImage, (70, 70))
        transformButton.configure(image=buttonImageDisplay)
        transformButton.image = buttonImageDisplay


        ## ****** Output Image ******
        self.outputImageLabel = Label(self.mainframe)
        self.outputImageLabel.grid(row=0, column=6, columnspan=4, rowspan=4, sticky=E, padx=50, pady=30)


        ## ****** Put Empty Image in Image Labels ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, self.IMAGE_SIZE)
        self.inputImageLabel.configure(image=empty_image_display)
        self.inputImageLabel.image = empty_image_display
        self.outputImageLabel.configure(image=empty_image_display)
        self.outputImageLabel.image = empty_image_display

        ## ****** Set Font ******
        myFont = Font(family="Arial", size=24)

        ## ****** Rotate Widget ******
        self.rotationSelection = IntVar()
        rotationCheckButton = Checkbutton(self.mainframe, text="  Rotation (°)", font=myFont, bg="gainsboro",
                                          onvalue=1, offvalue=0, variable=self.rotationSelection)
        rotationCheckButton.grid(row=4, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.rotationAngleEntry = Entry(self.mainframe)
        self.rotationAngleEntry.grid(row=4, column=2, columnspan=2, rowspan=1, sticky=W)
        self.rotationAngleEntry.insert(0, 'Angle in °')

        ## ****** Scaling Widget ******
        self.scalingSelection = IntVar()
        scalingCheckButton = Checkbutton(self.mainframe, text="  Scaling  ", font=myFont, bg="gainsboro",
                                          onvalue=1, offvalue=0, variable=self.scalingSelection)
        scalingCheckButton.grid(row=5, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        ## ****** Interpolation Pulldown ******
        interpolationLabel = Label(self.mainframe, text="      Interpolation:", bg="gainsboro", font=myFont)
        interpolationLabel.grid(row=6, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.interpVar = StringVar(self.mainframe)
        self.interpVar.set("Nearest Neighbor");

        interpolationPullDown = OptionMenu(self.mainframe, self.interpVar, "Nearest Neighbor", "Bilinear", "Bicubic")
        interpolationPullDown.grid(row=6, column=2, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)


    def getInputImage(self):
        filename = filedialog.askopenfilename()
        print("Setting input image to: ", filename)

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        self.displayImageOnLabel(self.inputImageLabel, self.inputImage, self.IMAGE_SIZE)
        self.setStatus("Loaded input image.")

    def runTransformation(self):
        if self.inputImage is None:
            self.setStatus("Please load and input image.")
            return
        if self.rotationSelection.get() == 1:
            rotationObject = Rotation(self.inputImage)
            rotated_image = rotationObject.temporaryRotatedImage(self.retrieveRotationAngle())
            rotated_image_display = self.makeDisplayImage(rotated_image, self.IMAGE_SIZE)
            self.outputImageLabel.configure(image=rotated_image_display)
            self.outputImageLabel.image = rotated_image_display
            self.setStatus("Rotated image " + str(self.retrieveRotationAngle()) + "°.")
        else:
            print("Rotation is not selected.")

    def retrieveRotationAngle(self):
        rotationAngleString = self.rotationAngleEntry.get()
        rotationAngle = 0
        try:
            rotationAngle = int(rotationAngleString)
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

