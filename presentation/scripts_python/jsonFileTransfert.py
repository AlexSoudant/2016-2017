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

import os

from shutil import copyfile


path_city = "/Users/alex/Documents/pythonProjects/opencvTraining/derivedimages/angers"

pathesList = imgDir(dirNames,path_city)

path_json = "/Users/alex/Documents/pythonProjects/opencvTraining/angers"

for path in pathesList:
    source = "/Users/alex/Documents/pythonProjects/opencvTraining/" + path.replace('/images','').replace('/Users/alex/Documents/pythonProjects/opencvTraining/derivedimages/','') + '/result.json'
    destination = path.replace('/images','') + '/result.json'
    copyfile(source, destination)
