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
BASE_URL = 'http://statsapi.web.nhl.com/api/v1/game/{0}/feed/live/'
SCHEDULE_URL = 'http://statsapi.web.nhl.com/api/v1/schedule/'

# Local Directory
PWD = os.path.join(os.path.dirname(__file__))

def get_game_number(team="avalanche"):
    '''Returns a int of the gamenumber (i.e. 2017020285).
       A team is required to find the scheduled game for today.'''

    url = SCHEDULE_URL
    data = urlopen(url)

    if isinstance(team, str):
        team = team_ids[team.lower()]

    resp = urlopen(url)
    raw_data = resp.read()
    todays_schedule = json.loads(raw_data)
    for game in todays_schedule['dates'][0]['games']:
        if game['teams']['home']['team']['id'] == team or \
           game['teams']['away']['team']['id'] == team:
            gamenumber = game['gamePk']
            break
    if gamenumber:
        return gamenumber
    else:
        raise Exception("Cannot find game today for specified team")

def main():
    gamenumber, timestamp, new_goal, live_game = None
    score = {'home':0,'away':0}

    team = "Avalanche"
    gamenumber = get_game_number(team)
    url = BASE_URL.format(get_game_number(team))

    while(not live_game):
        resp = urlopen(url)
        raw_data = resp.read()
        data = json.loads(raw_data)

        if data['gameData']['status']['abstractGameState'] == 'Final':
            raise Exception('Game is over')
        elif data['gameData']['status']['abstractGameState'] == 'Live':
            gamenumber = data['gamePk']
            timestamp = data['metaData']['timeStamp']
            score = data['liveData']['plays']['currentPlay']['about']['goals']
            live_game = True
        else:
            game_starts = time.mktime(time.strptime(
                            data['gameData']['datetime']['dateTime'],
                            "%Y-%m-%dT%H:%M:%SZ"))
            sleep_time = game_starts - time.mktime(time.gmtime())
            time.sleep(sleep_time + 30 if sleep_time > 0 else 30)

    while(True):
        resp = urlopen(url+'diffPatch?site=en_nhl&startTimecode='+timestamp)
        raw_data = resp.read()
        data = json.loads(raw_data)

        try:
            for datum in data[0]['diff']:
                if datum['op'] == 'replace':
                    if datum['path'] == '/metaData/timeStamp':
                        timestamp = datum['value']
                elif datum['op'] == 'add':
                    try:
                        if datum['value']['result']['eventTypeId'] == 'GOAL':
                            if datum['value']['team']['id'] == team_ids[team.lower()]
                                new_goal = True
                            score = datum['value']['about']['goals']
                        except KeyError:
                            pass
        except KeyError:
            print('Game over')
            break


if __name__ == "__main__":
    main()