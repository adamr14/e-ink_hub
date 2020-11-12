#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:53:38 2020

@author: adamrankin
"""

from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens/task_token.pickle'):
        with open('tokens/task_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/task_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokens/task_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    # will need to get task list id
    results = service.tasks().list(tasklist = 'MTc2Njg5NTAzNDYzODI2ODA1Njc6MDow', maxResults=10).execute()
    items = results.get('items', [])

    tasks = []
    if not items:
        tasks = ['Enjoy your day :)']
    else:
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))
            tasks.append(item['title'])
    with open ('data/tasks.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(tasks)
        

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    