import json
import os
import re
import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://www.flashscore.de/fussball/deutschland/'
todayStr = 'Heutige Spiele'

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    league = data['MODULE']['league']

for l in league:
    response = requests.get(url + l)
    soup = BeautifulSoup(response.content, 'html.parser')
    if (soup.get_text().find(todayStr) > 0):
        print("Hamwa")
        # Zeige Modul für Bundesliga an
