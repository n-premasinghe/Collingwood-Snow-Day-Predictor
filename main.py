import pandas as pd
import numpy as np

snowDaysRaw = pd.read_excel('SCSTC_SchoolBus_user_tweets.xlsx')
weatherData = pd.read_csv('weather_data_24hr.csv')
snowDaysRaw.head()

snowDaysRaw.sort_index(axis=1)

def dateClean(text):
    #start = text.find('20')
    if text[text.find('20') + 4] != '-':
        trueText = text[text.find('20') + 2:]
        start = trueText.find('20')
    else:
        start = text.find('20')
        
    end = text.find('T')
    
    text = text[start:end]
    text = text.replace("-", "/")
        
    return text


keywordsWest = ['cancelled', 'West']
keywordsAll = ['cancelled', 'All', 'Simcoe County']
snowDayTweets = []
snowDayTweetDates = []
for t in snowDaysRaw['Text']:
    if all(x in t for x in keywordsWest):
        snowDayTweets.append(t)
        
        tweetDate = str(snowDaysRaw.loc[snowDaysRaw['Text'] == t, 'UTC'])
        print(dateClean(tweetDate))
        snowDayTweetDates.append(dateClean(tweetDate))
        
    elif all(x in t for x in keywordsAll):
        snowDayTweets.append(t)
        
        tweetDate = str(snowDaysRaw.loc[snowDaysRaw['Text'] == t, 'UTC'])
        print(dateClean(tweetDate))
        snowDayTweetDates.append(dateClean(tweetDate))
        
print(len(snowDayTweets))
print(len(snowDayTweetDates))

snowDaysClean = pd.DataFrame(list(zip(snowDayTweets, snowDayTweetDates)), columns=['Tweet', 'Snow Days Date'])

print(snowDaysClean.head())