"""This module checks to see if the data is cached and otherwise
 requests the data.

 Inspired by MLBGAME, https://github.com/panzarino/mlbgame"""

import os, time, json

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

team_ids = {"devils":1,
            "islanders":2,
            "rangers":3,
            "flyers":4,
            "penguins":5,
            "bruins":6,
            "sabres":7,
            "canadiens":8,
            "senators":9,
            "leafs":10,
            "maple leafs":10,
            "hurricanes":12,
            "panthers":13,
            "lightning":14,
            "capitals":15,
            "blackhawks":16,
            "red wings":17,
            "predators":18,
            "blues":19,
            "flames":20,
            "avalanche":21,
            "oilers":22,
            "canucks":23,
            "ducks":24,
            "stars":25,
            "kings":26,
            "sharks":28,
            "blue jackets":29,
            "wild":30,
            "jets":52,
            "coyotes":53,
            "golden knights":54}

#URL Templates
"""BASE_URL.format(gamenumber)"""
BASE_URL = 'http://statsapi.web.nhl.com/api/v1/game/{0}/feed/live'
"""SCHEDULE_URL.format(team,year,timezone)"""
SCHEDULE_URL = 'http://statsapi.web.nhl.com/api/v1/schedule/'

# Local Directory
PWD = os.path.join(os.path.dirname(__file__))

def get_game_url(gamenumber=None, team="avalanche"):
'''Returns a string for the URL pointing to the game. Given a gamenumber 
 (i.e. 2017020285) no other parameter is needed. Lacking a gamenumber, then
 a team is required to find the scheduled game for today.'''
    if gamenumber:
        return BASE_URL.format(gamenumber)

    url = SCHEDULE_URL
    data = urlopen(url)

    if isintance(team, str):
        team = team_ids[team]

