
import tweepy

'''
Función utilizada para utilizar la Api de Twitter
'''
def get_auth():
    consumer_key = 'qDqiLQoTgQusOGa9x0YJJtXr8'
    consumer_secret = 'HBb2eOxW1XbO1ERIul0UR0zN3MDNz4P1IF6UKqA1qjdXcSBVL4'
    access_token = '2792071239-gwhCrTsicTXttl5Z9gk1YMYilZ7kybn1fJDaTiS'
    access_token_secret = 'hlOYQZ47LU6eeyx9T3nAaTrixz4hJTFtEMOkwFF0yxfAG'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth