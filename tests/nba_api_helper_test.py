import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from ohmysportsfeedspy import MySportsFeeds
import nba_api_helper

msf = MySportsFeeds(version="1.2")
msf.authenticate("5d25b9f7-fe4d-48fe-b492-20d97d", "sball12345")

def test_get_random_player_data():
    player_data = nba_api_helper.get_random_player_data()

    assert(type(player_data[0]) == str)
    assert(type(player_data[1]) == str)
    assert(player_data[2][0:30] == "https://ak-static.cms.nba.com/")
    assert(player_data[3] != None)
    assert(player_data[4] != None)
    assert(player_data[5] != None)

def test_get_player_first_hint():
    output = msf.msf_get_data(league='nba',season='2018-2019-regular',feed='active_players',player="stephen-curry",format='json',force="true")
    return output

def test_get_player_second_hint():
    pass

def test_get_player_first_hint():
    pass

def main():
    test_get_random_player_data()
    print(test_get_player_first_hint())


if __name__ == '__main__':
    main()
