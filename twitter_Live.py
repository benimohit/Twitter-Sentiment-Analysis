#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:46:23 2018

@author: mohitbeniwal
"""

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import pandas as pd
#nltk.download('stopwords')
pd.options.mode.chained_assignment = None  # default='warn'

#Keys and token to connect to twitter 
consumer_key = 'YbqH7k9CUlEf8IVh04Amxvocv'
consumer_secret = 'fXw3d2tyMgE1uVoGX3nflhBQwUGmHY9E9ElN1xpA4ZQlSX3Iub'
access_token = '1063497654221635584-OaCR2C8eUZuPwLmh86kQoTg3fZEIHo'
access_token_secret = 'er53piuTdTx8OONYoFGIcCz1GKyWuaTeHNwVWMpmYGEbS'
#Authentiaction
try: 
    # creating OAuthHandler object 
    auth = OAuthHandler(consumer_key, consumer_secret) 
    # seting access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    # createing object to fetch tweets 
    api = tweepy.API(auth) 
except: 
    print("Error: Authentication Failed") 
    
def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'
  
def getTweets(query, count = 10): 

    #list to store tweets 
    tweets_df = pd.DataFrame(columns=['time','sentiment','retweet_count','actual_text','clean_text'])
  
    try: 
        #call twitter api to fetch tweets 
        fetch_tweets = api.search(q = query, count = count,lang="en") 
        i=0
        #parsing tweets one by one 
        for tweet in fetch_tweets: 
            #dictionary to store required paramaters
            #tweet_dic = {} 
            #print(tweet)
            #text of tweet 
            actual_text=tweet.text
            clean_text = clean_tweet(tweet.text) 
            #sentiment of tweet 
            sentiment = get_tweet_sentiment(tweet.text)
            retweet_count=tweet.retweet_count
            time=tweet.created_at
            if(clean_text in tweets_df['clean_text'].tolist()):
                continue
            else:
                tweets_df.loc[i]=[time,sentiment,retweet_count,actual_text,clean_text]
            i+=1
            
            
            

            #tweets.append(tweet_dic)
        # return tweets 
        tweets_df.index = range(len(tweets_df.index))
        return tweets_df 
  
    except tweepy.TweepError as e: 
        # print error (if any) 
        print("Error : " + str(e)) 

def main(q,n):
    
    # calling function to get tweets 
    tweets = getTweets(query = q, count = n,)
    try:
        positiveTweets=tweets[(tweets.sentiment=='positive')]
    except:
        print("no positive")
    try:
        negativeTweets=tweets[(tweets.sentiment=='negative')]
    except:
        print("no negative")
    try:
        neturalTweets=tweets[(tweets.sentiment=='neutral')]
    except:
        print("no neutral")
  
    return tweets,positiveTweets,negativeTweets,neturalTweets
#tweets=pd.concat([tweets,tweets1]).drop_duplicates().reset_index(drop=True)
#main('trump',1000)


