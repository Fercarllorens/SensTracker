import folium as folium
from datetime import date
from wordcloud import WordCloud

def wordcloud(username, df):
    textArray = df['Texto'].to_list()
    noLinksTextArray = []
    for txt in textArray:
        if 'http' in txt:
            indexhttp = txt.find('http')
            noLinksTextArray.append(txt[:indexhttp])
        else:
            noLinksTextArray.append(txt)
    text = " ".join(txt for txt in noLinksTextArray)
    wordCloud = WordCloud(collocations= False, background_color='white').generate(text)
    wordCloud.to_file('funcionalities//WordCloud//' + username + str(date.today()) + '.png')