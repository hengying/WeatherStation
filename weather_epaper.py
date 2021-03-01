import sys
import os
from PIL import Image, ImageDraw, ImageFont
import configparser

driver_folder = '/home/pi/install/e-Paper/RaspberryPi_JetsonNano/python/'
libdir = driver_folder + 'lib'

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time

from weather_spider import WeatherSpider
from weather_painter_small import WeatherPainterSmall
from weather_data import WeatherData

WIDTH = 250
HEIGHT = 122

CONFIG_FILE = "weather_config.ini"

class App():

    def __init__(self, width, height):

        self._width = width
        self._height = height

        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_FILE)
        self._realtime_api = self._config.get('weather', 'realtime_api')
        self._airquality_api = self._config.get('weather', 'airquality_api')
        self._refresh_seconds = int(self._config.get('weather', 'refresh_seconds'))
        self._city_code = self._config.get('city', 'code')

        self._spider = WeatherSpider(realtime_api = self._realtime_api,
                                     airquality_api = self._airquality_api)
        self._weather_data = WeatherData(self._city_code)

        self._epd = epd2in13_V2.EPD()

        self._image = Image.new('1', (self._width, self._height), 'white')
        image_draw = ImageDraw.Draw(self._image)
        self._weather_painter = WeatherPainterSmall(image_draw, self._width, self._height)

    def update_weather_info(self):
        while True:
            print("in clock")

            self._spider.get_realtime_data(self._weather_data)

            self.init_epaper()

            self._weather_painter.paint(self._weather_data)

            self.paint_epaper()

            self.close_epaper()

            time.sleep(self._refresh_seconds)

    def init_epaper(self):
        logging.info("init and Clear")
        self._epd.init(self._epd.FULL_UPDATE)

    def close_epaper(self):
        logging.info("sleep")
        self._epd.sleep()

    def clear_epaper(self):
        self._epd.Clear(0xFF)

    def paint_epaper(self):
        self._epd.display(self._epd.getbuffer(self._image))


logging.basicConfig(level=logging.DEBUG)

try:
    app = App(width = WIDTH, height = HEIGHT)
    app.update_weather_info()
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()

