from nba_api.stats.static import players
from nba_api.stats.endpoints import drafthistory,commonplayerinfo,commonallplayers
from pandas import DataFrame

import webbrowser

from pprint import pprint
import random

def get_random_player():
    info = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    drafthistory2 = drafthistory.DraftHistory()

    draft_dict = drafthistory2.get_normalized_dict()
    curr_player_dict = info.get_normalized_dict()

    players = curr_player_dict['CommonAllPlayers']
    random_player = random.choice(players)

    players_draft_history = draft_dict['DraftHistory']

    match = None
    for player in players_draft_history:
        if player['PERSON_ID'] == random_player['PERSON_ID']:
            match = player

    dict_fomr = commonplayerinfo.CommonPlayerInfo(random_player['PERSON_ID'])
    aaaa = dict_fomr.get_normalized_dict()
    whatever = aaaa['CommonPlayerInfo'][0]
    url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{}.png".format(random_player["PERSON_ID"])
    return (whatever, match, url)
