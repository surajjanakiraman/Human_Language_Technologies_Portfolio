# Weather Forcast Bot

from lib2to3.pgen2.token import tok_name
from urllib import response
from webbrowser import get
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
import numpy
from collections import defaultdict
import requests
from WeatherInfo import WeatherInfo
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from datetime import date
from datetime import datetime

def processInput(text):    
    # tokenize text
    tokens = nltk.word_tokenize(text)
    # lower case every word in tokens
    tokens = [word.lower() for word in tokens]
    # remove stop words
    filteredTokens = [word for word in tokens if word not in stopwords.words() or word == 'next']
    # tag tokens based on their part of speech
    tagged = nltk.pos_tag(filteredTokens)
        
    city = ''
    questionType = ''
    partOfDay = ''
    weekDay = defaultdict(str) # day (Ex: monday) and a number
    monthDay = defaultdict(str)
    
    # find city 
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                # print(chunk.label(), ' '.join(c[0] for c in chunk))
                city = ' '.join(c[0] for c in chunk)
    
    
    bigrams = list(ngrams(filteredTokens,2))
    months = ['december', 'april', 'may', 'july', 'august', 'september', 'october', 'november', 'december']
    weekDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'satarday', 'sunday']
    
    weekDaysNum = {
        'monday': 0,
        'tuesday': 1, 
        'wednesday': 2, 
        'thursday': 3, 
        'friday': 4,
        'satarday': 5, 
        'sunday': 6, 
    }
    
    # look for keys words in bigrams to identidy time and what kind of question the user is asking 
    for bigram in bigrams:
        word1 = bigram[0]
        word2 = bigram[1]
        # identify time 
        if word1 == 'weather':
            questionType = 'weatherQuestion'
        elif word1 == 'sunrise':
            questionType = 'sunriseQuestion'
        elif word1 == 'sunset':
            questionType = 'sunsetQuestion'
        elif word1 == 'humidity':
            questionType = 'humidityQuestion'
        elif word1 == 'pressure':
            questionType = 'pressureQuestion'
        elif word1 == 'minimum' and word2 == 'temperature':
            questionType = 'minTemperatureQuestion'
        elif word1 == 'maximum' and word2 == 'temperature':
            questionType = 'maxTemperatureQuestion'
        elif word1 == 'temperature':
            if len(questionType) == 0:
                questionType = 'temperatureQuestion'
                
        # identify part of the day      
        if word1 == 'morning' or word1 == 'day' or word1 == 'evening':
            partOfDay = word1
        
        # identify date
        if word1 == 'next' and word2 in weekDays:
            weekDay['day'] = weekDaysNum[word2]
            weekDay['context'] = word1     
        elif word1 in weekDay:
            weekDay['day'] = weekDaysNum[word1]
            weekDay['context'] = 'now' 
        elif word1 in months:
            monthDay['month'] = word1
            num = ''
            for ch in word2:
                if ch.isnumeric():
                    num += ch
            if len(num) > 0:
                weekDay['num'] = int(num)
            monthDay['day'] = num
          
    return [city, questionType, partOfDay, weekDay, monthDay] 

# identifies question type and gets the corresponding informatin from API data
def ChatBotOutput(weatherData, questionType, partOfDay, weekDay, monthDay):    
    todayDate = date.today()
    dt = datetime.now()
    todayWeekDay = dt.weekday()
    dayInd = 0
    
    # find the index of the day 
    if len(weekDay) > 0:
        if weekDay['context'] == 'next':
            dayInd += 6 - todayWeekDay
            dayInd += weekDay['day'] + 1
        elif weekDay['context'] == 'now':
            dayInd += 6 - todayWeekDay
    # give answer to the user depending on the question type
    # if the bot can't asnwer, it will tell that it doesn't understand   
    if  questionType == 'weatherQuestion':
        resp = weatherData.getWeatherForDay(dayInd)
        print('[Chat Bot]: It looks like: ', resp)
    elif questionType == 'sunriseQuestion':
        resp = weatherData.getSunrise(dayInd)
        resp = dt.datetime.utcfromtimestamp(resp)
        print('[Chat Bot]: The sunrise is', resp)
    elif questionType == 'sunsetQuestion':
        resp = weatherData.getSunrise(dayInd)
        resp = dt.datetime.utcfromtimestamp(resp)
        print('[Chat Bot]: The sunset is', resp)
    elif questionType == 'temperatureQuestion':
        resp = (weatherData.getDayTemp(dayInd) - 273) * 1.8 + 32
        print('[Chat Bot]: The temperature is', round(resp, 0), 'F')
    elif questionType == 'humidityQuestion':
        res = weatherData.getHumidity(dayInd)
        print('[Chat Bot]: The humidity is', res, '%')
    elif questionType == 'pressureQuestion':
        res = weatherData.getPressure(dayInd)
        print('[Chat Bot]: The pressure is', res, 'Hg')
    elif questionType == 'minTemperatureQuestion':
        resp = (weatherData.getMinTemp(dayInd) - 273) * 1.8 + 32
        print('[Chat Bot]: The minimum temperature is', round(resp, 0), 'F')
    elif questionType == 'maxTemperatureQuestion':
        resp = (weatherData.getMaxTemp(dayInd) - 273) * 1.8 + 32
        print('[Chat Bot]: The maximum temperature is', round(resp, 0), 'F')
    else:
        print('[Chat Bot]: Sorry, I am not sure I understand')
           
def main():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n',
          '======================================================================================= \n',
          'Hello! I am a Weather Forcast Chat Bot!\n', 
          'What I can do:\n', 
          '1. Tell minimum, maximum, or general temperature for the next 40 days\n',
          '2. Tell the weather on a particular day\n',
          '3. Tell you what the humidity will be on a particular day\n',
          '4. Tell you what pressure will be on a particular day\n',
          '~ Note: You do not have to tell me the name of a city every time, I can remember that ~\n'
          '~ To quit the chat, type \"bye\" ~\n'
          '======================================================================================== \n'
          )
    
    weatherData = None # this is wehre api data is stored 
    userInput = ''
    while userInput != 'bye':
        userInput = input('[User]: ')
        # check if the user typed "bye" to quit the program as their first message
        if userInput == 'bye':
            break
        city, questionType, partOfDay, weekDay, monthDay = processInput(userInput)
        # check if the user inputed a city name 
        if not weatherData and city == '':
            print('[Chat Bot]: I can not tell you anything until you tell me the name of a city')
        else:
            # get weather data for the next 40 days
            if len(city) > 0: 
                weatherData = WeatherInfo(city)
            # generete chat output
            ChatBotOutput(weatherData, questionType, partOfDay, weekDay, monthDay)
         
if __name__ == "__main__":
    main()