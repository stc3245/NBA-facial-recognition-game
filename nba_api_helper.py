import base64
import requests
import json
from ohmysportsfeedspy import MySportsFeeds
import random

msf = MySportsFeeds(version="1.2")
msf.authenticate("5d25b9f7-fe4d-48fe-b492-20d97d", "sball12345")

output = msf.msf_get_data(league='nba',season='2018-2019-regular',feed='active_players',format='json',force="true")
def get_random_player():

    players = output['activeplayers']['playerentry']

    player =  players[random.randint(1,844)]['player']
    if player['officialImageSrc'] == None:
        player =  players[random.randint(1,844)]['player']

    playerName = player["FirstName"] + " " + player["LastName"]
    return player
