import requests

class WeatherInfo:
    def __init__(self, city):
        self.API_KEY = '0df4f32b4fe92f13f3c242fb49765758'
        self.lat, self.lon = self.getLoc(city)
        self.weatherData = self.getWeatherData(self.lat, self.lon)
    
    
    def getLoc(self, city):
        geoBaseUrl = 'http://api.openweathermap.org/geo/1.0/direct?'
        params = {
            'q': city,
            'appid': self.API_KEY,        
        }
        
        res = requests.get(url=geoBaseUrl, params=params).json()[0]
        lat = res['lat']
        lon = res['lon']
        return [lat, lon]
    
    def getWeatherData(self, lat, lon):
        # get weather at the given location (next 40 days)
        weatherBaseUrl = 'http://api.openweathermap.org/data/2.5/forecast?'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.API_KEY,
        }
        
        res = requests.get(url=weatherBaseUrl, params=params).json()
        return res['list']

        
    def getWeatherForDay(self, day = 0):
        dayData = self.weatherData[day]
        weather = dayData['weather'][0]['main']
        weatherDescription = dayData['weather'][0]['description']
        
        return weatherDescription
        
    def getHumidity(self, day):
        dayData = self.weatherData[day]
        humidity = dayData['main']['humidity']
        return humidity

    def getPressure(self, day):
        dayData = self.weatherData[day]
        pressure = dayData['main']['pressure']
        return pressure
    
    def getSunrise(self, day):
        dayData = self.weatherData[day]
        sunriseTime = dayData['sunrise']
        return sunriseTime
              
    def getSunSet(self, day):
        dayData = self.weatherData[day]
        sunriseTime = dayData['sunset']
        return sunriseTime
        
    def getMinTemp(self, day):
        dayData = self.weatherData[day]
        temp = dayData['main']['temp_min']
        return temp
        
    def getMaxTemp(self, day):
        dayData = self.weatherData[day]
        temp = dayData['main']['temp_max']
        return temp
        
    def getDayTemp(self, day):
        dayData = self.weatherData[day]
        temp = dayData['main']['temp']
        return temp