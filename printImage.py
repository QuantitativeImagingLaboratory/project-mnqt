def printUnsignedImage(image):
    (N, M) = image.shape
    if N < 25:
        for i in range(N):
            for j in range(M):
                print('{: <8}'.format(image[i][j]), "  " , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")

def printImage(image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print("%.2f" % image[i][j], "  " , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")


def printComplexImage(image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print('{: <16}'.format('{:.2f}'.format(image[i][j])) , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")



def makeDisplayImage(filterMatrix):
    (N, M) = filterMatrix.shape
    display_image = np.zeros((N, M), np.uint8)
    for i in range(N):
        for j in range(M):
            display_image[i][j] = round(255.0 * filterMatrix[i][j])
    return display_image