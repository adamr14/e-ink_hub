#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:53:49 2020

@author: adamrankin
"""

import requests
from datetime import datetime
import json
from PIL import Image,ImageDraw,ImageFont
import os
import sys

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
    

def main():
    os.chdir(os.path.dirname(sys.argv[0]))
    with open('./credentials/weather_credentials.txt', 'r') as credentials_file:
        credentials = json.load(credentials_file)
    with open('./config.txt', 'r') as config_file:
        config = json.load(config_file)
    zip_code = config['zip_code']
    url = "https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}".format(zip_code, credentials['weather_key'])
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    #update cache
    with open ('./data/weather.txt', 'w') as outfile:
        json.dump(data, outfile)
    
if __name__ == '__main__':
    main()