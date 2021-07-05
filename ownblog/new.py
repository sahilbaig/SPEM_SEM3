import tweepy
# import pandas as pd 

consumer_key = "lvScNOq7azP6b2uVL6KmQ3kK2"
consumer_secret = "EJQMHS61LON7gY8nvYltu6KlQXod17UykDhY0ldwi2aEzdKihF"
access_token = "1046412032399028227-7bYR2n01RJPXTH1M1Znv6Ms2tl4Sae"
access_token_secret = "8WNr4yJ7jXTB1qpSfCuRZttrQZfSEdKnVZ1fN0LRrGXgd"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

search = input()

cursor = tweepy.Cursor(api.search, q=search,tweet_mode="extended").items(5)

for i in cursor:
    print(i.full_text)