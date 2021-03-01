from PIL import Image, ImageDraw, ImageFont
import time

FONT_FILE = 'fonts/uni_dzh.ttf'
FONT_ARIAL = 'fonts/Arial Unicode.ttf'

class WeatherPainterSmall():
    def __init__(self, image_draw, width, height):
        self._image_draw = image_draw
        self._width = width
        self._height = height
        self._font16 = ImageFont.truetype(FONT_FILE, 16)
        self._font10 = ImageFont.truetype(FONT_ARIAL, 10)
        #self._font24 = ImageFont.truetype(FONT_ARIAL, 24)
        self._font35 = ImageFont.truetype(FONT_ARIAL, 35)
        #self._font50 = ImageFont.truetype(FONT_ARIAL, 50)

    def paint(self, weather_data):
        self._image_draw.rectangle([(0,0), (self._width - 1,self._height - 1)], fill = 255)

        # 爬虫更新信息
        refresh_info = ''
        if weather_data.get_ok:
            # 最后一个字符显示不全，加个空格试试
            refresh_info = 'published at: ' + weather_data.publish_time + ' '
        else:
            refresh_info = 'failed at: ' + weather_data.refresh_time + ' '

        # anchor = 'rd',  # anchor 不知为何不起作用，只好自己计算
        text_width, text_height = self._image_draw.textsize(refresh_info, self._font10)
        self._image_draw.text((self._width - 1 - text_width - 2, self._height - 1 - text_height - 2),
                              refresh_info,
                              font = self._font10,
                              fill = 0)

        # 图标
        image_index = -1
        try:
            image_index = int(weather_data.img)
        except ValueError:
            pass

        ICON_LEFT = 5
        ICON_TOP = 25

        if(image_index >= 0 and image_index <= 33):
            # 下载的图片绘制时会有边框，后来发现要使用alpha通道就可以去掉边框。
            # 有边框的地方使用了白色绘制，但是alpha是0！
            icon = Image.open('day/' + weather_data.img + '.png')
            r,g,b,a = icon.split()
            # 下面这句如果不加，树莓派墨水屏上图标显示不清楚。
            # 但是加了这句话，iMac上图标不好看。
            # 暂时以树莓派为准吧。
            a = a.convert('1')
            self._image_draw.bitmap((ICON_LEFT, ICON_TOP), a, fill=0)#, fill='black')
        else:
            #self._image_draw.text((ICON_LEFT + 10, ICON_TOP - 5), '无', font=self._font50, fill=0)
            self._image_draw.text((ICON_LEFT + 10, ICON_TOP - 5), '无', font=self._font35, fill=0)

        TEXT_LEFT = 88

        # 温度
        self._image_draw.text((TEXT_LEFT, 5), str(weather_data.temperature) + ' ℃', font = self._font35, fill = 0)

        # 湿度
        self._image_draw.text((TEXT_LEFT, 58), '湿度：' + str(weather_data.humidity) + '%', font = self._font16, fill = 0)

        # 风向、风速
        self._image_draw.text((TEXT_LEFT, 78), weather_data.wind_direction + ' ' + weather_data.wind_power, font = self._font16, fill = 0)

        # 空气质量
        aq_str = weather_data.aq_text + '(' + str(weather_data.aqi) + ')'
        text_width, text_height = self._image_draw.textsize(aq_str, self._font16)
        self._image_draw.text((42 - text_width / 2, 85), aq_str, font = self._font16, fill = 0)

