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

weather_font = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 90)
weather_font_small = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 48)
weather_font_tiny = ImageFont.truetype(os.path.join(picdir, 'meteocons-webfont.ttf'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        

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
    def __init__(self, horizontal = True):
        self.font18 = font18
        self.font24 = font24
        self.font36 = font36
        self.font48 = font48
        self.font60 = font60
        self.font20 = font20
        self.weather_font = weather_font
        self.weather_font_small = weather_font_small
        self.weather_font_tiny = weather_font_tiny
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        if horizontal:
            self.buffer = Image.new('1', (self.epd.width, self.epd.height), 255) #clear frame
        else:
            self.buffer = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.buffer)
        
    def draw_weather_h(self, x, y, weather):        
        #.draw.text((x, y), 'Weather', font = self.font24, fill = 0)
        temp = k_to_f(weather['main']['temp'])
        feels = k_to_f(weather['main']['feels_like'])
        icon = weather['weather'][0]['icon']
        location = weather['name']
        self.draw.text((x, y), location, font = self.font24, fill = 255)
        self.draw.text((x-20, y+30), ICON_MAP[icon], font = self.weather_font, fill=255)
        self.draw.text((x+60, y+30), str(temp), font = self.font60, fill=255)
        self.draw.text((x+120, y+25), '+', font = self.weather_font_small, fill=255)
        self.draw.text((x-10, y+100), 'Feels like: {}'.format(str(feels)), font = self.font24, fill=255)
        self.draw.text((x+120, y+90), '+', font = self.weather_font_tiny, fill=255)
        print(weather)
        
    def draw_weather_v(self, weather):
        temp = k_to_f(weather['main']['temp'])
        feels = k_to_f(weather['main']['feels_like'])
        icon = weather['weather'][0]['icon']
        location = weather['name']
        description = weather['weather'][0]['description'].capitalize()
        self.draw.text((3, 5), location, font = self.font18, fill = 0)
        self.draw.text((300, 150), description, font = self.font24, fill = 0)
        self.draw.text((195, 90), ICON_MAP[icon], font = self.weather_font, fill=0)
        self.draw.text((340, 95), str(temp), font = self.font60, fill=0)
        self.draw.text((395, 95), '+', font = self.weather_font_small, fill=0)
        #self.draw.text((250, 140), 'Feels like: {}'.format(str(feels)), font = self.font24, fill=255)
        #self.draw.text((257, 140), '+', font = self.weather_font_tiny, fill=255)
        print(weather)
        
    def draw_tasks_h(self, y, tasks):
        print (tasks)
        self.draw.rectangle((275, y, 800, y+45), fill=0)
        self.draw.text((290,y + 10), 'To-Do:', font = self.font24, fill=255)
        for i, task in reversed(list(enumerate(tasks))):
            self.draw.text((290, y+55+25*(len(tasks)-i-1)), '- {}'.format(task), font = self.font20, fill=0)
            
    def draw_tasks_v(self, y, tasks):
        print (tasks)
        self.draw.rectangle((0, y, 480, y+45), fill=0)
        self.draw.text((210,y + 10), 'To-Do:', font = self.font24, fill=255)
        for i, task in reversed(list(enumerate(tasks))):
            self.draw.text((5, y+55+28*(len(tasks)-i-1)), '- {}'.format(task), font = self.font24, fill=0)
        
    def draw_date_h(self, x, y):
        today = date.today()
        self.draw.rectangle((0, 0, 270, 480), fill=0)
        day = today.strftime("%A")
        day_num = today.strftime("%d")
        mon_year = today.strftime("%B, %Y")
        # calculate x offsets to center each
        day_x = 40 - (len(day) % 6)*13
        day_num_x = 70 + (len(day_num) % 2)*20
        
        
        self.draw.text((x+day_x,y), day, font = self.font48, fill=255)
        self.draw.text((x+day_num_x,y+50), day_num, font = self.font60, fill=255)
        self.draw.text((x+20,y+120), today.strftime("%B, %Y"), font = self.font24, fill=255)
    
    def draw_date_v(self):
        today = date.today()
        #self.draw.rectangle((0, 0, 480, 190), fill=0)
        day = today.strftime("%A")
        date_string = today.strftime("%B %d, %Y")
        # calculate x offsets to center each
        day_x = 240 - (len(day))*13 + 5
        date_x = 240 - (len(date_string))*6
        
        #self.draw.text((x+day_x,y), day, font = self.font48, fill=255)
        #self.draw.text((x+day_num_x,y+50), day_num, font = self.font60, fill=255)
        #self.draw.text((x+20,y+120), today.strftime("%B, %Y"), font = self.font24, fill=255)
        self.draw.text((day_x, 10), day, font = self.font48, fill=0)
        self.draw.text((date_x, 65), date_string, font = self.font24, fill=0)
        
        
    def draw_calendar_h(self,events):
        print(events)
        self.draw.rectangle((275, 5, 800, 50), fill=0)
        self.draw.text((290,15),'Today ', font = self.font24, fill=255)
        for i, event in enumerate(events):
            if not event['time']:
                self.draw.text((290, 60+25*i), event['description'], font = self.font20, fill=0)
            else:
                time_string = time_convert(event['time'].split('-')[0])
                self.draw.text((290, 60+25*i), '{}:'.format(time_string), font = self.font20, fill=0) 
                self.draw.text((385, 60+25*i), '{}'.format(event['description']), font = self.font20, fill=0) 

    def draw_calendar_v(self,events):
        print(events)
        self.draw.rectangle((0, 195, 480, 240), fill=0)
        self.draw.text((210,205),'Today ', font = self.font24, fill=255)
        for i, event in enumerate(events):
            if not event['time']:
                self.draw.text((10, 240+28*i), event['description'], font = self.font24, fill=0)
            else:
                time_string = time_convert(event['time'].split('-')[0])
                self.draw.text((10, 240+28*i), '{}:'.format(time_string), font = self.font24, fill=0) 
                self.draw.text((115, 240+28*i), '{}'.format(event['description']), font = self.font24, fill=0) 


    def update(self):
        self.epd.display(self.epd.getbuffer(self.buffer))
        self.epd.sleep()
        self.epd.Dev_exit()
        
        

