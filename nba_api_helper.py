import base64
import requests
import json
import pprint
from ohmysportsfeedspy import MySportsFeeds

msf = MySportsFeeds(version="1.2")
msf.authenticate("5d25b9f7-fe4d-48fe-b492-20d97d", "sball12345")

output = msf.msf_get_data(league='nba',season='2018-2019-regular',feed='active_players',format='json',force="true")
print(output)
