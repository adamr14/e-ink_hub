import sys
import os
import logging
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir) 
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import json
import csv
from weather import ICON_MAP
from datetime import date

ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

weather_font = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 76)
weather_font_small = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 48)
weather_font_tiny = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
        

#
# Kelvin to Farenheit Converter
#
def k_to_f(kelvin):
    return int((kelvin-273.15)*(9/5) + 32)

def time_convert(time):
    hours, minutes, seconds = time.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = 'AM'
    if hours > 12:
        setting = 'PM'
        hours -=12
    elif hours == 0:
        setting = 'AM'
        hours = 12
    return ("%d:%02d" + setting) % (hours, minutes)


class Hub_Graphics:
    #
    # Constructor
    #
    def __init__(self):
        self.font18 = font18
        self.font24 = font24
        self.font36 = font36
        self.font60 = font60
        self.weather_font = weather_font
        self.weather_font_small = weather_font_small
        self.weather_font_tiny = weather_font_tiny
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.buffer = Image.new('1', (self.epd.height, self.epd.width), 255) #clear frame
        self.draw = ImageDraw.Draw(self.buffer)
        
    def draw_weather(self, x, y, weather):        
        #.draw.text((x, y), 'Weather', font = self.font24, fill = 0)
        temp = k_to_f(weather['main']['temp'])
        feels = k_to_f(weather['main']['feels_like'])
        icon = weather['weather'][0]['icon']
        location = weather['name']
        self.draw.text((x, y), location, font = self.font24, fill = 0)
        self.draw.text((x-20, y+30), ICON_MAP[icon], font = self.weather_font, fill=0)
        self.draw.text((x+60, y+30), str(temp), font = self.font60, fill=0)
        self.draw.text((x+120, y+25), '+', font = self.weather_font_small, fill=0)
        self.draw.text((x-10, y+100), 'Feels like: {}'.format(str(feels)), font = self.font24, fill=0)
        self.draw.text((x+120, y+90), '+', font = self.weather_font_tiny, fill=0)
        print(weather)
        
    def draw_tasks(self, x, y, tasks):
        print (tasks)
        self.draw.text((x+15,y), 'Todo:', font = self.font24, fill=0)
        self.draw.line((x+10, y+30, x+80, y+30), width=4, fill=0)
        for i, task in enumerate(tasks):
            self.draw.text((x, y+35+30*i), '- {}'.format(task), font = self.font24, fill=0)
    
    def draw_date(self, x, y):
        today = date.today()
        self.draw.rectangle((0, 0, 480, 100), fill=0)
        self.draw.text((x,y), today.strftime("%a, %b %d"), font = self.font60, fill=255)
        
    def draw_calendar(self, x, y, events):
        print(events)
        self.draw.text((x+50,y),'Today ', font = self.font24, fill=0)
        for i, event in enumerate(events):
            if not event['time']:
                self.draw.text((x, y+35+30*i), event['description'], font = self.font24, fill=0)
            else:
                time_string = time_convert(event['time'].split('-')[0])
                self.draw.text((x, y+35+30*i), '{}:'.format(time_string), font = self.font24, fill=0) 
                self.draw.text((x+105, y+35+30*i), '{}'.format(event['description']), font = self.font24, fill=0) 

    def update(self):
        self.epd.display(self.epd.getbuffer(self.buffer))
        self.epd.sleep()
        self.epd.Dev_exit()
        
        

