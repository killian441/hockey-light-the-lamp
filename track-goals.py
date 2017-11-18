"""This module checks to see if the data is cached and otherwise
 requests the data.

 Inspired by MLBGAME, https://github.com/panzarino/mlbgame"""

import os, time

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError


#URL Templates
"""BASE_URL.format(gamenumber)"""
BASE_URL = 'http://statsapi.web.nhl.com/api/v1/game/{0}/feed/live'
"""SCHEDULE_URL.format(team,year,timezone)"""
SCHEDULE_URL = 'https://www.nhl.com/{0}/schedule/{1}/{2}/fullseason'

# Local Directory
PWD = os.path.join(os.path.dirname(__file__))

def get_game_url(gamenumber=None, team=avalanche, year=None, timezone=MT):
'''Returns a string for the URL pointing to the game. Given a gamenumber 
 (i.e. 2017020285) no other parameter is needed. Lacking a gamenumber, then
 a team is required to find the scheduled game for today.'''
if not year:
	year = time.localtime().tm_year
	if time.localtime().tm_mon < 8:
		year = year-1

