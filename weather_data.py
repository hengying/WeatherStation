
class WeatherData():
    def __init__(self, city_code):
        self.city_code = city_code

        self.refresh_time = ''
        self.get_ok = False
        self.publish_time = ''
        self.temperature = 0
        self.humidity = 0
        self.info = '无'
        self.wind_direction =''
        self.wind_power = ''
        self.img = ''

        self.get_airquality_ok = False
        self.aqi = 0
        self.aq_text = ''

