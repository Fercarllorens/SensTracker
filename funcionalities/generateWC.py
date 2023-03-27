import pandas as pd
import folium as folium
from datetime import date
from wordcloud import WordCloud
from funcionalities.Tweepy import TweetExtractor
from funcionalities.tweetReader import readTweets
import re

def wordcloudsimple(username):
    fileTweets = TweetExtractor(username)
    tweets = readTweets(username)
    header = tweets[0]
    tweets.pop(0)
    df = pd.DataFrame(tweets, columns=header)
    return wordcloud(username, df)


def wordcloud(username, df):
    usersample = username.split()[0]
    textArray = df['Texto'].to_list()
    noLinksTextArray = []
    for txt in textArray:
        if 'http' in txt:
            indexhttp = txt.find('http')
            noLinksTextArray.append(txt[:indexhttp])
        else:
            noLinksTextArray.append(txt)
    text = " ".join(txt for txt in noLinksTextArray)
    if len(username.split()) > 1:
        for word in username.split():
            text = text.replace(re.sub('\W+','', word),'')
            text = text.replace(re.sub('\W+','', word).upper(),'')  
            text = text.replace(re.sub('\W+','', word).lower(),'')
    text = text.replace('RT', '')      
    wordCloud = WordCloud(collocations= False, background_color='white').generate(text)
    fileName = username.split()[0] + str(date.today()) + '.png'
    wordCloud.to_file('funcionalities//WordCloud//' + fileName)
    return 'funcionalities//WordCloud//' + fileName
