import tkinter  # 导入Tkinter模块
from PIL import Image, ImageTk, ImageDraw, ImageFont
from weather_spider import WeatherSpider
import time

tkimg2 = None
image2 = None
draw = None
im = None# 这个必须保持参考，不然图像就显示不出来了！

def update_clock():
    global tkimg2
    global im # 这个必须保持参考，不然图像就显示不出来了！

    print("in clock")

    if not tkimg2 is None:
        canvas2.delete(tkimg2)

    draw = ImageDraw.Draw(image2)
    draw.rectangle((120, 80, 220, 105), fill=255)
    draw.text((120, 80), time.strftime('%H:%M:%S'), font=font16, fill=0)
    im = ImageTk.PhotoImage(image2)
    tkimg2 = canvas2.create_image(0, 0, anchor=tkinter.NW, image=im)

    canvas2.after(1000, update_clock)

WIDTH = 250
HEIGHT = 122

spider = WeatherSpider()
spider.get_realtime_data()

root = tkinter.Tk()
canvas2 = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
canvas2.config(highlightthickness=0) #去掉边框
canvas2.pack()  # 将Canvas添加到主窗口

font_path = 'uni_dzh.ttf'
font16 = ImageFont.truetype(font_path, 16)

image2 = Image.new('1', (WIDTH, HEIGHT), 'white')
#image = Image.new('RGB', (WIDTH, HEIGHT), 'green')
draw = ImageDraw.Draw(image2)

#draw.rectangle([(0,0),(50,50)],outline = 0)
im = ImageTk.PhotoImage(image2)

y = 0
for i in range(5, 30):
    font = ImageFont.truetype(font_path, i)
    #draw.text((0, y), str(i) + u' 1234567890晴阴霾雨雪雷电', font=font, fill=0)
    y += i+1


#下载的图片绘制时会有边框，后来发现要使用alpha通道就可以去掉边框。
#有边框的地方使用了白色绘制，但是alpha是0！
icon = Image.open('night/0.png')
r,g,b,a = icon.split()
draw.bitmap((100, 100), a, fill='white')
draw.bitmap((100, 160), a, fill=1)#, fill='black')
#draw.bitmap((0,0), r, fill=(255,0,0))
#draw.bitmap((0,50), g, fill=(0,0,255))
#draw.bitmap((0,100), b, fill=(0,255,0))

draw.text((100, 10), "Hello", font=font, fill=0)
draw.text((100, 20), "Hello2", font=font, fill=0)

im = ImageTk.PhotoImage(image2)
tkimg2 = canvas2.create_image(0, 0, anchor=tkinter.NW, image=im)
#canvas2.create_line(100, 0, 0, 100, fill='black')


canvas2.after(5000, update_clock)

root.mainloop()
