import pandas as pd
import numpy as np
import folium as folium
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from funcionalities.Tweepy import TweetExtractor
import os.path
import numpy as np 
import matplotlib.pyplot as plt 
from funcionalities.tweetReader import readTweets


def versusUsers(username1, username2, df1, df2):
    tweetsDictUser1 = df1.to_dict('record')
    tweetsDictUser2 = df2.to_dict('record')

    sentimentHeader = ['User', 'Dia', 'Puntuacion']
    dfUser1 = pd.DataFrame([], columns=sentimentHeader)
    dfUser2 = pd.DataFrame([], columns=sentimentHeader)

    sia = SentimentIntensityAnalyzer()

    day = None
    groupScores = []
    for tweet in tweetsDictUser1:
        sentimentDict = sia.polarity_scores(tweet['Texto'])
        tweetday = tweet['Fecha_creación'].split()[0]
        if day is None:
            day = tweetday
            groupScores.append(sentimentDict['compound'])
        elif day == tweetday:
            groupScores.append(sentimentDict['compound'])
        else:
            scoremean = 0
            for score in groupScores:
                scoremean += score
            scoremean = scoremean/len(groupScores)
            dfUser1.loc[len(dfUser1.index)] = [username1, day, scoremean]
            groupScores = []
            day = tweetday
            groupScores.append(sentimentDict['compound'])
    scoremean = 0
    for score in groupScores:
        scoremean += score
    scoremean = scoremean/len(groupScores)
    dfUser1.loc[len(dfUser1.index)] = [username1, day, scoremean]
    
    groupScores = []
    day = None
    for tweet in tweetsDictUser2:
        sentimentDict = sia.polarity_scores(tweet['Texto'])
        tweetday = tweet['Fecha_creación'].split()[0]
        if day is None:
            day = tweetday
            groupScores.append(sentimentDict['compound'])
        elif day == tweetday:
            groupScores.append(sentimentDict['compound'])
        else:
            scoremean = 0
            for score in groupScores:
                scoremean += score
            scoremean = scoremean/len(groupScores)
            dfUser2.loc[len(dfUser2.index)] = [username2, day, scoremean]
            groupScores = []
            day = tweetday
            groupScores.append(sentimentDict['compound'])
    scoremean = 0
    for score in groupScores:
        scoremean += score
    scoremean = scoremean/len(groupScores)
    dfUser2.loc[len(dfUser2.index)] = [username2, day, scoremean]
    groupScores = []

    

    daysUser1 = dfUser1['Dia']
    daysUser2 = dfUser2['Dia']

    daysleft1 = list(set(daysUser2) - set(daysUser1))
    daysleft2 = list(set(daysUser1) - set(daysUser2))

    for dayleft in daysleft1:
        dfUser1.loc[len(dfUser1.index)] = [username1, dayleft, 0]
    for dayleft in daysleft2:
        dfUser2.loc[len(dfUser2.index)] = [username2, dayleft, 0]

    dfUser1['Dia'] = pd.to_datetime(dfUser1['Dia'])
    dfUser1.sort_values(by='Dia', inplace=True)
    dfUser1['Dia'] = dfUser1['Dia'].dt.strftime('%Y-%m-%d')
    dfUser2['Dia'] = pd.to_datetime(dfUser2['Dia'])
    dfUser2.sort_values(by='Dia', inplace=True)
    dfUser2['Dia'] = dfUser2['Dia'].dt.strftime('%Y-%m-%d')

    days = dfUser1['Dia']

    scoreUser1 = dfUser1['Puntuacion']
    scoreUser2 = dfUser2['Puntuacion']
    r = np.arange(len(days))
    width1 = 0.5
    plt.subplot(1,1,1)
    plt.bar(r, scoreUser1, width=width1, label=username1)
    plt.bar(r + width1, scoreUser2, width=width1, label=username2)
    plt.title(username1 + ' vs ' + username2)
    plt.xticks(r, days, rotation = 20)
    plt.legend()
    fileName = 'funcionalities//GraficoSAVersus//' + username1 + '-' + username2 + str(date.today()) + '.png'
    plt.savefig(fileName)
    return fileName


def vsprofiles(username1, username2):

    check_file = os.path.isfile('funcionalities//Tweets//' + username1 + str(date.today()) + '.csv')
    if not check_file:
        TweetExtractor(username1)
    tweetsUser1 = readTweets(username1)

    check_file = os.path.isfile('funcionalities//Tweets//' + username2 + str(date.today()) + '.csv')
    if not check_file:
        TweetExtractor(username2)
    tweetsUser2 = readTweets(username2)

    header = tweetsUser1[0]
    tweetsUser1.pop(0)
    tweetsUser2.pop(0)

    dfUser1 = pd.DataFrame(tweetsUser1, columns=header)
    dfUser2 = pd.DataFrame(tweetsUser2, columns=header)
    
    check_file = os.path.isfile('funcionalities//GraficoSAVersus//' + username1 + '-' + username2 + str(date.today()) + '.png') 
    fileName = ""
    if not check_file:
        fileName = versusUsers(username1, username2, dfUser1, dfUser2)

    return fileName