#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:46:23 2018

@author: mohitbeniwal
"""

import re 
import os
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from nltk.corpus import stopwords
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB

#nltk.download('stopwords')
pd.options.mode.chained_assignment = None  # default='warn'
# function to collect hashtags
def get_hashtag(tweet):
    hashtags = []
    for i in tweet:
        h_t = re.findall(r"#(\w+)", i)
        hashtags.append(h_t)
    return hashtags

def dummydata(tweets,dummy):
    d_list=[]
    for i in range(0,len(tweets)):
        list_b=[]
        l=tweets[i].split()
        for w in dummy:
            count=0
            for w1 in l:
                if(w1.startswith(w) or w1.startswith(str('#')+w)):
                   count+=1
            list_b.append(count)    
        d_list.append(list_b)
    
    dummpy_df=pd.DataFrame(d_list,columns=dummy)
    return dummpy_df
    
def model():
    file_dir = os.path.join('/','Users', 'mohitbeniwal','Downloads','data_science_with_Python_677','project','Twitter Sentiment Analysis') 
    file_name = os.path.join(file_dir, 'train_tweets.csv')
    df = pd.read_csv(file_name)
    pd.options.mode.chained_assignment = None  # default='warn'
    word_list=[]
    
    stop_words = set(stopwords.words('english'))
    df['tweet'] = df['tweet'].str.replace("(@[A-Za-z0-9]+)|([^a-zA-Z0-9# \t])", " ")
    
    df['tweet']= df['tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    
    for i in range(0,len(df['tweet'].values)):
        words=df['tweet'].values[i].split()
        for w in words:
            if(w not in stop_words):
                word_list.append(w)
    
    
    
    stemmer = PorterStemmer()
    df_words=pd.DataFrame(word_list,columns=["words"])
    df_words = df_words.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
    
    all_words = nltk.FreqDist(w.lower() for w in df_words['words'])
    word_features = list(all_words)[:500]
    
    
    
    # getting hashtag for non racist/sexist
    HT_neutral = get_hashtag(df['tweet'][df['label']==0])
    
    # getting hashtags from racist/sexist 
    HT_negative = get_hashtag(df['tweet'][df['label']==1])
    
    # unnesting list
    HT_neutral = sum(HT_neutral,[])
    freq = nltk.FreqDist(HT_neutral)
    tag = pd.DataFrame({'Hashtag': list(freq.keys()),'Count': list(freq.values())})
    # selecting most frequent hashtags     
    tag = tag.nlargest(columns="Count", n = 25) 
    plt.figure(figsize=(25,5))
    ax = sns.barplot(data=tag, x= "Hashtag", y = "Count")
    ax.set(ylabel = 'Count')
    plt.show()
    
    HT_negative = sum(HT_negative,[])
    freq = nltk.FreqDist(HT_negative)
    tags = pd.DataFrame({'Hashtag': list(freq.keys()), 'Count': list(freq.values())})
    # selecting most frequent hashtags
    tags = tags.nlargest(columns="Count", n = 500)   
    plt.figure(figsize=(500,5))
    ax = sns.barplot(data=tags, x= "Hashtag", y = "Count")
    ax.set(ylabel = 'Count')
    plt.show()
    dummy=tag['Hashtag'].tolist()
    for w in tags['Hashtag'].values:
        dummy.append(w)
    for w in word_features:
        if(w.startswith('#')):
                        continue
        else:
            dummy.append(w)
    df1=dummydata(df['tweet'],dummy)
    df=df.join(df1) 
    train, test = train_test_split(df, test_size=0.2)
    columns=range(3,len(dummy)+3)
    y_train=train['label']
    x_train= train.iloc[:,columns]
    
    y_test=test['label']
    x_test=test.iloc[:,columns]
    
    LogReg = LogisticRegression()
    LogReg.fit(x_train, y_train)
    y_pred = LogReg.predict(x_test)
    print('Accuracy for logistic regression: %.2f' % accuracy_score(y_test, y_pred))
    print('confusion matrix for logidtic regression: \n'+str(confusion_matrix(y_test, y_pred))) 
    
    naive_multi = MultinomialNB()
    naive_multi.fit(x_train, y_train)
    y_pred = naive_multi.predict(x_test)
    print('Accuracy for Navive Bayes Multinommial: %.2f' % accuracy_score(y_test, y_pred))
    print('confusion matrix for Navive Beyes Multinommial: \n'+str(confusion_matrix(y_test, y_pred)))
    

model()
