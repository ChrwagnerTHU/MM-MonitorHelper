#! /usr/bin/python3

import json
import os
from bs4 import BeautifulSoup
import requests
from datetime import date

url = 'https://www.flashscore.de/fussball/deutschland/bundesliga/#/OIbxfZZI/table/overall'
today = date.today()
date_string = today.strftime("%d.%m.")
gameday_today = False

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    league = data['MODULE']['league']
    url_league_off = data['MODULE']['url_league_off']
    url_league_on = data['MODULE']['url_league_on']

# Initially show soccer module
requests.get(url_league_on)

for l in league:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    if date_string in response.text:
        gameday_today = True

if gameday_today:
    requests.get(url_league_on)
else:
    requests.get(url_league_off)
