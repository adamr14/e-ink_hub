#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:40:50 2020

@author: adamrankin
"""

from __future__ import print_function
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
from datetime import date
import os
import sys






def main():
    os.chdir(os.path.dirname(sys.argv[0]))

    creds = None
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens/calendar_token.pickle'):
        with open('tokens/calendar_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/calendar_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokens/calendar_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    appointments = []
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    print("Date: ", date_string)
    
    if not events:
        print('No upcoming events found.')
        appointments = [{'time': '', 'description': ''}]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if date_string in start:
            times = start.replace(date_string, '')
            appointments.append({'time': times[1:], 'description': event['summary']})
         
        print(start, event['summary'])

    # write events to csv
    columns = ['time', 'description']
    with open ('data/calendar.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = columns)
        for app in appointments:
            writer.writerow(app)


if __name__ == '__main__':
    main()