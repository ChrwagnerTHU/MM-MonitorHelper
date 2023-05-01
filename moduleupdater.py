import json
import os

import requests

url = 'https://www.flashscore.de/fussball/deutschland/'
todayStr = 'Heutige Spiele'

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    league = data['MODULE']['league']
    url_league_off = data['MODULE']['url_league_off']
    url_league_on = data['MODULE']['url_league_on']

# Initially show soccer module
requests.get(url_league_on)

for l in league:
    response = requests.get(url + l)
    if todayStr in response.text:
        requests.get(url_league_on)
        break
    else:
        requests.get(url_league_off)
