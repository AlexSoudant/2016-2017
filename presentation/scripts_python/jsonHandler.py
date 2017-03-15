import os
import json
import numpy as np
import csv

# city to build database upon
city = "angers"

pathToCity = "/Users/alex/Documents/pythonProjects/opencvTraining/derivedImages/" + city + "/"

# path name
listAdvertRepo = [name for name in os.listdir(pathToCity)]


TableAdverts = np.zeros((len(listAdvertRepo),6))


for i,advert in enumerate(listAdvertRepo):

    titleAdvert = ""
    picturesAdvert = 0
    surfaceAdvert = 0
    RoomsAdvert = 1
    LandAdvert = 0
    priceAdvert = 0

    pathToJsonFile =  pathToCity + listAdvertRepo[i] + "/"

    if os.path.isdir(pathToJsonFile):
        if len(os.listdir(pathToJsonFile)) == 3:
            jsonFilePath = pathToJsonFile + os.listdir(pathToJsonFile)[2]
        else : jsonFilePath = pathToJsonFile + os.listdir(pathToJsonFile)[1]


        with open(jsonFilePath) as data_file:
            data = json.load(data_file)

            # title advert
        titleAdvert = data['titleS']

            # pictures number
        picturesAdvert = len(data['pictures'])



            # House surface
        for j,item in enumerate(data['features']):
            if len(data['features'][j].split(' ')) > 1:
                if data['features'][j].split(' ')[1].encode('utf-8') == 'm\xc2\xb2':
                    surfaceAdvert = float(data['features'][j].split(' ')[0].encode('utf-8').replace(',','.').replace('\xef\xbf\xbd',''))

            # nb rooms
        for k,item in enumerate(data['features']):
            if len(data['features'][k].split(' ')) > 1:
                if data['features'][k].split(' ')[1].encode('utf-8') == 'chambres':
                    RoomsAdvert = int(data['features'][k].split(' ')[0])

            # Land size
        for f,item in enumerate(data['features']):
            if len(data['features'][f].split(' ')) > 1:
                if data['features'][f].split(' ')[0].encode('utf-8') == 'Terrain':
                    LandAdvert = float(data['features'][f].split(' ')[1].encode('utf-8').replace(',','.').replace('\xef\xbf\xbd',''))

            # Price
        if len(data['price'].split(' ')) == 1:
            priceAdvert = int(data['price'].replace('&#xFFFD;','').replace('&#xA0;&#x20AC;',''))
        else:
            if str(data['price'].split(' ')[-1].replace('&#xFFFD;','').replace('&#xA0;&#x20AC;','')) == 'NC':
                priceAdvert = 0
            else: priceAdvert = int(data['price'].split(' ')[-1].replace('&#xFFFD;','').replace('&#xA0;&#x20AC;',''))

        listAdvertRow = []

        listAdvertRow.append(listAdvertRepo[i].replace('-',''))
        listAdvertRow.append(picturesAdvert)
        listAdvertRow.append(surfaceAdvert)
        listAdvertRow.append(RoomsAdvert)
        listAdvertRow.append(LandAdvert)
        listAdvertRow.append(priceAdvert)


        TableAdverts[i,:] = listAdvertRow


    np.savetxt("advertsInfoAngers.csv", TableAdverts, delimiter=",")
