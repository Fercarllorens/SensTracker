import csv
import folium as folium
from datetime import date


def extractFromFakeJson(value, text, delimiter = ",", offset_1 = 0, offset_2 = 0):
    start = text.find(value) + offset_1
    end = text.find(delimiter, start) + offset_2
    return text[start:end]

def mapCoord(text):
    separator = text.find(",")
    first_coord = float(text[1:separator])
    second_coord = float(text[separator+1:-2])
    return (first_coord, second_coord)

def readTweets(username):
    file = 'funcionalities//Tweets//' + username + str(date.today()) + ".csv"
    with open(file, "r", encoding='utf8') as f:
        reader = csv.reader(f, delimiter=";")
        tweets = []
        counter = 0
        for i, line in enumerate(reader):
            if line[10] != "":
                if line[10] != 'lugar':
                    inicio = line[10].find('name') + 6
                    final = line[10].find(",", inicio) - 1
                    name = str(line[10])[inicio:final]

                    inicio = line[10].find('coordinates') + 14
                    final = line[10].find('],', inicio) +1
                    coordenadas = str(line[10])[inicio:final]
                    line[10] = [name,mapCoord(coordenadas)]
            tweets.append(line)
            counter = counter + 1
    return tweets