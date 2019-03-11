import base64
import requests
import json
from ohmysportsfeedspy import MySportsFeeds
import random

msf = MySportsFeeds(version="1.2")
msf.authenticate("5d25b9f7-fe4d-48fe-b492-20d97d", "sball12345")

output = msf.msf_get_data(league='nba',season='2018-2019-regular',feed='active_players',format='json',force="true")

def get_random_player_data():

    players = output['activeplayers']['playerentry']
    player_pic = None

    while player_pic == None:
        player =  players[random.randint(1,844)]['player']
        player_pic = player['officialImageSrc']

    playerName = player["FirstName"] + " " + player["LastName"]
    playerLastName = player["LastName"]
    print(playerName)
    firstHint = get_player_first_hint(player)
    secondHint = get_player_second_hint(player)
    thirdHint = get_player_third_hint(player)
    return (playerName, playerLastName, player_pic, firstHint, secondHint, thirdHint)


def get_player_first_hint(player):
    if player['College'] != None:
        return "This player played college basketball at "+ player['College']
    elif 'BirthCountry' in player:
        if player['BirthCountry']!= None:
            return "This player was born in " + player['BirthCountry']
    return None


def get_player_second_hint(player):
    if player['IsRookie'] == True:
        return "This player is a rookie and  plays for the "
    elif player['draft'] != None:
        return "This player was drafted in round number " + player["draft"]["Round"] + " at pick number " + player["draft"]["RoundPick"] + " by the " + player['draft']['team']["City"] + " " + player['draft']['team']["Name"]
    return "This player went undrafted."


def get_player_third_hint(player):
    return None


def main():
    print(get_random_player_data())

if __name__ == '__main__':
    main()
