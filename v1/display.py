#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd7in5_V2
import time
#from PIL import Image,ImageDraw,ImageFont
import traceback
import json


#
# Kelvin to Farenheit Converter
#
def k_to_f(kelvin):
    return int((kelvin-273.15)*(9/5) + 32)

logging.basicConfig(level=logging.DEBUG)

with open('data/weather.txt', 'r') as weather_file:
    weather = json.load(weather_file)

# Load Weather Data
with open('data/disp_weather.txt', 'r') as disp_weather:
    display_weather = json.load(disp_weather)
    

    
# TODO: Load current todo list data
    

    

disp_temp = k_to_f(display_weather['main']['temp'])
disp_feels = k_to_f(display_weather['main']['feels_like'])
disp_icon = display_weather['weather'][0]['icon']

temp = k_to_f(weather['main']['temp'])
feels = k_to_f(weather['main']['feels_like'])
icon = weather['weather'][0]['icon']

update = False


if (disp_temp != temp or disp_feels != feels or disp_icon != icon):
    with open('data/disp_weather.txt', 'w') as disp_weather:
        json.dump(weather, disp_weather)
    update = True
    



x = 0
while x==0:
    x=0

try:
    logging.info("epd7in5_V2 Demo")

    epd = epd7in5_V2.EPD()
    logging.info("init and Clear")
    epd.init()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.text((90, 70), 'Date', font = font24, fill = 0)
    draw.text((325, 70), 'Weather', font = font24, fill = 0)
    draw.text((20, 140), 'Todo', font = font24, fill = 0)
    
    # Dividers
    draw.line((0, 120, 480, 120),width = 4, fill = 0)
    draw.line((300, 0, 300, 120),width = 4, fill = 0)
    epd.display(epd.getbuffer(Limage))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()
    epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    #epd7in5.epdconfig.module_exit()
    exit()
