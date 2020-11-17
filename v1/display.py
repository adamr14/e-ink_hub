#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
import traceback
import json
import csv
from hub_graphics import Hub_Graphics
from hub_graphics import k_to_f
logging.basicConfig(level=logging.DEBUG)



def main():
    #change directory
    #os.chdir(os.path.dirname(sys.argv[0]))
    
    #
    # Check for updates with weather, tasks, and calendar items
    #
    update = False
    
    # load current weather data
    with open('data/weather.txt', 'r') as weather_file:
        weather = json.load(weather_file)
    
    # Load displayed Weather Data
    with open('data/disp_weather.txt', 'r') as disp_weather:
        display_weather = json.load(disp_weather)
        
    
    disp_temp = k_to_f(display_weather['main']['temp'])
    disp_feels = k_to_f(display_weather['main']['feels_like'])
    disp_icon = display_weather['weather'][0]['icon']
    
    temp = k_to_f(weather['main']['temp'])
    feels = k_to_f(weather['main']['feels_like'])
    icon = weather['weather'][0]['icon']
    
    # compare current and displayed
    if (disp_temp != temp or disp_feels != feels or disp_icon != icon):
        #Update displayed weather data
        with open('data/disp_weather.txt', 'w') as disp_weather:
            json.dump(weather, disp_weather)
        update = True
        
    
    # load current task list
    current_tasks = []
    with open('data/tasks.csv', 'r', newline='') as csvfile:
        task_reader = csv.reader(csvfile, delimiter =',')
        for row in task_reader:
            current_tasks = row
        #print(current_tasks)
        
    #load displayed task list
    disp_tasks =[]
    with open('data/disp_tasks.csv', 'r', newline='') as csvfile:
        disp_task_reader = csv.reader(csvfile, delimiter=',')
        for row in disp_task_reader:
            disp_tasks = row
        #print(disp_tasks)
        
    # compare current and dipslayed
    if disp_tasks != current_tasks:
        #print('update')
        #update displayed task data
        with open ('data/disp_tasks.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(current_tasks)
        update = True
        
        
    # load current calendar items
    current_calendar = []
    with open('data/calendar.csv', 'r', newline='') as csvfile:
        calendar_reader = csv.reader(csvfile, delimiter =',')
        for row in calendar_reader:
            current_calendar.append({'time': row[0], 'description': row[1]})
        #print(current_calendar)
        
    # load current calendar items
    disp_calendar = []
    with open('data/disp_calendar.csv', 'r', newline='') as csvfile:
        calendar_reader = csv.reader(csvfile, delimiter =',')
        for row in calendar_reader:
            disp_calendar.append({'time': row[0], 'description': row[1]})
        #print(disp_calendar)
        
    if disp_calendar != current_calendar:
        print('update')
        # update displayed calendar data
        columns = ['time', 'description']
        with open ('data/disp_calendar.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = columns)
            for app in current_calendar:
                writer.writerow(app)
    
    update = True
    if update:
        try:
            display = Hub_Graphics(False)
            display.draw_date_v()
            display.draw_weather_v(weather)
            display.draw_calendar_v(current_calendar)
            display.draw_tasks_v(245 + len(current_calendar)*28, current_tasks)
            #display.draw_date_v(20, 0)
            #display.draw_weather_v(300, 30, weather)
            #display.draw_tasks_v(65 + len(current_calendar)*25, current_tasks)
            #display.draw_calendar_v(current_calendar)
            display.update()
                
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            #epd7in5.epdconfig.module_exit()
            exit()

if __name__ == '__main__':
    main()