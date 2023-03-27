import pandas as pd
import folium as folium
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from funcionalities.Tweepy import TweetExtractor
import os.path
from funcionalities.tweetReader import readTweets
from funcionalities.mapGenerator import createMap
from funcionalities.generateWC import wordcloud
import re
import requests



def analyseTweetsPerDay(username, df):
    tweetsdict = df.to_dict('record')

    sentimentHeader = ['Id', 'Dia', 'UserId', 'Texto', 'Puntuacion', 'Animo']
    dfSentimentTweet = pd.DataFrame([], columns=sentimentHeader)

    sia = SentimentIntensityAnalyzer()
    
    day = None
    count = 0
    for tweet in tweetsdict:
        tweetday = tweet['Fecha_creación'].split()[0]
        if day is None:
            day = tweetday
        if day != tweetday:
            day = tweetday
        sentimentDict = sia.polarity_scores(tweet['Texto'])
        sentiment = ''
        if sentimentDict['compound'] >= 0.05 :
            sentiment = "Positive"
        elif sentimentDict['compound'] <= - 0.05 :
            sentiment = "Negative"
        else :
            sentiment = "Neutral"
        dfSentimentTweet.loc[len(dfSentimentTweet.index)] = [count, tweetday, username, tweet['Texto'], sentimentDict['compound'], sentiment]
        count = count+1
    
    dfSentimentTweet.to_csv('funcionalities//SA//' + username + str(date.today()) +'.csv', sep=';', encoding='utf-8', index=False)
    
    sentimentsTweetDict = dfSentimentTweet.to_dict('record')
    sentimentDayHeader = ['Dia','Puntuacion']
    dfSentimentDay = pd.DataFrame([], columns=sentimentDayHeader)

    day = None
    groupScores = []
    for tweet in sentimentsTweetDict:
        tweetday = tweet['Dia']
        if day is None:
            day = tweetday
            groupScores.append(tweet['Puntuacion'])
        elif day == tweetday:
            groupScores.append(tweet['Puntuacion'])
        else:
            scoremean = 0
            for score in groupScores:
                scoremean += score
            scoremean = scoremean/len(groupScores)
            dfSentimentDay.loc[len(dfSentimentDay.index)] = [day, scoremean]
            groupScores = []
            day = tweetday
            groupScores.append(tweet['Puntuacion'])
    scoremean = 0
    for score in groupScores:
        scoremean += score
    scoremean = scoremean/len(groupScores)
    dfSentimentDay.loc[len(dfSentimentDay.index)] = [day, scoremean]
    groupScores = []

    axSentimentTweet = dfSentimentTweet.plot.bar(x='Id', y='Puntuacion', rot=0)
    figaxSentimentTweet = axSentimentTweet.get_figure()
    figaxSentimentTweet.savefig('funcionalities//GraficoSAPorTweet//' +username + str(date.today()) + '.png')

    axSentimentDay = dfSentimentDay.plot.bar(x='Dia', y='Puntuacion', rot=20)
    figaxSentimentDay = axSentimentDay.get_figure()
    figaxSentimentDay.savefig('funcionalities//GraficoSAPorDia//' +username +str(date.today()) + '.png')

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    list = [m.group(0) for m in matches]
    final = ""
    for word in list:
        if final != "":
            final = final + " " + word
        else:
            final = word
    return final

def analyseprofile(username):
    username = username.lower()
    
    check_file = os.path.isfile('funcionalities//Tweets//' + username + str(date.today()) + '.csv')
    if not check_file:
        TweetExtractor(username)
    tweets = readTweets(username)
    header = tweets[0]
    tweets.pop(0)
    df = pd.DataFrame(tweets, columns=header)
    check_file = os.path.isfile('funcionalities//Maps//' + username + str(date.today()) + '.png')
    if not check_file:
        createMap(username, df)
    check_file = os.path.isfile('funcionalities//GraficoSAPorTweet//' + username + str(date.today()) + '.png') and os.path.isfile('GraficoSAPorDia//' + username + str(date.today()) + '.png')
    if not check_file:
        analyseTweetsPerDay(username, df)
    check_file = os.path.isfile('funcionalities//WordCloud//' + username + str(date.today()) + '.png')
    if not check_file:
        wordcloud(username, df)
    
    name = camel_case_split(username)
    response = requests.get("https://newsapi.org/v2/top-headlines?apiKey=037229ddf6df4db58f835b96158bf93e&q=" + name)
    articles = response.json().get('articles')
    listNews = []
    count = 0
    for article in articles:
        title = article['title']
        url = article['url']
        listNews.append([title,url])
        count = count+1
        if count == 4:
            break
    fileName = username + str(date.today()) + '.png'
    files = []
    files.append("funcionalities//Maps//" + fileName)
    files.append("funcionalities//GraficoSAPorTweet//" + fileName)
    files.append("funcionalities//WordCloud//" + fileName)
    return files
    
analyseprofile("joebiden")



    
    





        
    


    
