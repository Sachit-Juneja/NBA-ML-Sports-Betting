from datetime import datetime
import re
import requests
import pandas as pd
from .dict import team_index_current

# Common headers for HTTP requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Language': 'en',
    'Referer': 'https://github.com'
}

# Headers specific to fetching NBA game data
games_header = {**headers, 'Accept-Encoding': 'gzip, deflate, sdch'}

# Headers specific to fetching general data
data_headers = {**headers, 'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}

def get_json_data(url, headers):
    """Fetch JSON data from a URL using specified headers."""
    try:
        response = requests.get(url, headers=headers)
        json_data = response.json()
        return json_data.get('resultSets', {})
    except Exception as e:
        print(e)
        return {}

def get_todays_games_json(url):
    """Fetch today's NBA games from a URL."""
    json_data = get_json_data(url, games_header)
    return json_data.get('gs', {}).get('g', [])

def to_data_frame(data):
    """Convert 'resultSets' data to a Pandas DataFrame."""
    try:
        data_list = data[0]
        return pd.DataFrame(data=data_list.get('rowSet', []), columns=data_list.get('headers', []))
    except Exception as e:
        print(e)
        return pd.DataFrame(data={})

def create_todays_games(input_list):
    """Create a list of home and away teams from a given list of games."""
    return [[game['h']['tc'] + ' ' + game['h']['tn'], game['v']['tc'] + ' ' + game['v']['tn']] for game in input_list]

def create_todays_games_from_odds(input_dict):
    """Create a list of home and away teams from a dictionary of odds data."""
    return [[home_team, away_team] for game, odds in input_dict.items() if (home_team := game.split(":")[0]) in team_index_current and (away_team := game.split(":")[1]) in team_index_current]

def get_date(date_string):
    """Parse a date string and return a datetime object."""
    year, month, day = re.search(r'(\d+)-\d+-(\d\d)(\d\d)', date_string).groups()
    year = int(year) + 1 if int(month) <= 8 else int(year)
    return datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')
