import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import configparser

from weather_spider import WeatherSpider
from weather_painter_small import WeatherPainterSmall
from weather_data import WeatherData

WIDTH = 250
HEIGHT = 122

CONFIG_FILE = "weather_config.ini"

class App(tk.Frame):

    def __init__(self, width, height, master = None):
        tk.Frame.__init__(self, master)

        self._width = width
        self._height = height

        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_FILE)
        self._realtime_api = self._config.get('weather', 'realtime_api')
        self._airquality_api = self._config.get('weather', 'airquality_api')
        self._refresh_milliseconds = int(self._config.get('weather', 'refresh_seconds')) * 1000
        self._city_code = self._config.get('city', 'code')

        self._spider = WeatherSpider(realtime_api = self._realtime_api,
                                     airquality_api = self._airquality_api)
        self._weather_data = WeatherData(self._city_code)

        self._canvas = tk.Canvas(root, width = self._width, height = self._height, bg = 'white')
        self._canvas.config(highlightthickness=0)  # 去掉边框
        self._canvas.pack()

        self._image = Image.new('1', (self._width, self._height), 'white')
        image_draw = ImageDraw.Draw(self._image)
        self._weather_painter = WeatherPainterSmall(image_draw, self._width, self._height)
        self._tkimg = None

        self.update_weather_info()

    def update_weather_info(self):
        print("in clock")

        self._spider.get_realtime_data(self._weather_data)

        if not self._tkimg is None:
            self._canvas.delete(self._tkimg)

        self._weather_painter.paint(self._weather_data)

        self._im = ImageTk.PhotoImage(self._image)
        self._tkimg = self._canvas.create_image(0, 0, anchor = tk.NW, image = self._im)

        self._canvas.after(self._refresh_milliseconds, self.update_weather_info)


root = tk.Tk()
app = App(width = WIDTH, height = HEIGHT, master = root)
app.mainloop()
