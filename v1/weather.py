#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:53:49 2020

@author: adamrankin
"""

import requests
from datetime import datetime
import json

import os.path
from os import path

with open('./credentials.txt', 'r') as credentials_file:
    credentials = json.load(credentials_file)
    
    

with open('./config.txt', 'r') as config_file:
    config = json.load(config_file)
    
    
open_weather_key = credentials['weather_key']
zip_code = config['zip_code']


url = "https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}".format(zip_code, credentials['weather_key'])

response = requests.get(url)

data = json.loads(response.text)

print(data)

#download icon
if not path.exists('./data/icons/{}'.format(data['weather'][0]['icon'])):
    #nothing
    image_url = 'http://openweathermap.org/img/wn/{}@2x.png'.format(data['weather'][0]['icon'])
    img_data = requests.get(image_url).content
    with open('./data/icons/{}.jpg'.format(data['weather'][0]['icon']), 'wb') as handler:
        handler.write(img_data)
        
#update cache
with open ('./data/weather.txt', 'w') as outfile:
    json.dump(data, outfile)