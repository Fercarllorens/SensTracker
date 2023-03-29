from datetime import date
from funcionalities.Tweepy import TweetExtractorMovies
from funcionalities.tweetReader import readTweets
from funcionalities.mapGenerator import createMap
from funcionalities.generateWC import wordcloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import pandas as pd
import os

def analyseTweetsMovie(movie, df):
    moviesample = movie.split()[0]
    tweetsdict = df.to_dict('record')

    sentimentHeader = ['Pelicula', 'Dia','Puntuacion']
    dfSentimentDay = pd.DataFrame([], columns=sentimentHeader)

    sia = SentimentIntensityAnalyzer()
    
    groupScores = []
    day = None
    for tweet in tweetsdict:
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
            dfSentimentDay.loc[len(dfSentimentDay.index)] = [movie, day, scoremean]
            groupScores = []
            day = tweetday
            groupScores.append(sentimentDict['compound'])
    scoremean = 0
    for score in groupScores:
        scoremean += score
    scoremean = scoremean/len(groupScores)
    dfSentimentDay.loc[len(dfSentimentDay.index)] = [movie, day, scoremean]
    groupScores = []

    axSentimentDay = dfSentimentDay.plot.bar(x='Dia', y='Puntuacion', rot=20)
    figaxSentimentDay = axSentimentDay.get_figure()
    figaxSentimentDay.savefig('funcionalities//GraficoSAPorDia//' +moviesample +str(date.today()) + '.png') 



def analyseMovie(movie):
    movie = movie.lower()
    files = []
    moviesample = movie.split()[0]
    fileName = moviesample + str(date.today())
    check_file = os.path.isfile('funcionalities//Tweets//' + fileName + '.csv')
    if not check_file:
        TweetExtractorMovies(movie)
    tweets = readTweets(moviesample)
    header = tweets[0]
    tweets.pop(0)
    df = pd.DataFrame(tweets, columns=header)
    check_file = os.path.isfile('funcionalities//Maps//' + fileName + '.png')
    if not check_file:
        createMap(moviesample, df)
    check_file = os.path.isfile('funcionalities//WordCloud//' + fileName + '.png')
    if not check_file:
        wordcloud(movie, df)
    check_file = os.path.isfile('funcionalities//GraficoSAPorDia//' + fileName + '.png')
    if not check_file:
        analyseTweetsMovie(movie, df)
    
    #Añadimos los ficheros necesarios
    fileName = fileName + ".png"
    check_file = os.path.isfile('funcionalities//Maps//' + fileName)
    if check_file:
        files.append('funcionalities//Maps//' + fileName)
    check_file = os.path.isfile('funcionalities//WordCloud//' + fileName)
    if check_file:
        files.append('funcionalities//WordCloud//' + fileName)
    check_file = os.path.isfile('funcionalities//GraficoSAPorDia//' + fileName)
    if check_file:
        files.append('funcionalities//GraficoSAPorDia//' + fileName)

    movie = movie.replace(' ', '+')
    response = requests.get("https://api.themoviedb.org/3/search/movie?api_key=d6c4f64b76f81594ea569e6d4b887fa4&query=" + movie)
    idMovie = response.json().get('results')[0].get('id')
    response = requests.get("https://api.themoviedb.org/3/movie/"+ str(idMovie) +"/watch/providers?api_key=d6c4f64b76f81594ea569e6d4b887fa4")
    whereToWatchLink = response.json().get('results').get('ES')
    if whereToWatchLink is None:
        whereToWatchLink = response.json().get('results').get('US')
    whereToWatchLink = whereToWatchLink.get('link')
    #return whereToWatchLink

    files.append(whereToWatchLink)
    return files
