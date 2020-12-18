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
font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
font56 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 52)
        

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
        self.font30 = font30
        self.font48 = font48
        self.font60 = font60
        self.font52 = font56
        self.font20 = font20
        self.font72 = font72
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
        
    def draw_weather_v(self, weather):
        temp = k_to_f(weather['main']['temp'])
        feels = k_to_f(weather['main']['feels_like'])
        icon = weather['weather'][0]['icon']
        location = weather['name']
        description = weather['weather'][0]['description'].capitalize()
        
        loc_x = 480 - len(location)*10
        
        self.draw.text((loc_x, 5), location, font = self.font18, fill = 0)
        #self.draw.text((300, 110), description, font = self.font24, fill = 0)
        self.draw.text((280, 5), ICON_MAP[icon], font = self.weather_font, fill=0)
        self.draw.text((385, 30), str(temp), font = self.font60, fill=0)
        self.draw.text((440, 30), '+', font = self.weather_font_small, fill=0)
        #self.draw.text((250, 140), 'Feels like: {}'.format(str(feels)), font = self.font24, fill=255)
        #self.draw.text((257, 140), '+', font = self.weather_font_tiny, fill=255)
        #print(weather)
        
            
    def draw_tasks_v(self, y, tasks, max_tasks):
        #print (tasks)
        self.draw.rectangle((0, y, 480, y+45), fill=0)
        self.draw.text((240 - len('To-Do:')*8,y + 5), 'To-Do:', font = self.font30, fill=255)
        print(max_tasks)
        start = len(tasks)-max_tasks + 1
        excess = False
        if max_tasks < len(tasks):
            tasks = tasks[start:]
            tasks.insert(0, '+ {} more'.format(start))
            excess = True
        for i, task in reversed(list(enumerate(tasks))):
            if i == 0:
                if excess:
                    self.draw.text((5, y+55+30*(len(tasks)-i-1)), task, font = self.font24, fill=0)
                else:
                    self.draw.text((5, y+55+30*(len(tasks)-i-1)), '- {}'.format(task), font = self.font24, fill=0)    
            else:
                self.draw.text((5, y+55+30*(len(tasks)-i-1)), '- {}'.format(task), font = self.font24, fill=0)
    
    
    def draw_date_v(self):
        today = date.today()
        #self.draw.rectangle((0, 0, 480, 190), fill=0)
        date_string = today.strftime("%B %d, %Y")
        day = today.strftime("%A")
        # calculate x offsets to center each
        day_x = 200 - (len(day))*15 + 5
        date_x = 100 - (len(date_string))*6
        
        #self.draw.text((x+day_x,y), day, font = self.font48, fill=255)
        #self.draw.text((x+day_num_x,y+50), day_num, font = self.font60, fill=255)
        #self.draw.text((x+20,y+120), today.strftime("%B, %Y"), font = self.font24, fill=255)
        if day == 'Wednesday':
            self.draw.text((5, 25), day, font = self.font52, fill=0)
        elif day == 'Saturday' or day == 'Thursday':
            self.draw.text((15, 10), day, font = self.font60, fill=0)
        else:
            self.draw.text((5, 5), day, font = self.font72, fill=0)

    def draw_calendar_v(self,events):
        #print(events)
        today = date.today()
        self.draw.rectangle((0, 100, 480, 145), fill=0)
        date_string = today.strftime("%B %d, %Y")
        date_x = 240 - (len(date_string))*8
        #self.draw.text((210,205),'Today ', font = self.font24, fill=255)
        self.draw.text((date_x, 105), date_string, font = self.font30, fill=255)
        for i, event in enumerate(events):
            if not event['time']:
                self.draw.text((10, 155+30*i), event['description'], font = self.font24, fill=0)
            else:
                time_string = time_convert(event['time'].split('-')[0])
                self.draw.text((10, 155+30*i), '{}:'.format(time_string), font = self.font24, fill=0) 
                self.draw.text((115, 155+30*i), '{}'.format(event['description']), font = self.font24, fill=0)
                
    def draw_message(self, message):            
        self.draw.rectangle((40, 300, 440, 460), fill=255)
        self.draw.rectangle((44, 304, 436, 456), fill=0)
        self.draw.rectangle((48, 308, 432, 452), fill=255)
        #msg_x = 200 - (len(day))*15 + 5
        if len(message) > 14:
            msg_x = 240 - (len(message)*12)/2
            self.draw.text((msg_x, 350), message, font = self.font24, fill=0)
        else:        
            msg_x = 240 - (len(message)*24)/2
            self.draw.text((msg_x, 350), message, font = self.font48, fill=0)
        self.draw.text((350, 420), '-Adam', font = self.font24, fill=0)        
        

    def update(self):
        self.epd.display(self.epd.getbuffer(self.buffer))
        self.epd.sleep()
        self.epd.Dev_exit()
        
        

