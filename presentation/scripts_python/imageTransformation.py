#from imagehandler import imageHandler

#imgHandler = imageHandler()


import os,sys
from PIL import Image
import cv2

#class imageHandler():

def check_image_with_pil(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True

def dirNames(path):
    dirNameList = []
    for f in os.listdir(path):
        child = os.path.join(path, f)
        if os.path.isdir(child):
            dirNameList.append(child)
    return dirNameList

def imgDir(func,path):
    imageDir = []
    for dirName in dirNames(path):
        imageDir.append(dirName + "/images")
    return imageDir

def imageExtentionCleaning(path):
    if os.path.exists(path):
        for filename in os.listdir(path):
            infilename = os.path.join(path,filename)
            statinfo = os.stat(infilename)
            if statinfo.st_size > 10000 :
                if check_image_with_pil(infilename) :
                    oldbase = os.path.splitext(filename)
                    if (oldbase[1] != '.jpg' and oldbase[1] != '.png'):
                        if oldbase[1][:4] != '.php' and oldbase[1][:4] != '.net' :
                            newname = infilename.replace(oldbase[1], oldbase[1][:4])
                        else: newname = infilename.replace(oldbase[1], '.jpg')
                        output = os.rename(infilename, newname)
                    if (oldbase[1] == '.png'):
                        os.remove(infilename)
                    print infilename
            else: os.remove(infilename)

        #_____________________________Reading image_____________________________

def imageGrayScale(path):
    return cv2.imread(path,0)

            #_____________________________Cropping image_____________________________

def imageCropping(img,height_target_crop,width_target_crop):

    height, width = img.shape[:2]
    height_to_crop = height - height_target_crop
    width_to_crop = width - height_target_crop

    return img[(height_to_crop/2):(height - (height_to_crop/2)), (width_to_crop/2):width - (width_to_crop/2)]

                #_____________________________Resizing image_____________________________

def imageResizing(img,dim_target_resize):

    height, width = img.shape[:2]

    dim_to_resize = round(float(dim_target_resize) / float(height),4)

    return cv2.resize(img,None,fx=dim_to_resize, fy=dim_to_resize, interpolation = cv2.INTER_CUBIC)

                #_____________________________Saving image_____________________________

def imageSaving(img,imgpath,imgName,pathOriginal,pathDerived):

    pathDerivedCityImages = pathDerived + imgpath.replace(pathOriginal, "")
    pathDerived = pathDerivedCityImages.replace(imgName,"")

    if not os.path.exists(pathDerived):
        os.makedirs(pathDerived)

    cv2.imwrite(pathDerivedCityImages,img)

                #_____________________________All in one function_____________________________


def imgHandlingForNeuralNetwork(path,height_target_crop,width_target_crop,dim_target_resize,pathOriginal,pathDerived):
    dirRunned = []
    if os.path.exists(path):
        for filename in os.listdir(path):
            infilename = os.path.join(path,filename)
            if check_image_with_pil(infilename) :
                if str(type(cv2.imread(infilename,0))) != "<type 'NoneType'>":
                    imgResized = imageResizing(imageCropping(imageGrayScale(infilename),height_target_crop,width_target_crop),dim_target_resize)
                    if imgResized.shape[:2] == (56, 56):
                        imageSaving(imgResized,infilename,filename,pathOriginal,pathDerived)
        #else: dirWithNoImgs.append(temp_path[3])
    dirRunned.append(path)
    print dirRunned


#_____________________ Cleaning _______________________

path_city = "/Users/alex/Documents/pythonProjects/opencvTraining/rennes"

pathesList = imgDir(dirNames,path_city)

[imageExtentionCleaning(pathToImages) for pathToImages in pathesList]

#_____________________ resizing _______________________

height_target_crop = 28*14
width_target_crop = 28*14
dim_target_resize = 28*2

pathOriginal = '/Users/alex/Documents/pythonProjects/opencvTraining'

pathDerived = "/Users/alex/Documents/pythonProjects/opencvTraining/derivedImages"

[imgHandlingForNeuralNetwork(path,height_target_crop,width_target_crop,dim_target_resize,pathOriginal,pathDerived) for path in pathesList]
