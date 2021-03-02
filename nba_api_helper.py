import base64
import requests
import json
from ohmysportsfeedspy import MySportsFeeds
import random

msf = MySportsFeeds(version="1.2")
msf.authenticate("5d25b9f7-fe4d-48fe-b492-20d97d", "sball12345")

output = msf.msf_get_data(league='nba',season='2020-2021-regular',feed='active_players',format='json',force="false")

def get_random_player_data():

    players = output['activeplayers']['playerentry']
    player_pic = None
    draft_status = None
    list_size = len(players)
    while player_pic == None or draft_status == None or roster_status == None:
        random_player_id = random.randint(1,list_size)
        player =  players[random_player_id]['player']
        player_pic = player['officialImageSrc']
        roster_status =  player['RosterStatus']
        draft_status = player["draft"]

    playerName = player["FirstName"] + " " + player["LastName"]
    playerLastName = player["LastName"]

    firstHint = get_player_first_hint(player)
    secondHint = get_player_second_hint(player)
    thirdHint = get_player_third_hint(player, players, random_player_id)

    print(player)

    return (playerName, playerLastName, player_pic, firstHint, secondHint, thirdHint)


def get_player_first_hint(player):
    if player['College'] != None:
        return "This player played college basketball at "+ player['College']
    elif 'BirthCountry' in player:
        if player['BirthCountry']!= None:
            return "This player was born in " + player['BirthCountry']
    return None


def get_player_second_hint(player):
    if player['IsRookie'] == "true":
        return "This player is a rookie"
    elif player['draft'] != None:
        return "This player was drafted in round number " + player["draft"]["Round"] + " at pick number " + player["draft"]["RoundPick"] + " of the " + player['draft']["Year"] + " draft by the " + player['draft']['team']["City"] + " " + player['draft']['team']["Name"]
    return "This player went undrafted."


def get_player_third_hint(player, players, playerID):
    if "JerseyNumber" in player and "Position" in  player and 'team' in players[playerID]:
        return "This player wears the number " + player["JerseyNumber"]  + " and plays for the " + players[playerID]['team']['City'] + " " + players[playerID]['team']['Name']
    return "This player is currently a free agent."


def main():
    print(get_random_player_data())

if __name__ == '__main__':
    main()
