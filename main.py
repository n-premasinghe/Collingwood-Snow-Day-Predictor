# Importing libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
# Reading data stored in spreadsheets.
snowDaysRaw = pd.read_excel('SCSTC_SchoolBus_user_tweets.xlsx')
weatherData = pd.read_csv('weather_data_24hr.csv')
snowDaysRaw.head()

# Sorting to make more readable.
snowDaysRaw.sort_index(axis=1)

# function to turn raw UTC data into weather data compatible date format.
def dateClean(text):
    # Determining whether or not the index value contains "20" by seeing if the position of the "-" is in the right place.
    if text[text.find('20') + 4] != '-':
        # In the case that the index value of the date contains "20" add 2 to the index position to pass it.
        trueText = text[text.find('20') + 2:]
        # Perform normal procedure on edited text. 
        # (Note: This implementation is a quick fix I put in place knowing that there were no where near 
        # #2000 datapoints within the set. If there were, a simple loop could solve the problem by consistently checking to see if the "-" is in the right place.)
        start = trueText.find('20')
    else:
        start = text.find('20')
        
    end = text.find('T')
    
    text = text[start:end]
    # Formatting the date so .loc commands can be run on the weatherData dataframe.
    text = text.replace("-", "/")

    # Returns cleaned date.    
    return text

# 
#   Extracting tweets that show there was a snow day on that date.
#

# Keywords to look for. (Two lists need to be used to account for times all zones have a snow day, and days when it is just the west zone.)
keywordsWest = ['cancelled', 'West']
keywordsAll = ['cancelled', 'All', 'Simcoe County']

# List containing the text of the tweets that have the keywords in them.
snowDayTweets = []
# List containing the dates that the tweets with the keywords were made. (Tuples were intentionally not used to take advantage of the simplicity of the zip() function
# when translating the values to dataframes later.)
snowDayTweetDates = []

# Iterating through every tweet to look for snow days
for t in snowDaysRaw['Text']:
    if all(x in t for x in keywordsWest):
        snowDayTweets.append(t)
        
        tweetDate = str(snowDaysRaw.loc[snowDaysRaw['Text'] == t, 'UTC'])
        #print(dateClean(tweetDate))
        snowDayTweetDates.append(dateClean(tweetDate))
        
    elif all(x in t for x in keywordsAll):
        snowDayTweets.append(t)
        
        tweetDate = str(snowDaysRaw.loc[snowDaysRaw['Text'] == t, 'UTC'])
        #print(dateClean(tweetDate))
        snowDayTweetDates.append(dateClean(tweetDate))


#print(len(snowDayTweets))
#print(len(snowDayTweetDates))

#snowDaysClean = pd.DataFrame(list(zip(snowDayTweets, snowDayTweetDates)), columns=['Tweet', 'Snow Days Date'])

# Add column to specify whether or not a day was a snow day.
weatherData['Snow Day'] = "False"

for n in weatherData['date']:
    for d in snowDayTweetDates:
        if d == n:
            weatherData.loc[weatherData['date'] == n, 'Snow Day'] = "True"
        else:
            pass

#print(weatherData.loc[[6]])

snowDay = pd.get_dummies(weatherData['Snow Day'], drop_first=True)
print(snowDay.head())

#trainingData, testingData = train_test_split(weatherData, test_size=0.3, random_state=25)
