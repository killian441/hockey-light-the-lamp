"""This module checks to see if the data is cached and otherwise
 requests the data.

 Loosely inspired by MLBGAME, https://github.com/panzarino/mlbgame"""

import os, time, json

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

#Team IDs defined here: http://statsapi.web.nhl.com/api/v1/teams
#TODO: Load this list dynamically
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
SCHEDULE_URL = 'http://statsapi.web.nhl.com/api/v1/schedule/'

# Local Directory
PWD = os.path.join(os.path.dirname(__file__))

def get_game_url(gamenumber=None, team="avalanche"):
    '''Returns a string for the URL pointing to the game. Given a gamenumber 
       (i.e. 2017020285) no other parameter is needed. Lacking a gamenumber,
       then a team is required to find the scheduled game for today.'''
    if gamenumber:
        return BASE_URL.format(gamenumber)

    url = SCHEDULE_URL
    data = urlopen(url)

    if isinstance(team, str):
        team = team_ids[team]

    resp = urlopen(url)
    raw_data = resp.read()
    todays_schedule = json.loads(raw_data)
    for game in todays_schedule['dates'][0]['games']:
        if game['teams']['home']['team']['id'] == team or \
           game['teams']['away']['team']['id'] == team:
            gamenumber = game['gamePk']
            break
    if gamenumber:
        return BASE_URL.format(gamenumber)
    else:
        raise Exception("Cannot find game today for specified team")

def open_game_url(url=None):
    '''Open url, verify that the game is live and then return the current
       gamenumber, timestamp, and score.'''
    if not url:
        url = get_game_url()

    resp = urlopen(url)
    raw_data = resp.read()
    data = json.loads(raw_data)

    if data['gameData']['status']['abstractGameState'] != 'Live':
        raise Exception('Game is not live')

    gamenumber = data['gamePk']
    timestamp = data['metaData']['timeStamp']

    goals = data['liveData']['plays']['currentPlay']['about']['goals']

    return(gamenumber, timestamp, goals)

    


