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




city_name = "Blacksburg"

state_code = "Va"

zip_code = '24060'


url = "https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}".format(zip_code, api_key)

response = requests.get(url)

data = json.loads(response.text)

#download icon
if not path.exists('../data/icons/{}'.format(data['weather'][0]['icon'])):
    #nothing
    image_url = 'http://openweathermap.org/img/wn/{}@2x.png'.format(data['weather'][0]['icon'])
    img_data = requests.get(image_url).content
    with open('../data/icons/{}.jpg'.format(data['weather'][0]['icon']), 'wb') as handler:
        handler.write(img_data)
        
#update cache
with open ('../data/weather.txt', 'w') as outfile:
    json.dump(data, outfile)