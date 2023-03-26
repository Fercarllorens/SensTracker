import folium as folium
from datetime import date
from wordcloud import WordCloud
import re

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
    wordCloud.to_file('funcionalities//WordCloud//' + usersample + str(date.today()) + '.png')