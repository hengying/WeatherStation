import requests
import json
import time

class WeatherSpider:
    def __init__(self, realtime_api, airquality_api):
        self._realtime_api = realtime_api
        self._airquality_api = airquality_api

    def get_realtime_data(self, weather_data):
        weather_data.refresh_time = time.strftime('%Y-%m-%d %H:%M:%S')

        url = self._realtime_api + weather_data.city_code

        #print (url)

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            print(e)
            weather_data.get_ok = False
        else:
            #print(r.text)
            data = r.json()

            '''
            print(
                data['publish_time'],
                data['weather']['temperature'],
                data['weather']['humidity'],
                data['weather']['info'],
                data['wind']['power'],
                data['weather']['img'])
            '''

            weather_data.get_ok = True
            weather_data.publish_time = data['publish_time']
            weather_data.temperature = data['weather']['temperature']
            weather_data.humidity = data['weather']['humidity']
            weather_data.info = data['weather']['info']

            weather_data.wind_direction = data['wind']['direct']
            weather_data.wind_power = data['wind']['power']
            weather_data.img = data['weather']['img']

            # test data
            #weather_data.temperature = -22.5
            #weather_data.humidity = 45
            #weather_data.info = '晴'
            #weather_data.wind_direction = '无持续风向'
            #weather_data.wind_power = '微风'
            #weather_data.img = '-1'


        url = self._airquality_api + weather_data.city_code

        #print (url)

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            print(e)
            weather_data.get_airquality_ok = False
        else:
            #print(r.text)
            data = r.json()
            weather_data.get_airquality_ok = True
            weather_data.aqi = data['aqi']
            weather_data.aq_text = data['text']


