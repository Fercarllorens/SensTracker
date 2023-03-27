import tweepy
import csv #Import csv
# import libraries

from datetime import date, datetime
import os
from funcionalities.autenticate import get_auth




'''
Código base para la obtención de los tweets. 
'''

def almacenar_tweet( status, username):
            csvFile = open('funcionalities//Tweets//' + username + str(date.today()) + '.csv', 'a', encoding= 'utf-8', newline='')
            csvWriter = csv.writer(csvFile, delimiter=';')
            if status is not False and status.text is not None:
                try:
                    texto = status.extended_tweet["full_text"]
                except AttributeError:
                    texto = status.text
                texto = texto.replace('\n', ' ')
                print(texto)


                linea = [status.created_at,
                         status.id, texto, status.source, status.truncated,
                         status.in_reply_to_status_id, status.in_reply_to_user_id,
                         status.in_reply_to_screen_name, status.geo, status.coordinates,
                         status.place,status.contributors, status.lang, status.retweeted]
                linea = linea
                csvWriter.writerow(linea)
            print("Almacenamos Tweet")
            csvFile.close()
            print("fin")





def TweetExtractorMovies(movie):
    print("===== Captador de tweets =====")
    # Get an API item using tweepy
    auth = get_auth()  # Retrieve an auth object using the function 'get_auth' above
    api = tweepy.API(auth)  # Build an API object.

    if os.path.isfile(
                    'funcionalities//Tweets//' + movie + str(date.today()) + '.csv'):
               print('Preparado el fichero')
    else:
                print('El archivo no existe.')
                csvFile = open('funcionalities//Tweets//' + movie + str(date.today()) +'.csv', 'w', encoding= 'utf-8',  newline='')
                csvWriter = csv.writer(csvFile, delimiter=';')
                cabecera=['Fecha_creación','Id','Texto','Fuente','Truncado'
                    ,'Respuesta_al_tweet','Respuesta_al_usuario_id'
                    ,'Respuesta_al_usuario_nombre', 'geo', 'coordenadas', 'lugar',
                    'contribucion', 'lenguaje', 'retweeteado'

                ]
                csvWriter.writerow(cabecera)
                csvFile.close()
                print("Creación de la cabecera")
    
    end_date = date.today()

    for tweet in tweepy.Cursor(api.search_tweets, q=movie + movie, lang='en', until= end_date ).items():
                print(tweet.created_at, tweet.text)
                almacenar_tweet(tweet, movie)


    # End
    print("Terminado")


def TweetExtractor(username):
    print("===== Captador de tweets =====")
    # Get an API item using tweepy
    auth = get_auth()  # Retrieve an auth object using the function 'get_auth' above
    api = tweepy.API(auth)  # Build an API object.
    fileName = 'funcionalities//Tweets//' + username + str(date.today()) +'.csv'
    if os.path.isfile(
                    'funcionalities//Tweets//' + username + str(date.today()) + '.csv'):
               print('Preparado el fichero')
    else:
                print('El archivo no existe.')
                csvFile = open('funcionalities//Tweets//' + username + str(date.today()) +'.csv', 'w', encoding= 'utf-8',  newline='')
                csvWriter = csv.writer(csvFile, delimiter=';')
                cabecera=['Fecha_creación','Id','Texto','Fuente','Truncado'
                    ,'Respuesta_al_tweet','Respuesta_al_usuario_id'
                    ,'Respuesta_al_usuario_nombre', 'geo', 'coordenadas', 'lugar',
                    'contribucion', 'lenguaje', 'retweeteado'

                ]
                csvWriter.writerow(cabecera)
                csvFile.close()
                print("Creación de la cabecera")
    
    end_date = date.today()

    for tweet in tweepy.Cursor(api.search_tweets, q="from:" + username,until= end_date ).items():
                print(tweet.created_at, tweet.text)
                almacenar_tweet(tweet, username)


    # End
    print("Terminado")
    return fileName