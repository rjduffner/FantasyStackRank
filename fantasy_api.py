import os
import yaml
import yql


# YQL query to get current nhl game key
# select * from fantasysports.games where use_login=1 and game_key in ('nhl')
GAME_KEY = 341

# League ID found on league page
#
LEAGUE_ID = 13222

# Create league key from game key and league id
#
LEAGUE_KEY = '%s.l.%s' % (GAME_KEY, LEAGUE_ID)

# Team Key
#
# To get stats
# select * from fantasysports.teams.stats where team_key='341.l.13222.t.10'
#
# To get stat_ids
# select * from fantasysports.leagues.settings where league_key='341.l.13222'
TEAM_NUMBER = '10'
TEAM_KEY = '%s.t.%s' % (LEAGUE_KEY, TEAM_NUMBER)


class FantasyApi(object):
    def __init__(self, key_configuration_file=None):

        if key_configuration_file is None:
            self.key_configuration_file = os.path.join(
                os.getenv('API_KEYS'), 'yahoo.yaml')
        else:
            self.key_configuration_file = key_configuration_file

        self.configuration = self._load_yaml_configuration()

        self.y3 = yql.ThreeLegged(
            self.configuration.get('consumer_key'),
            self.configuration.get('consumer_secret'))

    def _load_yaml_configuration(self):
        with open(self.key_configuration_file) as f:
            keys = yaml.safe_load(f)
        return keys

    def _save_yaml_configuration(self):
        with open(self.key_configuration_file, 'w') as f:
            f.write(yaml.dump(self.configuration, default_flow_style=False))

    def get_access_token_manually(self):
        y3 = yql.ThreeLegged(self.configuration.get('consumer_key'),
                             self.configuration.get('consumer_secret'))
        request_token, auth_url = y3.get_token_and_auth_url()

        print auth_url
        verifier = raw_input('Please enter the PIN shown: ')

        access_token = y3.get_access_token(request_token, verifier)
        return access_token

    def get_access_token(self):
        try:
            token = yql.YahooToken.from_string(self.configuration['access_token'])
        except KeyError:
            token = self.get_access_token_manually()
            self.configuration['access_token'] = token.to_string()

        return token

    def make_call(self, query):
        # Get access token from file or manually
        access_token = self.get_access_token()

        # Check token for timeout
        access_token = self.y3.check_token(access_token)

        # Run Query
        response = self.y3.execute(query, token=access_token)

        # Save configuration
        self._save_yaml_configuration()

        # Return results
        return response


def yql_query(query):
    fapi = FantasyApi()
    response = fapi.make_call(query)
    return response.raw


def get_raw_standings():
    query = "select * from fantasysports.leagues.standings where league_key='%s'" % LEAGUE_KEY
    return yql_query(query)


def get_raw_stats():
    query = "select * from fantasysports.teams.stats where team_key='%s'" % TEAM_KEY
    return yql_query(query)


def get_stat_catergories():
    query = "select * from fantasysports.leagues.settings where league_key='341.l.13222'"
    catergories = {}
    response = yql_query(query)
    for stat in response.get('results')['league']['settings']['stat_categories']['stats']['stat']:
        stat_id = stat.get('stat_id')
        stat_name = stat.get('name')
        catergories[stat_id] = stat_name

    return catergories


def get_league_stats_by_team():
    
    catergories = get_stat_catergories()
    league_stats = {}

    response = get_raw_standings()
    teams = response['results']['league']['standings']['teams']['team']
    
    for team in teams:
        stats = team['team_stats']['stats']['stat']

        team_stats = {}
        for stat in stats:
            team_stats[catergories[stat['stat_id']]] = {'id': stat['stat_id'],
                                                        'value': stat['value']}
            league_stats[team['name']] = {'team_id': team['team_id'], 'team_stats': team_stats}

    return league_stats


for key, value in get_league_stats_by_team().items():
    print key
    print value['team_stats'].keys()
    print value['team_stats']['Goals']['value']
